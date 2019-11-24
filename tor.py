import os
import subprocess

import config
from process import Process


def build(path, index):
    if not os.path.exists(path):
        raise Exception('Path does not exists')

    index = max(1, index)
    instance_name = 'tor_' + str(index)
    base_path = os.path.join(path, instance_name)
    config_file_path = os.path.join(base_path, TorWrapper.CONFIG_NAME)

    if not os.path.exists(base_path):
        os.mkdir(base_path)

        # create hashed password
        hashed_ctrl_pwd = subprocess.run([TorWrapper.CMD, '--hash-password', config.TOR_CONTROL_PASSWORD + str(index)],
                                         capture_output=True,
                                         text=True).stdout
        # calculate the port
        socks_port = tor_port_number_by_index(index)

        # create the config file
        with open(config_file_path, 'w') as config_file:
            config_file.writelines(['SocksPort ' + str(socks_port),
                                    '\n', 'ControlPort ' + str(socks_port + 1),
                                    '\n', 'RunAsDaemon 1',
                                    '\n', 'HashedControlPassword ' + hashed_ctrl_pwd,
                                    '\n', 'DataDirectory ' + os.path.join(base_path, 'data'),
                                    '\n', 'Log debug file ' + os.path.join(base_path, 'notices.log'),
                                    '\n', 'Log notice file ' + os.path.join(base_path, 'debug.log'),
                                    '\n', 'PidFile ' + os.path.join(base_path, 'pid')
                                    ])
            config_file.flush()
            config_file.close()

    # launch command to verify configuration
    result = subprocess.run([TorWrapper.CMD, "-f", config_file_path, "--verify-config"],
                            capture_output=True,
                            text=True)
    if 'Configuration was valid' not in result.stdout:
        raise Exception('Invalid configuration')

    return TorWrapper(config_file_path)


def tor_port_number_by_index(index: int):
    # sequence like 9052/3 9054/5 9056/7
    return TorWrapper.BASE_PORT + (max(index, 1) * 2)


class TorWrapper(Process):
    CMD = 'tor'
    BASE_PORT = 9050
    CONFIG_NAME = 'torrc'

    def __init__(self, config_file_path: str):
        super().__init__()
        self.config_file_path = config_file_path
        self.base_dir = os.path.dirname(os.path.abspath(config_file_path))
        self.pid_file = os.path.join(self.base_dir, 'pid')

    @property
    def run_command(self):
        return [self.CMD, '-f', self.config_file_path]
