1. Download liblinear (https://www.csie.ntu.edu.tw/~cjlin/liblinear/)
2. cd liblinear
3. make
4. python feature_extract.py (Python 3)
5. Train model: liblinear/train -s 6 -w-1 0.1 -e 0.01 data/train_svm.txt models/model
6. Test model : liblinear/predict -b 1 data/test_svm.txt models/model submission/sample-submission-liblinear
7. Create submission file: python create_submission_file.py
