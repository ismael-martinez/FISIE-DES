####### Create figures from CSV Data #######
import matplotlib.pyplot as plt
import pandas as pd

csvfile_name = "fisie_state_data_1.csv"
df = pd.read_csv(csvfile_name)

# Plot Parameters
strats = ['Conservative', 'Aggressive', 'Cyclic', 'Balanced', 'Opportunistic']
# Dark Blue, Sky Blue, Reddish-Orange, Green, Pinkish-Purple
colours = ['#0072B2', '#56B4E9', '#F54A00', '#009E73', '#AA00AA']
dashes = ['-', '--', '-.', ':', (0,(4,1,1,1,1,1))]

plt.figure(figsize=(8, 4.6))
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

plt.figure(figsize=(8, 4.6))
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

plt.figure(figsize=(8, 4.6))
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