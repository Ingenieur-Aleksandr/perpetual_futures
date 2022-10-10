import json
import requests
import toml
from copy import deepcopy


def get_available_apis():
    print('Currently available: FTX, Binance')


class API:
    def __init__(self, config_path: str, exchange_source: str):
        self.config_path = config_path
        self.exchange_source = exchange_source
        self.config = toml.load(self.config_path)[self.exchange_source]

    @staticmethod
    def _check_request_result_code(result: requests.request):
        answer = None
        if result.status_code == 200:
            answer = json.loads(result.text)
        else:
            answer = 'Error ' + str(result.status_code)
        return answer

    def get_all_available_tickers(self):
        """
        Return all available futures with current price info
        Returns
        -------
        any(string, list, dict)
            answer of request with data or error-message
        """
        method = self.config['futures_list']['method']
        request_address = self.config['head'] + self.config['futures_list']['request']['address']
        result = requests.request(method, url=request_address)
        answer = API._check_request_result_code(result)
        return answer

    def get_historical_data(self, **parameters):
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
            answer of request with data or error-message
        """
        method = self.config['historical_data']['method']
        request_body = self.config['historical_data']['request']
        # parameters = self.config['historical_data']['parameters']
        parameters_mapping = self.config['historical_data']['parameters_mapping']

        request_address = self.config['head'] + request_body['address']
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
