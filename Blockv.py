# -*- coding: utf-8 -*-
import BaseModul

from helper_log import prettify


class Blockv(BaseModul.BaseModul):
    
    NAME =              "BLOCKv"
    CROWDSALE_ADDRESS = '0x'
    ERC20_ADDRESS =     '0x340d2bde5eb28c1eed91b2f790723e3b160613b7'

    def __init__(self, tx):
        self.set_variables(tx, self.ERC20_ADDRESS)
        self.item = {}

        self.output("[%s] Processing: %s " % (self.NAME, tx["hash"]))

        self.item = self.triage_transaction(tx)
        
        if not self.item:
            method = self.get_method(tx["input"])
            self.output("[%s] Method missing for: %s" % (self.NAME, method))
            self.store_unhandled_method(method, tx)
            
            """ """ """ """ """ """ """ """ """
            # ### ### #### #### #### #### ### ###
            #     STORE CUSTOM METHODS HERE     #
            # ### ### #### #### #### #### ### ###
            """ """ """ """ """ """ """ """ """ 

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