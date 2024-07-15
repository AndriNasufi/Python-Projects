from flask_app.config.mysqlconnection import connectToMySQL


class Weather:
    db_name = "weather_project"
    def __init__(self, data):
        self.id = data['id']
        self.current_temp = data['current_temp']
        self.feels_like = data['feels_like']
        self.weather_description = data['weather_description']
        

    @classmethod
    def insert_data(cls, data):
        query = "INSERT INTO weather (current_temp, feels_like, weather_description) VALUES (%(current_temp)s, %(feels_like)s, %(weather_description)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
