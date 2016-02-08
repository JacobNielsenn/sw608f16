from pandas import *
import os
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

test_files = []
files = [f for f in os.listdir('.') if os.path.isfile(f)]

for f in files:
    if f.endswith('.data'):
        test_files.append(f)

test_files.sort()

with PdfPages('Break_lineplot.pdf') as pdf:
    dfs = []
    for f in test_files:
        df = read_csv(f, delim_whitespace=True)
        df = df.drop('id', axis=1)
        df = df.set_index('Degrees')
        df.columns = ['Motor ' + f.split('_', 3)[3].split('.')[0]]
        dfs.append(df)

    result = concat(dfs, axis=1)
    result.set_index(result.index.values - 360, inplace=True)
    ax = result.plot(marker="v")

    #Legend box is manually moved since it move cover the plot
    #http://stackoverflow.com/questions/10101700/moving-matplotlib-legend-outside-of-the-axis-makes-it-cutoff-by-the-figure-box
    handles, labels = ax.get_legend_handles_labels()
    lgd = ax.legend(handles, labels, loc='upper right', bbox_to_anchor=(1.3, 1))
    ax.grid('on')

    ax.set_ylabel("Count")

    plt.tight_layout()
    pdf.savefig(bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.close()

with PdfPages('Break_barplot.pdf') as pdf:
    dataSeries = []
    for f in test_files:
        df = read_csv(f, delim_whitespace=True)
        df = df.drop("id", axis = 1)

        data = []
        df.loc[0]['Degrees']
        for index in df.index.values.tolist():
            pos = 0
            while pos < df.loc[index]['Count']:
                data.append(df.loc[index]['Degrees'])
                pos = pos + 1
        df = DataFrame(data)
        df.columns = ['Motor ' + f.split('_', 3)[3].split('.')[0]]
        dataSeries.append(df)

    datas = concat(dataSeries, axis=1)
    datas = datas - 360
    datas.mean().plot(kind='bar', yerr=datas.std())

    datas.std().to_csv("StandardDeviation")

    plt.tight_layout()
    pdf.savefig()
    plt.close()
