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
            with open(self.config_file_path) as file:
                self.config_data = json.load(file)
        except Exception as ex:
            self.debug_log['config'] = "error on reading config file: " + str(ex)
        if self.config_data is None:
            self.create_std_config()

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

    def create_std_config(self):
        """creates the standard configuration and stores it to a file"""
        self.config_data = {'FULL_SCREEN': False,
                            'MIDI_DEVICE_ID': -1,
                            'SHOW_DEBUG': True}
        json_config = json.dumps(self.config_data, indent=2)
        with open(self.config_file_path, 'w', encoding='utf-8') as file:
            try:
                file.write(json_config)
            except Exception as ex:
                self.debug_log['config'] = "error on writing config data: " + str(ex)
