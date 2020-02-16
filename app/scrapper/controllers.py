from flask import Blueprint, request
from app.scrapper.ctfd import CTFdScrape
from app.utils.handler import restExceptionHandler
from app.utils.handler import responseHandler
from app.utils.enum import HTTPStatus

main = Blueprint('scrapper', __name__)

@main.route("/", methods=['POST'])
def scrap():
  json_request = request.json
  try:
    scrapper = CTFdScrape(
      json_request['user'],
      json_request['password'],
      json_request['url'],
      "output/"
    )
    scrapper.getChallenges()
    scrapper.createArchive()
    scrapper.review()
  except Exception as e:
    return restExceptionHandler(e)

  return responseHandler(
    httpStatus = HTTPStatus.OK,
    success = True,
    message = "Berhasil"
    )