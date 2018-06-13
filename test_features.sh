#!/usr/bin/env bash
#SBATCH --gres=gpu:1
#SBATCH --mem 17000
#SBATCH -c 2
#SBATCH -t 600
#SBATCH -o out_batch
#SBATCH -e err_batch

# A : array, e : element
# Return e if e is in A, "" otherwise
for c in 0.00 0.10 0.20 0.30 0.40 0.50 0.60 0.70 0.80 0.90 1.00 1.10 1.20 1.30 1.40 1.50 1.60 1.70 1.80 1.90 2.00 2.10 2.20 2.30 2.40 2.50 2.60 2.70 2.80 2.90 3.00 3.10 3.20 3.30 3.40 3.50 3.60 3.70 3.80 3.90 4.00 4.10 4.20 4.30 4.40 4.50 4.60 4.70 4.80 4.90 5.00 5.10 5.20 5.30 5.40 5.50 5.60 5.70 5.80 5.90 6.00 6.10 6.20 6.30 6.40 6.50 6.60 6.70 6.80 6.90 7.00 7.10 7.20 7.30 7.40 7.50 7.60 7.70 7.80 7.90 8.00 8.10 8.20 8.30 8.40 8.50 8.60 8.70 8.80 8.90 9.00 9.10 9.20 9.30 9.40 9.50 9.60 9.70 9.80 9.90; do
    echo $c
    cmd="liblinear/train -s 6 -c $c -v 5 data/train_svm.txt"
    results=$(eval $cmd)
    score=$(echo "$results"| tr '\n' ' ' | sed "s/ //g" | awk -F"Validation=" '{print $2}')
    echo $score
    echo "model_${score}" > "$score.txt"
done;