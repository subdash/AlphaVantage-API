#!/usr/bin/env python3

from tools.compare_earnings import compare_earnings
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-k', action='store', metavar='apikey', required=True,
                    help='API key')
parser.add_argument('-t', action='store', metavar='ticker',
                    help='stock ticker')
parser.add_argument('--cmpearnings', action='store_true',
                    help='compare predicted earnings with past earnings')
args = parser.parse_args()

api_key = args.k
ticker = None

if args.t:
    ticker = args.t

if args.cmpearnings:
    if not ticker:
        print("Error: cmpearnings requires -t [ticker] argument")
        exit(1)

    result = compare_earnings(api_key, ticker)
    exit(result)
