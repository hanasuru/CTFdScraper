from flask import Blueprint, request, send_file
from app.scrapper.ctfd import CTFdScrape
from app.utils.handler import restExceptionHandler
from app.utils.handler import responseHandler
from app.utils.enum import HTTPStatus
import os
import shutil

main = Blueprint('scrapper', __name__)

@main.route("/", methods=['POST'])
def scrap():
  try:
    scrapper = CTFdScrape(
      request.form['user'],
      request.form['password'],
      request.form['url'],
      os.path.join("output", "")
    )
    scrapper.getChallenges()
    scrapper.createArchive()
    scrapper.review()
  except Exception as e:
    return restExceptionHandler(e)

  destination = os.path.join('..', scrapper.title)
  shutil.make_archive(destination, "zip", scrapper.path)

  return send_file(scrapper.path + '.zip', as_attachment=True)