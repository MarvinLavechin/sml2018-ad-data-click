import random
import argparse
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import os

"""
Python script to split a file containing our data into a training set and a test set.
"""

parser = argparse.ArgumentParser()
parser.add_argument("--input_file", type=str, required=True, help="csv file containing data to split")
parser.add_argument("--output_train", type=str, required=True, help="name of the output train file")
parser.add_argument("--output_test", type=str, required=True, help="name of the output test file")
parser.add_argument("--train_frac", type=float, default=0.8, help="percentage of rows to use for training set")
a = parser.parse_args()


def main():

    df = pd.read_csv(a.input_file, header=0, sep=',', parse_dates=['logged_at'])
    train_df, test_df = train_test_split(df, test_size=1-a.train_frac, random_state=42)

    directory_data = 'data/'
    if not os.path.exists(directory_data):
        os.makedirs(directory_data)

    print("Writing training data : ")
    train_df.to_csv(path_or_buf=directory_data+a.output_train, index=False)
    print("\t Done.")

    print("Writing test data : ")
    test_df.to_csv(path_or_buf=directory_data+a.output_test, index=False)
    print("\t Done.")

main()