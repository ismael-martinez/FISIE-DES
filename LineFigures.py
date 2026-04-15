####### Create figures from CSV Data #######
import matplotlib.pyplot as plt
import pandas as pd

ratio = '0-05_'
csvfile_name = f"fisie_merged_ar_{ratio}avg_reputation.csv"
#csvfile_name = f"fisie_state_data_ar_{ratio}0.csv"
df = pd.read_csv(csvfile_name)

# Plot Parameters
strats = ['Conservative', 'Aggressive', 'Cyclic', 'Balanced', 'Opportunistic']
# Dark Blue, Reddish-Orange, Green, Sky Blue, Pinkish-Purple
colours = ['#0072B2', '#F54A00', '#009E73', '#E69F00', '#AA00AA']
dashes = ['-', '--', '-.', ':', (0,(4,1,1,1,1,1))]

plt.figure(figsize=(9, 5))
for i, s in enumerate(strats):
    df_strat = df[df['strategy']==s]
    avg_rep = df_strat['avg_reputation']
    time = df_strat['Time']
    plt.plot(time, avg_rep, color=colours[i], label=s, linestyle=dashes[i])
plt.xlabel(r"Audit Cycle $t$")
plt.ylabel(r"Avg. Reputation $r_f(t)$")
plt.legend(title="Legend — Strategies", title_fontproperties={'weight': 'bold', 'size': 'small'})
plt.title("Reputation over Time by Strategy")
plt.tight_layout()
plt.show()

csvfile_name = f"fisie_merged_ar_{ratio}avg_profit.csv"
df = pd.read_csv(csvfile_name)

plt.figure(figsize=(9, 5))
for i, s in enumerate(strats):
    df_strat = df[df['strategy']==s]
    avg_profit = df_strat['avg_profit']
    time = df_strat['Time']
    plt.plot(time, avg_profit, color=colours[i], label=s, linestyle=dashes[i])
plt.xlabel(r"Audit Cycle $t$")
plt.ylabel(r"Avg. Profit $G_f(t)$")
plt.legend(title="Legend — Strategies", title_fontproperties={'weight': 'bold', 'size': 'small'})
plt.title("Profit over Time by Strategy")
plt.tight_layout()
plt.show()


csvfile_name = f"fisie_merged_ar_{ratio}fog_count.csv"
df = pd.read_csv(csvfile_name)

plt.figure(figsize=(9, 5))
for i, s in enumerate(strats):
    df_strat = df[df['strategy']==s]
    fog_count = df_strat['fog_count']
    time = df_strat['Time']
    plt.plot(time, fog_count, color=colours[i], label=s,linestyle=dashes[i])
plt.xlabel(r"Audit Cycle $t$")
plt.ylabel(r"No. of Active Fog Nodes $|F^A_t|$")
plt.legend(title="Legend — Strategies", title_fontproperties={'weight': 'bold', 'size': 'small'})
plt.title("Active Fog Nodes over Time by Strategy")
plt.tight_layout()
plt.show()