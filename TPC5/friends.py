"""

NAME
   myscript - calculate friend's list

SYNOPSIS
   friends [options] inputFile
   options:
        -f [3] : shows top [3] friends for every character
        -o dump.json : makes dump.json the output file (default to STDOUT) 
        -c Harry : Shows Harry's friend list
        
DESCRIPTION
    Tool that displays associations between caracters in a text,
    we call this a list of friends, sorted by importance.

"""

import spacy
import sys
from jjcli import * # type: ignore
import json
from spacy.language import Language
from spacy.symbols import ORTH


def extract_chapters(markdown_text):
    chapters = {}
    lines = markdown_text.split('\n')
    current_chapter_number = None
    current_chapter_text = ''
    actualText = ""

    # Discard preface
    for i,line in enumerate(lines):
        if line.startswith('# '):
            actualText = lines[i:]
            break

    
    # Actual Text
    for line in actualText:
        if line.startswith('# '):

            if current_chapter_number is not None:
                chapters[current_chapter_number] = current_chapter_text.strip()
                current_chapter_text = ''
            current_chapter_number = line.replace("# ","")
        else:
            current_chapter_text += line

    # Add the last chapter
    if current_chapter_number is not None:
        chapters[str(current_chapter_number)] = current_chapter_text.strip()

    return '\n'.join(chapters.values())


@Language.component("set_custom_boundaries")
def set_custom_boundaries(doc):

    for token in doc[:-1]:
        if token.text == "——":
            doc[token.i + 1].is_sent_start = True
        if token.text == "—":
            doc[token.i + 1].is_sent_start = True
    return doc


def process(text):

    dicFriends = {}

    for sentence in text.sents:
        for token in sentence:
            if not token.is_space:
                if token.pos_ == "PROPN":
                    str_key = token.text.lower().capitalize()

                    if str_key not in dicFriends:
                        dicFriends[str_key] = {}
                    
                    for tokenIn in sentence:
                        friend = tokenIn.text.lower().capitalize()
                        if friend != str_key:
                            if tokenIn.pos_ == "PROPN":
                                if friend in dicFriends[str_key]:
                                    dicFriends[str_key][friend] += 1
                                else:
                                    dicFriends[str_key][friend] = 1

    sortedDicFriends = {}
    for character in dicFriends:
        list = dicFriends[character].items()
        sortedList = sorted(list, key=lambda x: x[1],reverse=True)
        sortedDicFriends[character] = sortedList

    return sortedDicFriends

def main():

    cl = clfilter("f:o:c:", doc=__doc__)

    
    for text in cl.text():

        nlp = spacy.load("pt_core_news_lg")
        nlp.add_pipe("set_custom_boundaries", before="parser")

        doc = nlp(text)

        friendOs = process(doc)

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
        else:
            jsonStr = json.dumps(friendOs,indent=4,ensure_ascii=False)
            print(jsonStr)


if __name__ == "__main__":
    main()
