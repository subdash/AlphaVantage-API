from enum import Enum


class Interval(Enum):
    MIN1 = "1min"
    MIN5 = "5min"
    MIN15 = "15min"
    MIN30 = "30min"
    MIN60 = "60min"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class OutputSize(Enum):
    COMPACT = "compact"
    FULL = "full"


class DataType(Enum):
    CSV = "csv"
    JSON = "json"


class SeriesType(Enum):
    CLOSE = "CLOSE"
    OPEN = "OPEN"
    HIGH = "HIGH"
    LOW = "LOW"


class MAType(Enum):
    SMA = 0    # Simple Moving Average
    EMA = 1    # Exponential Moving Average
    WMA = 2    # Weighted Moving Average
    DEMA = 3   # DoubleExponential Moving Average
    TEMA = 4   # Triple Exponential Moving Average
    TRIMA = 5  # Triangular Moving Average
    T3 = 6     # T3 Moving Average
    KAMA = 7   # Kaufman Adaptive Moving Average
    MAMA = 8   # MESA Adaptive Moving Average


class Horizon(Enum):
    THREE_MONTH = "3month"
    SIX_MONTH = "6month"
    TWELVE_MONTH = "12month"


validate_param = {
    "function": lambda val: val.value in dir(AVFunction),
    "apikey": lambda val: isinstance(val, str),
    "symbol": lambda val: isinstance(val, str),
    "interval": lambda val: isinstance(val, Interval),
    "adjusted": lambda val: isinstance(val, bool),
    "outputsize": lambda val: isinstance(val, OutputSize),
    "datatype": lambda val: isinstance(val, DataType),
    "from_currency": lambda val: isinstance(val, str),
    "to_currency": lambda val: isinstance(val, str),
    "from_symbol": lambda val: isinstance(val, str),
    "to_symbol": lambda val: isinstance(val, str),
    "time_period": lambda val: isinstance(val, int) and val > 0,
    "series_type": lambda val: isinstance(val, SeriesType),
    "fast_period": lambda val: isinstance(val, int) and val > 0,
    "slow_period": lambda val: isinstance(val, int) and val > 0,
    "signal_period": lambda val: isinstance(val, int) and val > 0,
    "nbdevup": lambda val: isinstance(val, int) and val > 0,
    "nbdevdn": lambda val: isinstance(val, int) and val > 0,
    "matype": lambda val: isinstance(val, MAType) or val in range(0, 9),
    "horizon": lambda val: isinstance(val, Horizon)
}

enum_params = ["function", "interval", "outputsize", "datatype", "seriestype", "matype"]


# Function enumeration
class AVFunction:
    """
    Each nested class is a function that can be passed as a query param.
    The value field is the string passed as the query param, and the required
    field is a set of the other query params that are required which correspond
    to the function. function and apikey are always required, so those are
    omitted from the set and checked elsewhere.

    For optional query params, refer to the API documentation here.
    https://www.alphavantage.co/documentation/
    """

    ###########################################################################
    # Stock time series
    ###########################################################################
    class TIME_SERIES_INTRADAY:
        value = "TIME_SERIES_INTRADAY"
        required = {"symbol", "interval"}

    class TIME_SERIES_DAILY_ADJUSTED:
        value = "TIME_SERIES_DAILY_ADJUSTED"
        required = {"symbol"}

    class QUOTE_ENDPOINT:
        value = "QUOTE_ENDPOINT"
        required = {"symbol"}

    ###########################################################################
    # Fundamental data
    ###########################################################################
    class OVERVIEW:
        value = "OVERVIEW"
        required = {"symbol"}

    class EARNINGS:
        value = "EARNINGS"
        required = {"symbol"}

    # CSV-only
    class EARNINGS_CALENDAR:
        value = "EARNINGS_CALENDAR"
        required = set()
        response_type = DataType.CSV

    # CSV-only
    class IPO_CALENDAR:
        value = "IPO_CALENDAR"
        required = set()
        response_type = DataType.CSV

    ###########################################################################
    # Forex
    ###########################################################################
    class CURRENCY_EXCHANGE_RATE:
        value = "CURRENCY_EXCHANGE_RATE"
        required = {"from_currency", "to_currency"}

    class FX_INTRADAY:
        value = "FX_INTRADAY"
        required = {"interval", "from_symbol", "to_symbol"}

    ###########################################################################
    # Crypto
    ###########################################################################
    class CRYPTO_RATING:
        value = "CRYPTO_RATING"
        required = {"symbol"}

    ###########################################################################
    # TA indicators
    ###########################################################################
    class SMA:
        value = "SMA"
        required = {"symbol", "interval", "time_period", "series_type"}

    class EMA:
        value = "EMA"
        required = {"symbol", "interval", "time_period", "series_type"}

    class VWAP:
        value = "VWAP"
        required = {"symbol", "interval"}

    class MACD:
        value = "MACD"
        required = {"symbol", "interval", "series_type"}

    class STOCH:
        value = "STOCH"
        required = {"symbol", "interval"}

    class RSI:
        value = "RSI"
        required = {"symbol", "interval", "time_period", "series_type"}

    class ADX:
        value = "ADX"
        required = {"symbol", "interval", "time_period"}

    class CCI:
        value = "CCI"
        required = {"symbol", "interval", "time_period"}

    class AROON:
        value = "AROON"
        required = {"symbol", "interval", "time_period"}

    class BBANDS:
        value = "BBANDS"
        required = {"symbol", "interval", "time_period", "series_type"}

    class AD:
        value = "AD"  # # symbol, interval (datatype)
        required = {"symbol", "interval"}

    class OBV:
        value = "OBV"  # # symbol, interval (datatype)
        required = {"symbol", "interval"}
