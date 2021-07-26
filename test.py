#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 25 15:46:04 2021

@author: SSP
"""

import yfinance as yf

from utils_ssp_extended import get_sharecounts

def fundamental_data(ticker_str):
    ticker_obj = yf.Ticker(ticker_str)
    
    _bs = ticker_obj.balancesheet   # balance sheet
    _is = ticker_obj.financials     # income statement
    _cf = ticker_obj.cashflow       # cashflow statement
    
    # reverse columns to go left (earliest) 2 right (latest)
    _bs = _bs.iloc[:, ::-1]
    _is = _is.iloc[:, ::-1] 
    _cf = _cf.iloc[:, ::-1]
    
    tmp = get_sharecounts(ticker_str)   # get share counts with custom function
    _bs = _bs.append(tmp)               # append share counts to _bs data
    
    return {'bs' : _bs, 
            'is' : _is, 
            'cf' : _cf}

# tk_dbs = yf.Ticker('D05.si')
# tk_uob = yf.Ticker('U11.si')
# tk_ocbc= yf.Ticker('H02.si')

# earn_dbs = tk_dbs.earnings
# earn_uob = tk_uob.earnings
# earn_ocbc= tk_ocbc.earnings

# shares_dbs = tk_dbs.info['sharesOutstanding']
# shares_uob = tk_uob.info['sharesOutstanding']
# shares_ocbc = tk_ocbc.info['sharesOutstanding']

# bs_dbs = tk_dbs.balancesheet

tickers = ['D05.si']
data = {}

for ticker in tickers:
    data[ticker] = fundamental_data(ticker)

bs_dbs = data['D05.si']['bs']
is_dbs = data['D05.si']['is']
cf_dbs = data['D05.si']['cf']

''' 
info_dbs = tk_dbs.history(period='2y',interval='1d')
info_uob = tk_uob.history(period='2y',interval='1d')
info_ocbc= tk_ocbc.history(period='2y',interval='1d')
'''