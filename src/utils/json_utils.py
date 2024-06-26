import json
from sqlalchemy.ext.declarative import DeclarativeMeta

# See https://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable?noredirect=1&lq=1
# Below is the first answer


def toJSON(obj):
    return json.dumps(obj, default=lambda o: o.__dict__, sort_keys=True, indent=4)


# Convert an sqlalchemy row object to JSON (Flat version)
# See https://stackoverflow.com/a/10664192/3910066
def new_alchemy_encoder_flat():
    _visited_objs = []

    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):
                # don't re-visit self
                if obj in _visited_objs:
                    return None
                _visited_objs.append(obj)

                # an SQLAlchemy class
                fields = {}
                for field in [
                    x for x in dir(obj) if not x.startswith("_") and x != "metadata"
                ]:
                    fields[field] = obj.__getattribute__(field)
                # a json-encodable dict
                return fields

            return json.JSONEncoder.default(self, obj)

    return AlchemyEncoder


# A recursive, possibly-circular, selective implementation
# See https://stackoverflow.com/a/10664192/3910066
def new_alchemy_encoder_recursive_selective(revisit_self=False, fields_to_expand=[]):
    _visited_objs = []

    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):
                # don't re-visit self
                if revisit_self:
                    if obj in _visited_objs:
                        return None
                    _visited_objs.append(obj)

                # go through each field in this SQLalchemy class
                fields = {}
                for field in [
                    x for x in dir(obj) if not x.startswith("_") and x != "metadata"
                ]:
                    val = obj.__getattribute__(field)

                    # is this field another SQLalchemy object, or a list of SQLalchemy objects?
                    if isinstance(val.__class__, DeclarativeMeta) or (
                        isinstance(val, list)
                        and len(val) > 0
                        and isinstance(val[0].__class__, DeclarativeMeta)
                    ):
                        # unless we're expanding this field, stop here
                        if field not in fields_to_expand:
                            # not expanding this field: set it to None and continue
                            fields[field] = None
                            continue

                    fields[field] = val
                # a json-encodable dict
                return fields

            return json.JSONEncoder.default(self, obj)

    return AlchemyEncoder
