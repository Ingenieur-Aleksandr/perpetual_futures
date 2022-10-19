import json
import requests
import toml
from copy import deepcopy


# GLOBALS
# Package version
__version__ = '0.0.1'
# Available APIs
AVAILABLE = ['FTX', 'Binance']


def get_available_apis():
    print('Currently available: ' + ', '.join(AVAILABLE))


class API:
    """
    API object allows user to connect to the API of desirable CEX or DEX\n
    Using RestAPI requests and requests library API object with predefined methods allows to get such data as:\n
    * list of all futures\n
    * historical base actives prices\n
    * historical futures prices\n
    * historical funding rates\n

    Parameters
    ----------
    config_path : str
        path to config file in .toml format
    exchange_source : str
        exchange that should be used as data source
    """
    __version__ = '0.0.1'

    def __init__(self, config_path='settings.toml', exchange_source='FTX'):
        self.config_path = config_path
        self.exchange_source = exchange_source
        self.config = toml.load(self.config_path)[self.exchange_source]

    def get_all_available_futures(self):
        """
        Return all available futures with current price info

        Returns
        -------
        any(string, list, dict)
            answer of request with data or error-message
        """
        return self._get_data('futures_list')

    def get_historical_futures_prices(self, **parameters):
        """
        Return historical market data from API using predefined parameters (see the parameters in the official
        documentation of the platform you are interested in; currently, Binance and FTX are available).\n
        Parameters of API request to get historical prices data are following:\n
            > ticker -- name of ticker for example BTCUSDT, BTC-PERP etc.\n
            > candle_interval -- time interval of one candle, defined by open, high, low, close prices and volume\n
            > start_time -- start time of period of interest\n
            > end_time -- end time of period of interest\n

        Parameters
        ----------
        parameters : **kwargs
            parameters of API request which should be provided to get historical data

        Returns
        -------
        any(string, list, dict)
            answer of request with data or an error-message
        """
        return self._get_data('historical_prices', **parameters)

    def get_historical_funding_rates(self, **parameters):
        """
        Return historical funding rates from API using predefined parameters (see the parameters in the official
        documentation of the platform you are interested in; peace).\n
        Parameters of API request to get historical prices data are following:\n
            > ticker -- name of ticker for example BTCUSDT, BTC-PERP etc.\n
            > start_time -- start time of period of interest\n
            > end_time -- end time of period of interest\n

        Parameters
        ----------
        parameters : **kwargs
            parameters of API request which should be provided to get historical data

        Returns
        -------
        any(string, list, dict)
            answer of request with data or an error-message
        """
        return self._get_data('funding_rates', **parameters)

    def _get_data(self, requested_data: str, **parameters):
        # Method returns data from API according to its label provided in requested_data variable\n
        # Agreement: parameters SHOULD NOT BE PROVIDED for requests without parameters

        method = self.config[requested_data]['method']
        request_body = self.config[requested_data]['request']
        request_address = self.config['head'] + request_body['address']

        if parameters != dict(): # process parameters part provided in input and config
            assert 'parameters_mapping' in self.config[requested_data].keys(), 'No parameters mapping is available'
            parameters_mapping = self.config[requested_data]['parameters_mapping']
            old_parameters_keys = deepcopy(list(parameters.keys()))
            for k_old in old_parameters_keys:
                parameters[parameters_mapping[k_old]] = parameters.pop(k_old)
            if all(('replaceable' in request_body.keys(), 'replaceable' in parameters.keys())):
                replaceable = request_body['replaceable']
                request_address = request_address.replace(replaceable, parameters['replaceable'])
                parameters.pop('replaceable')

        result = requests.request(method, url=request_address, params=parameters)
        answer = API._check_request_result_code(result)
        return answer

    @staticmethod
    def _check_request_result_code(result: requests.request):
        # Static method for request results status code processing
        return json.loads(result.text) if result.status_code == 200 else 'Error ' + str(result.status_code)
