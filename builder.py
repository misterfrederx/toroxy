from abc import abstractmethod, ABC


class Builder(ABC):

    @abstractmethod
    def build(self, path, index):
        raise NotImplemented

    def config_correction(self, config, key, value):
        if config[key] != value:
            config[key] = value
            return True
        return False
