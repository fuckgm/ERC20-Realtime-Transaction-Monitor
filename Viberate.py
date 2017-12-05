# -*- coding: utf-8 -*-
import BaseModul
from helper_log import prettify
from prepareBasicTransaction import get_value_from_input

class Viberate(BaseModul.BaseModul):

    CROWDSALE_ADDRESS = '0x91c94bee75786fbbfdcfefba1102b68f48a002f4'
    ERC20_ADDRESS =     '0x2c974b2d0ba1716e644c1fc59982a89ddd2ff724'

    PUSH_ANGEL_METHOD           = '0xf28afb1e'
    CLAIM_TEAM_TOKENS_METHOD    = '0x826776fa'
    CLAIM_BOUNTY                = '0x02f58015' # Viberate ICO Buyer-Contract
    CLAIM_REWARD                = '0xb88a802f'
    PERSONAL_WITHDRAW           = '0xbbf59a41' # Viberate ICO Buyer-Contract withdrawl

    """
    @staticmethod
    def filterAddresses():
        return [self.CROWDSALE_ADDRESS, self.ERC20_ADDRESS]
    """
    def __init__(self, tx):
        self.set_variables(tx, self.ERC20_ADDRESS)
        self.item = {}
        self.output("[Viberate] Processing: " + tx["hash"])

        self.item = self.triage_transaction(tx)

        if not self.item:
            method = self.get_method(tx["input"])

            if method == self.PUSH_ANGEL_METHOD:
                # Angel investments won't make it to this point b/c
                # the contract addr is not in the main tx information and only in logs
                # add multiple possible contracts to check for tx_to?
                self.item = self.angel(tx)

            elif method == self.CLAIM_TEAM_TOKENS_METHOD:
                # same as above. didnt really check for sufficient work
                # need to take a look at it again
                self.item = self.team_tokens(tx)

            else:
                self.output("[Viberate] Method missing for: " + method)
                self.store_unhandled_method(method, tx)

            #print "viberate specific transaction"

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
    
    def angel(self, tx):
        tmp = self.basic_preparation(tx)
        tmp["type"] = "angel"
        tmp["eth_value"] = get_value_from_input(tx["input"])
        return tmp

    def team_tokens(self,tx):
        tmp = self.basic_preparation(tx)
        tmp["type"] = "team_tokens"
        return tmp