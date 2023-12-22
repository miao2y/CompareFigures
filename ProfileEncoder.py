import json

from Profile import Profile


class ProfileEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Profile):
            print("CompareResult")
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
