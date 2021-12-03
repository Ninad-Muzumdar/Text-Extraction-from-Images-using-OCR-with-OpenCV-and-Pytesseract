from bs4 import BeautifulSoup
# from requests_html import HTMLSession
from urllib.parse import urljoin, urlparse
from flask import Flask, request, session, redirect, render_template, url_for, jsonify
import requests
import datetime
import hashlib
import json
from uuid import uuid4
import cv2
import pytesseract
import os
from PIL import Image
from pandas import DataFrame

app = Flask(__name__)

images = os.path.join('static', 'images')

app.config['UPLOAD_FOLDER'] = images


@app.route("/")
def main():
    image = os.path.join(app.config['UPLOAD_FOLDER'], 'dl_bg.jpg')
    return render_template("ocr_main.html", bg_img=image)


IMAGE_DIR = "D:\\OCR\\static\\images"

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\Tesseract-OCR\\tesseract.exe'


@app.route("/upload_form", methods = ['POST'])
def ocr_form():
    filename = request.form["filename"]
    IMAGE_DIRECT = IMAGE_DIR + "\\" + filename
    for path, subdirs, files in os.walk(IMAGE_DIRECT):
        for name in files:
            #count = count+1
            compath = os.path.join(path, name)
            result.append(compath)
            print(compath)
            print(name)
            img = cv2.imread(name)
            # print(img)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            x = pytesseract.image_to_string(img)
            print(type(x))
            print(pytesseract.image_to_string(img))
            hImg, wImg, _ = img.shape
            boxes = pytesseract.image_to_data(img)
            # print(boxes)
            for x, b in enumerate(boxes.splitlines()):

                if x != 0:
                    b = b.split()
                    # print(b)
                    if len(b) == 12:
                        x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        cv2.putText(
                            img, b[11], (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (240, 240, 0), 2)
    return redirect(url_for('color_ocr'), filename = filename)
    # cv2.imshow("Result",img)
      # cv2.waitKey(0)
    # img.save("ocr_pic.jpg")

@app.route("/color_ocr", methods = ['POST'])
def color_ocr():
    filename = request.form["filename"]
    IMAGE_DIRECT = IMAGE_DIR + "\\" + filename
    img = cv2.imread(IMAGE_DIRECT)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    print(pytesseract.image_to_string(img))
    x = pytesseract.image_to_string(img)
    hImg, wImg, _ = img.shape
    boxes = pytesseract.image_to_data(img)
    # print(boxes)
    for x, b in enumerate(boxes.splitlines()):
        if x != 0:
            b = b.split()
            # print(b)
            if len(b) == 12:
                x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(img, b[11], (x+100, y+100),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (240, 240, 0), 2)
    img=pytesseract.image_to_string(img)
    return img

if __name__ == "__main__":
    app.run(debug=True)
