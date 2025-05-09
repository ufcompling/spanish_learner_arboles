## Putting sentences in all_random_sents_new_sentid.conllu back to individual files

import os
from collections import defaultdict
import re

input_path = "/Users/liu.ying/Desktop/all_random_sents_new_sentid.conllu"  # Change if needed
output_dir = "output_conllu_files"  # Folder to save individual files
os.makedirs(output_dir, exist_ok=True)

# Read the input file
with open(input_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Group sentences by doc_id
docs = defaultdict(list)
current_sent = []
doc_id = None
sent_id = None

for line in lines:
    if line.startswith("#"):
        if "doc_id" in line:
            doc_id = line.split("=")[-1].strip()
        if "sent_id" in line:
            sent_id = line.split("=")[-1].strip()
        if 'split = ' not in line:
            current_sent.append(line)
    elif line.strip() == "":
        if doc_id and sent_id:
            docs[doc_id].append(("sent" + sent_id, sent_id.split(':')[-1], current_sent))
        current_sent = []
        doc_id = None
        sent_id = None
    else:
        current_sent.append(line)

# Add any remaining sentence at EOF
if current_sent and doc_id and sent_id:
    docs[doc_id].append(("sent" + sent_id, current_sent))

# Write sorted and renumbered sentences to individual files
for doc, sent_list in docs.items():
    # Sort by numeric value of sent_id
#    sent_list.sort(key=lambda x: float(re.findall(r"\d+", x[1])))
    sent_list.sort(key=lambda x: float(x[1]))
    output_lines = []
#    for i, (_, sent) in enumerate(sent_list, start=0):
    for i, (_, _, sent) in enumerate(sent_list, start=0):
        for line in sent:
            if line.startswith("# sent_id"):
                output_lines.append(f"# sent_id = {i}\n")
            else:
                output_lines.append(line)
        output_lines.append("\n")

    output_path = os.path.join(output_dir, f"{doc}.conllu")
    with open(output_path, "w", encoding="utf-8") as out_f:
        out_f.writelines(output_lines)

print("Done! Files written to:", output_dir)