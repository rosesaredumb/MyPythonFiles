from globals import datetime, json, os, pytz
from globals import tasks_db_json_path, time_format, time_zone, json_funcs


class MyTasks:
    def __init__(self):
        self.json_helper = json_funcs()
        self.filepath = tasks_db_json_path
        self.json_helper.ensure_json_file(self.filepath)

    def add_task(self):
        