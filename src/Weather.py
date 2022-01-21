import sys
sys.path.append('./')
from packages import *
from src.config import host

class Weather:

    def __init__(self):
        pass

    def get_data(self, localization):
        pass

    def get_weather(self, localization, time):
        pass

    def get_weather_forecast(self, localization):
        pass

    def predict_weather(self, localization):
        pass

    def weather_static(self, localization):
        pass

    def safe_weather(self, localization, input_data):
        pass

    def update_weather(self, localization, update_data):
        pass

    def delete_weather(self, localization):
        pass
