import sys
from pathlib import Path
import re
import json


def readEnvFile(envFile="./sortAbbreviation.env") -> dict:
    with open(envFile, 'r') as f:
        return dict(tuple(line.replace('\n', '').split('=')) for line
                    in f.readlines() if not line.startswith('#'))


def getPrice(symbol,
             shortForm,
             longForm):

    sys.stdout.write("Neue Abkürzung wird hinzugefügt:")
    sys.stdout.write("\nKürzel: " + symbol)
    sys.stdout.write("\nKurzform: " + shortForm)
    sys.stdout.write("\nLangform: " + longForm)

    # Read env file
    envVariables = readEnvFile()
    abbreviationPath = envVariables.get('PATH')
    abbreviationPathComplete = Path(Path.cwd(), abbreviationPath)

    # Read abbreviations
    
    with open(abbreviationPathComplete, 'r', encoding="utf-8") as file:
        data = file.read().rstrip()
    #print(data)


    pattern = re.compile(r"\\acro\{(.+)\}\[(.+)\]\{(.+)\}")
    regex_result = re.findall(pattern, data)
    output = {}
    indexCounter = 0
    for index, (symbolAbbre, shortformAbbre, longformAbbre) in enumerate(regex_result, start=1):
        output[f'abbreviation_{symbolAbbre}'] = \
            dict(symbol=symbolAbbre, shortform=shortformAbbre, longform=longformAbbre, length=len(shortformAbbre))
        #indexCounter = index

    # Add new abbreviation
    output[f'abbreviation_{symbol}'] = \
            dict(symbol=symbol, shortform=shortForm, longform=longForm, length=len(shortForm))
    sorted_output = dict(sorted(output.items(), key=lambda x: x[1]['shortform'].lower()))

    #print(sorted_output)

    with open('output.json', 'w') as output_file:
        json.dump(sorted_output, output_file, indent=4)


    max_word = max(sorted_output, key=lambda x: sorted_output[x]['length'])

    replace = True
    longestWord = True
    with open(abbreviationPathComplete, 'w', encoding="utf-8") as file:
        for line in data.split('\n'):
            if(line.startswith(r'\begin{acronym}')):
                if(longestWord):
                        line = line.replace(line, r'\begin{acronym}['+sorted_output[max_word]["shortform"]+']\itemsep0pt')
                        longestWord = False
            if (line.strip().startswith(r'\acro{')):
                if replace:
                    for key in sorted_output:
                        file.write('\t')
                        file.write(r'\acro{'+sorted_output[key]["symbol"]+'}['+sorted_output[key]["shortform"]+']{'+sorted_output[key]["longform"]+'}\n')
                replace = False
            else:
                file.write(line.replace("\b", "\\b").replace("\a", "\\a")+'\n')
if __name__ == "__main__":
    getPrice(str(sys.argv[1]),
             str(sys.argv[2]),
             str(sys.argv[3]))