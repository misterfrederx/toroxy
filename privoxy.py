import os

import configparser
import subprocess

from process import Process


def build(config_path):
    result = subprocess.run([PrivoxyWrapper.CMD, '--config-test', config_path])
    if result.returncode != 0:
        raise Exception('Invalid configuration')
    config = configparser.parse(config_path, collapsed_head=False)
    required_settings = [
        'listen-address',
        'forward-socks5t',
        'logdir',
        'logfile'
    ]
    for setting_key in required_settings:
        if setting_key not in config:
            raise Exception("Can't find mandatory setting %s" % setting_key)
    return PrivoxyWrapper(config_path, config, os.path.join(config['logdir'], config['logfile']))


class PrivoxyWrapper(Process):
    CMD = 'privoxy'

    def __init__(self, config_path, log_file, config):
        super().__init__()
        self.config_path = config_path
        self.log_file = log_file
        self.base_dir = os.path.dirname(os.path.abspath(config_path))
        self.pid_file = os.path.join(self.base_dir, 'pid')
        self.config = config

    @property
    def run_command(self):
        return [self.CMD, '--pidfile', self.pid_file, self.config_path]
