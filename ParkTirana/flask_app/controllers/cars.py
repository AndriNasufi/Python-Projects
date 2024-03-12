from flask_app import app
from flask import render_template, redirect, flash, session, request

from flask_app.models.user import User
from flask_app.models.car import Car

from urllib.parse import unquote
from werkzeug.utils import secure_filename




import os
from werkzeug.exceptions import RequestEntityTooLarge

from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from werkzeug.exceptions import HTTPException, NotFound
from flask_app.models.car import Car
import urllib.parse

from datetime import datetime
from urllib.parse import unquote
UPLOAD_FOLDER = 'flask_app/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/cars')
def all_cars():
    if 'user_id' in session:
        loggedUserData = {
            'user_id': session['user_id'],
        }
    loggedUser = User.get_user_by_id(loggedUserData)
    if not loggedUser:
        return redirect('/')
    
    return render_template('cars.html', cars=Car.get_all_cars(),loggedUser=loggedUser)

@app.route('/cars/new')
def showPage():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('addcar.html')

@app.route('/cars/create', methods=['POST'])
def create_car():
    if 'user_id' not in session:
        return redirect('/')
    

    if not Car.validate_car(request.form):
        return redirect(request.referrer)
    
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    image_file = request.files['imageupload']

    if image_file.filename == '':
        flash('No image selected', 'image_upload_error')
        return redirect(request.referrer)

    # Check if the file is an allowed image format (optional)
    if not allowed_file(image_file.filename):
        flash('Invalid image format. Please upload a valid image (png, jpg, jpeg)', 'image_upload_error')
        return redirect(request.referrer)

    # Generate a unique filename for the image
    filename = secure_filename(image_file.filename)
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = time + '_' + filename

    # Save the image to the uploads folder
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image_file.save(image_path)

    data = {
        'car_brand': request.form['car_brand'],
        'license_plate': request.form['license_plate'],
        'image_upload': filename,
        'user_id': session['user_id'],
    }
    
    Car.create_car(data)
    return redirect('/cars')

@app.route('/cars/<int:car_id>')
def show_car(car_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'car_id': car_id
    }
    car = Car.get_car_by_id(data)

    if not car:
        return redirect('/cars')
    return render_template('showcar.html', car=car)

@app.route('/cars/<int:car_id>/edit')
def edit_car(car_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'car_id': car_id
    }
    car = Car.get_car_by_id(data)
    if not car:
        return redirect('/cars')
    return render_template('editcar.html', car=car)

@app.route('/cars/<int:car_id>/update', methods=['POST'])
def update_car(car_id):
    if 'user_id' not in session:
        return redirect('/')
    if not Car.validate_car(request.form):
        return redirect(f'/cars/{car_id}/edit')
    data = {
        'car_id': car_id,
        'car_brand': request.form['car_brand'],
        'license_plate': request.form['license_plate'],
        'user_id': request.form['user_id']
    }
    Car.edit_car(data)
    return redirect('/cars')

@app.route('/delete/<int:id>')
def delete_car(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'car_id': id
    }
    Car.delete_car(data)
    return redirect('/cars')