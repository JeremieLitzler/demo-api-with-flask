import json

# See https://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable?noredirect=1&lq=1
# Below is the first answer


def toJSON(obj):
    return json.dumps(obj, default=lambda o: o.__dict__, sort_keys=True, indent=4)
