import argparse
import datetime

parser = argparse.ArgumentParser()

parser.add_argument("--input_train", type=str, default="enriched_data_train.csv", help="The csv file containing the training features")
parser.add_argument("--input_test", type=str, default="enriched_data_test.csv", help="The csv file containing the test features")
parser.add_argument("--max_id", type=str, default="maxID.txt", help="The txt file containing the pairs (feature/maxID)")
parser.add_argument("--scale_file", type=str, default="trainSCALE.txt", help="The txt file containing the 2-uplets (number feature/mean/std)")
parser.add_argument("--output_train", type=str, default="train_svm.txt", help="The output file where to write the training extracted features")
parser.add_argument("--output_test", type=str, default="test_svm.txt", help="The output file where to write the test extracted features")
parser.add_argument("--list_cat_features", nargs='+', default = [], type=int, help="The list of categorical features to extract")
parser.add_argument("--list_num_features", nargs='+', default=[], type=int, help="The list of numerical features to extract")

a = parser.parse_args()



def extract_features(input, max_id, scale_file, output, list_cat_features, list_numerical_features):
    """
    Extract the features contained in input file (csv) and write the extracted features in the output file (SVM format)
    :param input: the csv file containing the features
    :param max_id: the txt file containing the pairs (feature/maxID)
    :param output: the output file where to write the extracted features
    :param list_cat_features: the categorical features to extract
    :param date_feature: the date feature to extract (only 1 date feature for now)
    :param list_cat_features: the numerical features to extract (copy)
    :return:
    """
    data_directory = 'data/'

    # Open raw features file
    fin = open(data_directory+input)
    featname = fin.readline().strip().split(',')

    # Open maxID file
    maxID = {}
    finID = open(data_directory+max_id)

    # For each features, construct the table of the maxID
    for line in finID:
        i, id = line.strip().split('\t')
        maxID[featname[int(i)]] = int(id) + 1

    scale = {}
    scale_file = open(data_directory+scale_file)
    # For each numerical features, construct the table of the mean/scale
    for line in scale_file:
        i, mean, std, maximum = line.strip().split(' ')
        scale[featname[int(i)]] = [float(mean), float(std), float(maximum)]

    # Open output file which will contain extracted features
    fout = open(data_directory+output,'w')

    # Use One Hot Encoding
    i = 0
    for line in fin:
        data = line.strip().split(',')

        # Get the target
        if data[14] == '0':
            click = '-1' # The ad hasn't been clicked
        elif data[14] == '1':
            click = '+1' # The ad has been clicked
        elif data[14] == '':
            click = '0' # No data (test set)

        x = []
        sum_cum = 1
        interval = [sum_cum]

        #Extract date feature into two categorical features and one numerical
        #Extract categorical features
        #In SVM format, index start with 1 while it starts with 0 in python
        for cat_feature in list_cat_features:
            x.append(str(int(data[cat_feature]) + sum_cum))
            sum_cum = sum_cum + maxID[featname[int(cat_feature)]]
            interval.append(sum_cum)

        #Extract numerical features
        x_num = []

        for num_feature in list_numerical_features:
            mean = scale[featname[int(num_feature)]][0]
            std = scale[featname[int(num_feature)]][1]
            maximum = scale[featname[int(num_feature)]][2]

            if data[num_feature] != '':
                scaled_data = (float(data[num_feature])-mean)/std
            else:
                #None values
                if(featname[int(num_feature)] == 'last_login_interval' or
                        featname[int(num_feature)] == 'last_paid_interval'):
                    scaled_data = maximum
                else:
                    scaled_data = 0.0

            x_num.append(str(sum_cum) + ':' + str(scaled_data))
            sum_cum = sum_cum + 1
            interval.append(sum_cum)

        x_svm = [click]
        for index in x:
            x_svm.append(index + ':1')

        extracted_features = x_svm+x_num
        # print(extracted_features)
        fout.write(' '.join(extracted_features) + '\n')

        # i = i+1
        # if i == 5:
        #     break
    for i in range(0,len(interval)-1):
        print("Created feature from %d to %d" % (interval[i], interval[i+1]-1))

    fin.close()
    fout.close()




def main():

    print("Extraction of the training features : ")
    extract_features(a.input_train, a.max_id, a.scale_file, a.output_train, a.list_cat_features, a.list_num_features)
    print("\t Done.")

    print("Extraction of the test features : ")
    extract_features(a.input_test, a.max_id, a.scale_file, a.output_test, a.list_cat_features, a.list_num_features)
    print("\t Done.")

main()


