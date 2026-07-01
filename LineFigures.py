####### Create figures from CSV Data #######
import matplotlib.pyplot as plt
import pandas as pd

ratio = '0-025'
survival_file = f"fisie_survival_points_{ratio}.csv"
s_df = pd.read_csv(survival_file)

# Plot Parameters
strats = ['Conservative', 'Aggressive', 'Balanced', 'Progressive', 'Opportunistic']
# Dark Blue, Reddish-Orange, Green, Sky Blue, Pinkish-Purple
colours = ['#0072B2', '#F54A00', '#E69F00', '#009E73', '#AA00AA']
markers = ['p', 'H', '*', '^', 'v']
dashes = ['-', '--', ':', '-.', (0,(4,1,1,1,1,1))]
plt_figsize = (9,6.5)

csvfile_name = f"fisie_merged_ar_{ratio}_avg_reputation.csv"
df = pd.read_csv(csvfile_name)

plt.figure(figsize=plt_figsize)
for i, s in enumerate(strats):
    df_strat = df[df['strategy']==s]
    avg_rep = df_strat['avg_reputation']
    time = df_strat['Time']
    s_df_rep = s_df[s_df['strategy'] == s]
    markers_on = s_df_rep['rep_idx'].to_list()
    markers_on.append(len(df_strat)-1)

    plt.plot(time, avg_rep, color=colours[i], label=s, linestyle=dashes[i], markevery=markers_on, marker=markers[i])

    # s_df_rep = s_df[s_df['strategy'] == s]
    # plt.scatter(s_df_rep['Time'], s_df_rep['reputation'], color=colours[i], marker='.')
plt.xlabel(r"Time $t$", fontsize=12)
plt.ylabel(r"Avg. Reputation $r_f(t)$", fontsize=12)
plt.legend(title="Legend — Strategies", title_fontproperties={'weight': 'bold', 'size': 'small'}, loc=0, markerfirst=True, handlelength=3)
plt.title("Reputation over Time by Strategy", fontsize=14)
plt.tight_layout()
plt.show()

csvfile_name = f"fisie_merged_ar_{ratio}_avg_profit.csv"
df = pd.read_csv(csvfile_name)

plt.figure(figsize=plt_figsize)
for i, s in enumerate(strats):
    df_strat = df[df['strategy']==s]
    avg_profit = df_strat['avg_profit']
    time = df_strat['Time']
    s_df_pr = s_df[s_df['strategy'] == s]
    markers_on = s_df_pr['pr_idx'].to_list()
    markers_on.append(len(df_strat)-1)

    plt.plot(time, avg_profit, color=colours[i], label=s, linestyle=dashes[i], markevery=markers_on, marker=markers[i])

    # s_df_pr = s_df[s_df['strategy'] == s]
    # plt.scatter(s_df_pr['Time'], s_df_pr['profit'], color=colours[i], markevery=markers_on, marker=markers[i])
plt.xlabel(r"Time $t$", fontsize=12)
plt.ylabel(r"Avg. Net Profit $\psi_f(t)$", fontsize=12)
plt.legend(title="Legend — Strategies", title_fontproperties={'weight': 'bold', 'size': 'small'}, loc=3, markerfirst=True, handlelength=3.0)
plt.title("Net Profit over Time by Strategy", fontsize=14)
plt.tight_layout()
#plt.yscale('log')
plt.show()


# csvfile_name = f"fisie_merged_ar_{ratio}_avg_reliability.csv"
# df = pd.read_csv(csvfile_name)
#
# plt.figure(figsize=plt_figsize)
# for i, s in enumerate(strats):
#     df_strat = df[df['strategy']==s]
#     avg_reliability = df_strat['avg_reliability']
#     time = df_strat['Time']
#     s_df_rel = s_df[s_df['strategy'] == s]
#     markers_on = s_df_rel['rel_idx'].to_list()
#
#     plt.plot(time, avg_reliability, color=colours[i], label=s, linestyle=dashes[i], markevery=markers_on, marker=markers[i])
#
#     #plt.scatter(s_df_rel['Time'], s_df_rel['reliability'], color=colours[i], markevery=markers_on, marker=markers[i])
# plt.xlabel(r"Audit Cycle $t$")
# plt.ylabel(r"Avg. Reliability $\zeta(t)$")
# plt.legend(title="Legend — Strategies", title_fontproperties={'weight': 'bold', 'size': 'small'})
# plt.title("Reliability over Time by Strategy")
# plt.tight_layout()
# #plt.yscale('log')
# plt.show()

# csvfile_name = f"fisie_merged_ar_{ratio}_fog_count.csv"
# df = pd.read_csv(csvfile_name)
#
# plt.figure(figsize=plt_figsize)
# for i, s in enumerate(strats):
#     df_strat = df[df['strategy']==s]
#     fog_count = df_strat['fog_count']
#     time = df_strat['Time']
#     plt.plot(time, fog_count, color=colours[i], label=s,linestyle=dashes[i])
# plt.xlabel(r"Audit Cycle $t$")
# plt.ylabel(r"No. of Active Fog Nodes $|F^A_t|$")
# plt.legend(title="Legend — Strategies", title_fontproperties={'weight': 'bold', 'size': 'small'}, loc=3)
# plt.title("Active Fog Nodes over Time by Strategy")
# plt.tight_layout()
# plt.show()