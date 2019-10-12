import os
import re
import shutil


class Orchestrator:

    def __init__(self, template_path):
        if not os.path.exists(template_path):
            raise Exception('Template does not exists')
        self.template_path = template_path
        (self.template_container_path, self.template_name) = os.path.split(os.path.normpath(template_path))
        self.template_regex = re.compile("%s_(\d+)" % self.template_name)
        self.items = {}
        self.max_index = 0
        self.refresh()

    def refresh(self):
        max_index = 0
        for subdir_name in os.listdir(self.template_container_path):
            subdir_path = os.path.join(self.template_container_path, subdir_name)
            if os.path.isdir(subdir_path) and subdir_name.startswith(self.template_name):
                match = self.template_regex.search(subdir_name)
                if match:
                    index = int(match.group(1))
                    # register existing member
                    if index not in self.items:
                        self.items[index] = OrchestraMember(index, subdir_path)
                    # search max index
                    if index > max_index:
                        max_index = index
        self.max_index = max_index

    def create_new(self):
        index = self.max_index + 1
        name = "{template}_{index}".format(template=self.template_name, index=index)
        new_path = os.path.join(self.template_container_path, name)
        if os.path.exists(new_path):
            raise Exception('Something wrong. A directory indexed %d has been found.' % index)
        shutil.copytree(self.template_path, new_path)
        new_member = OrchestraMember(index, new_path)
        self.items[index] = new_member
        self.max_index = index
        return new_member


class OrchestraMember:

    def __init__(self, index, path):
        self.index = index
        self.path = path

    def delete(self):
        shutil.rmtree(self.path, True)
