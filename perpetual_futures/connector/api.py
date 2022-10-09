import json
import requests
import toml


def _check_request_result_code(result: requests.request):
    answer = None
    if result.status_code == 200:
        answer = json.loads(result.text)
    else:
        answer = 'Error ' + str(result.status_code)
    return answer


class API:
    def __init__(self, config_path: str, exchange_source: str):
        self.config_path = config_path
        self.exchange_source = exchange_source
        self.config = toml.load(self.config_path)[self.exchange_source]

    def get_all_available_tickers(self):
        method = self.config['futures_list']['method']
        query = self.config['head'] + self.config['futures_list']['query']
        result = requests.request(method, url=query)
        answer = _check_request_result_code(result)
        return answer

    def get_historical_data(self, candle_interval, start_time, end_time):
        method = self.config['historical_data']['method']
        query = self.config['historical_data']['query']
        parameters = self.config['historical_data']['parameters']
        result = requests.request(method, url=query, params=parameters)
        answer = _check_request_result_code(result)
        return answer
