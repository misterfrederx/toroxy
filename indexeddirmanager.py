import os
import re
import shutil


class IndexedDirManager:

    def __init__(self, path, base_name):
        if not os.path.exists(path):
            raise Exception('Path does not exists')
        self.path = path
        self.base_name = base_name
        self.pattern_re = re.compile("%s_(\d+)" % base_name)
        self.items = {}
        self.max_index = 0
        self.refresh()

    def refresh(self):
        max_index = 0
        for subdir_name in os.listdir(self.path):
            subdir_path = os.path.join(self.path, subdir_name)
            if os.path.isdir(subdir_path) and subdir_name.startswith(self.base_name):
                match = self.pattern_re.search(subdir_name)
                if match:
                    index = int(match.group(1))
                    # register existing member
                    if index not in self.items:
                        self.items[index] = IndexedItem(index, subdir_path)
                    # search max index
                    if index > max_index:
                        max_index = index
        self.max_index = max_index

    @property
    def next_index(self):
        return self.max_index + 1


class IndexedItem:

    def __init__(self, index, path):
        self.index = index
        self.path = path
        self.instance = None

    def delete(self):
        if self.instance:
            self.instance.shutdown()
        shutil.rmtree(self.path, True)
