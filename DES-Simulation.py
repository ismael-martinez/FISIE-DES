import random

import simpy

import FISIE_classes as FC
from FISIE_classes import IoTDevices as IoT
from FISIE_classes import IIMSC
import BetaDistribution as BD
import AuditSelection as AS
import numpy as np

# Arrival Rates
oracle_AR = 1
IoT_AR = 100

####### Setup #######

# f fog nodes per strategy (5)
fog_per = 200
num_strategies = 5
fog_nodes = [None]*(fog_per * num_strategies)
for s in range(num_strategies):
    for f in range(fog_per):
        idx = f + s*fog_per
        fog_nodes[idx] = FC.FogNode(FC.Strategy(s))

# fog_dict = dict()
# for f in fog_nodes:
#     fog_dict[f.fog_id] = f

###### State variables ######

# Reputation over time
rep_state = []

# Payment - Cost over time
payment_state = []


# Simpy Processes
def audit_selection_oracle(env):
    while True:
        interarrival = np.random.exponential(1./oracle_AR)
        yield env.tiimeout(interarrival)
        print(f"Beginning full audit from oracle at {env.now}")
        fn = AS.audit_selection(fog_nodes)
        print(f"Selected fog node with id {fn.fog_id}")
        audit_observation(env,fn)
def audit_selection_iot(env):
    while True:
        interarrival = np.random.exponential(1./IoT_AR)
        yield env.timeout(interarrival)
        print(f"Beginning partial verification from IoT at {env.now}")
        fn = AS.audit_selection(fog_nodes, False)
        print(f"Selected fog node with id {fn.fog_id}")
        audit_observation(env, fn, False)

def audit_observation(env, fog_node, oracle=True):
    passed_audit = True

    # Audit
    if oracle:
        if fog_node.honest < 1:
            print(f"Fog node {fog_node.fog_id} failed Oracle audit at {env.now}")
            passed_audit = False
            reputation_update(env, fog_node, False)
        else:
            print(f"Fog node {fog_node.fog_id} passed Oracle audit at {env.now}")
            reputation_update(env, fog_node, True)
    else: # IoT
        eta = IoT.prob_pass_audit(fog_node)
        if random.random() > eta: # failure
            print(f"Fog node {fog_node.fog_id} failed IoT partial verification at {env.now}")
            passed_audit = False
            reputation_update(env, fog_node, False)
        else:
            print(f"Fog node {fog_node.fog_id} passed IoT partial verification at {env.now}")
            reputation_update(env, fog_node, True)

    # Service Payment
    fog_node.payment -= fog_node.honesty * IoT.cost
    if passed_audit:
        fog_node.payment += IoT.payment(fog_node)

def reputation_update(env, fog_node, success=True):
    if success:
        fog_node.reputation = min([fog_node.reputation + IIMSC.rep_inc, IIMSC.rep_max])
        print(f"Fog node {fog_node.fog_id} reputation increased to {fog_node.reputation} at {env.now}")
    else:
        fog_node.reputation -= IIMSC.rep_dec
        fog_node.deposit -= IIMSC.deposit_dec
        if fog_node.deposit <= 0 or fog_node.reputation < IIMSC.rep_min:
            print(f"Fog node {fog_node.fog_id} is ejected from the system at {env.now}")
            fog_node.active = False
        else:
            print(f"Fog node {fog_node.fog_id} has {fog_node.reputation} reputation and {fog_node.deposit} deposit remaining at {env.now}")
    reputation_state_update(env)
    honesty_update(env, fog_node)

def honesty_update(env, fog_node):
    print(f"Fog node {fog_node.fog_id} updating honesty at {env.now}")
    fog_node.update_honesty()

def reputation_state_update(env):
    print(f"Updating reputation state at {env.now}")
    strate_dict = dict()
    for i in range(num_strategies):
        strat_fog_reps = [f.reputation for f in fog_nodes if f.active and f.stategy == FC.Strategy(s)]
        strat_fog_payments = [(f.payment - IIMSC.deposit + f.deposit) for f in fog_nodes
                              if f.active and f.stategy == FC.Strategy(s)]
    strate_dict[FC.Strategy(s).name] = {'R': strat_fog_reps, 'P': strat_fog_payments}


######### Simpy #########
env = simpy.Environment()
env.process(audit_selection_oracle(env))
env.process(audit_selection_iot(env))

# System end when no fog node remain active