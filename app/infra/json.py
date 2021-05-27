import json


def default_method(item):
    if isinstance(item, object) and hasattr(item, '__dict__'):
        return item.__dict__
    else:
        raise TypeError


def to_json(item):
    return json.dumps(item, default=default_method, indent=2, ensure_ascii=False)
