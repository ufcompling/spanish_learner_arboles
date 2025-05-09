# All the annotations to be subjected to the random split are in annotated_essays
# TODO: rename annotated_essays to e.g., random_annotated_essays
# Combine all randomly selected essays that have been annotated to one *.conllu file, named "random_trees.conllu", to be consistent with machamp_low_conf_trees.conllu'
# Gather descriptive statistics of random_trees.conllu
# Randomly split random_trees.conllu to random_trees_train.conllu and random_trees_test.conllu, trying to balance the number of tokens (or sentences) per level, per topic
# random_trees_test.conllu will also be the test set for machamp_low_conf_trees.conllu

import io, os, sys, random
import statistics

random.seed(8)

pos_tag_list = [
    "ADJ",
    "ADP",
    "ADV",
    "AUX",
    "CCONJ",
    "DET",
    "INTJ",
    "NOUN",
    "NUM",
    "PART",
    "PRON",
    "PROPN",
    "PUNCT",
    "SCONJ",
    "SYM",
    "VERB",
    "X",
]

## Checking if any *.conllu files have weird formatting
for essay in os.listdir('parsed_essays/annotated_essays/first_round/'):
	with open('parsed_essays/annotated_essays/first_round/' + essay, 'r', encoding = 'utf-8') as f:
		for line in f:
			if line.startswith('#') is False:
				toks = line.strip().split("\t")
				if toks != ['']:
					if len(toks) != 10:   # not 10 columns
						print(toks, essay)
						print('\n')
					if toks[2] in pos_tag_list:
						print(toks, essay)


# Read CoNLL-U format
def conll_read_sentence(file_handle):
	sent = []
	for line in file_handle:
		line = line.strip('\n')
		if not line.startswith('#'):
			toks = line.split("\t")
		#	if len(toks) == 10 and '-' not in toks[0] and '.' not in toks[0]:
			if len(toks) == 10 and '.' not in toks[0]:
				if toks[0] == 'q1':
					toks[0] = '1'
				if toks[7] == 'ROOT':
					toks[7] = 'root'
				sent.append(toks)
			elif sent:
				for w in sent:
					if '-' in w[0]:
						sent.remove(w)
				yield sent
				sent = []
	if sent:
		yield sent  # Ensure the last sentence is returned


# Collect annotated sentences from a given *.conllu file
def essay_trees(file_handle):
	trees = []
	with open(file_handle) as f:
		trees = list(conll_read_sentence(f))

	return trees

# Gather descriptive statistics of random_trees.conllu
total_essays = 0
total_num_tokens = 0
total_num_sentences = 0

topic_list = []
level_list = []
topic_level_dict = {}

# Combine all randomly selected essays that have been annotated to one *.conllu file, named "random_trees.conllu"
random_annotated_essays_dir = sys.argv[1] 
random_annotated_essays = []
for essay in os.listdir(random_annotated_essays_dir):
	if essay.endswith('.conllu'):
		total_essays += 1 # count the total number of annotated essays 

		essay_name = essay.split('.') # e.g., beautiful.F20_201766_SPA116.conllu
		topic = essay_name[0]
		level = essay_name[1].split('_')[-1]
		topic_list.append(topic)
		level_list.append(level)
	
		trees = essay_trees(random_annotated_essays_dir + essay)
		updated_trees = [] # to store doc_id and sent_id along with the trees

		doc_id = essay[ : -7]
		sent_id = 0

		num_sentences = len(trees) # count the total number of sentences
		num_tokens = 0
		for tree in trees:
			num_tokens += len(tree) # count the total number of tokens
			random_annotated_essays.append('# doc_id = ' + doc_id)
			random_annotated_essays.append('# sent_id = ' + str(sent_id))

			info = ['# doc_id = ' + doc_id, '# sent_id = ' + str(sent_id)]

			for tok in tree:
				random_annotated_essays.append('\t'.join(w for w in tok))
				info.append('\t'.join(w for w in tok))
			
			random_annotated_essays.append('\n')
			info.append('\n')

			updated_trees.append(info) # a list of sublists, each sublist contains the doc_id, sent_id, and the tree

			sent_id += 1

		print(essay, num_sentences, num_tokens)

		total_num_tokens += num_tokens
		total_num_sentences += num_sentences

		topic_level = topic + '_' + level
		if topic_level not in topic_level_dict:
			topic_level_dict[topic_level] = {'num_tokens': num_tokens, 'num_sentences': num_sentences, 'trees_list': updated_trees}
		else:
			topic_level_dict[topic_level]['num_tokens'] += num_tokens
			topic_level_dict[topic_level]['num_sentences'] += num_sentences
			topic_level_dict[topic_level]['trees_list'] += updated_trees ## TODO: Remember to test this as more files of the same topic + level are annotated
			
print('Total number of annotated essays:', total_essays)
print('Total number of tokens:', total_num_tokens)
print('Total number of sentences:', total_num_sentences)
print('Total number of topics', len(set(topic_list))) # 8
print('Total number of levels', len(set(level_list))) # 21
print('\n')

# Outputing randomly selected sentences to random_trees.conllu
c = 0
with open('random_trees.conllu', 'w') as f:
	for tree in random_annotated_essays:
		f.write(tree + '\n')

print('\n')

# Read CoNLL-U format of machamp_low_conf_trees.conllu; it has 11 columns
def low_conf_read_sentence(file_handle):
	sent = []

	for line in file_handle:
		line = line.strip('\n')
		if line.startswith('#') is False:
			toks = line.split("\t")
			if len(toks) == 11 and '-' not in toks[0] and '.' not in toks[0]:
				sent.append(toks)
			else:
				return sent

	return None

# Collect annotated sentences from machamp_low_conf_trees.conllu
def low_conf_essay_trees(file_handle):
    trees = []
    with open(file_handle) as f:
        sent = low_conf_read_sentence(f)
        while sent is not None:
            trees.append(sent)
            sent = low_conf_read_sentence(f)
    
    return trees

# Calculate descriptive statistics for machamp_low_conf_trees.conllu
low_conf_tokens = 0
low_conf_sentences = 0
low_conf_trees = low_conf_essay_trees('machamp_low_conf_trees.conllu')
for tree in low_conf_trees:
	low_conf_tokens += len(tree)
	low_conf_sentences += 1

print('Total number of tokens in machamp_low_conf_trees.conllu:', low_conf_tokens)
print('Total number of sentences in machamp_low_conf_trees.conllu:', low_conf_sentences)

# Note: not each level has the same set of topics
print('Total number of topic + level combinations:', len(topic_level_dict))
print('\n')

## Randomly sample a proportion of sentences from each topic + level combination to be in the test set
train_test_ratio = float(sys.argv[2])

train_trees = []
num_train_trees = 0
num_train_toks = 0

test_trees = []
num_test_trees = 0
num_test_toks = 0

inter_annotator_trees = []
num_inter_annotator_trees = 0
num_inter_annotator_toks = 0

for k, v in topic_level_dict.items():
	trees_list = v['trees_list']
	random.shuffle(trees_list)
	cutt_off = int(len(trees_list) * train_test_ratio)

	for i in range(cutt_off):
		train_trees.append(trees_list[i])
		num_train_trees += 1
		num_train_toks += len(trees_list[i])
	for i in range(cutt_off, len(trees_list)):
		test_trees.append(trees_list[i])
		num_test_trees += 1
		num_test_toks += len(trees_list[i])
#	for i in range(int(len(trees_list) * 0.1) + 1):
#		inter_annotator_trees.append(trees_list[i])
#		num_inter_annotator_trees += 1
#		num_inter_annotator_toks += len(trees_list[i])

print('Number of trees in the training set: ', num_train_trees)
print('Number of tokens in the training set: ', num_train_toks)
print('\n')
print('Number of trees in the test set: ', num_test_trees)
print('Number of tokens in the test set: ', num_test_toks)
#print('\n')
#print('Number of trees in the inter annotator set: ', num_inter_annotator_trees)
#print('Number of tokens in the inter annotator set: ', num_inter_annotator_toks)


# Outputing random_trees_train.conllu and random_trees_test.conllu
with open('random_trees_train.conllu', 'w') as f:
	for tree in train_trees:
		for tok in tree:
			f.write(tok + '\n')

with open('random_trees_test.conllu', 'w') as f:
	for tree in test_trees:
		for tok in tree:
			f.write(tok + '\n')

#with open('random_trees_inter_annotator.conllu', 'w') as f:
#	for tree in inter_annotator_trees:
#		for tok in tree:
#			f.write(tok + '\n')

### Checking for validation errors

new_sents = []

with open("random_trees_train.conllu") as f:
    train_sents = f.read().split("\n\n")

for sent in train_sents:
    new_lines = []
    for line in sent.split("\n"):
        if line.startswith("# doc_id"):
            doc_id = line.split(" = ")[1]
            new_lines.append(line)
        elif line.startswith("# sent_id"):
            line = line.replace(" = ", f" = {doc_id}:")
            new_lines.append(line)
            new_lines.append("# split = test")
        else:
            new_lines.append(line)
    new_sents.append("\n".join(new_lines))

with open("random_trees_test.conllu") as f:
    test_sents = f.read().split("\n\n")

for sent in test_sents:
    new_lines = []
    for line in sent.split("\n"):
        if line.startswith("# doc_id"):
            doc_id = line.split(" = ")[1]
            new_lines.append(line)
        elif line.startswith("# sent_id"):
            line = line.replace(" = ", f" = {doc_id}:")
            new_lines.append(line)
            new_lines.append("# split = test")
        else:
            new_lines.append(line)
    new_sents.append("\n".join(new_lines))

with open('all_random_sents_new_sentid.conllu', 'w') as f:
	for tok in new_sents:
		f.write(tok + '\n')

'''
def conll_read_sentence(file_handle):
	sent = []

	for line in file_handle:
		line = line.strip('\n')
		if line.startswith('#') is False:
			if essay.startswith('yourself.W21_204788_SPA22V'):
				print(line.split("\t"))
			toks = line.split("\t")
		#	if essay.startswith('yourself.W21_204788_SPA22V'):
		#		print(toks)
		#	if len(toks) != 10 and sent not in [[], ['']] and list(set([tok[1] for tok in sent])) != ['_']:
		#		return sent 
			if len(toks) == 10 and '-' not in toks[0] and '.' not in toks[0]:
				if toks[0] == 'q1':
					toks[0] = '1'
			#	print(toks)
				if toks[7] == 'ROOT':
					toks[7] = 'root'
				sent.append(toks)
		#	if len(toks) != 10 and sent != []:
			else:
		#		if essay.startswith('yourself.W21_204788_SPA22V'):
		#			print(sent)
				return sent

	return None
'''