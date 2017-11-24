# -*- coding: utf-8 -*-

import time; 
from helper_log import prettify,save_dictionary_to_json

def getTransactionsFromBlock(block):
    txs = []
    for tx in block[u'transactions']:
        txs.append(tx)
    return txs

def getFilteredTransactionsFromBlock(block, filter_list):
    txs = []
    if not type(block) == dict:
        print "\tMalformed block found: "  + str(block)
        return txs

    if u'transactions' not in block.keys():
        return txs

    for tx in block[u'transactions']:
        if tx[u'to'] is None: #skip contract creation txs and stuff
            continue

        if tx[u'to'].upper() in filter_list.keys():
            tx["ico_id"] = filter_list[tx['to'].upper()]
            txs.append(tx)

        else:
            for hashes in filter_list.keys():
                if hashes[2:] in tx[u'input'].upper():
                    tx["ico_id"] = filter_list[hashes]
                    txs.append(tx)
            
    return txs

def getBlockTimestamp(block):
    stamp = int(block[u'timestamp'],16)
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stamp))
    