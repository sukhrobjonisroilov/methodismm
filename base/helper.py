
def cr(status, data=None, message=None):
    if type(status) is not bool:
        status = False
    return {
        "status": status,
        "data": data,
        "message": message
    }
