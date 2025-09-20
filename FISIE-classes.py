# Smart Contract
class SmartContract:
    R = {'min': 2, 'max':10, 'init':7}
    V_max = 2
    r_pen_min = 3
    r_Delta = 5
    r_reward = 1
    @staticmethod
    def escalating_penalty(violations):
        return SmartContract.r_pen_min + violations * SmartContract.r_Delta



# Oracle
class Oracle:
    oracle_id = 0
    def new_address(self):
        o_id = 'Oracle {}'.format(Oracle.oracle_id)
        Oracle.oracle_id += 1
        return o_id

    def __init__(self):
        self.oracle_id = self.new_address()

# IoT
class IoT:
    address_id = 0
    def new_address(self):
        a_id = 'IoT {}'.format(IoT.address_id)
        IoT.address_id += 1
        return a_id

    def __init__(self):
        self.address_id = self.new_address()

# Fog
class FogNode:
    fog_id = 0
    def new_address(self):
        f_id = 'Fog {}'.format(FogNode.fog_id)
        FogNode.fog_id += 1
        return f_id

    def __init__(self):
        self.fog_id = self.new_address()
        self.deposit = 15
        self.funds = 0
        self.reputation = SmartContract.R['init'] # Initial
        self.violations = 0

