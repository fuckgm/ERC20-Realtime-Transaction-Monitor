# -*- coding: utf-8 -*-
from transactionTypes import crowdsale, angel, transfer, team_tokens, transfer_from, deposit_token, withdraw_token, sweep
from analyzeTransaction import get_method
from helper_log import logy_unknown_txs

TRANSFER_METHOD             = '0xa9059cbb'
PUSH_ANGEL_METHOD           = '0xf28afb1e'
CLAIM_TEAM_TOKENS_METHOD    = '0x826776fa'
WITHDRAW_TOKEN              = '0x9e281a98' # Etherdelta Smart Contract
CLAIM_BOUNTY                = '0x02f58015' # Viberate ICO Buyer-Contract
DEPOSIT_TOKEN               = '0x338b5dea' # Etherdelta Smart Contract
CLAIM_REWARD                = '0xb88a802f'
BUY_ICO                     = '0xc59b5562' # ICO Buying Contract
TRANSFER_FROM               = '0x23b872dd'
PERSONAL_WITHDRAW           = '0xbbf59a41' # Viberate ICO Buyer-Contract withdrawl
SWEEP                       = '0x6ea056a9'

def prepareTx(tx):
    fin = {}
    """ Values from Transaction """
    
    input = tx["input"]

    if input == "0x":   # probably crowdsale
        fin = crowdsale(tx)
        
    else:
        method = get_method(input)

        if method == PUSH_ANGEL_METHOD: # Angel Investment Distribution
            fin = angel(tx)

        elif method == TRANSFER_METHOD: # Regular Transfer
           fin = transfer(tx)
        
        elif method == CLAIM_TEAM_TOKENS_METHOD:
            fin = team_tokens(tx)
        
        elif method == DEPOSIT_TOKEN:
            fin = deposit_token(tx)

        elif method == WITHDRAW_TOKEN:
            fin = withdraw_token(tx)

        elif method == TRANSFER_FROM:
            fin = transfer_from(tx)

        elif method == SWEEP:
            fin = sweep(tx)

        else:
            print "Unknown method: " + method + " @ " + tx["hash"]
            logy_unknown_txs(str(method) + ' '+ str(tx["hash"]))

    return fin