## This script turns COWSL2H csv data into CoNLL-U format using SpaCy
import os
import pandas as pd
import spacy

exceptions = ['FIRST_NAME', 'LAST_NAME', 'CITY', 'STATE', 'UNIVERSITY', 'AGE', 'NUMBER', 'PLACE', 'BIRTH_DATE', 'EMAIL', 'ADDRESS']

def parse_and_save_essays(csv_path, lang_model="es_core_news_sm"):
    # Load the SpaCy Spanish model
    nlp = spacy.load(lang_model)
    
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Extract topic from the filename
    filename = os.path.basename(csv_path)[ : -4] # remove .csv
    topic = filename.split(".")[0]
    quarter = filename.split('.')[1]
    
    for _, row in df.iterrows():
        essay_id = row['id']
    #    course = row['course']
        course = row['course'] if pd.notna(row['course']) else "Unknown_Course"
        # remove space in course
        # for some course annotations, the space is not consistent, e.g., SPA 22 vs. SPA22
        course = course.replace(' ', '')
        essay_text = row['essay']

        # e.g., *FIRST_NAME* --> FIRST_NAME
        new_essay_text = []
        essay_text = essay_text.split()
        for i in range(len(essay_text)):
            w = essay_text[i]
            if w.count('*') == 2: #e.g., *CITY*,
                while '*' in w:
                    w = w.replace('*', '')
            new_essay_text.append(w)
        new_essay_text = ' '.join(w for w in new_essay_text)
        
        # Some course information is NA
        if course != "Unknown_Course":
            # Create course directory
            course_dir = os.path.join(base_output_dir, course)
            os.makedirs(course_dir, exist_ok=True)
        
            # Create topic directory inside course directory
            topic_dir = os.path.join(course_dir, topic)
            os.makedirs(topic_dir, exist_ok=True)
        
            # Process the essay
            doc = nlp(new_essay_text)
        
            # Create the output file path
            output_file = os.path.join(topic_dir, f"{filename}_{essay_id}_{course}.conllu")
        
            with open(output_file, "w", encoding="utf-8") as f:
                # Write metadata as comments
                for col in df.columns:
                    if col != "essay":
                      f.write(f"# {col} = {row[col]}\n")
                f.write("# text = " + ' '.join(w for w in essay_text) + "\n")
                f.write("# global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC\n")
            
                # Write tokenized text in CoNLL-U format
                for sent in doc.sents:
                    for i, token in enumerate(sent, start=1):
                        head_idx = token.head.i - sent.start + 1 if token.head != token else 0
                        tok = token.text
                        if tok in exceptions:
                    #        print(tok)
                            tok = '*' + tok + '*'
                     #       print(tok)
                        f.write(f"{i}\t{tok}\t{token.lemma_}\t{token.pos_}\t_\t_\t{head_idx}\t{token.dep_}\t_\t_\n")
                    f.write("\n")  # Separate sentences with a blank line

if __name__ == "__main__":

    # Ensure output directories exist
    base_output_dir = "parsed_essays"
    os.makedirs(base_output_dir, exist_ok=True)

    csv_path = "cowsl2h/csv/"  # Change this to your actual CSV file path
    for file in os.listdir(csv_path):
        print(file)
        parse_and_save_essays(csv_path + file)
