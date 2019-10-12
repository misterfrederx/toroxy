import subprocess

import configparser
from process import Process


def build(config_path, index):
    result = subprocess.run([TorWrapper.CMD, "-f", config_path, "--verify-config"],
                            capture_output=True,
                            text=True)
    if 'Configuration was valid' not in result.stdout:
        raise Exception('Invalid configuration')
    config = configparser.parse(config_path)
    required_settings = [
        'SocksPort',
        'ControlPort',
        'RunAsDaemon',
        'HashedControlPassword',
        'DataDirectory',
        'Log debug file',
        'Log notice file',
        'PidFile'
    ]
    for setting_key in required_settings:
        if setting_key not in config:
            raise Exception("Can't find mandatory setting %s" % setting_key)

    # check and adjust config according to index
    overwrite_config = False
    socks_port = TorWrapper.BASE_PORT * index

    check = lambda config, key, value

    if config['SocksPort'] != socks_port:
        config['SocksPort'] = socks_port
        overwrite_config = True
    if config['ControlPort'] != socks_port + 1:
        config['ControlPort'] = socks_port + 1
        overwrite_config = True

    for key, value in config:
        pass


    return TorWrapper(config_path,
                      config['ControlPort'],
                      config['HashedControlPassword'],
                      config['PidFile'],
                      config)


class TorWrapper(Process):
    CMD = 'tor'
    BASE_PORT = 9050

    def __init__(self, index, config_path, control_port, hashed_pwd, pid_file, config):
        super().__init__()
        self.index = index
        self.config_path = config_path
        self.control_port = control_port
        self.hashed_pwd = hashed_pwd
        self.pid_file = pid_file
        self.config = config

    @property
    def run_command(self):
        return [self.CMD, '-f', self.config_path]
