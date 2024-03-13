import re
import sys

letters = "a-zA-ZáÁéÉíÍóÓúÚàÀèÈìÌòÒùÙãÃõÕâÂêÊüÜçÇ"
regexAccept = fr"[{letters}]+([\-'][{letters}]+)*"

regex = re.compile(regexAccept)

f = open("palavrasFreq.txt",'r')
lines = f.readlines()
f.close()

f = open("cleanPalavrasFreq2.txt",'w')
dump = ""
i=0


for line in lines:
    lineList = line[:-1].split('\t')

    if (regex.fullmatch(lineList[1]) != None ):
        dump += line

    if(i%5000==0):
        print(i)

    i+=1


f.write(dump)
f.close()
