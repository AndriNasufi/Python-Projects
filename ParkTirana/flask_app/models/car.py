from flask_app.config.mysqlconnection import connectToMySQL
 
from flask import flash


class Car():
    db_name = 'ParkTirana'
    def __init__(self, data):
        self.car_brand = data['car_brand']
        self.license_plate = data['license_plate']
        self.user_id = data['user_id']
        self.image_upload = data['image_upload']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @staticmethod
    def validate_car(data):
        is_valid = True
        if len(data['car_brand']) < 3:
            flash('Car brand must be at least 3 characters', 'car_brand')
            is_valid = False
        if len(data['license_plate']) < 3:
            flash('License plate must be at least 3 characters', 'license_plate')
            is_valid = False
        return is_valid

    @classmethod
    def create_car(cls, data):
        query = "INSERT INTO cars (car_brand, license_plate, user_id, image_upload) VALUES (%(car_brand)s, %(license_plate)s, %(user_id)s, %(image_upload)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all_cars(cls):
        query = "SELECT * FROM cars;"
        results = connectToMySQL(cls.db_name).query_db(query)
        cars = []
        if results:
            for car in results:
                cars.append(car)
        return cars
    
    @classmethod
    def get_car_by_id(cls, data):
        query = 'SELECT * FROM cars WHERE id = %(car_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return Car(results[0])
        return None
    
    @classmethod
    def edit_car(cls, data):
        query = "UPDATE cars SET car_brand = %(car_brand)s, license_plate = %(license_plate)s, user_id = %(user_id)s, image_upload = %(image_upload)s WHERE id = %(car_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def delete_car(cls, data):
        query = "DELETE FROM cars WHERE id = %(car_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)