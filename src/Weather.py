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
        data = self.get_data(localization)
        return data[data["datetime"]==pd.to_datetime(time)]

    def get_weather_forecast(self, localization, number_of_days):
        data = self.get_data(localization)
        forecast_time = pd.date_range(list(data['datetime'])[-1].date(), periods=number_of_days+1, freq="D")
        return pd.DataFrame({"datetime": forecast_time[1:]})

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
