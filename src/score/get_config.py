# -*- coding: utf-8 -*-

import json
# import time
import os.path
# from score.global_var import set_value
from score.global_var import get_value


class config():
    def __init__(self) -> None:
        abs_path = get_value('abs_path')
        with open(os.path.join(abs_path, 'config.json'), "r", encoding='utf-8') as f:
            JsonObj = json.loads(f.read())
            self.cookie = JsonObj['cookie']
            self.useragent = JsonObj['useragent']
            self.proxies = JsonObj['proxies']
            self.log_file_name = f'''{JsonObj['log']['file_name']}.log'''
            self.log_path_name = os.path.join(
                abs_path, JsonObj['log']['path_name'])
            self.log_level = JsonObj['log']['level']
            self.sql_host = JsonObj['sql']['host']
            self.sql_port = JsonObj['sql']['port']
            self.sql_username = JsonObj['sql']['username']
            self.sql_password = JsonObj['sql']['password']
            self.sql_database = JsonObj['sql']['database']
