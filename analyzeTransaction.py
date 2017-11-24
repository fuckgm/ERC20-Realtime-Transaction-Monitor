# -*- coding: utf-8 -*-
from rpc_connector import get_transaction_receipt
from analyzeReceipt import get_logs, get_to_addr_from_input

WEI_TO_VIB = 1e-18
WEI_TO_ETH = 1e-18

def basic(tx):
    tmp = {}
    tmp["blockNumber"] = int(tx["blockNumber"],16)
    tmp["tx_from"] = tx["from"]
    tmp["hash"] = tx["hash"]
    tmp["tx_to"] = tx["to"]
    tmp["type"] = "crowdsale"
    tmp["erc20_to"] = "0x"+get_to_addr_from_input(tx["input"])

    eth_value = tx["value"]
    if eth_value == "0x0":
        tmp["eth_value"] = 0
    else:
        tmp["eth_value"] = int(eth_value,16) * WEI_TO_ETH # change it back to ,16?

    ret_receipt = get_transaction_receipt(tx["hash"])
    tmp["gas_used"] = int(ret_receipt["gasUsed"],16)
    tmp["gas_limit"] = int(tx["gas"],16)

    if "status" in ret_receipt.keys():
        tmp["status"] = int(ret_receipt["status"],16)

    # Some have more log-entries than just one. 
    # haven't into it in detail, but the log-entry with the most "hits" usually has the relevant data/value
    # ==> Look it up in the docs!    
    logs = get_logs(ret_receipt)
    ana_logs = {}
    if logs:
        if len(logs) == 1:
            tmp["erc20_value"] = int(logs[0]["data"],16) * WEI_TO_VIB   
        elif len(logs) > 1:
            for i in range(0, len(logs)):
                data = logs[i]["data"]
                if data in ana_logs.keys():
                    ana_logs[data] += 1
                else:
                    ana_logs[data] = 1
            try:     
                maxi = max(ana_logs, key=ana_logs.get)
                tmp["erc20_value"] = int(maxi,16) * WEI_TO_VIB
            except StandardError as StdEX:
                print "\tHasheeee:" + tx["hash"]
                print "\tError in Basic! " + str(StdEX)
            

    tmp["success"] = transaction_succeess(tmp)
    return tmp

def transaction_succeess(fin):
    byzantium = 4370000
    if fin["blockNumber"] >= byzantium:
        if fin["status"]:
            return True
        else:
            return False
    return (fin["gas_used"] < fin["gas_limit"])

def get_method(input):
    if (len(input) - 8 - 2) % 64 != 0:
        print '\tData size misaligned with parse request'
        print input
    return input[:10]

def get_value_from_input(input):
    params = input[10:]
    value = params[64:]
    value = int(value, 16) * WEI_TO_VIB
    return value

def get_to_address_transferFrom(input):
    params = input[10+64:]
    return params[:64].strip('0')