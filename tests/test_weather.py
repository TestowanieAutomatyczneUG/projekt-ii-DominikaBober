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
    @unittest.skipIf(testing!= "test_get_weather" and testing!="all", "TDD")
    def test_get_weather(self, site, time, value):
        temp = data_meteo[["datetime", site]]
        temp.columns = ["datetime", "value"]
        self.serwer.get_data = mock.Mock(name = "get_data")
        self.serwer.get_data.return_value = temp
        self.assertTrue(value == self.serwer.get_weather(site, time).values[0][1])

unittest.main()
