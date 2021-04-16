import requests
import urllib.parse
import urllib.request

from .data_classes import *


def get_request_info(**kwargs):
    """Accepts a variable number of keyword arguments which should be supplied
    as a dictionary. `function` and `apikey` are required. The validate_params
    table is a dictionary whose values are validation functions which will be
    applied to all params. Returns the data type of HTTP response and the
    request URL with the arguments embedded as query params.

    The `api_call` function calls this function directly and can accept the
    same arguments, but they should be kept separate so that a URL can be
    passed into the caching functions without making an API call.
    """
    base_url = "https://www.alphavantage.co/query?"
    function = kwargs["function"]

    if not function.required.issubset(kwargs.keys()):
        print("The following required query params are missing:")
        print(function.required.difference(kwargs.keys()))
        exit(1)

    for k, v in kwargs.items():
        if not validate_param[k](v):
            print(f"error with key/value pair: {k}, {v}")
            exit(1)

    # Keys can be primitives or enum values defined in Python. We want to
    # separate out the enum keys for processing.
    enum_keys = list(filter(lambda key: key in enum_params, kwargs.keys()))

    for k in enum_keys:
        # matype can be MAType enum or an int
        if k == "matype" and isinstance(kwargs[k], int):
            continue

        kwargs[k] = kwargs[k].value

    if "response_type" in dir(function) and function.response_type == DataType.CSV:
        params = urllib.parse.unquote(urllib.parse.urlencode(kwargs))
        return {"data_type": DataType.CSV, "url": base_url + params}

    else:
        # Assume JSON
        req = requests.Request('GET', base_url, params=kwargs).prepare()
        return {"data_type": DataType.JSON, "url": req.url}


def api_call(call_args):
    """Accepts a dictionary of query params for an API call. If the call is
    successful, it will return a response object. If not it will return an
    empty dictionary.
    """
    payload = get_request_info(**call_args)
    data_type = payload['data_type']
    url = payload['url']
    code, res = None, None

    if data_type == DataType.CSV:
        res = urllib.request.urlopen(url)
        code = res.code

    elif data_type == DataType.JSON:
        res = requests.get(url)
        code = res.status_code

    if code != 200:
        print(f"Error: request returned response code of {res.status_code}")
        print(f"Request url: {url}")
        return {}

    return res
