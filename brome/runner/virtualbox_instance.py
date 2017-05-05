from time import sleep
import subprocess

import paramiko
import netifaces as ni

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

        return self.browser_config.get('ip')

    def execute_command(self, command, **kwargs):
        """Execute a command on the node

        Args:
            command (str)

        Kwargs:
            username (str)
        """

        self.info_log("executing command: %s" % command)

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            username = kwargs.get(
                'username',
                self.browser_config.get('username')
            )
            password = self.browser_config.get('password')

            ssh.connect(self.get_ip(), username=username, password=password)

            stdin, stdout, stderr = ssh.exec_command(command)

            ssh.close()

            return (stdout, stderr)

        except Exception as e:
            msg = "Execute_command exception: %s" % str(e)
            self.error_log(msg)
            raise Exception(msg)

    def scp_file_remote_to_local(self, remote_path, local_path):
        """Scp a remote file to local

        Args:
            remote_path (str)
            local_path (str)
        """

        sshadd_command = [
            'ssh-add',
            '/Users/pyrat/.ssh/ubuntuNode'
        ]
        self.info_log(
            "executing command: %s" %
            ' '.join(sshadd_command)
        )
        p = subprocess.Popen(sshadd_command)
        p.wait()

        scp_command = [
            'scp',
            '-o',
            'StrictHostKeyChecking=no',
            '%s@%s:"%s"' %
            (
                self.browser_config.get('username'),
                self.get_ip(),
                remote_path
            ),
            local_path
        ]
        self.info_log(
            "executing command: %s" %
            ' '.join(scp_command)
        )
        p = subprocess.Popen(scp_command)
        p.wait()

    def startup(self):
        """This will launch and configure the virtual box machine
        """

        # Do not launch the virtual machine
        if not self.browser_config.get('launch', False):
            return True

        self.info_log("Starting up...")

        try:
            vm_already_running_cmd = [
                "VBoxManage",
                "showvminfo",
                self.browser_config.get('vbname'),
                "--machinereadable",
                "|",
                "grep",
                "VMState=",
                "|",
                "cut",
                "-d'='",
                "-f2"
            ]

            output = subprocess.check_output(
                ' '.join(vm_already_running_cmd),
                stderr=subprocess.STDOUT,
                shell=True
            ).decode('utf').strip()

            print(
                "Is vm already running output: {output}"
                .format(output=output)
            )

            if output.find('running') != -1:
                return True

            # Cleanup the vbox guestproperty variable
            subprocess.call([
                'VBoxManage',
                'guestproperty',
                'delete',
                self.browser_config.get('vbname'),
                'wait_until_ready'
            ])
            subprocess.call([
                'VBoxManage',
                'guestproperty',
                'delete',
                self.browser_config.get('vbname'),
                'hub_ip'
            ])

            startvm = [
                "VBoxManage",
                "startvm",
                "'{vbname}'"
                .format(
                    vbname=self.browser_config.get('vbname')
                ),
                "--type",
                self.browser_config.get('vbox_type', 'gui')
            ]

            out = subprocess.check_output(
                ' '.join(startvm),
                stderr=subprocess.STDOUT,
                shell=True
            )
            self.info_log('VBoxManage output: {out}'.format(out=out))

            instance_ready = False
            # TODO should be configurable
            timeout = 60

            self.info_log('Waiting for instance to start...')

            for i in range(timeout):
                getproperty = [
                    'VBoxManage',
                    'guestproperty',
                    'get',
                    self.browser_config.get('vbname'),
                    'wait_until_ready'
                ]
                output = subprocess.check_output(
                    ' '.join(getproperty),
                    stderr=subprocess.STDOUT,
                    shell=True
                ).decode('utf').strip()
                self.info_log(
                    'VBoxManage guestproperty output: {output}'
                    .format(output=output)
                )

                if output.find('ready') != -1:
                    instance_ready = True
                    break

                sleep(1)

            sleep(3)
            if instance_ready:
                self.info_log('[Done] Instance ready...')
            else:
                raise Exception("Timeout error: the virtualbox machine is still not ready.")  # noqa

            # HUB IP
            hub_ip = ni.ifaddresses('en0')[2][0]['addr']

            self.info_log("Hub ip: %s" % hub_ip)

            # Start selenium on the node
            # LINUX
            if self.browser_config.get('platform').lower() == "linux":

                self.info_log('Starting the selenium node server')

                # Update the hub_ip browser config
                self.browser_config.config['hub_ip'] = hub_ip

                command = self.browser_config.get(
                    "selenium_command"
                ).format(**self.browser_config.config)
                self.execute_command(command)

            # WINDOWS
            elif self.browser_config.get('platform').lower() == "windows":

                self.info_log("Setting the guest property in Windows")

                # user_session.machine.set_guest_property(
                #     "hub_ip", "%s:%s" % (hub_ip, '4444'), ''
                # )

            return True

        except Exception as e:
            self.error_log('Exception: %s' % e)
            raise

    def tear_down(self):
        """Tear down the virtual box machine
        """

        if not self.browser_config.get('terminate'):
            self.warning_log("Skipping terminate")
            return

        self.info_log("Tearing down")

        if self.browser_config.get('platform').lower() == 'linux':
            self.execute_command("shutdown -h now", username='root')

        elif self.browser_config.get('platform').lower() == 'windows':
            self.session.console.power_down()

    def start_video_recording(self, local_video_file_path, video_filename):
        """Start the video recording
        """

        self.runner.info_log("Starting video recording...")

        self.local_video_recording_file_path = local_video_file_path
        self.remote_video_recording_file_path = video_filename

        self.execute_command(
            "./start_recording.sh '%s'" % self.remote_video_recording_file_path
        )

    def stop_video_recording(self):
        """Stop the video recording
        """

        self.runner.info_log("Stopping video recording...")

        self.execute_command("./stop_recording.sh")
        # self.runner.info_log("output: %s"%output)

        sleep(5)

        self.scp_file_remote_to_local(
            self.remote_video_recording_file_path,
            self.local_video_recording_file_path
        )

    def get_id(self):
        return '%s - %s' % (self.browser_config.browser_id, self.index)

    def debug_log(self, msg):
        self.runner.debug_log("[%s]%s" % (self.get_id(), msg))

    def info_log(self, msg):
        self.runner.info_log("[%s]%s" % (self.get_id(), msg))

    def warning_log(self, msg):
        self.runner.warning_log("[%s]%s" % (self.get_id(), msg))

    def error_log(self, msg):
        self.runner.error_log("[%s]%s" % (self.get_id(), msg))

    def critial_log(self, msg):
        self.runner.critial_log("[%s]%s" % (self.get_id(), msg))
