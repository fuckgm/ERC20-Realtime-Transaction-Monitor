# -*- coding: utf-8 -*-

def get_logs(receipt):
    if "logs" in receipt.keys():
        return receipt["logs"]
    else: 
        return None

def get_to_addr_from_input(input):
    #print input
    params = input[10:]
    return params[:64].strip('0')

