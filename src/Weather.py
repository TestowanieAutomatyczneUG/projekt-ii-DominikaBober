import sys
sys.path.append('./')
from packages import *

class Weather:

    def __init__(self, host):
        self.host = host
        localizations_response: requests.Response = requests.get(f'{self.host}/localizations').json()
        self.localizations = localizations_response['localizations']

    def get_data(self, localization):
        if localization in self.localizations:
            get_data_response: requests.Response = requests.get(f'{self.host}/data/{localization}').json()
            data = pd.DataFrame.from_dict(get_data_response['data'])
            return data
        else:
            raise Exception("Localization not available")

    def get_weather(self, localization, time):
        data = self.get_data(localization)
        return data[data["datetime"]==pd.to_datetime(time)]

    def get_weather_forecast(self, localization, number_of_days):
        data = self.get_data(localization)
        forecast_time = pd.date_range(list(data['datetime'])[-1].date(), periods=number_of_days+1, freq="D")
        forecast_value = list(list(data['value'])[-1]+(i/number_of_days)*np.mean([list(data['value'])[-1],list(data['value'])[-2]]) for i in range(number_of_days) )
        return pd.DataFrame({"datetime": forecast_time[1:], "value": forecast_value})

    def weather_static(self, localization):
        if localization in self.localizations:
            data = self.get_data(localization)
            plt.hist(data['value'], bins=20)
            plt.title(f"{localization} statistic")
            plt.show()
            return data.describe()
        else:
            raise Exception("Localization not available")

    def save_weather(self, localization, input_data):
        post_data = input_data.copy()
        post_data.loc[:, 'datetime'] = post_data['datetime'].astype(str)
        post_data = {'payload': post_data.to_dict(orient='list')}
        save_response: requests.Response = requests.post(f'{self.host}/save/{localization}', json=post_data)
        localizations_response: requests.Response = requests.get(f'{self.host}/localizations').json()
        self.localizations = localizations_response['localizations']
        return save_response.text

    def update_weather(self, localization, update_data):
        if localization in self.localizations:
            post_data = update_data.copy()
            post_data.loc[:, 'datetime'] = post_data['datetime'].astype(str)
            post_data = {'payload': post_data.to_dict(orient='list')}
            update_response: requests.Response = requests.put(f'{self.host}/save/{localization}', json=post_data)
            return update_response.text
        else:
            raise Exception("Localization not available")

    def delete_weather(self, localization):
        if localization in self.localizations:
            delete_response: requests.Response = requests.delete(f'{self.host}/{localization}')
            localizations_response: requests.Response = requests.get(f'{self.host}/localizations').json()
            self.localizations = localizations_response['localizations']
            return delete_response.text
        else:
            raise Exception("Localization not available")
