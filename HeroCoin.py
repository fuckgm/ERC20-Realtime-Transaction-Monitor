# -*- coding: utf-8 -*-
import BaseModul
from prepareBasicTransaction import get_to_addr_from_input

from helper_log import prettify

class HeroCoin(BaseModul.BaseModul):

    NAME                = "HeroCoin"
    SYMBOL              = "PLAY"
    CROWDSALE_ADDRESS   = '0x'
    ERC20_ADDRESS       = '0xe477292f1b3268687a29376116b0ed27a9c76170'

    ADD_WHITELIST               = '0xe43252d7' #Herocoin addToWhitelist
    REQUEST_PAYOUT              = '0x8f97e3a0' #Herocoin RequestPayout

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

            if method == self.REQUEST_PAYOUT:
                self.item = self.request_payout(tx)

            elif method == self.ADD_WHITELIST:
                self.item = self.add_whitelist(tx)

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

    def request_payout(self,tx):
        tmp = self.basic_preparation(tx)
        tmp["type"] = "request_payout"
        tmp["tx_to"] = tmp["tx_from"]
        tmp["erc20_to"] = 0
        tmp["erc20_value"] = 0
        tmp["eth_value"] = int(tx["input"][10:],16)
        return tmp

    def add_whitelist(self,tx):
        tmp = self.basic_preparation(tx)
        tmp["type"] = "whitelisted"
        tmp["erc20_value"] = 0
        tmp["erc20_to"] = get_to_addr_from_input(tx["input"])
        return tmp