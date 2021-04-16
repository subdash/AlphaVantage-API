from service.sqlite_cache import SQLiteCache
from support import network


class AlphaVantageService:
    def __init__(self):
        self.cache = SQLiteCache()

    def get(self, payload):
        """Get JSON response that would be returned from a call to the Alpha
        Vantage API. There are three ways this method can return:

        1. Result has not been cached:
           - make api call
           - create new DB entry
        2. Result has been cached but is out of date (!is_recent):
           - make api call
           - update DB entry
        3. Result has been cached and is up to date (is_recent):
           - return result directly from DB

        Args:
            payload (dict): a dictionary containing at the least an API key
            and Function (required for all API calls), as well as any
            additional query params as key/value pairs

        Returns:
            dict: JSON response from Alpha Vantage API or SQLite cache
        """
        req_info = network.get_request_info(**payload)
        url = req_info['url']
        data_type = req_info['data_type']
        cache_res = self.cache.read_entry(url, data_type)

        if cache_res:
            if not self.cache.is_recent(url, data_type):
                res = network.api_call(payload)
                self.cache.update_entry(res)

                return res

            return self.cache.read_entry(url, data_type)

        res = network.api_call(payload)
        self.cache.create_entry(res)

        return res
