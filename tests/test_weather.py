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

    @parameterized.parameterized.expand(
        list(map(lambda localization:
                (localization, ), 
        list(data_meteo.columns)[1:]))
    )
    @requests_mock.Mocker()
    @unittest.skipIf(testing != "test_get_data" and testing != "all", "TDD")
    def test_get_data(self, localization, mock_request):
        temp = data_meteo[["datetime", localization]].copy()[-10:]
        temp.columns = ["datetime", "value"]
        temp.loc[:, 'datetime'] = temp['datetime'].astype(str)
        mock_request.get(f"{host}/data/{localization}", json={"data": temp.to_dict(orient='list')})
        self.assertTrue(self.serwer.get_data(localization).equals(temp.reset_index(drop=True)))

    @parameterized.parameterized.expand([
        ('', ),
        ('1234', ),
        ('56789', ),
        (123, ),
        (2*9+0, )
    ])
    @unittest.skipIf(testing != "test_get_data" and testing != "all", "TDD")
    def test_get_data_exception(self, localization):
        hamcrest.assert_that(hamcrest.calling(self.serwer.get_data).with_args(localization), hamcrest.raises(Exception))

    @parameterized.parameterized.expand(
        list(itertools.chain.from_iterable(
            list(map(lambda localization: list(map(lambda time, value: 
                (localization, time, value),
            data_meteo[::6*24]["datetime"], data_meteo[::6*24][localization])),
        list(data_meteo.columns)[1:]))))
    )
    @unittest.skipIf(testing != "test_get_weather" and testing != "all", "TDD")
    def test_get_weather(self, localization, time, value):
        temp = data_meteo[["datetime", localization]]
        temp.columns = ["datetime", "value"]
        self.serwer.get_data = mock.Mock(name = "get_data")
        self.serwer.get_data.return_value = temp
        self.assertTrue(value == self.serwer.get_weather(localization, time).values[0][1])

    @parameterized.parameterized.expand(
        list(itertools.chain.from_iterable(
            list(map(lambda localization: list(map(lambda days:
                (localization, days), 
        range(1,7))), list(data_meteo.columns)[1:]))))
    )
    @unittest.skipIf(testing != "test_get_weather_forecast" and testing != "all", "TDD")
    def test_get_weather_forecast_length(self, localization, days):
        temp = data_meteo[["datetime", localization]]
        temp.columns = ["datetime", "value"]
        self.serwer.get_data = mock.Mock(name = "get_data")
        self.serwer.get_data.return_value = temp
        self.assertTrue(days == len(self.serwer.get_weather_forecast(localization, days)))
    
    @parameterized.parameterized.expand(
        list(map(lambda localization:
                (localization, 1), 
        list(data_meteo.columns)[1:]))
    )
    @unittest.skipIf(testing != "test_get_weather_forecast" and testing != "all", "TDD")
    def test_get_weather_forecast_date(self, localization, days):
        temp = data_meteo[["datetime", localization]]
        temp.columns = ["datetime", "value"]
        self.serwer.get_data = mock.Mock(name = "get_data")
        self.serwer.get_data.return_value = temp
        self.assertTrue(list(temp['datetime'])[-1].date() + datetime.timedelta(days=1) == list(self.serwer.get_weather_forecast(localization, days)['datetime'])[0].date())

    @parameterized.parameterized.expand(
        list(map(lambda localization:
                (localization), 
        list(data_meteo.columns)[1:]))
    )
    @unittest.skipIf(testing != "test_weather_static" and testing != "all", "TDD")
    def test_weather_static_length(self, localization):
        temp = data_meteo[["datetime", localization]]
        temp.columns = ["datetime", "value"]
        self.serwer.get_data = mock.Mock(name = "get_data")
        self.serwer.get_data.return_value = temp
        self.assertTrue(len(self.serwer.weather_static(localization).index) == 8)

    @parameterized.parameterized.expand(
        list(map(lambda localization:
                (localization), 
        list(data_meteo.columns)[1:]))
    )
    @unittest.skipIf(testing != "test_weather_static" and testing != "all", "TDD")
    def test_weather_static_values(self, localization):
        temp = data_meteo[["datetime", localization]]
        temp.columns = ["datetime", "value"]
        self.serwer.get_data = mock.Mock(name = "get_data")
        self.serwer.get_data.return_value = temp
        hamcrest.assert_that([self.serwer.weather_static(localization)['value'], temp.describe()['value']], hamcrest.is_(is_good_Describtion_values()))
    
    @parameterized.parameterized.expand(
        list(map(lambda localization:
                (localization), 
        list(data_meteo.columns)[1:]))
    )
    @unittest.skipIf(testing != "test_weather_static" and testing != "all", "TDD")
    def test_weather_static_keys(self, localization):
        temp = data_meteo[["datetime", localization]]
        temp.columns = ["datetime", "value"]
        self.serwer.get_data = mock.Mock(name = "get_data")
        self.serwer.get_data.return_value = temp
        assertpy.assert_that(self.serwer.weather_static(localization).index).is_good_Describtion_keys()
    
    @parameterized.parameterized.expand(
        list(map(lambda localization:
                (localization), 
        list(data_meteo.columns)[1:]))
    )
    @unittest.skipIf(testing != "test_weather_static" and testing != "all", "TDD")
    def test_weather_static_localizations(self, localization):
        temp = data_meteo[["datetime", localization]]
        temp.columns = ["datetime", "value"]
        self.serwer.get_data = mock.Mock(name = "get_data")
        self.serwer.get_data.return_value = temp
        self.serwer.weather_static(localization)

    @parameterized.parameterized.expand([
        ('', ),
        ('1234', ),
        ('56789', ),
        (123, )
    ])
    @unittest.skipIf(testing != "test_weather_static" and testing != "all", "TDD")
    def test_weather_static_localizations_exceptions(self, localization):
        assertpy.assert_that(self.serwer.weather_static).raises(Exception).when_called_with(localization)

    @parameterized.parameterized.expand([
        ('24370401', ),
        ('10831039', ),
        ('33030983', ),
        ('20803878', )
    ])
    @mock.patch.object(Weather, 'save_weather', mock.MagicMock(return_value="OK"))
    @unittest.skipIf(testing != "test_save_weather" and testing != "all", "TDD")
    def test_save_weather(self, localization):
        self.assertTrue(self.serwer.save_weather(localization, pd.DataFrame(columns=['datetime', 'value'])) == 'OK')
    
    @parameterized.parameterized.expand(
        list(map(lambda localization:
                (localization), 
        list(data_meteo.columns)[1:]))
    )
    @mock.patch.object(Weather, 'update_weather', mock.MagicMock(return_value="OK"))
    @unittest.skipIf(testing != "test_update_weather" and testing != "all", "TDD")
    def test_update_weather(self, localization):
        temp = data_meteo[["datetime", localization]]
        temp.columns = ["datetime", "value"]
        self.assertTrue(self.serwer.update_weather(localization, temp) == 'OK')
    
    @parameterized.parameterized.expand([
        ('24370401', ),
        ('10831039', ),
        ('33030983', ),
        ('20803878', )
    ])
    @unittest.skipIf(testing != "test_update_weather" and testing != "all", "TDD")
    def test_update_weather_exception(self, localization):
        hamcrest.assert_that(hamcrest.calling(self.serwer.update_weather)
        .with_args(localization, pd.DataFrame(columns=["datetime", "value"])), hamcrest.raises(Exception))
    
    @parameterized.parameterized.expand(
        list(map(lambda localization:
                (localization), 
        list(data_meteo.columns)[1:]))
    )
    @mock.patch.object(Weather, 'delete_weather', mock.MagicMock(return_value="OK"))
    @unittest.skipIf(testing != "test_localizations" and testing != "all", "TDD")
    def test_delete_weather(self, localization):
        self.assertTrue(self.serwer.delete_weather(localization) == 'OK')
    
    @parameterized.parameterized.expand([
        ('24370401', ),
        ('10831039', ),
        ('33030983', ),
        ('20803878', )
    ])
    @unittest.skipIf(testing != "test_delete_weather" and testing != "all", "TDD")
    def test_delete_weather_exception(self, localization):
        hamcrest.assert_that(hamcrest.calling(self.serwer.delete_weather)
        .with_args(localization), hamcrest.raises(Exception))

    @parameterized.parameterized.expand([
        ('24370401', ),
        ('10831039', ),
        ('33030983', ),
        ('20803878', )
    ])
    @requests_mock.Mocker()
    @unittest.skipIf(testing != "test_localizations" and testing != "all", "TDD")
    def test_localizations_after_save_weather(self, localization, mock_request):
        mock_request.post(f'{host}/save/{localization}', text='OK')
        mock_request.get(f'{host}/localizations', 
            json={'localizations': list(itertools.chain.from_iterable([list(data_meteo.columns)[1:], [localization]]))})
        self.serwer.save_weather(localization, pd.DataFrame(columns=['datetime', 'value']))
        self.assertEqual(self.serwer.localizations, list(itertools.chain.from_iterable([list(data_meteo.columns)[1:], [localization]])))
    
    @parameterized.parameterized.expand(
        list(map(lambda localization:
                (localization), 
        list(data_meteo.columns)[1:]))
    )
    @requests_mock.Mocker()
    @unittest.skipIf(testing != "test_localizations" and testing != "all", "TDD")
    def test_localizations_after_update_weather(self, localization, mock_request):
        temp = data_meteo[["datetime", localization]]
        temp.columns = ["datetime", "value"]
        mock_request.put(f'{host}/save/{localization}', text='OK')
        self.serwer.update_weather(localization, temp)
        self.assertEqual(self.serwer.localizations, list(data_meteo.columns)[1:])
    
    @parameterized.parameterized.expand(
        list(map(lambda localization:
                (localization), 
        list(data_meteo.columns)[1:]))
    )
    @requests_mock.Mocker()
    @unittest.skipIf(testing != "test_localizations" and testing != "all", "TDD")
    def test_localizations_after_delete_weather(self, localization, mock_request):
        mock_request.delete(f'{host}/{localization}', text='OK')
        mock_request.get(f'{host}/localizations', 
            json={'localizations': list(filter(lambda el: el != localization, list(data_meteo.columns)[1:]))})
        self.serwer.delete_weather(localization)
        self.assertEqual(self.serwer.localizations, list(filter(lambda el: el != localization, list(data_meteo.columns)[1:])))

unittest.main()
