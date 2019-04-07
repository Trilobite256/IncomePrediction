import numpy as np
import matplotlib.pyplot as plt
import load_data as loader


def barhplot(data, feature, title):
    feature_name, counts = np.unique(data.loc[:, str(feature)], return_counts=True)
    plt.barh(feature_name, counts, height=0.3)
    plt.title(title)
    plt.xlabel('count')
    plt.ylabel(str(feature))
    for i, v in enumerate(counts):
        plt.text(v + 3, i, str(v), color='black')


def histogram(data, feature, title, bins=20):
    x = data.loc[:, str(feature)]
    plt.title(title)
    plt.xlabel(str(feature))
    plt.ylabel('Frequency')
    plt.hist(x, bins=bins)


# Load the data
data = loader.load_full_data()

max_unique = 20     # max number of unique values before it is considered continuous
i = 1               # to keep track of the number of loops
for feature in data:

    # Separate the dataset into possible high donors and regular donors
    hd = data[data['income'] == '>50K']
    rd = data[data['income'] == '<=50K']

    if data[feature].nunique() <= max_unique or str(feature) == 'native-country':

        # Create the first bar plot for high donors
        plt.subplot(2, 1, 1)
        barhplot(hd, feature, "Number of each type of person >50K")

        # Create the second bar plot for regular donors
        plt.subplot(2, 1, 2)
        barhplot(rd, feature, "Number of each type of person <=50K")

    else:

        # Create histogram for first bar plot
        plt.subplot(2, 1, 1)
        histogram(hd, feature, str(feature) + " Histogram >50K")

        plt.subplot(2, 1, 2)
        histogram(rd, feature, str(feature) + " Histogram <=50K")

    plt.tight_layout()

    print(str(feature))
    if str(feature) == 'hours-per-week':
        plt.rcParams["figure.figsize"] = (8, 20)
    else:
        plt.rcParams["figure.figsize"] = (8, 8)

    plt.savefig('graphs/fig' + str(i) + '.png')
    plt.show()
    i += 1
