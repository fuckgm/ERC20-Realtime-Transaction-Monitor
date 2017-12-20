# -*- coding: utf-8 -*-
import BaseModul

from helper_log import prettify

# Change NAME to Name of ERC20-Token
class TemplateCoin(BaseModul.BaseModul):

    NAME                = "TemplateCoin"    # Name
    SYMBOL              = "007"             # Token Symbol
    CROWDSALE_ADDRESS   = '0x'              # Contract of Crowdsale, leave '0x' if no separate contract was used
    ERC20_ADDRESS       = '0x'              # Address of ERC20-Contract 

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

