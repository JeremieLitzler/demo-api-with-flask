from collections import namedtuple
from inspect import getmembers


def get_tuple_from_type(cls):
    """
    Creates a namedtuple type based on the public attributes of a class.

    Args:
        cls (class): The class to use for generating the namedtuple type.

    Returns:
        namedtuple: A namedtuple type with fields matching the class's public attributes.
    """
    boring = dir(type("dummy", (object,), {}))
    cls_extract = [item for item in getmembers(cls) if item[0] not in boring]
    # ['__annotations__']
    if cls_extract.__len__ == 0:
        raise TypeError(
            '(Lvl1) The class has no attribute defined. Cannot use "get_tuple_from_type".'
        )
    if cls_extract[0].__len__ == 0:
        raise TypeError(
            '(Lvl2) The class has no attribute defined since "__annotations__" wasn´t found. Cannot use "get_tuple_from_type".'
        )
    if cls_extract[0][0] != "__annotations__":
        raise TypeError(
            'The class has no attribute defined since "__annotations__" wasn´t found. Cannot use "get_tuple_from_type".'
        )

    raw_field_names = cls_extract[0][1].keys()
    field_names = list(raw_field_names)
    return namedtuple(cls.__name__, field_names)
