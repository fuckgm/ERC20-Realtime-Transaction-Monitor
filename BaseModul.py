# -*- coding: utf-8 -*-

from helper_log import prettify
from prepareBasicTransaction import basic, get_to_address_transferFrom, get_value_from_input, remove_leading_zeros
from analyzeReceipt import get_logs_from_receipt, get_info_from_topics_in_logs, get_to_addr_from_input
from rpc_connector import get_transaction_receipt
from EtherDelta2 import withdraw_token, deposit_token, ed_trade, ed_cancel
from sql import open_connection, insert_unknown_tx

class BaseModul:

    def __init__(self):
        pass

    def output(self, input):
        print input

    def set_variables(self,tx, erc20):
        self.WEI_TO_ETH = 1e-18

        # ERC20 METHODS
        self.TRANSFER                    = '0xa9059cbb'
        self.TRANSFER_FROM               = '0x23b872dd'
        self.APPROVE                     = '0x095ea7b3'
        self.PAYABLE                     = '0x'

        # EXTERNAL STATIC
        self.BUY_ICO                     = '0xc59b5562' # ICO Buying Contract
        self.SWEEP                       = '0x6ea056a9' # Bittrex Sweep Method
        self.KRAKEN_TRANSFER             = '0xf7654176' # Kraken "Seep" Method

        # ETHERDELTA
        self.ED_WITHDRAW_TOKEN           = '0x9e281a98' # Etherdelta Smart Contract
        self.ED_DEPOSIT_TOKEN            = '0x338b5dea' # Etherdelta Smart Contract
        self.ED_CANCEL_ORDER             = '0x278b8c0e' # Etherdelta Smart Contract
        self.ED_TRADE                    = '0x0a19b14a' 
        
        # CONSTANT VALUES FOR ANALYSIS
        self.TRANSACTION_RECEIPT        = get_transaction_receipt(tx["hash"])
        self.CONTRACT_ADDRESS           = erc20


    # ### ### #### #### #### #### ### ###
    #     HELPER METHODS                #
    # ### ### #### #### #### #### ### ###

    # Analyze base parameters which are often the same
    def basic_preparation(self, tx):
        return basic(tx)
        
    # Extract integer from 'data' field in n-th log-array entry
    def erc20_value_from_data(self, tx, n):
        tx_logs = get_logs_from_receipt(self.TRANSACTION_RECEIPT)
        try:
            # More or Equal than n logentries
            if len(tx_logs) >= n:
                return int(tx_logs[n]["data"],16) 
            else:
                self.output("ERROR when getting int from data @ " + tx["hash"])
                return -1
        except StandardError as stdex:
            print "ERROR when getting int from data! " + str(stdex)

    # Extract method from input field
    def get_method(self, input_data):
        if (len(input_data) - 8 - 2) % 64 != 0:
            print '\tData size misaligned with parse request'
            print input_data
        return input_data[:10]

    # Save methods/tx_hashes to database which have no handler yet
    def store_unhandled_method(self, method, tx):
        sql = open_connection()
        insert_unknown_tx(sql, tx["hash"], method, tx["ico_id"])

    # ### ### #### #### #### #### ### ###
    #     ERC20 STANDARD METHODS        #
    # ### ### #### #### #### #### ### ###

    def transfer_method(self, tx):
        tmp = self.basic_preparation(tx)
        tmp["type"] = "transfer"
        tmp["erc20_value"] = self.erc20_value_from_data(tx["hash"], 0)
        return tmp

    def transfer_from_method(self,tx):
        tmp = self.basic_preparation(tx)
        tmp["erc20_value"] = self.erc20_value_from_data(tx,0)
        tmp["type"] = "transfer_from"
        tmp["tx_from"] = tmp["erc20_to"]
        tmp["erc20_to"] = "0x"+get_to_address_transferFrom(tx["input"])
        return tmp

    def approve_method(self, tx):
        tmp = self.basic_preparation(tx)
        tmp["type"] = "approve"
        tmp["erc20_value"] = get_value_from_input(tx["input"])
        return tmp

    def payable_method(self,tx): # usually crowdsale
        tmp = self.basic_preparation(tx)
        tmp["type"] = "crowdsale"
        tmp["erc20_value"] = self.erc20_value_from_data(tx,0)
        tmp["erc20_to"] = self.TRANSACTION_RECEIPT["from"]
        return tmp

    # ### ### #### #### #### #### ### ###
    #     SINGLE EXTERNAL FUNCTIONS     #
    # ### ### #### #### #### #### ### ###

    def sweep(self,tx):
        tmp = self.basic_preparation(tx)
        tmp["type"] = "sweep"
        tmp["tx_to"] = get_to_addr_from_input(tx["input"])
        tmp["erc20_value"] = get_value_from_input(tx["input"])
        logs = get_logs_from_receipt(self.TRANSACTION_RECEIPT)
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

    # ### ### #### #### #### #### ### ###
    #     HANDLING METHODS              #
    # ### ### #### #### #### #### ### ###

    def triage_transaction(self, tx):
        processed = self.is_standard_transaction(tx)
        if not processed: processed = self.is_external_standard_transaction(tx)
        if not processed: processed = self.is_etherdelta_transaction(tx)
        return processed
    
    def is_standard_transaction(self, tx):
        input_data = tx["input"]
        if input_data == self.PAYABLE:
            return self.payable_method(tx)
            
        method = self.get_method(input_data)

        if method == self.TRANSFER:
            return self.transfer_method(tx)

        elif method == self.TRANSFER_FROM:
            return self.transfer_from_method(tx)

        elif method == self.APPROVE:
            return self.approve_method(tx)

        return False
            #return self.is_external_standard_transaction(tx)

    def is_external_standard_transaction(self,tx):
        method = self.get_method(tx["input"])

        if method == self.SWEEP:
            return self.sweep(tx)

        #print method
        return False

    def is_etherdelta_transaction(self,tx):
        method = self.get_method(tx["input"])

        if method == self.ED_WITHDRAW_TOKEN:
            return withdraw_token(tx)

        elif method == self.ED_DEPOSIT_TOKEN:
            return deposit_token(tx)

        elif method == self.ED_TRADE:
            return ed_trade(tx, self.CONTRACT_ADDRESS)

        elif method == self.ED_CANCEL_ORDER:
            return ed_cancel(tx,self.CONTRACT_ADDRESS)
        
        