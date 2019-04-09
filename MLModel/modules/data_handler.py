import pandas as pd
import numpy as np
import pickle
import glob
import json


def load_full_data(remove_label=False):
    """
    Loads the full data set given (currently split in a training set and test set)
    :return: Dataframe containing all the samples from the training set and test set
    """
    train_data = pd.read_csv("./trainingset.csv")
    test_data = pd.read_csv("./testingset.csv")

    full_data = pd.concat([train_data, test_data], axis=0)
    if remove_label:
        return full_data.drop('income', axis=1, inplace=False)

    return full_data


def load(file_path, one_hot_encode=False, max_unique=20):
    """
    Load a .csv file
    :param file_path: path to .csv
    :param one_hot_encode: (opt) if true, applies one-hot encoding on columns with less than 'max_unique' values
    :param max_unique: (opt) upper bound of one-hot encoded unique columns
    :return: one-hot encoded data in format pd.data
    """
    # Read the file
    data = pd.read_csv(file_path)

    # Convert income to binary
    data.loc[data['income'] == '>50K', 'income'] = 1
    data.loc[data['income'] == '<=50K', 'income'] = 0

    # Hot encode the features that have < max_unique
    if one_hot_encode:
        hot_encoding_indices = []
        for col in data:
            if 1 < data[col].nunique() < max_unique and str(col) != 'income':
                hot_encoding_indices.append(col)
        data = pd.get_dummies(data, columns=hot_encoding_indices, prefix=hot_encoding_indices)

    return data


def one_hot_encode(data, max_unique=20):
    """

    :param data:
    :param max_unique:
    :return:
    """
    hot_encoding_indices = []
    for col in data:
        if 1 < data[col].nunique() < max_unique and str(col) != 'income':
            hot_encoding_indices.append(col)
    data = pd.get_dummies(data, columns=hot_encoding_indices, prefix=hot_encoding_indices)

    return data


def get_missing_features(train_data, test_data):
    """
    Makes the test set features the same as the training set features
    :param train_data: the training set data
    :param test_data: the testing set data
    :return: The test data with the features from the training data (Not Sorted)
    """
    # Drop income from train_data if income exists
    if 'income' in train_data:
        train_data = train_data.drop(['income'], axis=1, inplace=False)

    # Get features in each list
    train_features = list(train_data)
    test_features = list(test_data)

    # Get features that are in one but not the other
    missing_features = np.setdiff1d(train_features, test_features)
    not_needed_features = np.setdiff1d(test_features, train_features)

    # Drop columns in the testset not in the training set
    new_data = test_data.drop(not_needed_features, axis=1, inplace=False)

    # Add columns into the testset that are in the training set but not the test set
    for feature in missing_features:
        new_data[feature] = 0

    return new_data


def print_results_to_csv(actual, predicted):
    """
    Prints results to a .csv file
    :param actual: actual values of the label
    :param predicted: predicted values of the label
    :return:
    """
    # Check if predicted is a dataframe
    if not isinstance(predicted, pd.DataFrame):
        d = {'income_pred': predicted}
        predicted = pd.DataFrame(data=d)

    # Combine the two Dataframes
    actual['income_pred'] = predicted['income_pred'].values

    filename = 'results.csv'
    files_present = glob.glob(filename)

    # Check if the file already exists
    if not files_present:
        actual.to_csv(filename)
    else:
        print('\nFunction:', print_results_to_csv.__name__)
        print('WARNING: This file already exists')


def save_model(trained_model):
    """
    Save trained model to a file
    :param trained_model: The trained model
    """
    filename = 'finalized_model.pkl'
    pickle.dump(trained_model, open(filename, 'wb'))


def get_fullset_of_features():
    """
    Gets the full set of features for the final hot encoded data
    :return: A empty data frame with all the features needed for prediction
    """
    hot_encoded_data = {
        'age': [0],
        'fnlwgt': [0],
        'capital-gain': [0],
        'capital-loss': [0],
        'hours-per-week': [0],
        'workclass_?': [0],
        'workclass_Federal-gov': [0],
        'workclass_Local-gov': [0],
        'workclass_Never-worked': [0],
        'workclass_Private': [0],
        'workclass_Self-emp-inc': [0],
        'workclass_Self-emp-not-inc': [0],
        'workclass_State-gov': [0],
        'workclass_Without-pay': [0],
        'education_10th': [0],
        'education_11th': [0],
        'education_12th': [0],
        'education_1st-4th': [0],
        'education_5th-6th': [0],
        'education_7th-8th': [0],
        'education_9th': [0],
        'education_Assoc-acdm': [0],
        'education_Assoc-voc': [0],
        'education_Bachelors': [0],
        'education_Doctorate': [0],
        'education_HS-grad': [0],
        'education_Masters': [0],
        'education_Preschool': [0],
        'education_Prof-school': [0],
        'education_Some-college': [0],
        'education-num_1': [0],
        'education-num_2': [0],
        'education-num_3': [0],
        'education-num_4': [0],
        'education-num_5': [0],
        'education-num_6': [0],
        'education-num_7': [0],
        'education-num_8': [0],
        'education-num_9': [0],
        'education-num_10': [0],
        'education-num_11': [0],
        'education-num_12': [0],
        'education-num_13': [0],
        'education-num_14': [0],
        'education-num_15': [0],
        'education-num_16': [0],
        'marital-status_Divorced': [0],
        'marital-status_Married-AF-spouse': [0],
        'marital-status_Married-civ-spouse': [0],
        'marital-status_Married-spouse-absent': [0],
        'marital-status_Never-married': [0],
        'marital-status_Separated': [0],
        'marital-status_Widowed': [0],
        'occupation_?': [0],
        'occupation_Adm-clerical': [0],
        'occupation_Armed-Forces': [0],
        'occupation_Craft-repair': [0],
        'occupation_Exec-managerial': [0],
        'occupation_Farming-fishing': [0],
        'occupation_Handlers-cleaners': [0],
        'occupation_Machine-op-inspct': [0],
        'occupation_Other-service': [0],
        'occupation_Priv-house-serv': [0],
        'occupation_Prof-specialty': [0],
        'occupation_Protective-serv': [0],
        'occupation_Sales': [0],
        'occupation_Tech-support': [0],
        'occupation_Transport-moving': [0],
        'relationship_Husband': [0],
        'relationship_Not-in-family': [0],
        'relationship_Other-relative': [0],
        'relationship_Own-child': [0],
        'relationship_Unmarried': [0],
        'relationship_Wife': [0],
        'race_Amer-Indian-Eskimo': [0],
        'race_Asian-Pac-Islander': [0],
        'race_Black': [0],
        'race_Other': [0],
        'race_White': [0],
        'sex_Female': [0],
        'sex_Male': [0],
        'native-country_?': [0],
        'native-country_Cambodia': [0],
        'native-country_Canada': [0],
        'native-country_China': [0],
        'native-country_Columbia': [0],
        'native-country_Cuba': [0],
        'native-country_Dominican-Republic': [0],
        'native-country_Ecuador': [0],
        'native-country_El-Salvador': [0],
        'native-country_England': [0],
        'native-country_France': [0],
        'native-country_Germany': [0],
        'native-country_Greece': [0],
        'native-country_Guatemala': [0],
        'native-country_Haiti': [0],
        'native-country_Holand-Netherlands': [0],
        'native-country_Honduras': [0],
        'native-country_Hong': [0],
        'native-country_Hungary': [0],
        'native-country_India': [0],
        'native-country_Iran': [0],
        'native-country_Ireland': [0],
        'native-country_Italy': [0],
        'native-country_Jamaica': [0],
        'native-country_Japan': [0],
        'native-country_Laos': [0],
        'native-country_Mexico': [0],
        'native-country_Nicaragua': [0],
        'native-country_Outlying-US(Guam-USVI-etc)': [0],
        'native-country_Peru': [0],
        'native-country_Philippines': [0],
        'native-country_Poland': [0],
        'native-country_Portugal': [0],
        'native-country_Puerto-Rico': [0],
        'native-country_Scotland': [0],
        'native-country_South': [0],
        'native-country_Taiwan': [0],
        'native-country_Thailand': [0],
        'native-country_Trinadad&Tobago': [0],
        'native-country_United-States': [0],
        'native-country_Vietnam': [0],
        'native-country_Yugoslavia': [0]
    }

    return pd.DataFrame(data=hot_encoded_data)


def predict_income(jsondata):

    data = \
        '{ "age": 43, ' \
        '"workclass": "Never-worked",' \
        '"fnlwgt": 70800,' \
        '"education": "Bachelors",' \
        '"education-num": 13,' \
        '"marital-status": "Never-married",' \
        '"occupation": "?",' \
        '"relationship": "Unmarried",' \
        '"race": "Black",' \
        '"sex": "Male",' \
        '"capital-gain": 0,' \
        '"capital-loss": 0,' \
        '"hours-per-week": 40,' \
        '"native-country": "United-States",' \
        '"income": 0' \
        '}'

    # Parse the Json file
    donor = json.loads(data)
    donor_df = pd.DataFrame(data=donor, index=[0])
    # print(donor_df.info())

    full_data = get_fullset_of_features()
    for feature in donor_df:
        for hot_encoded_feature in full_data:
            if str(feature) == str(hot_encoded_feature):
                full_data.at[0, str(hot_encoded_feature)] = donor_df.iloc[0][feature]
                continue
            elif str(hot_encoded_feature) == str(str(feature) + '_' + str(donor_df.iloc[0][feature])):
                full_data.at[0, str(hot_encoded_feature)] = 1
                continue

    print(full_data.iloc[0])

    # Load the model and predict
    filename = "./finalized_model.pkl"
    loaded_model = pickle.load(open(filename, 'rb'))
    pred = loaded_model.predict(full_data)

    if pred[0] == 0:
        return "Regular Donor"
    else:
        return "High Donor"

