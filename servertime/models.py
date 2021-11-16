import hashlib
from typing import Optional
import time
from datetime import datetime

from flask import json

from . connect2db import TIME_RECORDER_DB as DB


class Activity():
    def __init__(self, name:str, description:str=""):
        self._id = None
        self.name:str = name
        self.description:str = description
        now = datetime.now()
        self.date:str = now.strftime("%Y-%m-%d")
        self.beginning:str = now.strftime("%H:%M")
        self.end:Optional[str] = None
        self.total:float = -1

    @staticmethod
    def id(created_at):
        id_fields = {"created_at": created_at}
        serialized = json.dumps(id_fields, separators=(",", ":"), sort_keys=True, ensure_ascii=False)
        return hashlib.sha1(serialized.encode("utf-8")).hexdigest()

    def save(self):
        self.created_at = time.time()
        self._id = Activity.id(self.created_at)
        DB.activity.insert_one(vars(self))

    @staticmethod
    def find_by_date(date:str):
        query = {
            "date": date
        }
        cursor = DB.activity.find(query)
        return list(cursor)
