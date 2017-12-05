# -*- coding: utf-8 -*-
import BaseModul

from helper_log import prettify

class RequestNetwork(BaseModul.BaseModul):

    NAME                = "RequestNetwork"
    SYMBOL              = "REQ"
    CROWDSALE_ADDRESS   = '0x97208bf5dc25e6fd4719cfc2a3c1d1a59a974c3b'
    ERC20_ADDRESS       = '0x8f8221afbb33998d8584a2b05749ba73c37a938a'

    def __init__(self, tx):
        self.set_variables(tx, self.ERC20_ADDRESS)
        self.item = {}
        
        self.output("[%s] Processing: %s " % (self.NAME, tx["hash"]))

        self.item = self.triage_transaction(tx)
        
        if not self.item:
            method = self.get_method(tx["input"])
            self.output("[%s] Method missing for: %s" % (self.NAME, method))
            self.store_unhandled_method(method, tx)
        
            """ """ """ """ """ """ """ """ """ """
            # ### ### #### #### #### #### ### ###
            #     STORE CUSTOM METHODS HERE     #
            # ### ### #### #### #### #### ### ###
            """ """ """ """ """ """ """ """ """ """
            
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

