import sys
sys.path.append("./")
from src.Weather import Weather
from packages import *

data_meteo = pd.read_csv("data/data_meteo_2008_03-07.csv")
data_meteo["datetime"] = pd.to_datetime(data_meteo["datetime"])

class Test_Weather(unittest.TestCase):

    testing = "all"

    def setUp(self):
        self.serwer = Weather()

    @parameterized.parameterized.expand(
        list(itertools.chain.from_iterable(
            list(map(lambda site: list(map(lambda time, value: 
                (site, time, value),
            data_meteo[::6*24]["datetime"], data_meteo[::6*24][site])),
        list(data_meteo.columns)[1:]))))
    )
    @unittest.skipIf(testing != "test_get_weather" and testing != "all", "TDD")
    def test_get_weather(self, site, time, value):
        temp = data_meteo[["datetime", site]]
        temp.columns = ["datetime", "value"]
        self.serwer.get_data = mock.Mock(name = "get_data")
        self.serwer.get_data.return_value = temp
        self.assertTrue(value == self.serwer.get_weather(site, time).values[0][1])

    @parameterized.parameterized.expand(
        list(itertools.chain.from_iterable(
            list(map(lambda site: list(map(lambda days:
                (site, days), 
        range(1,7))), list(data_meteo.columns)[1:]))))
    )
    @unittest.skipIf(testing != "test_get_weather_forecast" and testing != "all", "TDD")
    def test_get_weather_forecast_length(self, site, days):
        temp = data_meteo[["datetime", site]]
        temp.columns = ["datetime", "value"]
        self.serwer.get_data = mock.Mock(name = "get_data")
        self.serwer.get_data.return_value = temp
        self.assertTrue(days == len(self.serwer.get_weather_forecast(site, days)))
    
    @parameterized.parameterized.expand(
        list(map(lambda site:
                (site, 1), 
        list(data_meteo.columns)[1:]))
    )
    @unittest.skipIf(testing != "test_get_weather_forecast" and testing != "all", "TDD")
    def test_get_weather_forecast_date(self, site, days):
        temp = data_meteo[["datetime", site]]
        temp.columns = ["datetime", "value"]
        self.serwer.get_data = mock.Mock(name = "get_data")
        self.serwer.get_data.return_value = temp
        self.assertTrue(list(temp['datetime'])[-1].date() + datetime.timedelta(days=1) == list(self.serwer.get_weather_forecast(site, days)['datetime'])[0].date())

unittest.main()
