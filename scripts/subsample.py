"""
This script enables subsampling a UD treebank given a desired number of tokens. It is useful
for preparing datasets of different data sizes for the learning curve experiment.

Run it like this

    $ python subsample.py <path/to/original/conllu> <n> <path/to/subsampled/outut/file>

"""
import random
import sys

original_file_path = sys.argv[1]
subsample_n = float(sys.argv[2])
subsampled_file_path = sys.argv[3]

with open(original_file_path) as f:
    sents = f.read().split("\n\n")

random.shuffle(sents)
total_tokens = 0
subsampled_sents = []
for sent in sents:
    subsampled_sents.append(sent)
    num_tokens = len([line for line in sent.split("\n") if line.strip("\n") and not line.startswith("#")])
    total_tokens += num_tokens
    if total_tokens >= subsample_n:
        break

with open(subsampled_file_path, "w") as fout:
    fout.write("\n\n".join(subsampled_sents))

print("Subsampled {} sentences from {}".format(len(subsampled_sents), original_file_path))
print("Subsampled {} tokens from {}".format(total_tokens, original_file_path))
print("Subsampled file saved to {}".format(subsampled_file_path))

