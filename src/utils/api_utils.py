from flask import jsonify
from flask_restx import abort
from werkzeug.exceptions import HTTPException


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


def raise_business_error(
    id: int,
    success: bool,
    message: str = "null",
    httpCode=200,
    underlyingEx: Exception = None,
):
    """Standardize the response when not returning actual records

    Args:
        id (int): the record id
        success (bool): the result of the operation
        message (str, optional): the message to explicit the operation result. Defaults to "null".
        httpCode (int, optional): the http code to use. Defaults to 200.

    Returns:
        str: The JSON object
    """
    if httpCode - 200 < 99:
        return None

    underlyingExMessage = None
    # if underlyingEx is not None and underlyingEx.args is not None:
    #     underlyingExMessage = underlyingEx.args[0]

    abort(httpCode, message)


def handle_ex(ex: any):
    underlyingExMessage = None
    if ex.args is not None and len(ex.args) > 0:
        underlyingExMessage = ex.args[0]

    if hasattr(ex, "data"):
        underlyingExMessage = ex.data.get("message", None)

    httpCode = 500
    if hasattr(ex, "code"):
        try:
            httpCode = int(ex.code)
        except ValueError:
            httpCode = 500

    message = "Internal Error. See details."
    if hasattr(ex, "message"):
        message = ex.message
    if hasattr(ex, "description"):
        message = ex.description

    abort(httpCode, message, details={"inner_ex": f"{underlyingExMessage}"})
