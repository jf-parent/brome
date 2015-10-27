#! -*- coding: utf-8 -*-

from subprocess import Popen

import paramiko
import boto.ec2
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from brome.core.model.utils import *
from .base_instance import BaseInstance

class EC2Instance(BaseInstance):
    """EC2 instance

    Attributes:
        runner (object)
        browser_config (object)
        index (int)
    """

    def __init__(self, runner, browser_config, index):
        self.runner = runner
        self.browser_config = browser_config
        self.index = index
        
    def get_ip(self):
        """Return the ip address of the node
        """

        return self.private_ip

    def execute_command(self, command):
        """Execute a command on the node

        Args:
            command (str)
        """

        self.info_log("executing command: %s"%command)

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            k = paramiko.RSAKey.from_private_key_file(self.browser_config.get('ssh_key_path'))
            ssh.connect(self.private_ip, username = self.browser_config.get('username'), pkey = k)

            stdin, stdout, stderr = ssh.exec_command(command)

            output = stdout.read()

            ssh.close()

            return (stdout, stderr)

        except Exception as e:
            msg = "Execute_command exception: %s"%str(e)
            self.error_log(msg)
            raise Exception(msg)

    def startup(self):
        """Startup the ec2 instance
        """

        if not self.browser_config.get('launch'):
            self.warning_log("Skipping launch")
            return
        
        self.info_log("Starting up")

        instance = None
        try:

            #KEY NAME
            key_name = self.browser_config.get("ssh_key_path").split(os.sep)[-1][:-4]
            
            #SECURITY GROUP
            if type(self.browser_config.get("security_group_ids")) in [str, unicode]:
                security_group_ids = [self.browser_config.get("security_group_ids")]

            elif type(self.browser_config.get("security_group_ids")) == list:
                security_group_ids = self.browser_config.get("security_group_ids")

            else:
                msg = "The config security_group_ids must be a string or a list of string"
                self.critial_log(msg)
                raise Exception(msg)
                
            #LAUNCH INSTANCE
            ec2 = boto.ec2.connect_to_region(self.browser_config.get("region"))
            reservation = ec2.run_instances(
                    self.browser_config.get('amiid'),
                    key_name = key_name,
                    instance_type = self.browser_config.get("instance_type"),
                    security_group_ids = security_group_ids
            )

            wait_after_instance_launched = self.runner.get_config_value("ec2:wait_after_instance_launched")
            if wait_after_instance_launched:
                self.info_log("Waiting after instance launched: %s seconds..."%wait_after_instance_launched)
                sleep(wait_after_instance_launched)

            else:
                self.warning_log("Skipping waiting after instance launched")

            try:
                instance = reservation.instances[0]

            except Exception as e:
                self.critical_log('Instance reservation exception: %s'%str(e))
                raise

            self.instance_id = instance.id

            self.info_log('Waiting for the instance to start...')

            for i in range(60*5):
                try:
                    status = instance.update()
                    if status == 'running':
                        break

                    else:
                        sleep(1)
                except Exception as e:
                    self.error_log('Exception while wait pending: %s'%str(e))
                    sleep(1)

            #Wait until instance is running
            status = instance.update()
            if status == 'running':
                instance.add_tag("Name","%s-selenium-node-%s-%s"%(self.browser_config.get('platform'), self.browser_config.get('browserName'), self.index))

                self.info_log(
                    "New instance (%s) public ip (%s) private ip (%s)"%(
                        instance.id,
                        instance.ip_address,
                        instance.private_ip_address
                    )
                )
            else:
                msg = "Instance status is %s and should be (running)"%status
                self.error_log(msg)
                raise Exception(msg)

            if self.runner.get_config_value("ec2:wait_until_system_and_instance_check_performed"):
                check_successful = False

                for i in range(5*60):

                    try:

                        if not i%60:
                            self.info_log('System_status: %s, instance_status: %s'%(status.system_status, status.instance_status))

                        status = ec2.get_all_instance_status(instance_ids=[instance.id])[0]
                        if status.system_status.status == u'ok' and status.instance_status.status == u'ok':

                            self.info_log('system_status: %s, instance_status: %s'%(status.system_status, status.instance_status))
                            check_successful = True
                            break

                    except Exception as e:
                        self.error_log('Waiting instance ready exception: %s'%str(e))
                    sleep(1)

                if not check_successful:
                    msg = "System and instance check were not successful"
                    self.warning_log(msg)
                    raise Exception(msg)
            else:
                self.warning_log("Skipping wait until system and instance check performed")

            self.info_log('Starting the selenium node server')

            self.private_ip = instance.private_ip_address
            self.public_dns = instance.public_dns_name
            self.private_dns = instance.private_dns_name
            self.public_ip = instance.ip_address

            #LINUX
            if self.browser_config.get('platform').lower() == "linux":
                command = self.browser_config.get("selenium_command").format(**self.browser_config.config)
                self.execute_command(command)

            elif self.browser_config.get('platform').upper() == "windows":

                #TODO this code is out of date
                config = self.browser_config.config.copy()
                config['instance_ip_address'] = instance.ip_address
                command = self.browser_config("selenium_command").format(**config)
                process = Popen(command.split(" "), stdout=devnull, stderr=devnull)
                self.runner.xvfb_pids.append(process.pid)

            else:

                msg = "The provided platform name is not supported: select either (WINDOWS) or (LINUX)"
                self.critical_log(msg)
                raise Exception(msg)

            #PROXY
            if self.browser_config.get('enable_proxy'):
                port = self.browser_config.get('proxy_port', 8080)
                self.start_proxy(port = port)

            return True

        except Exception as e:
            self.error_log('Startup exception: %s'%str(e))
            raise

    def tear_down(self):
        """Tear down the instance
        """
        
        if not self.browser_config.get('terminate'):
            self.warning_log("Skipping terminate")
            return

        self.info_log("Tearing down...")
        
        ec2 = boto.ec2.connect_to_region(self.browser_config.get("region"))
        ec2.terminate_instances(instance_ids=[self.instance_id])

        #PROXY
        if self.browser_config.config.get('enable_proxy'):
            self.stop_proxy()

    def start_proxy(self, port = None):
        """Start the mitmproxy
        """
        
        self.runner.info_log("Starting proxy...")

        self.proxy_port = port
        
        self.network_data_path = os.path.join(
            self.runner.runner_dir,
            'network_data'
        )
        create_dir_if_doesnt_exist(network_data_path)

        self.local_proxy_output_path = os.path.join(
            self.network_data_path,
            string_to_filename('%s.data'%self.index)
        )

        self.remote_proxy_output_path = string_to_filename('%s.data'%self.index)

        path_to_mitmproxy = self.runner.brome.get_config_value("mitmproxy:path")

        filter_ = self.runner.brome.get_config_value("mitmproxy:filter")
        command = [
            path_to_mitmproxy,
            "-p",
            "%i"%self.proxy_port,
            "-w",
            self.remote_proxy_output_path
        ]

        if filter_:
            command.append(filter_)

        self.execute_command(command)

    def stop_proxy(self):
        """Stop the mitmproxy
        """

        self.runner.info_log("Stopping proxy...")

        #scp the network data
        scp_command = [
            'scp',
            '%s@%s:%s'%(self.browser_config.get('username'), self.get_ip(), self.remote_proxy_output_path),
            self.local_proxy_output_path
        ]
        self.execute_command(' '.join(scp_command))

        self.new_proxy_output_path = os.path.join(
            self.network_data_path,
            string_to_filename('%s.data'%self.index)
        )

        os.rename(self.local_proxy_output_path, self.new_proxy_output_path)
        os.remove(self.local_proxy_output_path)

        #kill the proxy
        self.execute_command("fuser -k %i/tcp"%self.proxy_port)

    def get_id(self):
        return '%s - %s'%(self.browser_config.browser_id, self.index)

    def debug_log(self, msg):
        self.runner.debug_log("[%s]%s"%(self.get_id(), msg))

    def info_log(self, msg):
        self.runner.info_log("[%s]%s"%(self.get_id(), msg))

    def warning_log(self, msg):
        self.runner.warning_log("[%s]%s"%(self.get_id(), msg))

    def error_log(self, msg):
        self.runner.error_log("[%s]%s"%(self.get_id(), msg))

    def critial_log(self, msg):
        self.runner.critial_log("[%s]%s"%(self.get_id(), msg))
