import random
random.seed = 100

import simpy

import FISIE_classes as FC
from FISIE_classes import IoTDevices as IoT
from FISIE_classes import IIMSC
import BetaDistribution as BD
import AuditSelection as AS
import numpy as np
import csv

# Arrival Rates
oracle_AR = 1
IoT_AR = 100

####### Setup #######

# f fog nodes per strategy (5)
fog_per = 1000
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
# Store states in csv file
fieldnames = ['Time', 'strategy', 'fog_count', 'avg_reputation', 'avg_profit']
csvfile_name = "fisie_state_data.csv"
with open(csvfile_name, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()


# Simpy Processes
def audit_selection_oracle(env):
    while True:
        verify_continue(env)
        interarrival = np.random.exponential(1./oracle_AR)
        yield env.timeout(interarrival)
        print(f"Beginning full audit from oracle at {env.now}")
        fn = AS.audit_selection(fog_nodes)
        print(f"Selected fog node with id {fn.fog_id}")
        audit_observation(env,fn)
def audit_selection_iot(env):
    while True:
        verify_continue(env)
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
        if fog_node.honesty < 1:
            print(f"Fog node {fog_node.fog_id} failed Oracle audit at {env.now}")
            passed_audit = False
        else:
            print(f"Fog node {fog_node.fog_id} passed Oracle audit at {env.now}")
            #passed_audit = True
    else: # IoT
        eta = IoT.prob_pass_audit(fog_node)
        if random.random() > eta: # failure
            print(f"Fog node {fog_node.fog_id} failed IoT partial verification at {env.now}")
            passed_audit = False
        else:
            print(f"Fog node {fog_node.fog_id} passed IoT partial verification at {env.now}")
            #passed_audit = True
    service_payment(env, fog_node, passed_audit)
    reputation_update(env, fog_node, passed_audit)



def reputation_update(env, fog_node, passed_audit=True):
    ejected = False
    if passed_audit:
        fog_node.reputation = min([fog_node.reputation + IIMSC.rep_inc, IIMSC.rep_max])
        print(f"Fog node {fog_node.fog_id} reputation increased to {fog_node.reputation} at {env.now}")
    else:
        fog_node.reputation -= IIMSC.rep_dec
        fog_node.deposit -= IIMSC.deposit_dec
        if fog_node.deposit <= 0 or fog_node.reputation < IIMSC.rep_min:
            print(f"Fog node {fog_node.fog_id} is ejected from the system at {env.now}")
            fog_node.active = False
            ejected = True
        else:
            print(f"Fog node {fog_node.fog_id} has {fog_node.reputation} reputation and {fog_node.deposit} deposit remaining at {env.now}")
    state_update(env, fog_node)
    if not ejected:
        honesty_update(env, fog_node)

def honesty_update(env, fog_node):
    print(f"Fog node {fog_node.fog_id} updating honesty at {env.now}")
    fog_node.update_honesty()

def state_update(env, fog_node):
    fn_strategy = fog_node.strategy
    print(f"Updating state at {env.now} for {fn_strategy.name} strategy")

    strat_fog_reps = [f.reputation for f in fog_nodes if f.active and f.strategy == fn_strategy]
    strat_fog_profits = [(f.profit - IIMSC.deposit + f.deposit) for f in fog_nodes
                                     if f.active and f.strategy == fn_strategy]
    strat_rep_avg, strat_count = np.mean(strat_fog_reps), len(strat_fog_reps)
    strat_profit_avg = np.mean(strat_fog_profits)
    # Append to csv
    ## ['Time', 'strategy', 'avg_reputation', 'rep_count', 'avg_profit', 'prof_count']
    new_row = [env.now, fn_strategy.name, strat_count, strat_rep_avg, strat_profit_avg]
    with open(csvfile_name, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(new_row)

def service_payment(env, fog_node, passed_audit=True):
    # Service Payment
    fog_node.profit -= fog_node.honesty * IoT.cost
    if passed_audit:
        fog_node.profit += IoT.payment(fog_node)

def verify_continue(env):
    active_count = len([f for f in fog_nodes if f.active])
    if active_count <= 0:
        exit() # Stop, all nodes ejected

######### Simpy #########
env = simpy.Environment()
env.process(audit_selection_oracle(env))
env.process(audit_selection_iot(env))
env.run(until=1000)

# System end when no fog node remain active