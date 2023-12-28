import json

from src import Profile


class ProfileEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Profile):
            print("CompareResult")
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
