# -*- coding: utf-8 -*-

from prepareBasicTransaction import basic, get_to_address_transferFrom, get_value_from_input, remove_leading_zeros

from helper_log import prettify

def withdraw_token(tx):
    tmp = basic(tx)
    tmp["type"] = "ed_withdraw"
    tmp["erc20_value"] = get_value_from_input(tx["input"])
    tmp["erc20_to"] = tmp["tx_from"]
    tmp["tx_from"] = tmp["tx_to"]
    return tmp

def deposit_token(tx):
    tmp = basic(tx)
    tmp["type"] = "ed_deposit"
    tmp["erc20_value"] = get_value_from_input(tx["input"])
    tmp["erc20_to"] = tmp["tx_to"]
    return tmp

def ed_trade(tx, ERC20_CONTRACT):
    tmp = basic(tx)
    tmp["type"] = "ed_trade"

    input_data = tx["input"]
    method = input_data[:10]
    params = input_data[10:]

    splitted = [(params[i:i+64]) for i in range(0, len(params), 64)]

    tokenGet = "0x" + remove_leading_zeros(splitted[0])
    amountGet = int(splitted[1],16)
    tokenGive = "0x"+ remove_leading_zeros(splitted[2])
    amountGive = int(splitted[3],16)
    addrUser = "0x"+ remove_leading_zeros(splitted[6])
    amount = int(splitted[10],16)
    
    if tokenGet == ERC20_CONTRACT:
        # MSG.SENDER gives AMOUNT of TOKENGET to USER_ADDRESS
        tmp["tx_from"] = tx["from"]
        tmp["erc20_value"] = amount
        tmp["erc20_to"] = addrUser
        if tokenGive == "0x": # trade vs ETH
            tmp["eth_value"] = amountGive * amount / amountGet
        else:
            tmp["eth_value"] = 0
    elif tokenGive == ERC20_CONTRACT:
        # USER gives (AMOUNTGIVE * AMOUNT) / AMOUNTGET to MSG.SENDER
        tmp["tx_from"] = addrUser
        tmp["erc20_value"] = amountGive * amount / amountGet
        tmp["erc20_to"] = tx["from"]
        if tokenGet == "0x": # trade vs ETH
            tmp["eth_value"] = amount
        else:
            tmp["eth_value"] = 0

    return tmp

def ed_cancel(tx, ERC20_CONTRACT):
    tmp = basic(tx)
    tmp["type"] = "ed_cancel"
    input_data = tx["input"]
    ed = analyzeInputData(input_data)
    
    if ed["tokenGet"] == ERC20_CONTRACT:
        # MSG.SENDER gives AMOUNT of TOKENGET to USER_ADDRESS
        tmp["tx_from"] = tx["from"]
        tmp["erc20_value"] = ed["amountGet"]
        tmp["erc20_to"] = "0x0"
        if ed["tokenGive"] == "0x": # trade vs ETH
            tmp["eth_value"] = ed["amountGive"]
        else:
            tmp["eth_value"] = 0

    elif ed["tokenGive"] == ERC20_CONTRACT:
        # USER gives (AMOUNTGIVE * AMOUNT) / AMOUNTGET to MSG.SENDER
        tmp["tx_from"] = tx["from"]
        tmp["erc20_value"] = ed["amountGive"]
        tmp["erc20_to"] = "0x0"
        if ed["tokenGet"] == "0x": # trade vs ETH
            tmp["eth_value"] = ed["amountGet"]
        else:
            tmp["eth_value"] = 0
    return tmp

def analyzeInputData(input_data):
    params = input_data[10:]
    ed_inputs = {}

    splitted = [(params[i:i+64]) for i in range(0, len(params), 64)]
    tokenGet = "0x" + remove_leading_zeros(splitted[0])
    amountGet = int(splitted[1],16)
    tokenGive = "0x"+ remove_leading_zeros(splitted[2])
    amountGive = int(splitted[3],16)
    #print "amountGive: " + str(amountGive)
    addrUser = "0x"+ remove_leading_zeros(splitted[6])
    if len(splitted) == 10:
        amount = int(splitted[10],16)
        ed_inputs["amount"] = amount

    ed_inputs["tokenGet"] = tokenGet
    ed_inputs["amountGet"] = amountGet
    ed_inputs["tokenGive"] = tokenGive
    ed_inputs["amountGive"] = amountGive
    ed_inputs["addrUser"] = addrUser
    return ed_inputs