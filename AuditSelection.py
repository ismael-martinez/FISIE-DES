import FISIE_classes as FC
import math
from random import random
import BetaDistribution as BD


# Oracle audit
def audit_selection(fog_nodes, oracle=True): #if false, IoT
    active_nodes = []
    if oracle:
        active_nodes = [f for f in fog_nodes if f.active]
    else:
        rep_threshold = BD.rep_threshold()
        active_nodes = [f for f in fog_nodes if f.active and f.reputation >= rep_threshold]
    sum_rep = sum([f.reputation for f in active_nodes])
    # Build distribution
    selection_dist = [0.0]*len(active_nodes)
    selection_dist[0] = (math.exp(-active_nodes[0].reputation))/sum_rep
    for i in range(1, len(active_nodes)):
        selection_dist[i] = (math.exp(-active_nodes[0].reputation))/sum_rep + selection_dist[i-1]

    r = random()
    for i, a in enumerate(active_nodes):
        if r < selection_dist[i]:
            return active_nodes[i]
        # else continue

