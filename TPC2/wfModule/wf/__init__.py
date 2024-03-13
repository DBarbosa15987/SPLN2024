#!/usr/bin/env python
'''
NAME
   myscript - calculate a frequenc of a word in a document

SYNOPSIS
   word_frequency [options] input_file
   options:
        -m 20 : shows 20 more common, alfabetically
        -n : Order alfabetically
        -c : Normalized word_freq
        -s : statistical analysis (n_occur vs expectation) 
        -l : which language to process (default pt)
        
DESCRIPTION
    Module that analysis text and calculates the frequency of occurence of words in it.

'''

__version__ = "0.0.1"


import re
from collections import Counter
from jjcli import * 

languages_dic = {"pt": "resources/pt/cleanPalavrasFreq2.txt"}

def tokenize(text):
    words = re.findall(r'\w+(?:[\-\']\w+)*|[,;./\-\(\)!?""\—]+', text)
    return words


def imprime(lst):
    for e, n_occ in lst:
        print(f"{e}\t{n_occ}")


def normaliza(dic):

    eliminate = []

    for k in dic.keys():
        if k[0] >= 'A' and k[0] <='Z':
            lower = k.lower()
            if lower in dic:
                dic[lower] = dic[lower] + dic[k]
                eliminate.append(k)

    for e in eliminate:
        dic.pop(e)


    return dic



def calcExpectedFreq(location ,min_occur=3):
    f = open(location)
    lst_clean = f.readlines()
    f.close()

    dic = {}
    totalWords = 0
    for line in lst_clean:
        l = line[:-1].split('\t')
        n = int(l[0])
        if(n<=min_occur):
            break
        dic[l[1]] = [n,0]
        totalWords += n

    for key,value in dic.items():
        percent = value[0]/totalWords * 1_000_000
        value[1] = percent

    return dic

def calcRealFreq(freqDic,frequency,min_occur=3):

    totalRealWords = 0
    for word,n_occur in frequency.items():
        totalRealWords += n_occur

    
    frequencyList = []

    for word,n_occur in frequency.items():
        if(n_occur > min_occur):
            if(word in freqDic):
                percentReal = round(n_occur/totalRealWords * 1_000_000,4)
                percentFreq = round(freqDic[word][1],4)
                ratio = percentReal/percentFreq
                frequencyList.append((word,n_occur,percentFreq,percentReal,ratio))

    frequencyList.sort(key=lambda x: x[1], reverse=True )
    return frequencyList


def writeToFile(l):

    f = open("resources/output.txt",'w')
    f.write("Palavara | Número de ocorrências | (Ocorrências no input,Ocorrências reais) | Rácio")

    s = ""

    for word, n_occur,  pf , pr, r in l:
        
        s += f"{word} | {n_occur} | {pf} | {pr} | {r}\n"

    f.write(s)
    f.close()


def main():
    
    cl=clfilter("nm:csl:", doc=__doc__)
    

    for txt in cl.text():

        toPrint = []
        prep_t = tokenize(txt)
        frequency = Counter(prep_t)
        location = languages_dic["pt"]

        if "-l" in cl.opt:

            lang = str(cl.opt.get("-l"))
            location = languages_dic[lang]


        if "-m" in cl.opt:

            toPrint = frequency.most_common(int(cl.opt.get("-m")) )  # type: ignore

        if "-n" in cl.opt:

            list(frequency).sort(key=lambda x:x[0] )
            toPrint = frequency.items()

        if "-c" in cl.opt:

            normalizedFreq = normaliza(frequency)
            toPrint = normalizedFreq.items()

        if "-s" in cl.opt:

            freqDic = calcExpectedFreq(location)
            freqList = calcRealFreq(freqDic,frequency)
            writeToFile(freqList)
            toPrint = [(x[0],x[-1]) for x in freqList]


        imprime(toPrint)
        
    
if __name__ == "__main__":
    main()

