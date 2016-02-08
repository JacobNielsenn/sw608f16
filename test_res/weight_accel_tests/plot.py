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

for f in test_files:
    with PdfPages('Motor_accel_loaded_' + f.split('_', 3)[3].split('.')[0] + '.pdf') as pdf:
        df = read_csv(f, delim_whitespace=True)
        df.plot(kind="scatter", x="Degrees", y="mS", s=df["Count"]*20, title='Motor ' + f.split('_', 3)[3].split('.')[0]   + ' acceleration test')

        pdf.savefig()
        plt.close()

with PdfPages('Accel_loaded_average.pdf') as pdf:
    dataSeries = []
    for f in test_files:
        df = read_csv(f, delim_whitespace=True)

        dataDegrees = []
        dataMS = []

        for index in df.index.values.tolist():
            pos = 0
            while pos < df.loc[index]['Count']:
                dataDegrees.append(df.loc[index]['Degrees'])
                dataMS.append(df.loc[index]['mS'])
                pos = pos + 1

        motor = 'Motor ' + f.split('_', 3)[3].split('.')[0]
        df = DataFrame([dataDegrees, dataMS], index=MultiIndex.from_tuples([(motor, 'Degrees'), (motor, 'mS')]))
        df = df.transpose()

        dataSeries.append(df)

    datas = concat(dataSeries, axis=1)
    datas.mean().unstack(level=0).plot(kind='bar', yerr=datas.std().unstack(level=0))

    datas.std().to_csv("StandartDeviation")

    plt.tight_layout()
    pdf.savefig()
    plt.close()
