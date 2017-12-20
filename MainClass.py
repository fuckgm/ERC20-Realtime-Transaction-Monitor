# -*- coding: utf-8 -*-

# General Imports
from rpc_connector import get_blockNumber, get_transaction, get_blockByNumber
from helper_log import logy, prettify,load_dictionary_from_json,save_dictionary_to_json, load_list_from_file
from analyzeBlock import getFilteredTransactionsFromBlock, getTransactionsFromBlock, getBlockTimestamp
from sql import open_connection, insert_data, retrieve_contract_watchlist, check_if_hash_exists
from time import gmtime, strftime
import time

# Supported Tokens
from Viberate import Viberate
from Blockv import Blockv
from RequestNetwork import RequestNetwork
from HeroCoin import HeroCoin
from ICON import ICON
from Aventus import Aventus
from RipioCreditNetwork import RipioCreditNetwork
from KyberNetworkCrystal import KyberNetwork
from Quantstamp import Quantstamp

class MainClass():

    def __init__(self):
        self.conn = open_connection()
        self.re_entry = 0

    @staticmethod
    def ico_factory(ico_id, tx):
        if ico_id == 1:
            return Viberate(tx)
        elif ico_id == 2:
            return RipioCreditNetwork(tx)
        elif ico_id == 3:
            return Aventus(tx)
        elif ico_id == 4:
            return HeroCoin(tx)
        elif ico_id == 5:
            return RequestNetwork(tx)
        elif ico_id == 6:
            return Quantstamp(tx)
        elif ico_id == 7:
            return Blockv(tx)
        elif ico_id == 8:
            return KyberNetwork(tx)
        elif ico_id == 9:
            return ICON(tx)
        else:
            return False

    def process_etherscan_crawl(self, path_to_crawl, ico_id):
        save_path = str(strftime("%H:%M", gmtime())) + " " + str(ico_id) + " ico_transactions.txt"

        thelist = load_list_from_file(path_to_crawl)
        ico_transactions = {}
        print str(strftime("%H:%M:%S", gmtime()))+ ": Total number of transactions found: %s" % (str(len(thelist)))
        total_txs = len(thelist)

        cnt = 0
        for tx_hash in thelist:
            try:
                tx = get_transaction(tx_hash)
                tx["ico_id"] = ico_id
                print str(strftime("%H:%M:%S", gmtime()))+ ": [" + str(cnt) +"/"+ str(total_txs) +" Processing: " + tx["hash"]
                cnt += 1
                if check_if_hash_exists(self.conn, tx_hash):
                    continue
                input_data = tx["input"]

                # Filter payable transactions
                if input_data == "0x":              
                    ico_transactions[tx_hash] = tx
                
                block = get_blockByNumber(int(tx["blockNumber"],16))
                tx["blockTimestamp"] = getBlockTimestamp(block)
                
                processed = self.ico_factory(ico_id, tx)
                """
                if processed:
                    insert_data(self.conn, processed.getAnalyzedTransaction())
                """
            except StandardError as stdEx:
                print "ERROR: @ " + tx_hash + "\n"+str(stdEx)

        save_dictionary_to_json(save_path, ico_transactions)
        

    def real_time_erc20_tracking(self, START_BLOCK):
        if START_BLOCK == 0:
            latest_block = get_blockNumber()
        else:
            latest_block = START_BLOCK

        print "Starting at Block: " + str(latest_block),        

        try:
            # Process starting block
            self.process_block(latest_block)

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
                            self.process_block(latest_block)
                            if latest_block+1 != _blocks_to_process:
                                latest_block += 1
                        
                    latest_block += 1
                    print "New Block was found: " + str(latest_block),
                    self.process_block(latest_block)
                    self.re_entry = latest_block

        except StandardError as stdEx:
            print "Throw in real_time: " + str(stdEx)
            print "Powernapping!"
            time.sleep(15)
            self.real_time_erc20_tracking(self.re_entry-5)
    
    def process_block(self, latest_block):
        # Retrieve Contract Addresses we want to monitor
        CONTRACT_WATCHLIST = retrieve_contract_watchlist(self.conn)
        
        # Retrieve enitre Block from Blockchain
        block = get_blockByNumber(latest_block)

        # Check for contract addresses on our watchlist
        txs = getFilteredTransactionsFromBlock(block, CONTRACT_WATCHLIST)

        print ": " + str(len(txs)) + " relevant transactions"

        if len(txs) > 0: # process relevant transactions
            
            for tx in txs:
                tx_hash = tx[u'hash']

                # Skip TXs which are already in the database
                if not check_if_hash_exists(self.conn, tx_hash):

                    ico_id = tx["ico_id"]
                    tx["blockTimestamp"] = getBlockTimestamp(block)

                    if ico_id == 1:
                        processor = Viberate(tx)
                    elif ico_id == 2:
                        processor = RipioCreditNetwork(tx)
                    elif ico_id == 3:
                        processor = Aventus(tx)
                    elif ico_id == 4:
                        processor = HeroCoin(tx)
                    elif ico_id == 5:
                        processor = RequestNetwork(tx)
                    elif ico_id == 6:
                        processor = Quantstamp(tx)
                    elif ico_id == 7:
                        processor = Blockv(tx)
                    elif ico_id == 8:
                        processor = KyberNetwork(tx)
                    elif ico_id == 9:
                        processor = ICON(tx)
                    else:
                        processor = False
                    
                    if processor:
                        insert_data(self.conn, processor.getAnalyzedTransaction())
        
   