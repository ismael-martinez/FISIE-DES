import random
seed_base = 250

import simpy

import FISIE_classes as FC
from FISIE_classes import IoTDevices as IoT
from FISIE_classes import IIMSC
import AuditSelection as AS
import numpy as np
import csv

# Arrival Rates
oracle_AR = 5
IoT_AR = 100
oracle_iot_fraction =  oracle_AR/IoT_AR
VERBOSE = False
suffix = f"ar_{oracle_iot_fraction}_"
suffix = suffix.replace('.','-')


# Simpy Processes
def audit_selection_oracle(env):
    while True:
        interarrival = np.random.exponential(1./oracle_AR)
        yield env.timeout(interarrival)
        if not verify_continue(env):
            break # End
        if VERBOSE:
            print(f"Beginning full audit from oracle at {env.now}")
        fn = AS.audit_selection(fog_nodes)
        if VERBOSE:
            print(f"Selected fog node with id {fn.fog_id}")
        audit_observation(env,fn)
def audit_selection_iot(env):
    while True:
        interarrival = np.random.exponential(1./IoT_AR)
        yield env.timeout(interarrival)
        if not verify_continue(env):
            break # End
        if VERBOSE:
            print(f"Beginning partial verification from IoT at {env.now}")
        fn = AS.audit_selection(fog_nodes, False)
        if VERBOSE:
            print(f"Selected fog node with id {fn.fog_id}")
        audit_observation(env, fn, False)

def audit_observation(env, fog_node, oracle=True):
    passed_audit = True

    # Audit
    if oracle:
        if fog_node.honesty < 1:
            if VERBOSE:
                print(f"Fog node {fog_node.fog_id} failed Oracle audit at {env.now}")
            passed_audit = False
        else:
            if VERBOSE:
                print(f"Fog node {fog_node.fog_id} passed Oracle audit at {env.now}")
            #passed_audit = True
    else: # IoT
        eta = IoT.prob_pass_audit(fog_node)
        if random.random() > eta: # failure
            if VERBOSE:
                print(f"Fog node {fog_node.fog_id} failed IoT partial verification at {env.now}")
            passed_audit = False
        else:
            if VERBOSE:
                print(f"Fog node {fog_node.fog_id} passed IoT partial verification at {env.now}")
            #passed_audit = True
    audit = FC.Audit(fog_node, oracle, passed_audit)
    service_payment(env, audit)
    reputation_update(env, audit)



def reputation_update(env, audit):
    fog_node = audit.fog_node
    passed_audit = audit.audit_pass
    ejected = False
    if passed_audit:
        fog_node.reputation = min([fog_node.reputation + IIMSC.rep_inc, IIMSC.rep_max])
        if VERBOSE:
            print(f"Fog node {fog_node.fog_id} reputation increased to {fog_node.reputation} at {env.now}")
    else:
        fog_node.reputation -= IIMSC.rep_dec
        fog_node.deposit -= IIMSC.deposit_dec
        if fog_node.deposit <= 0 or fog_node.reputation < IIMSC.rep_min:
            if VERBOSE:
                print(f"Fog node {fog_node.fog_id} is ejected from the system at {env.now}")
            fog_node.active = False
            ejected = True
        else:
            if VERBOSE:
                print(f"Fog node {fog_node.fog_id} has {fog_node.reputation} reputation and {fog_node.deposit} deposit remaining at {env.now}")
    state_update(env, audit)
    if not ejected:
        honesty_update(env, audit)

def honesty_update(env, audit):
    fog_node = audit.fog_node
    if VERBOSE:
        print(f"Fog node {fog_node.fog_id} updating honesty at {env.now}")
    fog_node.update_honesty()

def state_update(env, audit):
    fog_node = audit.fog_node
    fn_strategy = fog_node.strategy
    if VERBOSE:
        print(f"Updating state at {env.now} for {fn_strategy.name} strategy")

    strat_fog_reps = [f.reputation for f in fog_nodes if f.active and f.strategy == fn_strategy]
    strat_fog_profits = [(f.profit - IIMSC.deposit + f.deposit) for f in fog_nodes
                                     if f.active and f.strategy == fn_strategy]
    strat_fog_honesty = [f.honesty for f in fog_nodes if f.active and f.strategy == fn_strategy]
    strat_rep_avg, fog_count = np.nan, 0
    if len(strat_fog_reps) > 0:
        strat_rep_avg, fog_count = np.mean(strat_fog_reps), len(strat_fog_reps)
    strat_profit_avg = np.nan
    if len(strat_fog_profits) > 0:
        strat_profit_avg = np.mean(strat_fog_profits)
    strat_honesty_avg = np.nan
    if len(strat_fog_honesty) > 0:
        strat_honesty_avg = np.mean(strat_fog_honesty)
    # Append to csv
    ## ['Time', 'strategy', 'avg_reputation', 'rep_count', 'avg_profit', 'prof_count', 'avg_honesty']
    new_row = [env.now, fn_strategy.name, fog_count, strat_rep_avg, strat_profit_avg, strat_honesty_avg, audit.type, audit.audit_pass]
    with open(csvfile_name, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(new_row)

def service_payment(env, audit):
    fog_node = audit.fog_node
    passed_audit = audit.audit_pass
    # Service Payment
    fog_node.profit -= fog_node.honesty * IoT.cost
    if passed_audit:
        fog_node.profit += IoT.payment(fog_node)

def verify_continue(env):
    active_count = len([f for f in fog_nodes if f.active])
    if active_count <= 0:
        return False# Stop, all nodes ejected
    return True




for sim in range(0, 50):
    print(f"Simulation {sim}")
    random.seed = seed_base + sim

    ####### Setup #######

    # f fog nodes per strategy (5)
    fog_per = 1000
    num_strategies = 5
    fog_nodes = [None]*(fog_per * num_strategies)
    for s in range(num_strategies):
        for f in range(fog_per):
            idx = f + s*fog_per
            fog_nodes[idx] = FC.FogNode(FC.Strategy(s))

    ###### State variables ######

    # Reputation over time
    rep_state = []
    # Payment - Cost over time
    payment_state = []
    # Store states in csv file
    fieldnames = ['Time', 'strategy', 'fog_count', 'avg_reputation', 'avg_profit', 'avg_honesty', 'audit_type', 'audit_result']

    csvfile_name = "fisie_state_data_{}{}.csv".format(suffix, sim)
    with open(csvfile_name, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer = csv.writer(csvfile)
        for s in range(num_strategies):
            first_row = [0, FC.Strategy(s).name, fog_per, IIMSC.rep_init, 0, np.nan]
            writer.writerow(first_row)

    ######### Simpy #########
    env = simpy.Environment()
    env.process(audit_selection_oracle(env))
    env.process(audit_selection_iot(env))
    env.run(until=1000)

    # System end when no fog node remain active