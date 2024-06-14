import secrets

from flask import Response, render_template, request, redirect, url_for, flash
from app import app
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from utils import *


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/recognise", methods=['GET', 'POST'])
def recognise():
    if request.method == 'POST':
        random_name = secrets.token_hex(8)
        image_file = request.files['image']
        if image_file and allowed_file(image_file.filename):
            image_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{random_name}.jpg')
            image_file.save(image_file_path)
            info, link_more, new_path = get_full_info(image_file_path)
            return redirect(url_for('result_recognise',
                                    image_file_path=os.path.join('uploads', f'{random_name}.jpg'),
                                    info=info, link_more=link_more, new_path=new_path))
        else:
            flash('Недопустимый файл. Пожалуйста, загрузите изображение.')
            return redirect(url_for('recognise'))
    return render_template("recognise.html")


@app.route("/result_recognise")
def result_recognise():
    image_file_path = request.args.get('image_file_path')
    info = request.args.get('info')
    link_more = request.args.get('link_more')
    new_path = request.args.get('new_path')
    return render_template('result_recognise.html', image_file_path=image_file_path, info=info,
                           link_more=link_more, new_path=new_path)


@app.route("/similarity", methods=['GET', 'POST'])
def similarity():
    if request.method == 'POST':
        random_name = secrets.token_hex(8)
        image_file = request.files['image']
        if image_file and allowed_file(image_file.filename):
            image_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{random_name}.jpg')
            image_file.save(image_file_path)
            success, info, link_more, new_path = get_similarity(image_file_path)
            return redirect(url_for('result_similarity',
                                    image_file_path=os.path.join('uploads', f'{random_name}.jpg'),
                                    info=info, link_more=link_more, new_path=new_path))
        else:
            flash('Недопустимый файл. Пожалуйста, загрузите изображение.')
            return redirect(url_for('recognise'))
    return render_template("similarity.html")


@app.route("/result_similarity")
def result_similarity():
    image_file_path = request.args.get('image_file_path')
    info = request.args.get('info')
    link_more = request.args.get('link_more')
    new_path = request.args.get('new_path')
    return render_template('result_similarity.html', image_file_path=image_file_path, info=info,
                           link_more=link_more, new_path=new_path)


@app.route("/merger")
def merger():
    return render_template("merger.html")

@app.route("/result_merger")
def result_merger():
    return render_template("result_merger.html")
