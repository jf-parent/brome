import virtualbox
import paramiko
import netifaces as ni

from brome.core.utils import *
from brome.runner.base_instance import BaseInstance

class VirtualboxInstance(BaseInstance):
    """Virtual box instance
    
    Attributes:
        runner (object)
        browser_config (object)
        index (int)

    Kwargs:
        vbox (object)
    """

    def __init__(self, runner, browser_config, index, **kwargs):
        self.runner = runner
        self.browser_config = browser_config
        self.index = index

        self.vbox = kwargs.get('vbox')
        
    def get_ip(self):
        """Return the ip address of the node
        """

        return self.ip

    def execute_command(self, command, **kwargs):
        """Execute a command on the node

        Args:
            command (str)

        Kwargs:
            username (str)
        """

        self.info_log("executing command: %s"%command)

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            username = kwargs.get('username', self.browser_config.get('username'))
            password = self.browser_config.get('password')

            ssh.connect(self.ip, username = username, password = password)

            stdin, stdout, stderr = ssh.exec_command(command)

            output = stdout.read()

            ssh.close()

            return (stdout, stderr)

        except Exception as e:
            msg = "Execute_command exception: %s"%str(e)
            self.error_log(msg)
            raise Exception(msg)

    def startup(self):
        """This will launch and configure the virtual box machine
        """

        #Do not launch the virtual machine
        if not self.browser_config.get('launch', False):
            return

        self.info_log("Starting up")

        try:
            #Cleanup the vbox guestproperty variable
            call(['VBoxManage', 'guestproperty', 'delete', self.browser_config.get('vbname'), 'wait_until_ready'])
            call(['VBoxManage', 'guestproperty', 'delete', self.browser_config.get('vbname'), 'hub_ip'])

            #Find the machine
            vm = self.vbox.find_machine(self.browser_config.get('vbname'))

            #Session
            self.session = virtualbox.Session()

            #Determine if the vm is running or not
            #Launch it is necessary
            vm_already_running = False
            if str(vm.session_state) != 'Locked':
                vm.launch_vm_process(self.session, self.browser_config.get('vbox_type', 'gui'), '')
            else:
                vm_already_running = True

            user_session = vm.create_session()
            #NOTE this is another way to record the session
            #user_session.machine.video_capture_enabled = False 

            #User session
            self.vbox_session = user_session

            #Wait until the vm is ready
            if not vm_already_running:

                instance_ready = False
                #TODO should be configurable
                timeout = 60

                self.info_log('Waiting for instance to start...')

                for i in range(timeout):
                    try:
                        value, timestamp, flags = user_session.machine.get_guest_property('wait_until_ready')

                        if value == u'ready':
                            instance_ready = True
                            break

                    except virtualbox.library.VBoxErrorInvalidVmState:
                        pass

                    sleep(1)

                sleep(3)
                if instance_ready:
                    self.info_log('[Done] Instance ready...')
                else:
                    raise Exception("Timeout error: the virtualbox machine is still not ready.")

            #HUB IP
            hub_ip = ni.ifaddresses('en0')[2][0]['addr']

            self.info_log("Hub ip: %s"%hub_ip)

            #VM IP
            vm_ip = vm.get_guest_property("/VirtualBox/GuestInfo/Net/0/V4/IP")[0]
            self.ip = vm_ip

            self.info_log("vm ip: %s"%vm_ip)

            #Start selenium on the node
            if not vm_already_running:

                #LINUX
                if self.browser_config.get('platform').lower() == "linux":

                    self.info_log('Starting the selenium node server')

                    #Update the hub_ip browser config
                    self.browser_config.config['hub_ip'] = hub_ip

                    command = self.browser_config.get("selenium_command").format(**self.browser_config.config)
                    self.execute_command(command)

                #WINDOWS
                elif self.browser_config.get('platform').lower() == "windows":

                    self.info_log("Setting the guest property in Windows")

                    user_session.machine.set_guest_property("hub_ip", "%s:%s"%(hub_ip, '4444'), '')

            return True

        except Exception as e:
            self.error_log('Exception: %s'%e)
            raise
        
    def tear_down(self):
        """Tear down the virtual box machine
        """

        if not self.browser_config.get('terminate'):
            self.warning_log("Skipping terminate")
            return

        self.info_log("Tearing down")

        if self.browser_config.get('platform').lower() == 'linux':
            self.execute_command("shutdown -h now", username = 'root')

        elif self.browser_config.get('platform').lower() == 'windows':
            self.session.console.power_down()

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
