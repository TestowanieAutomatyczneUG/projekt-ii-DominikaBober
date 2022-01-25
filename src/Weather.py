import sys
sys.path.append('./')
from packages import *

class Weather:

    def __init__(self, host):
        self.host = host
        localizations_response: requests.Response = requests.get(f'{host}/localizations').json()
        self.localizations = localizations_response['localizations']

    def get_data(self, localization):
        if localization in self.localizations:
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

    def weather_static(self, localization):
        if localization in self.localizations:
            data = self.get_data(localization)
            return data.describe()
        else:
            raise Exception("Localization not available")

    def save_weather(self, localization, input_data):
        post_data = input_data.copy()
        post_data.loc[:, 'datetime'] = post_data['datetime'].astype(str)
        post_data = {'payload': post_data.to_dict(orient='list')}
        return requests.post(f'{self.host}/save/{localization}', json=post_data).text

    def update_weather(self, localization, update_data):
        if localization in self.localizations:
            post_data = update_data.copy()
            post_data.loc[:, 'datetime'] = post_data['datetime'].astype(str)
            post_data = {'payload': post_data.to_dict(orient='list')}
            return requests.put(f'{self.host}/save/{localization}', json=post_data).text
        else:
            raise Exception("Localization not available")

    def delete_weather(self, localization):
        if localization in self.localizations:
            return requests.delete(f'{self.host}/{localization}').text
        else:
            raise Exception("Localization not available")
