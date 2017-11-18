import requests
import random
import json
from helper_log import logy, prettify

""" Send Request to JSON-RPC """
def send_request(request):
    url = 'http://localhost:8545'
    headers = {'content-type': 'application/json'}
    payload = {'jsonrpc': '2.0', 'id': random.randint(0, int(1e9))}
    payload.update(request)
    response = None
    while not response:
        try:
            raw_block =requests.post(url, data=json.dumps(payload), headers=headers).json() 
            #print raw_block
            response = raw_block
        except requests.exceptions.ConnectionError as e:
            pass
    if response[u'id'] != payload['id']:
        raise Exception('Returned mismatching id')
    try:
        return response[u'result']
    except KeyError:
        logy('No result found!', response)
    except StandardError as Ex:
        pass
    raise Exception('No result returned')

""" Get Transaction from Transaction Hash """
def get_transaction(tx_hash):
    receipt = send_request({
        'method': 'eth_getTransactionByHash',
        'params': [tx_hash]
    })  
    return receipt

def get_blockNumber():
    receipt = send_request({
        'method' : 'eth_blockNumber',
        'params' : []
    })
    return int(receipt,16)

def get_blockByNumber(block_number):
    receipt = send_request({
        'method': 'eth_getBlockByNumber',
        'params': [hex(block_number), True]
    })
    return receipt

def get_transaction_receipt(tx_hash):
    receipt = send_request({
        'method': 'eth_getTransactionReceipt',
        'params': [tx_hash]
    })  
    return receipt