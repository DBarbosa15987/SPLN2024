"""

NAME
   myscript - calculate friend's list

SYNOPSIS
   friends [options] inputFile
   options:
        -f [3] : shows top [3] friends for every character
        -o dump.json : makes dump.json the output file (defalt to STDOUT) 
        -c Harry : Shows Harry's friend list
        
DESCRIPTION
    Tool that displays associations between caracters in a text,
    we call this a list of friends, sorted by importance.

"""

from curses.ascii import isspace
import spacy
import sys
from jjcli import * 
from spacy import displacy
import json


def process(text):

    nlp = spacy.load("pt_core_news_lg")

    # f = open(sys.argv[-1],'r')
    # text = f.read()
    # f.close()
    doc = nlp(text)

    with doc.retokenize() as retokenizer:
        for entity in doc.ents:
            retokenizer.merge(entity)

    dicFriends = {}

    #data = "Palavra\tPOS_\tlemma_\tDEP\n"
    for sentence in doc.sents:
        for token in sentence:
            if not token.is_space:
                if token.pos_ == "PROPN":
                    str_key = token.text

                    if str_key not in dicFriends:
                        dicFriends[str_key] = {}
                    
                    for tokenIn in sentence:
                        friend = tokenIn.text
                        if friend != str_key:
                            if tokenIn.pos_ == "PROPN":
                                if friend in dicFriends[str_key]:
                                    dicFriends[str_key][friend] += 1
                                else:
                                    dicFriends[str_key][friend] = 1
                                    
                # if token.pos_ == "PRON":
                #     data += f"{token.text}\t{token.pos_}\t{token.ent_type}\t{token.dep_}\n"
                # else:
                #     data += f"{token.text}\t{token.pos_}\t{token.lemma_}\t{token.dep_}\n"

    sortedDicFriends = {}
    for character in dicFriends:
        list = dicFriends[character].items()
        sortedList = sorted(list, key=lambda x: x[1],reverse=True)
        sortedDicFriends[character] = sortedList

    return sortedDicFriends

def main():

    cl = clfilter("f:o:c:", doc=__doc__)

    
    for text in cl.text():
        friendOs = process(text)

        if "-c" in cl.opt:
            characterPivot = str(cl.opt.get("-c"))
            if characterPivot in friendOs:   
                friendOs = {characterPivot:friendOs[characterPivot]}
            else:
                raise Exception(f"{characterPivot} does not exist.")
                
        if "-f" in cl.opt:
            n = int(cl.opt.get("-f")) # type: ignore
            for k,v in friendOs.items():
                friendOs[k] = v[:n]
        
        if "-o" in cl.opt:

            outputFile = str(cl.opt.get("-o"))
            with open(outputFile,'w') as f:
                json.dump(friendOs,f,ensure_ascii=False,indent=4)
            #f = open("spacyOutput.csv",'w')
            #f.write(data)
            #f.close()
        else:
            jsonStr = json.dumps(friendOs,indent=4,ensure_ascii=False)
            print(jsonStr)



if __name__ == "__main__":
    main()
