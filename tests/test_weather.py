import sys
sys.path.append("./")
from src.Weather import Weather
from packages import *

from matchers import is_good_Describtion_values, is_good_Describtion_keys
from src.config import host

assertpy.add_extension(is_good_Describtion_keys)

data_meteo = pd.read_csv("data/data_meteo_2008_03-07.csv")
data_meteo["datetime"] = pd.to_datetime(data_meteo["datetime"])

class Test_Weather(unittest.TestCase):

    testing = "all"

    @requests_mock.Mocker()
    def setUp(self, mock_request):
        mock_request.get(f'{host}/localizations', json={'localizations': list(data_meteo.columns)[1:]})
        self.serwer = Weather(host)
    
    @parameterized.parameterized.expand([
        ('', ),
        ('1234', ),
        ('56789', ),
        (123, ),
        (2*9+0, )
    ])
    @unittest.skipIf(testing != "test_get_data" and testing != "all", "TDD")
    def test_get_data_exception(self, site):
        hamcrest.assert_that(hamcrest.calling(self.serwer.get_data).with_args(site), hamcrest.raises(Exception))

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

    @parameterized.parameterized.expand(
        list(map(lambda site:
                (site), 
        list(data_meteo.columns)[1:]))
    )
    @unittest.skipIf(testing != "test_weather_static" and testing != "all", "TDD")
    def test_weather_static_length(self, site):
        temp = data_meteo[["datetime", site]]
        temp.columns = ["datetime", "value"]
        self.serwer.get_data = mock.Mock(name = "get_data")
        self.serwer.get_data.return_value = temp
        self.assertTrue(len(self.serwer.weather_static(site).index) == 8)

    @parameterized.parameterized.expand(
        list(map(lambda site:
                (site), 
        list(data_meteo.columns)[1:]))
    )
    @unittest.skipIf(testing != "test_weather_static" and testing != "all", "TDD")
    def test_weather_static_values(self, site):
        temp = data_meteo[["datetime", site]]
        temp.columns = ["datetime", "value"]
        self.serwer.get_data = mock.Mock(name = "get_data")
        self.serwer.get_data.return_value = temp
        hamcrest.assert_that([self.serwer.weather_static(site)['value'], temp.describe()['value']], hamcrest.is_(is_good_Describtion_values()))
    
    @parameterized.parameterized.expand(
        list(map(lambda site:
                (site), 
        list(data_meteo.columns)[1:]))
    )
    @unittest.skipIf(testing != "test_weather_static" and testing != "all", "TDD")
    def test_weather_static_keys(self, site):
        temp = data_meteo[["datetime", site]]
        temp.columns = ["datetime", "value"]
        self.serwer.get_data = mock.Mock(name = "get_data")
        self.serwer.get_data.return_value = temp
        assertpy.assert_that(self.serwer.weather_static(site).index).is_good_Describtion_keys()
    
    @parameterized.parameterized.expand(
        list(map(lambda site:
                (site), 
        list(data_meteo.columns)[1:]))
    )
    @unittest.skipIf(testing != "test_weather_static" and testing != "all", "TDD")
    def test_weather_static_localizations(self, site):
        temp = data_meteo[["datetime", site]]
        temp.columns = ["datetime", "value"]
        self.serwer.get_data = mock.Mock(name = "get_data")
        self.serwer.get_data.return_value = temp
        self.serwer.weather_static(site)

    @parameterized.parameterized.expand([
        ('', ),
        ('1234', ),
        ('56789', ),
        (123, )
    ])
    @unittest.skipIf(testing != "test_weather_static" and testing != "all", "TDD")
    def test_weather_static_localizations_exceptions(self, site):
        assertpy.assert_that(self.serwer.weather_static).raises(Exception).when_called_with(site)
    
    @parameterized.parameterized.expand(
        list(map(lambda site:
                (site), 
        list(data_meteo.columns)[1:]))
    )
    @requests_mock.Mocker()
    @unittest.skipIf(testing != "test_save_weather" and testing != "all", "TDD")
    def test_save_weather(self, site, mock_request):
        temp = data_meteo[["datetime", site]]
        temp.columns = ["datetime", "value"]
        mock_request.post(f'{host}/save/{site}', text='OK')
        self.assertTrue(self.serwer.save_weather(site, temp) == 'OK')
    
    @parameterized.parameterized.expand(
        list(map(lambda site:
                (site), 
        list(data_meteo.columns)[1:]))
    )
    @requests_mock.Mocker()
    @unittest.skipIf(testing != "test_update_weather" and testing != "all", "TDD")
    def test_update_weather(self, site, mock_request):
        temp = data_meteo[["datetime", site]]
        temp.columns = ["datetime", "value"]
        mock_request.put(f'{host}/save/{site}', text='OK')
        self.assertTrue(self.serwer.update_weather(site, temp) == 'OK')
    
    @parameterized.parameterized.expand(
        list(map(lambda site:
                (site), 
        list(data_meteo.columns)[1:]))
    )
    @requests_mock.Mocker()
    @unittest.skipIf(testing != "test_delete_weather" and testing != "all", "TDD")
    def test_delete_weather(self, site, mock_request):
        mock_request.delete(f'{host}/{site}', text='OK')
        self.assertTrue(self.serwer.delete_weather(site) == 'OK')

unittest.main()
