# -*- coding: utf-8 -*-

from rpc_connector import get_blockNumber, get_transaction, get_blockByNumber
from helper_log import logy, prettify,load_dictionary_from_json,save_dictionary_to_json
from analyzeBlock import getFilteredTransactionsFromBlock, getTransactionsFromBlock, getBlockTimestamp
from prepareTransaction import prepareTx
from sql import open_connection, insert_data

WEI_TO_ETH = 1e-18

START_BLOCK = 0
ICO_ID = 1 
ERC20_CONTRACT_ADDRESS = '0x2C974B2d0BA1716E644c1FC59982a89DDD2fF724'
JSON_STORE_FILENAME = 'Viberate_Transactions.json'

def process_block(latest_block):
    block = get_blockByNumber(latest_block)
    txs = getFilteredTransactionsFromBlock(block, ERC20_CONTRACT_ADDRESS)
    print ": " + str(len(txs)) + " relevant transactions"

    if len(txs) > 0: # process relevant transactions
        add_tx = load_dictionary_from_json(JSON_STORE_FILENAME)
        conn = open_connection()

        for tx in txs:
            hash = tx[u'hash']
            _tx = prepareTx(tx)
            add_tx[hash] = _tx
            _tx["ico_id"] = ICO_ID
            _tx["blockTimestamp"] = getBlockTimestamp(block)
            insert_data(conn, _tx)

        save_dictionary_to_json(JSON_STORE_FILENAME,add_tx)

def track_erc20(START_BLOCK, ERC20_CONTRACT_ADDRESS):
    latest_block = get_blockNumber()
    print "Starting at Block: " + str(latest_block),

    process_block(latest_block)
    run = True

    while run:
        new_block = get_blockNumber()
        if new_block > latest_block:
            
            if (new_block-latest_block > 1):
                print "Blöcke aufholen! " + str(new_block-latest_block)
                # blöcke aufholen!
                _blocks_to_process = new_block - latest_block

                for i in range (0, _blocks_to_process):
                    print "Catching up with: " + str(latest_block+i),
                    process_block(latest_block+i)
                
            
            latest_block += 1
            print "New Block was found: " + str(latest_block),
            process_block(latest_block)
 

""" ##################################################  """
""" ##################################################  """
""" ##################################################  """
""" ##################################################  """
""" ##################################################  """

#block = get_blockByNumber(4565493)
#getTransactionsFromBlock(block)
#txs = getFilteredTransactionsFromBlock(block, ERC20_CONTRACT_ADDRESS)
#print str(len(txs))
#process_block(4565972)


track_erc20(START_BLOCK, ERC20_CONTRACT_ADDRESS)

