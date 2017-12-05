# -*- coding: utf-8 -*-
from analyzeReceipt import get_logs_from_receipt, get_to_addr_from_input, get_gas_limit, get_gas_used, get_status
from rpc_connector import get_transaction_receipt
import re

def basic(tx):
    tmp = {}
    tmp["blockNumber"] = int(tx["blockNumber"],16)
    tmp["blockTimestamp"] = tx["blockTimestamp"]
    tmp["tx_from"] = tx["from"]
    tmp["hash"] = tx["hash"]
    tmp["tx_to"] = tx["to"]
    tmp["erc20_to"] = "0x"+remove_leading_zeros(get_to_addr_from_input(tx["input"]))

    eth_value = tx["value"]
    if eth_value == "0x0":
        tmp["eth_value"] = 0
    else:
        tmp["eth_value"] = int(eth_value,16) 

    ret_receipt = get_transaction_receipt(tx["hash"])
    tmp["gas_used"] = get_gas_used(ret_receipt)
    tmp["status"] = get_status(ret_receipt)

    tmp["gas_limit"] = get_gas_limit(tx)
    tmp["success"] = transaction_succeess(tmp)

    return tmp
    
def get_to_address_transferFrom(input_data):
    params = input_data[10+64:]
    return remove_leading_zeros(params[:64])

def remove_leading_zeros(foo):
    regex = r'(0*)(.*)'
    search = re.search(regex, foo)
    return search.group(2)

def get_value_from_input(input_data):
    params = input_data[10:]
    value = params[64:]
    value = int(value, 16)
    return value

def get_value_from_input(input):
    params = input[10:]
    value = params[64:]
    value = int(value, 16)
    return value

# Pre-Byzantium update: No Flag if tx successfull or not
# gaslimit = gasused is an indicator(!) 
#   to be 100% sure use trace Transaction!
def transaction_succeess(fin):
    byzantium = 4370000
    if fin["blockNumber"] >= byzantium:
        if fin["status"]:
            return True
        else:
            return False
    return (fin["gas_used"] < fin["gas_limit"])