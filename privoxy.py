import os
import subprocess

import config
from process import Process
from tor import tor_port_number_by_index


def build(path, index):
    if not os.path.exists(path):
        raise Exception('Path does not exists')

    index = max(1, index)
    instance_name = 'privoxy_' + str(index)
    base_path = os.path.join(path, instance_name)
    config_file_path = os.path.join(base_path, PrivoxyWrapper.CONFIG_NAME)

    if not os.path.exists(base_path):
        os.mkdir(base_path)

        # calculate tor port
        forward_port = tor_port_number_by_index(index)

        log_dir = os.path.join(base_path, 'log')
        os.mkdir(log_dir)

        # create the config file
        with open(config_file_path, 'w') as config_file:
            config_file.writelines([
                'listen-address localhost:' + str(PrivoxyWrapper.BASE_PORT + index), '\n',
                'forward-socks5t / {}:{} .'.format(config.PRIVOXY_FORWARDING_ADDRESS, str(forward_port)), '\n',
                'logdir ' + log_dir, '\n',
                'logfile logfile'
            ])
            config_file.flush()
            config_file.close()

    # launch command to verify configuration
    result = subprocess.run([PrivoxyWrapper.CMD, '--config-test', config_file_path])
    if result.returncode != 0:
        raise Exception('Invalid configuration')

    return PrivoxyWrapper(config_file_path)


class PrivoxyWrapper(Process):
    CMD = 'privoxy'
    BASE_PORT = 8119
    CONFIG_NAME = 'config'

    def __init__(self, config_file_path):
        super().__init__()
        self.config_file_path = config_file_path
        self.base_dir = os.path.dirname(os.path.abspath(config_file_path))
        self.pid_file = os.path.join(self.base_dir, 'pid')

    @property
    def run_command(self):
        return [self.CMD, '--pidfile', self.pid_file, self.config_file_path]
