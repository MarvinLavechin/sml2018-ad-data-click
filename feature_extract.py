import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--input_train", type=str, default="data/data_train.csv", help="The csv file containing the training features")
parser.add_argument("--input_test", type=str, default="data/data_test.csv", help="The csv file containing the test features")
parser.add_argument("--max_id", type=str, default="data/maxID.txt", help="The txt file containing the pairs (feature/maxID)")
parser.add_argument("--output_train", type=str, default="data/train_svm.txt", help="The output file where to write the training extracted features")
parser.add_argument("--output_test", type=str, default="data/test_svm.txt", help="The output file where to write the test extracted features")
parser.add_argument("--list_cat_features", nargs='+', type=int, help="The list of categorical features to extract", required=True)

a = parser.parse_args()

def extract_one_hot_encoding(input, max_id, output, list_cat_features):
    """
    Extract the features contained in input file (csv) and write the extracted features in the output file (SVM format)
    :param input: the csv file containing the features
    :param max_id: the txt file containing the pairs (feature/maxID)
    :param output: the output file where to write the extracted features
    :param list_cat_features: the features to extract
    :return:
    """
    # Open raw features file
    fin = open(input)
    featname = fin.readline().strip().split(',')

    # Open maxID file
    maxID = {}
    finID = open(max_id)

    # For each features, construct the table of the maxID
    for line in finID:
        i, id = line.strip().split('\t')
        maxID[featname[int(i)]] = int(id) + 1

    # Open output file which will contain extracted features
    fout = open(output,'w')

    # Use One Hot Encoded
    i = 0
    for line in fin:
        data = line.strip().split(',')

        # Get the target
        if data[14] == '0':
            click = '-1' # The hasn't been clicked
        elif data[14] == '1':
            click = '+1' # The ad has been clicked
        elif data[14] == '':
            click = '0' # No data (test set)

        #In SVM format, index start with 1 while it starts with 0 in python
        x = []
        sum_cum = 1
        for feature in list_cat_features:
            x.append(str(int(data[feature]) + sum_cum))
            sum_cum = sum_cum + maxID[featname[int(feature)]]

        x_svm = [click]
        for index in x:
            x_svm.append(index + ':1')

        fout.write(' '.join(x_svm) + '\n')

    fin.close()
    fout.close()


def main():

    print("Extraction of the training features : ")
    extract_one_hot_encoding(a.input_train, a.max_id, a.output_train, a.list_features)
    print("\t Done.")

    print("Extraction of the test features : ")
    extract_one_hot_encoding(a.input_test, a.max_id, a.output_test, a.list_features)
    print("\t Done.")

main()


