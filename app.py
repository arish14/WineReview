from cgitb import small
import codecs
from crypt import methods
from email.mime import image
from fileinput import filename
from pickle import GET
from pydoc import render_doc
from sqlite3 import Cursor
import string
from typing import Collection
from unicodedata import name
from unittest import result
from urllib import response
from xml.dom.xmlbuilder import DocumentLS
from flask import Flask, render_template, render_template_string, url_for, redirect, request, jsonify
from flask_pymongo import pymongo
import json
import os
import re
import gridfs
import io
import base64
import PIL.Image as Image 


app = Flask(__name__)
connection_string = "mongodb+srv://wine_review:N2gUV9VXWapvLBy1@mongoproject.miuch.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(connection_string)
db = client.get_database('MongoProject')
Collection = "Winedb"
user_collection = pymongo.collection.Collection(db,'Winedb')

@app.route('/')
def index():
    return render_template('/home.html')

@app.route('/wine_info', methods =["GET", "POST"])
def wine_info():
    if request.method == "POST":
        wine_country = request.form.get("country")
        regx = re.compile("^"+wine_country, re.IGNORECASE)
        cursor = documents = db.Winedb.find({'country': regx,}).limit(10)
        return render_template('./wine_info_contd.html', cursor=cursor)
    return render_template('./wine_info.html')


@app.route('/wine_info_fetch01', methods=["GET", "POST"])
def wiine_info_fetch01():
    id = int(request.args.get("id"))
    #id = request.form.get("id")
    coll = db.Winedb.find({'ID': id})
    return render_template('/display.html', coll=coll)


@app.route('/wine_location', methods =["GET", "POST"])
def wine_location():
    response = []
    if request.method == "POST":
        wine_review = request.form.get("review")
        regx = re.compile("^"+wine_review, re.IGNORECASE)
        cursor = documents= db.wine_db.find({ 'description': regx}).limit(10)
        return render_template('./wine_location_contd.html', cursor=cursor)
    return render_template('./wine_location.html')


@app.route('/geo', methods =["GET", "POST"] )
def geo():
    response = []
    if request.method == "POST":
        longi = float(request.form.get("longi"))
        lati = float(request.form.get("lati"))
        max_dist = int(request.form.get("max_dist"))
        coll = db.wine_db.find({'loc': {'$near':{'$geometry':{'type': "Point", 'coordinates': [longi,lati]},'$maxDistance': max_dist}}}) #cannot limit this as this fetches the countries which are at a long distance.
        return render_template('./geo_contd.html', coll=coll)
    return render_template("./geo.html")

@app.route('/about', methods =["GET", "POST"])
def about():
    if request.method == "POST":
        small = int(request.form.get("small"))
        big = int(request.form.get("big"))
        print(small,big)
        documents = db.wine_db.find({'price': {'$gt': small, '$lt': big}})
        return render_template('./about_contd.html', documents=documents)
    return render_template('./about.html')

@app.route('/wine_contd_fetch', methods=["GET","POST"])
def wine_contd_fetch():
    if request.method == "POST":
        id = int(request.form.get("id"))
        cmt = request.form.get("cmt")
        result = db.wine_db.update_one({'ID': id}, {'$set': {'comments': cmt}})
    return redirect(request.referrer)

@app.route('/get_comments', methods = ["GET","POST"])
def get_comments(id=None):
    if id == None:
        id = int(request.args.get("id"))
    coll = db.wine_db.find({'ID': id})
    return render_template('/view_comment.html', coll=coll)

@app.route('/image', methods = ["GET","POST"])
def image():
    coll = db.Winedb.find({'country': "Argentina"})
    return render_template('/image.html', coll=coll)



if __name__== '__main__':
    app.run(debug=True)