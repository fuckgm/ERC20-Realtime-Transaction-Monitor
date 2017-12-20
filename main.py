# -*- coding: utf-8 -*-

from rpc_connector import get_blockNumber, get_transaction, get_blockByNumber
from helper_log import logy, prettify,load_dictionary_from_json,save_dictionary_to_json
from analyzeBlock import getFilteredTransactionsFromBlock, getTransactionsFromBlock, getBlockTimestamp
from Viberate import Viberate
from Blockv import Blockv
from RequestNetwork import RequestNetwork
from HeroCoin import HeroCoin
from sql import open_connection, insert_data, retrieve_contract_watchlist, check_if_hash_exists

from MainClass import MainClass

MODUL_HOLDER = {
    1 : "Viberate.py"
}
"""
def process_block(latest_block):
    # Retrieve Contract Addresses we want to monitor
    CONTRACT_WATCHLIST = retrieve_contract_watchlist(conn)
    
    # Retrieve enitre Block from Blockchain
    block = get_blockByNumber(latest_block)

    # Check for contract addresses on our watchlist
    txs = getFilteredTransactionsFromBlock(block, CONTRACT_WATCHLIST)

    print ": " + str(len(txs)) + " relevant transactions"

    if len(txs) > 0: # process relevant transactions
        
        for tx in txs:
            tx_hash = tx[u'hash']

            # Skip TXs which are already in the database
            if not check_if_hash_exists(conn, tx_hash):

                ico_id = tx["ico_id"]
                tx["blockTimestamp"] = getBlockTimestamp(block)

                if ico_id == 1:
                    processor = Viberate(tx)
                elif ico_id == 4:
                    processor = HeroCoin(tx)
                elif ico_id == 5:
                    processor = RequestNetwork(tx)
                elif ico_id == 7:
                    processor = Blockv(tx)

                else:
                    processor = False
                
                if processor:
                    insert_data(conn, processor.getAnalyzedTransaction())

def track_erc20(START_BLOCK):

    if START_BLOCK == 0:
        latest_block = get_blockNumber()
    else:
        latest_block = START_BLOCK

    print "Starting at Block: " + str(latest_block),        

    # Process starting block
    process_block(latest_block)

    run = True

    while run:
        new_block = get_blockNumber()
        if new_block > latest_block:
            
            # blöcke aufholen!
            if (new_block-latest_block > 1):
                _blocks_to_process = new_block - latest_block

                print "Not up to date! Need to catch up with " + str(_blocks_to_process) + " blocks"

                for i in range (0, _blocks_to_process):
                    print "Catching up with: " + str(latest_block),
                    process_block(latest_block)
                    if latest_block+1 != _blocks_to_process:
                        latest_block += 1
                
            latest_block += 1
            print "New Block was found: " + str(latest_block),
            process_block(latest_block)
 """

""" ##################################################  """
""" ##################################################  """
""" ##################################################  """
""" ##################################################  """
""" ##################################################  """


# Connection re-opens with every block
#conn = open_connection()
#track_erc20(4620771)
#track_erc20(4495684) 

process = MainClass()
process.real_time_erc20_tracking(4762338)


#process_block(4568493) # vib transfer
#process_block(4581660) #vib_transfer from
#process_block(4576691) #vib approve
#process_block(4240950) # vib crowdsale
#process_block(4558637) # ed_withdraw
#process_block(4566936)  # ed_deposit
#process_block(4589852) # bittrex deposit /sweep
#process_block(4240769) # push angel investment @ viberate
#process_block(4241086) # vib team tokens

#process_block(4617997) # blockv transfer

#process_block(4610518)