from support.network import *
from support.data_classes import *
from functools import reduce


def compare_earnings(api_key, ticker):
    earnings_history_args = {
        "function": AVFunction.EARNINGS,
        "symbol": ticker,
        "apikey": api_key
    }
    earnings_calendar_args = dict(earnings_history_args)
    earnings_calendar_args['function'] = AVFunction.EARNINGS_CALENDAR

    # Submit requests
    earnings_history_res = api_call(earnings_history_args)
    earnings_calendar_res = api_call(earnings_calendar_args)

    # Parse out JSON data of last 4 quarters
    last_4_quarters = earnings_history_res.json()['quarterlyEarnings'][:4]
    if not last_4_quarters:
        print("Quarterly earnings information unavailable.")
        exit(1)

    # If reportedEPS data is unavailable, we don't have a complete set of the
    # last 4 quarters data.
    if 'None' in list(map(lambda x: x['reportedEPS'], last_4_quarters)):
        sans_this_quarter = earnings_history_res.json()['quarterlyEarnings'][1:5]
        if 'None' in list(map(lambda x: x['reportedEPS'], sans_this_quarter)):
            print("Quarterly earnings is missing data.")
            exit(1)
        last_4_quarters = sans_this_quarter

    last_year_avg = reduce(lambda x, y: float(x) + float(y),
                           list(map(lambda x: x['reportedEPS'], last_4_quarters))) / 4

    # Parse out CSV data of expected earnings
    lines = [line.decode('utf-8') for line in earnings_calendar_res.readlines()]

    has_earnings_projection = len(lines) > 1 and lines[1].split(',')[4]
    announcement_date = "N/A"
    expected_earnings = "(unavailable)"

    if has_earnings_projection:
        announcement_date = lines[1].split(',')[2]
        expected_earnings = lines[1].split(',')[4]

        if not expected_earnings:
            has_earnings_projection = False

    print(f"Ticker: {ticker}")
    print(f"Earnings will be announced: {announcement_date}")
    print("Earnings information for last 4 quarters:")
    print("=" * 43)
    print("\tyearly EPS average: {:.2f}".format(last_year_avg))
    for q in last_4_quarters:
        print("=" * 43)
        print(f"\treportedDate: {q['reportedDate']}")
        print(f"\treportedEPS: {q['reportedEPS']}")
        print(f"\tsurprisePercentage: {q['surprisePercentage']}")

    print(f"\nNext quarter expected earnings:\n\t{expected_earnings}")

    if has_earnings_projection:
        earnings_delta_last_q = float(expected_earnings) / float(last_4_quarters[0]['reportedEPS'])
        earnings_delta_last_year = float(expected_earnings) / float(last_year_avg)
        print("Expected earnings / last quarter earnings:\n\t{:.2f}".format(earnings_delta_last_q))
        print("Expected earnings / last year avg. earnings:\n\t{:.2f}".format(earnings_delta_last_year))

    exit(0)
