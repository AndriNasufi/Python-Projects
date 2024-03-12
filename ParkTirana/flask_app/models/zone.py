from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
from flask_app.models.car import Car

class Zone:
    db_name = 'ParkTirana'

    def __init__(self, data):
        self.id = data['id']
        self.zone_name = data['zone_name']
        self.begin_time = data['begin_time']
        self.end_time = data['end_time']
        self.full_name = data['full_name']
        self.car_brand = data['car_brand']
        self.tel_num = data['tel_num']



    @classmethod
    def get_all_zones(cls):
        query = "SELECT * FROM zones;"
        results = connectToMySQL(cls.db_name).query_db(query)
        zones = []
        if results:
            for zone in results:
                zones.append(cls(zone))
        return zones
    
    @classmethod
    def add_reservation(cls, data):
        query = "INSERT INTO reservations (user_id, full_name, zone_name, begin_time, end_time, car_brand, tel_num) VALUES (%(user_id)s, %(full_name)s,%(zone_name)s , %(begin_time)s, %(end_time)s, %(car_brand)s, %(tel_num)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_zone_by_id(cls, data):
        query="SELECT * from zones where id=%(zone_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        zones = []
        if results:
            for result in results:
                zones.append(cls(result))
        return zones
