# Summary
# Open the training set
# Load the maximum index
## In maxID.txt, we have pairs "number of the feature"/"maximum of this feature"
# Save the features in SVM light format
# Note that the original version of feature_extract.py uses only advertiser_id, campaign_id and category_id
# Note also that they dummy_encode the features here !
# Note that we try to compute an accuracy score after extracting the features and training the model.
# But the test set doesn't contain any target values !
# ---> Need to build my own train/test set :')






#Extract features and save as SVM light format
fin = open('data_train.csv')

featname = fin.readline().strip().split(',')

#Load the maximum index
maxID = {}
finID = open('maxID.txt')

for line in finID:
    i,id = line.strip().split('\t')
    maxID[featname[int(i)]] = int(id) + 1

fout = open('train_svm.txt','w')

#Use advertiser_id,campaign_id,category_id
for line in fin:
    data = line.strip().split(',')

    if data[14] == '0':
        click = '-1'
    else:
        click = '+1'
    #In SVM format, index start with 1 while it starts with 0 in python
    x = []
    x.append(str(int(data[1]) + 1))
    x.append(str(int(data[2]) + 1 + maxID[featname[1]]))
    x.append(str(int(data[3]) + 1 + maxID[featname[1]] + maxID[featname[2]]))

    x_svm = [click]
    for index in x:
        x_svm.append(index + ':1')

    fout.write(' '.join(x_svm) + '\n')


fin.close()
fout.close()

#Extract features and save as SVM light format
fin = open('data_test.csv')
fin.readline()

fout = open('test_svm.txt','w')

for line in fin:
    data = line.strip().split(',')

    #In SVM format, index start with 1 while it starts with 0 in python
    x = []
    x.append(str(int(data[1]) + 1))
    x.append(str(int(data[2]) + 1 + maxID[featname[1]]))
    x.append(str(int(data[3]) + 1 + maxID[featname[1]] + maxID[featname[2]]))

    x_svm = ['0']
    for index in x:
        x_svm.append(index + ':1')

    fout.write(' '.join(x_svm) + '\n')


fin.close()
fout.close()


