#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 20:09:04 2021

Contains function adapted from yfinance package to grab share counts over time

@author: SSP
"""

from __future__ import print_function

import requests as _requests
import re as _re
import pandas as _pd
import numpy as _np
import sys as _sys
import re as _re

try:
    import ujson as _json
except ImportError:
    import json as _json

user_agent_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

_scrape_url = 'https://finance.yahoo.com/quote/'

def get_sharecounts(ticker, proxy=None, session=None):
    '''
    Gets share counts from yahoo finance. Enter ticker

    Parameters
    ----------
    ticker : string
        ticker of the stock on yahoo finance.
    proxy : TYPE, optional
        Not sure what it does, copied from yfinance. The default is None.
    session : TYPE, optional
        Not sure what it does, copied from yfinance. The default is None.

    Returns
    -------
    df
        sharecounts as dataframe.

    '''
    url = _scrape_url + ticker + '/balance-sheet'   # go into balance sheet page
    
    session = session or _requests
    html = session.get(url=url, proxies=proxy, headers=user_agent_headers).text
        
    if "QuoteTimeSeriesStore" not in html:
        html = session.get(url=url, proxies=proxy).text
        if "QuoteTimeSeriesStore" not in html:
            return {}

    json_str = html.split('root.App.main =')[1].split(
        '(this)')[0].split(';\n}')[0].strip()
    
    data = _json.loads(json_str)['context']['dispatcher']['stores']['QuoteTimeSeriesStore']
    
    data = data['timeSeries']['annualOrdinarySharesNumber']     # list
    
    datestrings = []
    sharecounts = []
    for item in data:
        datestring = item['asOfDate']
        sharecount = item['reportedValue']['raw']
        datestrings.append(datestring)
        sharecounts.append(sharecount)
            
    df = _pd.DataFrame({'Sharecounts' : sharecounts}, index=datestrings)
    return df.transpose()
