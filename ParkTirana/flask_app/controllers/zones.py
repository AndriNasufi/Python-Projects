from flask_app import app
from flask import render_template, redirect, flash, session, request

from flask_app.models.user import User
from flask_app.models.car import Car
from flask_app.models.zone import Zone

@app.route('/profilepage')
def profile():
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'user_id': session['user_id']
    }
    
    logged_user = User.get_user_by_id(data)

    
    return render_template('profile.html', loggedUser=logged_user)



@app.route('/aboutus')
def aboutpage():
   if 'user' not in session:
      return redirect('/')
   return render_template('about.html')


@app.route('/zones')
def all_zones():
   if 'user_id' in session:
      loggedUserData = {
         'user_id': session['user_id'],
      }
   loggedUser = User.get_user_by_id(loggedUserData)
   cars = Car.get_all_cars()
   
   return render_template('zones.html', cars = cars, loggedUser=loggedUser)

@app.route('/add/reservation', methods=['POST'])
def add_reservation():
   if 'user_id' not in session:
      return redirect('/')
   data = {
      'user_id': session['user_id'],
      'zone_name': request.form['zone_name'],
      'full_name': request.form['full_name'],
      'begin_time': request.form['begin_time'],
      'end_time': request.form['end_time'],
      'car_brand': request.form['car_brand'],
      'tel_num': request.form['tel_num'],
   }
   Zone.add_reservation(data)
   return redirect(request.referrer)
