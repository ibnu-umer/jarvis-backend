def success(message, data=None):
    return {
        "success": True,
        "message": message,
        "data": data
    }


def failure(message, data=None):
    return {
        "success": False,
        "message": message,
        "data": data
    }