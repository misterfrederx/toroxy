import os
import subprocess
from abc import abstractmethod, ABC


class Process(ABC):

    def __init__(self):
        self.pid_file = None

    def get_pid(self):
        if os.path.isfile(self.pid_file):
            result = subprocess.run(['pgrep', '-F', self.pid_file], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        return None

    def is_running(self):
        return self.get_pid()

    def run(self):
        if not self.is_running():
            result = subprocess.run(self.run_command)
            return result.returncode == 0
        return False

    def stop(self):
        pid = self.get_pid()
        if pid:
            result = subprocess.run(['pkill', '-F', self.pid_file])
            return result.returncode == 0
        return False

    @property
    @abstractmethod
    def run_command(self):
        raise NotImplemented
