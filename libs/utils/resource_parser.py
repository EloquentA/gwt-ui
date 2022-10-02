__author__ = "Developed by EA"

import os
import json


class ResourceParser:
    """ convert resource files to python dict """

    def __init__(self, project):
        if not project:
            raise Exception(f"Invalid project name <{project}>")
        base_path = os.path.dirname(os.path.dirname(__file__))
        config_file = os.path.join(base_path, "config", "project_key_to_path.json")
        with open(config_file) as json_file:
            config = json.load(json_file)
        self.project_resources_path = os.path.join(os.path.dirname(base_path), config[project], "resources")
        print(f"Fetching resources from <{self.project_resources_path}>")
        if not os.path.exists(self.project_resources_path):
            raise Exception(f"Invalid path <{self.project_resources_path}>")

    def get_resources(self):
        resources = dict()
        filelist = []
        for dirname, dirnames, filenames in os.walk(self.project_resources_path):
            filelist.extend([os.path.join(dirname, filename) for filename in filenames])

        for file in filelist:
            _data = self._parse(file)
            duplicates = set(resources).intersection(set(_data))
            if len(duplicates):
                raise Exception(f"Following duplicates found in resources <{duplicates}> while parsing <{file}>")
            resources.update(_data)
        if not len(resources):
            raise Exception("No resources could be fetched. Make sure mapping of project name to path is correct.")
        return resources

    def _parse(self, filename):
        with open(filename) as json_file:
            data = json.load(json_file)
        return data


if __name__ == "__main__":
    obj = ResourceParser(project="ameyo")
    resources = obj.get_resources()
    print(resources)
