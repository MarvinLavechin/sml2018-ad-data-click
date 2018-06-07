
fin = open('sample-submission-liblinear')
fin.readline()

fout = open('sample-submission.dat','w')

for line in fin:
    data = line.strip().split(' ')
    fout.write(data[1] + '\n')

fin.close()
fout.close()
