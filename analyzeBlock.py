# -*- coding: utf-8 -*-

import time; 
from helper_log import prettify,save_dictionary_to_json

def getTransactionsFromBlock(block):
    txs = []
    for tx in block[u'transactions']:
        txs.append(tx)
    return txs

def getFilteredTransactionsFromBlock(block, filter):
    txs = []
    
    if u'transactions' not in block.keys():
        return txs

    for tx in block[u'transactions']:
        if tx[u'to'] is None: #skip contract creation txs and stuff
            continue

        if tx[u'to'].upper() == filter.upper():
            txs.append(tx)

        elif filter.upper()[2:] in tx[u'input'].upper():
            txs.append(tx)
            
    return txs

def getBlockTimestamp(block):
    stamp = int(block[u'timestamp'],16)
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stamp))
    