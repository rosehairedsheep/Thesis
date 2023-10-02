import glob
import pandas as pd
import re

if __name__ == "__main__":
    path = '/Users/emma/Documents/University/Linguistic Corpus Annotation/Project/Subtitles/HTML/*'
    files = glob.glob(path)

    dict = {}

    for name in files:
        print(name)

        with open(name, encoding = "UTF-8") as f:
        # opens the source file

            dfcol = pd.read_html(f)
            result = str()
            for df in dfcol:
                df = df.dropna()
                listoflists = df.values.tolist()
                for line in listoflists:
                    if len(line[0]) <= 30:
                        line[1] = re.sub(r'\[[^\]]*\]', "", line[1])
                        if line[0] not in dict.keys():
                            dict[line[0]] = 0
                        dict[line[0]] += len(line[1].strip().split(" "))
                    else:
                        listoflists.remove(line)
                df = pd.DataFrame(listoflists)
                result += df.to_csv(header = False, index = False, sep ='\t')
            name = name[:len(name) - 5]
            nameList = name.split("HTML/")
            newName = nameList[0] + nameList[1] + ".txt"
            with open(newName, 'a', encoding = "UTF-8") as f2:
                f2.write(result)
    print(dict)
            