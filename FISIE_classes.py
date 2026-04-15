from scipy.stats import beta as BetaDist
from enum import Enum
import BetaDistribution as BD
from random import random

# static
class IIMSC:
    rep_min = 2  # R_min
    rep_max = 10  # R_max
    rep_init = 7 # R_init
    rep_inc = 1  # r^+
    rep_dec = 3  # r^-
    deposit_dec = 1  # d^-
    deposit = 5  # D

# static
class IoTDevices:

    cost = 0.1
    gamma = 0.05
    alpha = 1
    beta = 10
    @staticmethod
    def partial_sample_length():
        return BetaDist.rvs(1, 10)

    @staticmethod
    def rep_threshold(self):
        return BetaDist.rvs(2,5)

    @staticmethod
    def prob_pass_audit(fog_node):
        ell = IoTDevices.partial_sample_length()
        h = fog_node.honesty
        if ell > h:
            return 0
        elif ell == 0 or h == 1:
            return 1
        else: # 0 < ell <= h < 1
            eta = (h-ell)/(1-ell)
            return eta

    @staticmethod
    def payment(fog_node):
        norm_r = (fog_node.reputation - IIMSC.rep_min)/(IIMSC.rep_max - IIMSC.rep_min)
        payment = IoTDevices.cost + IoTDevices.gamma * norm_r
        return payment



class FogNode:
    fog_id = 0
    def __init__(self, strat):
        self.fog_id = FogNode.fog_id
        self.reputation = IIMSC.rep_init
        self.honesty = 0
        self.threshold = 0
        self.strategy = strat
        self.deposit = IIMSC.deposit
        self.profit = 0 # Accumulated payments
        self.active = True
        if self.strategy is Strategy.Cyclic:
            self.threshold = 6 + 3 * random()
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
            case Strategy.Cyclic:
                self.honesty = BD.cyclic_strat(self.reputation, self.threshold)
            case Strategy.Opportunistic:
                self.honesty = BD.opportunistic_strat(self.reputation)
            case _:
                print("Not a valid strategy")


class Strategy(Enum):
    Aggressive = 0
    Conservative = 1
    Balanced = 2
    Cyclic = 3
    Opportunistic = 4

class Audit:
    # sample_length - float [0,1], fnode FogNode
    def __init__(self, fnode, oracle=True, audit_pass = True):
        self.fog_node = fnode
        self.type = (oracle == True)
        self.audit_pass = (audit_pass == True)