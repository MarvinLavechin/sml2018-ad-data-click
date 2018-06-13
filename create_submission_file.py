
fin = open('submission/sample-submission-liblinear')
fin.readline()

fout = open('submission/sample-submission.dat','w')

for line in fin:
    data = line.strip().split(' ')
    fout.write(data[1] + '\n')

fin.close()
fout.close()
