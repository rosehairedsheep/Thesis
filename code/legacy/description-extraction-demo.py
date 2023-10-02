import glob
import pandas as pd
import re

if __name__ == "__main__":
    path_base = "/Users/emma/Documents/University/Linguistic Corpus Annotation/Project/LCA-miniproject/"
    # set this to the project folder
    path_korra = path_base + "html_source/korra/*"
    path_atla = path_base + "html_source/atla/*"
    files_korra = glob.glob(path_korra)
    files_atla = glob.glob(path_atla)
    # where the HTML source files are, makes a list of every file path in those folders
    show_paths = dict()
    show_paths["korra"] = files_korra
    show_paths["atla"] = files_atla
    # dictionary of all lists of path files attached to the show names
    speakers = dict()
    speakers_path = path_base + "scenes/speakers.txt"
    # dictionary for all speaker names

    for show_name in show_paths:
        result = ""
        filenumber = 0
        indexes = ""
        path_base_show = path_base + "scenes/" + show_name + "/"
        index_path = path_base_show + "index.txt"
        # sets up the paths and values for each show
        for name in show_paths[show_name]:
            print(name)
            with open(name, encoding = "UTF-8") as f:
            # opens each file from the selected show one by one
                dfcol = pd.read_html(f)
                for df in dfcol:
                    listoflists = df.values.tolist()
                    for line in listoflists:
                        if str(line[0]).strip() == "nan":
                            if (re.match(r'(.*)?([Ss]cene)|([Cc]amera)|([Cc]ut(s)? (back )?to)(.*)?', line[1])):
                            # if a line is a description and a scene change, write a file and reset values
                                if (result != ""):
                                    newName = path_base_show + "scene" + str(filenumber) + ".txt"
                                    indexes += "scene" + str(filenumber) + ".txt\n"
                                    with open(newName, 'w', encoding = "UTF-8") as f2:
                                        f2.write(result)
                                    result = ""
                                    filenumber += 1
                        else:
                            if len(line[0]) <= 30:
                            # if a line is spoken by a speaker, remove actions and add token count to speakers
                                line[1] = re.sub(r'\[[^\]]*\]', "", line[1])
                                if line[0].strip() not in speakers.keys():
                                    speakers[line[0].strip()] = 0
                                speakers[line[0].strip()] += len(line[1].strip().split(" "))
                            else:
                            # get rid of bad lines
                                listoflists.remove(line)
                            if len(line) == 2:
                            # add line to be written to file in the future
                                result += line[0] + " says: \"" + line[1].strip() + "\"\n"
        
        with open(index_path, 'w', encoding = "UTF-8") as f3:
        # writes all scene file names to one file for each show
            f3.write(indexes)
    
    with open(speakers_path, 'w', encoding = "UTF-8") as f4:
    # writes all speakers from all shows and the number of tokens they spoke
        for key in speakers.keys():
            f4.write(key + ": " + str(speakers[key]) + ", \n")