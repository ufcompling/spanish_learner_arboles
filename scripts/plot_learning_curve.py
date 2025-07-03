"""
Script for creating plots of learning curve results for each task:
Lemma acc, UPOS acc, UAS, and LAS

You can either get the metric results by processing the metric files via
command line tools (e.g. grep/awk) and pasting the results for "data_string"
and "data_string2", or use the `get_data_list` function to read the 
results from the metrics.json files.
"""
import json
import glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def get_data_list(experiment_prefix, path_to_exp_logs="./"):
    """
    An optional way to read the metrics from the machamp experiment logs.
    Assumes each experiment in the learning curve is consistently named.
    For intance, if the log directories are "ancora_only_n=..." for each
    step in the learning curve, pass "ancora_only_n=" as the 
    `experiment_prefix`.

    Alternatively, you could just create a data string with command-line 
    tools and replace the `data_string` variables below with that list.
    """
    uas = "best_dev_dependency_uas"
    las = "best_dev_dependency_las"
    lemma = "best_dev_lemma_accuracy"
    upos = "best_dev_upos_accuracy"

    data_vols = [f.split("=")[1] for f in glob.glob(f"{path_to_exp_logs}{experiment_prefix}*")]

    rows = []
    for data_vol in data_vols:
        metrics_file = glob.glob(f"ancora_train={data_vol}/*/metrics.json")[0]
        with open(metrics_file) as f:
            metrics = json.load(f)
            for m, mname in [(uas, "UAS"), (las, "LAS"), (lemma, "Lemma"), (upos, "UPOS")]:
                val = metrics[m]
                row = [data_vol, mname, val]
                rows.append(row)

    return sorted(rows)
#
# Here we just used grep/awk to retrieve the metrics for each learning curve experiment 
#(e.g. grep -P "best_dev.*accuracy|best_dev_dependency_.*as" logs/ancora_train\=*/*/metrics.json)
# The format here is <sample_size>,<task_metric>,<value>
# The first data string corresponds to the dotted line in the curve (AnCora+learner corpus), and the second corresponds to the solid line (AnCora only).
#

data_string1 = """10032,"UAS",0.890497737556561,
10032,"LAS",0.820814479638009,
10032,"Lemma",0.9475113122171945,
10032,"UPOS",0.9701357466063348,
15048,"UAS",0.890497737556561,
15048,"LAS",0.8244343891402715,
15048,"Lemma",0.9556561085972851,
15048,"UPOS",0.9728506787330317,
20064,"UAS",0.8886877828054298,
20064,"LAS",0.8226244343891402,
20064,"Lemma",0.9529411764705882,
20064,"UPOS",0.9701357466063348,
25080,"UAS",0.8841628959276018,
25080,"LAS",0.8126696832579186,
25080,"Lemma",0.9601809954751132,
25080,"UPOS",0.971945701357466,
30096,"UAS",0.8886877828054298,
30096,"LAS",0.8244343891402715,
30096,"Lemma",0.9638009049773756,
30096,"UPOS",0.9737556561085973,
35112,"UAS",0.8832579185520362,
35112,"LAS",0.8144796380090498,
35112,"Lemma",0.967420814479638,
35112,"UPOS",0.9746606334841629,
40128,"UAS",0.9031674208144796,
40128,"LAS",0.8289592760180996,
40128,"Lemma",0.9665158371040724,
40128,"UPOS",0.9710407239819004,
45144,"UAS",0.8923076923076924,
45144,"LAS",0.8244343891402715,
45144,"Lemma",0.9619909502262444,
45144,"UPOS",0.9737556561085973,
50160,"UAS",0.8923076923076924,
50160,"LAS",0.8253393665158371,
50160,"Lemma",0.9665158371040724,
50160,"UPOS",0.9710407239819004,
5016,"UAS",0.881447963800905,
5016,"LAS",0.8117647058823529,
5016,"Lemma",0.9493212669683257,
5016,"UPOS",0.9737556561085973,
55176,"UAS",0.902262443438914,
55176,"LAS",0.8371040723981901,
55176,"Lemma",0.9692307692307692,
55176,"UPOS",0.9737556561085973,
60192,"UAS",0.8950226244343892,
60192,"LAS",0.8298642533936652,
60192,"Lemma",0.971945701357466,
60192,"UPOS",0.9710407239819004,
65208,"UAS",0.8950226244343892,
65208,"LAS",0.8253393665158371,
65208,"Lemma",0.9710407239819004,
65208,"UPOS",0.9737556561085973,
70224,"UAS",0.890497737556561,
70224,"LAS",0.8235294117647058,
70224,"Lemma",0.9728506787330317,
70224,"UPOS",0.9755656108597285,
75240,"UAS",0.8832579185520362,
75240,"LAS",0.8199095022624434,
75240,"Lemma",0.971945701357466,
75240,"upos",0.9737556561085973,
80256,"UAS",0.8941176470588236,
80256,"LAS",0.8271493212669683,
80256,"Lemma",0.9782805429864253,
80256,"UPOS",0.9728506787330317,
85272,"UAS",0.8868778280542986,
85272,"LAS",0.8190045248868778,
85272,"Lemma",0.9737556561085973,
85272,"UPOS",0.9737556561085973,
90288,"UAS",0.8968325791855204,
90288,"LAS",0.8244343891402715,
90288,"Lemma",0.9737556561085973,
90288,"UPOS",0.971945701357466,
95304,"UAS",0.881447963800905,
95304,"LAS",0.8108597285067873,
95304,"Lemma",0.9755656108597285,
95304,"UPOS",0.9746606334841629,
0,"UAS",0.8643617021276596,
0,"LAS",0.7943262411347518,
0,"Lemma",0.9352836879432624,
0,"UPOS",0.9689716312056738,
"""

data_string2 = """
10032,"UAS",0.8063348416289593,
10032,"LAS",0.7221719457013575,
10032,"Lemma",0.9095022624434389,
10032,"UPOS",0.9574660633484163,
15048,"UAS",0.8298642533936652,
15048,"LAS",0.7538461538461538,
15048,"Lemma",0.918552036199095,
15048,"UPOS",0.9665158371040724,
20064,"UAS",0.8624434389140272,
20064,"LAS",0.7819004524886878,
20064,"Lemma",0.9239819004524887,
20064,"UPOS",0.9619909502262444,
25080,"UAS",0.8542986425339366,
25080,"LAS",0.7710407239819005,
25080,"Lemma",0.9429864253393665,
25080,"UPOS",0.96289592760181,
30096,"UAS",0.8542986425339366,
30096,"LAS",0.7719457013574661,
30096,"Lemma",0.9420814479638009,
30096,"UPOS",0.96289592760181,
35112,"UAS",0.8561085972850678,
35112,"LAS",0.7846153846153846,
35112,"Lemma",0.9466063348416289,
35112,"UPOS",0.96289592760181,
40128,"UAS",0.8769230769230769,
40128,"LAS",0.7900452488687782,
40128,"Lemma",0.9466063348416289,
40128,"UPOS",0.9656108597285068,
45144,"UAS",0.8615384615384616,
45144,"LAS",0.7828054298642534,
45144,"Lemma",0.9393665158371041,
45144,"UPOS",0.9656108597285068,
50160,"UAS",0.865158371040724,
50160,"LAS",0.7909502262443439,
50160,"Lemma",0.9493212669683257,
50160,"UPOS",0.96289592760181,
5016,"UAS",0.7330316742081447,
5016,"LAS",0.648868778280543,
5016,"Lemma",0.8316742081447964,
5016,"UPOS",0.951131221719457,
55176,"UAS",0.8669683257918552,
55176,"LAS",0.7927601809954751,
55176,"Lemma",0.9529411764705882,
55176,"UPOS",0.9665158371040724,
60192,"UAS",0.8705882352941177,
60192,"LAS",0.7981900452488688,
60192,"Lemma",0.9493212669683257,
60192,"UPOS",0.9656108597285068,
65208,"UAS",0.8705882352941177,
65208,"LAS",0.7927601809954751,
65208,"Lemma",0.9466063348416289,
65208,"UPOS",0.96289592760181,
40128,"UAS",0.8769230769230769,
40128,"LAS",0.7900452488687782,
40128,"Lemma",0.9466063348416289,
40128,"UPOS",0.9656108597285068,
45144,"UAS",0.8615384615384616,
45144,"LAS",0.7828054298642534,
45144,"Lemma",0.9393665158371041,
45144,"UPOS",0.9656108597285068,
50160,"UAS",0.865158371040724,
50160,"LAS",0.7909502262443439,
50160,"Lemma",0.9493212669683257,
50160,"UPOS",0.96289592760181,
5016,"UAS",0.7330316742081447,
5016,"LAS",0.648868778280543,
5016,"Lemma",0.8316742081447964,
5016,"UPOS",0.951131221719457,
55176,"UAS",0.8669683257918552,
55176,"LAS",0.7927601809954751,
55176,"Lemma",0.9529411764705882,
55176,"UPOS",0.9665158371040724,
60192,"UAS",0.8705882352941177,
60192,"LAS",0.7981900452488688,
60192,"Lemma",0.9493212669683257,
60192,"UPOS",0.9656108597285068,
65208,"UAS",0.8705882352941177,
65208,"LAS",0.7927601809954751,
65208,"Lemma",0.9466063348416289,
65208,"UPOS",0.96289592760181,
85272,"UAS",0.8723981900452489,
85272,"LAS",0.7936651583710407,
85272,"Lemma",0.9556561085972851,
85272,"UPOS",0.9683257918552036,
90288,"UAS",0.8552036199095022,
90288,"LAS",0.783710407239819,
90288,"Lemma",0.9547511312217195,
90288,"UPOS",0.9683257918552036
"""

data_list = [line.strip(",").split(',') for line in data_string1.strip().split('\n')]

#
# alternatively, skip creating the datalist from a hard-coded string of metric values:
# data_list = get_data_list("learner+ancora_train=", "/pah/to/machamp/logs")
#
data_list = [line for line in data_list if int(line[0]) < 50000]

df = pd.DataFrame(data_list, columns=['Data Volume', 'Metric', 'Value'])
df['Data Volume'] = df['Data Volume'].apply(lambda x: int(x.replace(' ', '')))
df['Value'] = pd.to_numeric(df['Value'])
df['Metric'] = df['Metric'].str.strip('"')
df['Data Volume'] = (df['Data Volume'] / 1000).round() * 1000

#
# Set the figure size and create subplots (2 rows, 4 columns)
#
fig, axs = plt.subplots(1, 4, figsize=(20, 5))


#
# Set hues for the legend
#
hue_order = ['Lemma', "UPOS", "UAS", "LAS"]
palette = ["#E69F00", "#56B4E9", "#009E73", "#CC79A7"]
sns.set_theme()

#
# Manually set baseline values
#
y_baseline_values = {
    'Lemma': 0.9352836879432624,
    'UPOS': 0.9689716312056738,
    'UAS': 0.8643617021276596,
    'LAS': 0.7943262411347518
}


# Prepare the AnCora-only data (will correspond to the solid line)
data_list2 = [line.strip(",").split(',') for line in data_string2.strip().split('\n')]
#
# alternatively, skip creating the datalist from a hard-coded string of metric values:
# data_list = get_data_list("ancora_train=", "/pah/to/machamp/logs")
#
data_list2 = [line for line in data_list2 if int(line[0]) < 50000]

df2 = pd.DataFrame(data_list2, columns=['Data Volume', 'Metric', 'Value'])
df2['Data Volume'] = df2['Data Volume'].apply(lambda x: int(x.replace(' ', '')))
df2['Value'] = pd.to_numeric(df2['Value'])
df2['Metric'] = df2['Metric'].str.strip('"')
df2['Data Volume'] = (df2['Data Volume'] / 1000).round() * 1000


for i, metric in enumerate(hue_order):
    #
    # plot the AnCora+learner data (dotted line)
    #
    sns.lineplot(data=df[df['Metric'] == metric], linewidth=3, x='Data Volume', y='Value', ax=axs[i], color=palette[i], linestyle="dotted")
    
    #
    # plots the AnCora only data (solid line)
    #
    sns.lineplot(data=df2[df2['Metric'] == metric], linewidth=1.5, x='Data Volume', y='Value', ax=axs[i], color=palette[i], linestyle="solid")
    axs[i].set_title(f"{metric}", fontsize=18)  # Increased font size for the title

    axs[i].grid(True)

    #
    # Add baseline values to the graphs
    #
    axs[i].axhline(y=y_baseline_values[metric], color="black", linewidth=2, alpha=0.5)
    axs[i].set_ylim(0.7, 1.0)
    axs[i].set_xlim(0, 50000)
    axs[i].set_xlabel("")
    axs[i].set_ylabel('')


fig.supxlabel('Number of AnCora training tokens', fontsize=18)
fig.supylabel('Accuracy', fontsize=18)
fig.tight_layout(rect=[0.01, 0.01, 1, 1])
plt.show()

