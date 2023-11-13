import json
from bson import json_util, ObjectId
from datetime import datetime


def parse_json(data: dict)->dict:
    """Parses a dict to json."""
    print(f"received data: {data}")
    print(f"returning data: {json.loads(json_util.dumps(data))}")
    return json.loads(json_util.dumps(data))


def mongodb_to_serializable(data):
    if isinstance(data, list):
        return [mongodb_to_serializable(item) for item in data]
    elif isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, ObjectId):
                data[key] = str(value)
            elif isinstance(value, datetime):
                data[key] = value.utcnow()
        return data
    else:
        return data
