from scipy.stats import beta as BetaDist
from enum import Enum
import BetaDistribution as BD
from random import random

# static
class IIMSC:
    rep_min = 2  # R_min
    rep_max = 10  # R_max
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
    def partial_sample_length(self):
        return BetaDist.rvs(1, 10)

    @staticmethod
    def rep_threshold(self):
        return BetaDist.rvs(2,5)

    @staticmethod
    def prob_pass_audit(self, fog_node):
        ell = IoTDevices.partial_sample_length()
        h = fog_node.honesty
        if ell > h:
            return 0
        elif ell == 0 or h == 1:
            return 1
        else: # 0 < ell <= h < 1
            eta = (h-ell)**2/(h*(1-ell))
            return eta



class FogNode:
    fog_id = 0
    def __init__(self, strat):
        self.fog_id = FogNode.fog_id
        self.reputation = 7
        self.honesty = 0
        self.threshold = 0
        self.strategy = strat
        self.deposit = IIMSC.deposit
        self.payment = 0 # Accumulated payments
        self.active = True
        if self.strategy is Strategy.Cyclic:
            self.threshold = 0.6 + 0.3 * random()
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
            case Strategy.Aggressive:
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
    def __init__(self, sample_length, fnode):
        self.sample_length = sample_length
        self.full = False
        if self.sample_length == 1:
            self.full = True


        pass