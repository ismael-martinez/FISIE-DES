import matplotlib.pyplot as plt
from scipy.stats import beta as BetaDist
import numpy as np

ab_min = 2
ab_max = 10

R_min = 2
R_max = 10

def opportunistic_strat(r):
    alpha = ab_max - (ab_max - ab_min) * ((r - R_min) / (R_max - R_min))
    beta = ab_min + (ab_max - ab_min) * ((r - R_min) / (R_max - R_min))
    return beta_sample(alpha, beta)

def balanced_strat():
    ab_tilde = (ab_max + ab_min) / 2
    return beta_sample(ab_tilde, ab_tilde)

def conservative_strat():
    alpha = ab_max
    beta = ab_min
    return beta_sample(alpha, beta)

def aggressive_strat():
    alpha = ab_min
    beta = ab_max
    return beta_sample(alpha, beta)

def cyclic_strat(r, R):
    if r > R:
        return aggressive_strat()
    else:
        return conservative_strat()

def partial_length():
    alpha = 1
    beta = 10
    return BetaDist.rvs(alpha, beta)

def rep_iot_threshold():
    alpha = 2
    beta = 5
    return BetaDist.rvs(alpha, beta)

def beta_sample(alpha, beta):
    try:
        return BetaDist.rvs(alpha, beta)
    except:
        print("Parameters are negative")

def plot_beta():
    ab_mid = int((ab_min + ab_max)/2)
    ab_array = [(ab_min, ab_max), (ab_mid, ab_mid), (ab_max, ab_min)]
    dashes = ['--', '-', '-.']
    # colours = ['#F54A00', '#5CF000', '#9400F0']
    # Reddish-Orange, Green, Pinkish-Purple
    colours = ['#F54A00', '#009E73', '#AA00AA']

    plt.subplots(figsize=(6.3,3.5))
    for i, ab in enumerate(ab_array):
        alpha = ab[0]
        beta = ab[1]
        plt_label = r'$(\alpha, \beta)=({}, {})$'.format(alpha, beta)
        x = np.linspace(0, 1, 100, True)
        y = [BetaDist.pdf(xi, alpha, beta) for xi in x]
        plt.plot(x,y, label=plt_label, linestyle=dashes[i], color=colours[i])

    plt.legend()
    plt_title = r'Beta Distributions for Behavioural Strategies—$(a_{\min},a_{\max})=$'
    vals = '({}, {})'.format(ab_min, ab_max)
    plt.title(plt_title + vals)
    plt.xlabel(r'Honesty Factor $h$', fontsize=10)
    plt.ylabel(r'Probability Density', fontsize=10)
    plt.tight_layout()
    plt.show()

# plot_beta()