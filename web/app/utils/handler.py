from flask import jsonify
from app.utils.enum import HTTPStatus

def restExceptionHandler(e: Exception):
  return responseHandler(
    httpStatus = HTTPStatus.OK,
    success = False,
    message = str(e)
  )

def responseHandler(
  httpStatus: HTTPStatus = HTTPStatus.OK, success: bool = True, 
  data = None, message: str = None):
  response = {'success': success}
  if data != None:
    response['data'] = data
  if message != None:
    response['message'] = message

  return jsonify(response), httpStatus.value