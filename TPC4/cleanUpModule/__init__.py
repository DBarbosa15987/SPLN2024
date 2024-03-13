import sys
import json

strTeste= "TLDR: o q esta errado aki ns..."

def get_dictionary(fileList):
    tempdic = {}
    for location in fileList:
        try:
            with open(location, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    parts = line[:-1].split(':')
                    k, v = parts[0], parts[1]
                    if k not in tempdic:
                        tempdic[k] = [v]
                    else:
                        if v not in tempdic[k]:
                            tempdic[k].append(v)
        except FileNotFoundError:
            print(f"File not found at location: {location}")
    return tempdic

def main(strTeste):
    dicEN = {}
    dicPT = {}

    lst_PT = ["abreviações/formal/volp-acp.txt", "abreviações/formal/waze.txt",
                "abreviações/informal/caminhoslanguages_brazilian-internet-slang-abbreviations.txt",
                "abreviações/informal/dnacriativo.txt", "abreviações/informal/explícito.txt",
                "abreviações/informal/globo.txt", "abreviações/informal/iscte.txt"]
    
    lst_EN = ["abreviações/inglesas/english_acronyms-.txt", "abreviações/inglesas/explícito.txt",
                "abreviações/inglesas/slicktext_text-abbreviations-guide.txt"]

    dicPT = get_dictionary(lst_PT)
    dicEN = get_dictionary(lst_EN)

    dicGeral = dicPT.copy()
    dicGeral.update(dicEN)
    
    dicPT_json = open("dicPT.json","w")
    dicPT_json.write(json.dumps(dicPT,indent=4,ensure_ascii=False))
    dicPT_json.close()

    dicEN_json = open("dicEN.json","w")
    dicEN_json.write(json.dumps(dicEN,indent=4,ensure_ascii=False))
    dicEN_json.close()

    dicGeral_json = open("dicGeral.json","w")
    dicGeral_json.write(json.dumps(dicGeral,indent=4,ensure_ascii=False))
    dicGeral_json.close()

if __name__ == '__main__':
    main(strTeste)