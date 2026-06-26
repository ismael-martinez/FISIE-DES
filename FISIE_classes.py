from scipy.stats import beta as BetaDist
from enum import Enum
import StrategyDistributions as BD
from random import random
import numpy.random as np_rand
import numpy as np

# static
class IIMSC:
    rep_min = 2  # R_min
    rep_max = 10  # R_max
    rep_init = 7 # R_init
    rep_inc = 1  # r^+
    rep_dec = 2  # r^-
    collateral_dec = 1  # d^-
    deposit = 5  # D

# static
class IoTDevices:
    alpha = 1
    beta = 10
    @staticmethod
    def partial_sample_length():
        return BetaDist.rvs(1, 10)

    @staticmethod
    def rep_threshold(self):
        return 10*BetaDist.rvs(2,5)

    @staticmethod
    def prob_pass_audit(fog_node):
        Audit.audit_cycle += 1
        if random() < 0.2: # No partial verification
            return 1
        ell = IoTDevices.partial_sample_length()
        h = fog_node.honesty
        if ell > h:
            return 0
        elif ell == 0 or h == 1:
            return 1
        else: # 0 < ell <= h < 1
            eta = (h-ell)/(1-ell)
            if eta > h:
                print("Error, eta > h")
            return eta

    @staticmethod
    def cost_payment():
        cost = np_rand.gamma(3, 0.05)
        payment = cost * (1 + BetaDist.rvs(2, 10))
        return [cost, payment]


class FogNode:
    fog_id = 0
    def __init__(self, strat):
        self.fog_id = FogNode.fog_id
        self.reputation = IIMSC.rep_init
        self.honesty = 0
        self.threshold = 0
        self.strategy = strat
        self.collateral = IIMSC.deposit
        self.profit = 0 # Accumulated payments
        self.active = True
        self.audit_total = 0
        self.audits_passed = 0
        self.pass_rate = np.nan
        self.update_honesty() # initial honesty

        FogNode.fog_id+=1
    def update_honesty(self):
        match self.strategy:
            case Strategy.Aggressive:
                self.honesty = BD.aggressive_strat()
            case Strategy.Conservative:
                self.honesty = BD.conservative_strat()
            case Strategy.Balanced:
                self.honesty = BD.balanced_strat()
            case Strategy.Progressive:
                self.honesty = BD.progressive_strat(self.collateral)
            case Strategy.Opportunistic:
                self.honesty = BD.opportunistic_strat(self.reputation)
            case _:
                print("Not a valid strategy")

    def update_rate(self, audit_passed):
        self.audit_total += 1
        self.audits_passed += (audit_passed == 1)
        self.pass_rate = self.audits_passed / self.audit_total

class Strategy(Enum):
    Aggressive = 0
    Conservative = 1
    Balanced = 2
    Progressive = 3
    Opportunistic = 4

class Audit:
    audit_cycle = 1
    def __init__(self, fnode, oracle=True, audit_pass = True):
        self.fog_node = fnode
        self.type = (oracle == True)
        self.audit_pass = (audit_pass == True)
        self.audit_cycle = Audit.audit_cycle
