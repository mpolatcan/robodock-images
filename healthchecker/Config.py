import yaml


class Config:
    def __init__(self, config_filename):
        try:
            self.config = yaml.load(open(config_filename, "r"))
        except yaml.YAMLError as err:
            print(err)

    def get_int(self, attr_name):
        try:
            return int(self.config[attr_name])
        except KeyError:
            raise KeyError("There is no attribute named \"" + attr_name + "\"")

    def get_str(self, attr_name):
        try:
            return str(self.config[attr_name])
        except KeyError:
            raise KeyError("There is no attribute named \"" + attr_name + "\"")

    def get(self, attr_name):
        try:
            return self.config[attr_name]
        except KeyError:
            raise KeyError("There is no attribute named \"" + attr_name + "\"")

    def len(self, attr_name):
        try:
            return 0 if self.config[attr_name] is None else self.config[attr_name].__len__()
        except KeyError:
            raise KeyError("There is no attribute named \"" + attr_name + "\"")

    def count(self, attr_name):
        try:
            return 0 if self.config[attr_name] is None else str(self.config[attr_name]).split(',').__len__()
        except KeyError:
            raise KeyError("There is no attribute named \"" + attr_name + "\"")

    def nodes(self, attr_name):
        try:
            return self.get_str(attr_name=attr_name).split(',')
        except KeyError:
            raise KeyError("There is no attribute named \"" + attr_name + "\"")