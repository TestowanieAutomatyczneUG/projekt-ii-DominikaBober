import sys
sys.path.append('./')
from packages import *

class Weather:

    def __init__(self, host):
        self.host = host
        self.localizations = []
    
    def set_localizations(self, localizations):
        self.localizations = localizations

    def get_localizations(self):
        return self.localizations

    def get_data(self, localization):
        if type(localization) is str and localization in self.get_localizations():
            pass
        else:
            raise Exception("Localization not available")

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
