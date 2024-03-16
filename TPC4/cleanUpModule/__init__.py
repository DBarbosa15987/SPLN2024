'''TODO'''


import sys
import json
from jjcli import *  # type: ignore
import re


lst_dics = {"e_en":"abreviações/e_en.txt", "e_pt":"abreviações/e_pt.txt", "f_pt":"abreviações/f_pt.txt",
                "i_en":"abreviações/i_en.txt", "i_pt":"abreviações/i_pt.txt" }


def tokenize(text):
    words = re.findall(r'(?:\w+(?:[\-\']\w+)*\.?)+|[,;:/\-\(\)!?""\—]+', text)
    return words

def get_dictionary(fileList):
    tempdic = {}
    for location in fileList:
        try:
            with open(location, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    parts = line[:-1].split(':')
                    k, v = parts[0].lower(), parts[1]
                    
                    if k not in tempdic:
                        tempdic[k] = [v]
                    else:
                        if v not in tempdic[k]:
                            tempdic[k].append(v)
                    
                    if "." in k:
                        altered = k.replace(".", "")
                        if altered not in tempdic:
                            tempdic[altered] = [v]
                        else:
                            if v not in tempdic[altered]:
                                tempdic[altered].append(v)
        except FileNotFoundError:
            print(f"File not found at location: {location}")
    return tempdic


def processText(word_list, dic):
    clean_list = []
    consonantsRegex = re.compile(r"[bcdfghjklmnpqrstvwxyzçBCDFGHJKLMNPQRSTVWXYZÇ]+")
    for word in word_list:
        lower = word.lower()
        if lower in dic:
            replacements = "[" + " | ".join(dic[lower]) + "]"
            clean_list.append(replacements)
        elif lower.endswith("."):
            clean_word, punctuation = lower[:-1], lower[-1]
            if clean_word in dic:
                replacements = "[" + " | ".join(dic[clean_word]) + "]"
                clean_list.append(replacements)
                clean_list.append(punctuation)
            elif bool(consonantsRegex.fullmatch(clean_word)):
                clean_list.append(f"{{{clean_word}}}")
                clean_list.append(punctuation)
            else:
                clean_list.append(word)
        elif bool(consonantsRegex.fullmatch(lower)):
            #abbreviation catcher
            clean_list.append(f"{{{word}}}")
            
        else:
            clean_list.append(word)

    cleaned_text = " ".join(clean_list)
    return cleaned_text



def main():

    comparisonDic = {}
    dicLocations = {lst_dics["i_en"],lst_dics["i_pt"],lst_dics["f_pt"]}
    toFile = False
    
    cl = clfilter(opt="l:efio",doc=__doc__)

    for txt in cl.text():

        comparisonDic = set()
        wordList = tokenize(txt)

        if "-e" in cl.opt:
            dicLocations.add(lst_dics["e_en"])
            dicLocations.add(lst_dics["e_pt"])
            
        
        if "-f" in cl.opt:
            dicLocations.discard(lst_dics["i_en"])
            dicLocations.discard(lst_dics["i_pt"])
            
        
        if "-i" in cl.opt:       
            dicLocations.discard(lst_dics["f_pt"])
            

        if "-o" in cl.opt:
            toFile = True

        if "-l" in cl.opt:
            lang = str(cl.opt.get("-l"))
            if lang == "pt":
                dicLocations.discard(lst_dics["i_en"])
                dicLocations.discard(lst_dics["e_en"])
            elif lang == "en":
                dicLocations.discard(lst_dics["i_pt"])
                dicLocations.discard(lst_dics["f_pt"])
                dicLocations.discard(lst_dics["e_pt"])

    comparisonDic = get_dictionary(dicLocations)
    cleanString = processText(wordList, comparisonDic)
    
    if toFile:
        dic_json = open("cleanText.txt","w")
        dic_json.write(cleanString)
        dic_json.close()
    else:
        print(f"This is your clean text: \n {cleanString}")


if __name__ == '__main__':
    main()