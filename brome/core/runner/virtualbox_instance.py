#! -*- coding: utf-8 -*-

import virtualbox
import paramiko
import netifaces as ni

from brome.core.model.utils import *
from .base_instance import BaseInstance

class VirtualboxInstance(BaseInstance):

    def __init__(self, **kwargs):
        self.runner = kwargs.get('runner')
        self.browser_config = kwargs.get('browser_config')
        self.index = kwargs.get('index')
        self.vbox = kwargs.get('vbox')
        
    def get_ip(self):
        return self.ip

    def execute_command(self, command):
        self.info_log("executing command: %s"%command)
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            username = self.browser_config.get('username')
            password = self.browser_config.get('password')

            ssh.connect(self.ip, username = username, password = password)

            stdin, stdout, stderr = ssh.exec_command(command)

            output = stdout.read()

            ssh.close()

            return output

        except Exception as e:
            self.info_log(u"execute_command_on_node exception: %s"%unicode(e))

    def startup(self):
        if not self.browser_config.get('launch', False):
            return

        self.info_log("Starting up")
        try:
            call(['VBoxManage', 'guestproperty', 'delete', self.browser_config.get('vbname'), 'wait_until_ready'])
            call(['VBoxManage', 'guestproperty', 'delete', self.browser_config.get('vbname'), 'hub_ip'])

            vm = self.vbox.find_machine(self.browser_config.get('vbname'))

            self.session = virtualbox.Session()

            vm_already_running = False
            if str(vm.session_state) != 'Locked':
                vm.launch_vm_process(self.session, self.browser_config.get('vbox_type', 'gui'), '')
            else:
                vm_already_running = True

            user_session = vm.create_session()
            #user_session.machine.video_capture_enabled = False 

            self.vbox_session = user_session

            if not vm_already_running:
                self.info_log('Waiting for instance to start...')
                for i in range(60):
                    try:
                        value, timestamp, flags = user_session.machine.get_guest_property('wait_until_ready')
                        if value == u'ready':
                            break
                    except virtualbox.library.VBoxErrorInvalidVmState:
                        pass
                    sleep(1)

                sleep(3)
                self.info_log('[Done] Instance ready...')

            hub_ip = ni.ifaddresses('en0')[2][0]['addr']
            self.info_log("Hub ip: %s"%hub_ip)

            vm_ip = vm.get_guest_property("/VirtualBox/GuestInfo/Net/0/V4/IP")[0]
            self.ip = vm_ip
            self.info_log("vm ip: %s"%vm_ip)

            if not vm_already_running:
                #LINUX
                if self.browser_config.get('platform') == "LINUX":

                    self.info_log('Starting the selenium node server')

                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                    ssh.connect(vm_ip, username=self.browser_config.get('username'), password=self.browser_config.get('password'))

                    self.browser_config.config['hub_ip'] = hub_ip
                    command = self.browser_config.get("selenium_command").format(**self.browser_config.config)
                    self.info_log('Command: %s'%command)
                    stdin, stdout, stderr = ssh.exec_command(command)

                #WINDOWS
                elif self.browser_config.get('platform') == "WINDOWS":
                    self.info_log("Setting the guest property in Windows")

                    user_session.machine.set_guest_property("hub_ip", "%s:%s"%(hub_ip, '4444'), '')

            return True

        except Exception as e:
            self.info_log('Exception: %s'%e)
            raise
        
    def tear_down(self):
        if not self.browser_config.get('terminate'):
            self.warning_log("Skipping terminate")
            return

        self.info_log("Tearing down")

        if self.browser_config.get('platform') == 'LINUX':
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            ssh.connect(self.get_ip(), username="root", password=self.browser_config.get('password'))

            command = "shutdown -h now"
            stdin, stdout, stderr = ssh.exec_command(command)

        elif self.browser_config.get('platform') == 'WINDOWS':
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
