import spacy
import sys
import re

nlp = spacy.load("pt_core_news_lg")

f = open(sys.argv[1],'r')
text = f.read()
f.close()


tokens = nlp(text)
data = "Palavra,POS_,lemma_\n"
setPalavras = set()
for token in tokens:
    if token.pos_ not in ["PUNCT","SPACE"] and token.text != "\n":
        if token.text not in setPalavras:     
            setPalavras.add(token.text)
            data += f"{token.text},{token.pos_},{token.lemma_}\n"
    
f = open("spacyOutput.csv",'w')
f.write(data)
f.close()

