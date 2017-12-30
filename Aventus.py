# -*- coding: utf-8 -*-
import BaseModul

from analyzeReceipt import get_logs_from_receipt, get_info_from_topics_in_logs
from prepareBasicTransaction import basic
from helper_log import prettify

# Change NAME to Name of ERC20-Token
class Aventus(BaseModul.BaseModul):

    NAME                = "Aventus"    # Name
    SYMBOL              = "AVT"             # Token Symbol
    CROWDSALE_ADDRESS   = '0x'              # Contract of Crowdsale, leave '0x' if no separate contract was used
    ERC20_ADDRESS       = '0x0d88ed6e74bbfd96b831231638b66c05571e824f'              # Address of ERC20-Contract 

    # 
    # Add method-identifiers here
    #

    def __init__(self, tx):
        # Push transaction and Contract address into BaseModul
        self.set_variables(tx, self.ERC20_ADDRESS)
        self.item = {}
        
        self.output("[%s] Processing: %s " % (self.NAME, tx["hash"]))

        # has transaction a standard type?
        # yes => item will contain a dictionary with identified values
        # no  => item will be 'False'

        self.item = self.triage_transaction(tx)

        if self.item is None:
            if len(tx["input"]) == 202:
                self.item = self.unknown_contract(tx)
        
        #overwrite custom transfer-function
        elif self.item["type"] == "transfer":
            tx_logs = get_logs_from_receipt(self.TRANSACTION_RECEIPT)
            self.item["erc20_value"] = self.erc20_value_from_data(tx,1)

        elif self.item["type"] == "transfer_from":
            tx_logs = get_logs_from_receipt(self.TRANSACTION_RECEIPT)
            erc20_to = get_info_from_topics_in_logs(tx_logs, 0, 3)
            self.item["erc20_to"] = "0x"+erc20_to[-40:]
            self.item["erc20_value"] = self.erc20_value_from_data(tx,1)
        
        if not self.item:

            """ """ """ """ """ """ """ """ """ """
            # ### ### #### #### #### #### ### ###
            #     STORE CUSTOM METHODS HERE     #
            # ### ### #### #### #### #### ### ###
            """ """ """ """ """ """ """ """ """ """

            # Save unknown method to database
            # Change here if you enter contract specific methods
            method = self.get_method(tx["input"])
            self.output("[%s] Method missing for: %s" % (self.NAME, method))
            self.store_unhandled_method(method, tx)

        
        if self.item:
            # Add ico_id and transform eth_value from WEI to ETH
            self.item["ico_id"] = tx["ico_id"]
            
            if self.item["eth_value"] is not None:
                self.item["eth_value"] = self.item["eth_value"] * self.WEI_TO_ETH
            else:
                self.item["eth_value"] = -1

            if self.item["erc20_value"] is not None:
                self.item["erc20_value"] = self.item["erc20_value"] * self.WEI_TO_ETH
            else:
                self.item["erc20_value"] = -1
                
        prettify(self.item)

    def getAnalyzedTransaction(self):
        return self.item

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

    def unknown_contract(self,tx):
        unknown = basic(tx)

        tx_logs = get_logs_from_receipt(self.TRANSACTION_RECEIPT)
        _erc20_to = get_info_from_topics_in_logs(tx_logs, 0,2)
        unknown["erc20_to"] = "0x" + _erc20_to[-40:]

        _erc20_value = get_info_from_topics_in_logs(tx_logs, 0,3)
        unknown["erc20_value"] = int(_erc20_value,16)

        _tx_from = get_info_from_topics_in_logs(tx_logs,0,1)
        unknown["tx_from"] = "0x" + _erc20_to[-40:]
        unknown["type"] = "unknown"

        return unknown
