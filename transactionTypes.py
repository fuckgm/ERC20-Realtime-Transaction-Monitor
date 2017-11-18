# -*- coding: utf-8 -*-
from analyzeTransaction import basic, get_transaction_receipt, get_logs, get_value_from_input, get_to_address_transferFrom

def crowdsale(tx):
    tmp = basic(tx)
    tmp["type"] = "crowdsale"
    
    ret_receipt = get_transaction_receipt(tx["hash"])
    logs = get_logs(ret_receipt)
    if logs:
    
        # overwrite values from basic()
        tmp["erc20_to"] = ret_receipt["from"]
    return tmp

def angel(tx):
    tmp = basic(tx)
    tmp["type"] = "angel"
    tmp["eth_value"] = get_value_from_input(tx["input"])
    return tmp

def deposit_token(tx):
    tmp = basic(tx)
    tmp["type"] = "ed_deposit"
    tmp["erc20_value"] = get_value_from_input(tx["input"])
    return tmp

def withdraw_token(tx):
    tmp = basic(tx)
    tmp["type"] = "ed_withdraw"
    tmp["erc20_value"] = get_value_from_input(tx["input"])
    return tmp

def transfer(tx):
    tmp = basic(tx)
    tmp["type"] = "transfer"
    return tmp

def team_tokens(tx):
    tmp = basic(tx)
    tmp["type"] = "team_tokens"
    return tmp

def transfer_from(tx):
    tmp = basic(tx)
    tmp["type"] = "transfer_from"
    tmp["erc20_from"] = tmp["erc20_to"]
    tmp["erc20_to"] = "0x"+get_to_address_transferFrom(tx["input"])
    return tmp

def sweep(tx):
    tmp = basic(tx)
    tmp["type"] = "sweep"
    tmp["erc20_value"] = get_value_from_input(tx["input"])
    return tmp