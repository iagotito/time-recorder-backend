import hashlib
from typing import Optional
import time
from datetime import datetime

from flask import json
import pymongo

from . connect2db import TIME_RECORDER_DB as DB


class Activity():
    def __init__(self, name:str):
        self._id:Optional[str] = None
        self.name:str = name
        self.description:str = ""
        now = datetime.now()
        self.date:str = now.strftime("%Y-%m-%d")
        self.beginning:str = now.strftime("%H:%M")
        self.end:Optional[str] = None
        self.total:Optional[str] = None
        self.total_hours:float = -1

    @staticmethod
    def id(created_at):
        id_fields = {"created_at": created_at}
        serialized = json.dumps(id_fields, separators=(",", ":"), sort_keys=True, ensure_ascii=False)
        return hashlib.sha1(serialized.encode("utf-8")).hexdigest()

    @staticmethod
    def find_by_date(date:str):
        query = {
            "date": date
        }
        cursor = DB.activity.find(query)
        return list(cursor)

    @staticmethod
    def find_last_of_date(date:str):
        query = {
            "date": date
        }
        cursor = DB.activity.find(query).sort([("created_at", pymongo.DESCENDING)])
        return next(cursor, None)

    @staticmethod
    def update_activity(activity_id, update_fields):
        query = {
            "_id": activity_id
        }
        update_doc = {
            "$set": update_fields
        }
        print(f"{update_fields = }")
        print(f"{update_fields = }")
        print(f"{update_fields = }")
        print(f"{update_fields = }")
        update_result = DB.activity.find_one_and_update(query, update_doc, return_document=pymongo.ReturnDocument.AFTER)
        return update_result


    def save(self):
        self.created_at = time.time()
        self._id = Activity.id(self.created_at)
        DB.activity.insert_one(vars(self))

