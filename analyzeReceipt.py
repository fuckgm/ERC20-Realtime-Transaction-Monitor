# -*- coding: utf-8 -*-

from helper_log import prettify

def get_logs_from_receipt(receipt):
    if "logs" in receipt.keys():
        return receipt["logs"]
    else: 
        return None

def get_to_addr_from_input(input):
    #print input
    params = input[10:]
    params = params[:64]
    return params[-40:]

def get_gas_used(receipt):
    return int(receipt["gasUsed"],16)

def get_gas_limit(tx):
    return int(tx["gas"],16)

def get_status(receipt):
    if "status" in receipt.keys():
        return int(receipt["status"],16)
    else:
        return -1

def get_info_from_topics_in_logs(_logs, index, spot):
    prettify(_logs)
    if len(_logs) < index:
        print "get info from logs: index too big"
        return -1
    
    if len(_logs[index]) < spot:
        print "get info from logs: spot too big for topic-array"
        return -1

    return _logs[index]['topics'][spot]