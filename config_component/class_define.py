import os
import configparser
import sys


class Config(object):
    """
    用于加载 INI 文件
    """

    def __init__(self, config_filename):
        # Linux 路径
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), config_filename).replace('\\', '/')
        self.cf = configparser.ConfigParser()
        self.cf.read(file_path, encoding='utf-8')

    def get_sections(self):
        return self.cf.sections()

    def get_options(self, section):
        return self.cf.options(section)

    def get_content(self, section):
        result = {}
        for option in self.get_options(section):
            value = self.cf.get(section, option)
            result[option] = int(value) if value.isdigit() else value
        return result

    def get_confs(self):
        conf_dict = {}

        for section in self.get_sections():
            conf_dict[section] = self.get_content(section)

        return conf_dict
