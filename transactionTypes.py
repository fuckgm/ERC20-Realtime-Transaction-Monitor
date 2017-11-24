# -*- coding: utf-8 -*-
from analyzeTransaction import basic, get_transaction_receipt, get_logs, get_value_from_input, get_to_address_transferFrom, get_to_addr_from_input

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
    tmp["tx_from"] = tmp["erc20_to"]
    tmp["erc20_to"] = "0x"+get_to_address_transferFrom(tx["input"])
    return tmp

def sweep(tx):
    tmp = basic(tx)
    tmp["type"] = "sweep"
    tmp["tx_to"] = get_to_addr_from_input(tx["input"])
    tmp["erc20_value"] = get_value_from_input(tx["input"])

    ret_receipt = get_transaction_receipt(tx["hash"])
    logs = get_logs(ret_receipt)
    if logs:
        
        topics = ["0","0","0"]
        for each_log in logs:
            if len(each_log['topics']) == 4:
                topics = each_log["topics"]    

        if topics[1] == "0":
            print "\ttopic not valid for sweep"
        tmp["tx_from"] = "0x"+topics[1].strip("0").strip("0x")
        tmp["erc20_to"] = "0x"+topics[2].strip("0").strip("0x")
    return tmp

def approve(tx):
    tmp = basic(tx)
    tmp["type"] = "approve"
    tmp["erc20_value"] = get_value_from_input(tx["input"])
    return tmp

def add_whitelist(tx): #Herocoin 
    tmp = basic(tx)
    tmp["type"] = "whitelisting"
    tmp["erc20_value"] = 0
    tmp["whitelisted"] = get_to_addr_from_input(tx["input"])
    return tmp