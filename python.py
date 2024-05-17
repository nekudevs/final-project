import spacy
nlp = spacy.load("en_core_web_sm")
with open ("freecodecamp_spacy/data/wiki_us.txt", "r") as f:
    text = f.read()

doc = nlp(text)

# for sent in doc.sents:
#     print(sent)

sentence1 = list(doc.sents)[0]
print(sentence1)