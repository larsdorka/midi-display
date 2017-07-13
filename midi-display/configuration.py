import json


class Configuration:
    """class for storing and persistence of application configuration"""

    def __init__(self, debug_log=dict()):
        """constructor
        :param debug_log: dictionary to write log entries into
        """
        self.debug_log = debug_log
        self.debug_log['config'] = ""
        self.config_data = None
        self.config_file_path = ""

    def load(self, config_file_path="config.json"):
        """loads the configuration file and decodes the json content
        :param config_file_path:
        """
        self.config_file_path = config_file_path
        try:
            file = open(self.config_file_path)
            self.config_data = json.load(file)
        except Exception as ex:
            self.debug_log['config'] = "error on reading config file: " + str(ex)
        finally:
            file.close()
        print(self.config_data)

    def get_config(self, key=""):
        """returns the value for the given key from the configuration data
        :param key: the key to the config property
        :return: the value of the config property
        """
        value = ""
        try:
            value = self.config_data[key]
        except Exception:
            self.debug_log['config'] = "error on reading config data: key {} not found".format(key)
        return value
