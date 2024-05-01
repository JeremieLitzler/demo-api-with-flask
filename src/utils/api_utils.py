from flask import jsonify


def get_response_json(id: int, success: bool, message: str = "null", httpCode=200):
    """Standardizw the response when not returning actual records

    Args:
        id (int): the record id
        success (bool): the result of the operation
        message (str, optional): the message to explicit the operation result. Defaults to "null".
        httpCode (int, optional): the http code to use. Defaults to 200.

    Returns:
        str: The JSON object
    """
    return (
        jsonify({"id": f"{id}", "success": f"{success}", "message": f"{message}"}),
        httpCode,
    )
