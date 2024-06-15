import secrets
from app import app
from flask import Flask, render_template, request, redirect, url_for, flash, Response
import os
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
    return redirect(url_for('recognise'))


@app.route("/recognise", methods=['GET', 'POST'])
def recognise():
    if request.method == 'POST':
        random_name = secrets.token_hex(8)
        image_file = request.files['image']
        if image_file and allowed_file(image_file.filename):
            extension = image_file.filename.rsplit('.', 1)[1]
            image_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{random_name}.{extension}')
            image_file.save(image_file_path)
            info, link_more, new_path = get_full_info(image_file_path)
            return redirect(url_for('result_recognise',
                                    image_file_path=os.path.join('uploads', f'{random_name}.{extension}'),
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
            extension = image_file.filename.rsplit('.', 1)[1]
            image_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{random_name}.{extension}')
            image_file.save(image_file_path)
            success, sim, title, new_path = get_similarity(image_file_path)

            return redirect(url_for('result_similarity',
                                    image_file_path=os.path.join("static/uploads", f'{random_name}.{extension}'),
                                    success=success, sim=sim, title=title, new_path=new_path))
        else:
            flash('Недопустимый файл. Пожалуйста, загрузите изображение.')
            return redirect(url_for('recognise'))
    return render_template("similarity.html")


@app.route("/result_similarity")
def result_similarity():
    image_file_path = request.args.get('image_file_path')
    success = request.args.get('success')
    sim = request.args.get('sim')
    title = request.args.get('title')
    new_path = request.args.get('new_path')
    print(new_path)
    return render_template('result_similarity.html', image_file_path=image_file_path,
                           success=success, sim=sim, title=title, new_path=new_path)


@app.route("/merger", methods=['GET', 'POST'])
def merger():
    if request.method == 'POST':
        random_name1 = secrets.token_hex(8)
        random_name2 = secrets.token_hex(8)
        image_file1 = request.files['image1']
        image_file2 = request.files['image2']

        if image_file1 and allowed_file(image_file1.filename) and image_file2 and allowed_file(image_file2.filename):
            extension1 = image_file1.filename.rsplit('.', 1)[1]
            extension2 = image_file2.filename.rsplit('.', 1)[1]

            image_file_path1 = os.path.join("static/uploads", f'{random_name1}.{extension1}')
            image_file_path2 = os.path.join("static/uploads", f'{random_name2}.{extension2}')

            image_file1.save(image_file_path1)
            image_file2.save(image_file_path2)

            extension3 = extension1
            random_name3 = secrets.token_hex(8)
            image_file_path3 = os.path.join("static/uploads", f'{random_name3}.{extension3}')

            merged_image_path = style_transfer(image_file_path1, image_file_path2, image_file_path3)
            return redirect(url_for('result_merger', file1_path=image_file_path1, file2_path=image_file_path2,
                                    merged_image_path=merged_image_path))
        else:
            flash('Недопустимые файлы. Пожалуйста, загрузите изображения.')
            return redirect(url_for('merger'))
    return render_template("merger.html")


@app.route("/result_merger")
def result_merger():
    file1_path = request.args.get('file1_path')
    file2_path = request.args.get('file2_path')
    merged_image_path = request.args.get('merged_image_path')
    return render_template('result_merger.html', file1_path=file1_path, file2_path=file2_path,
                           merged_image_path=merged_image_path)
