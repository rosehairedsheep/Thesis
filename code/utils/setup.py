import glob

path_base = "/Users/emma/Documents/thesis/sources/"
# set this to the source folder
codes = ('ADV', 'ATL', 'CLW', 'DUC', 'FUT', 'GRA', 'GUM', 'KOR', 'MLP', 'OWL', 'PPG', 'RAM', 'SHE', 'SPO', 'STU', 'VOL')
# set this to a tuple of all show codes to analyze

def initial_setup(folder, select_codes = codes):
    show_paths = dict()
    # create a dictionary of all file locations of all source files
    for code in select_codes:
        if code in codes:
            locals()["path_{}".format(code)] = "{}{}{}/*".format(path_base, folder, code)
            locals()["files_{}".format(code)] = glob.glob(locals()["path_{}".format(code)])
            # attach all file locations in a code folder to the dictionary under the code key
            show_paths[code] = locals()["files_{}".format(code)]
    return show_paths

def initialize_speakers(select_codes = codes):
# fills a dictionary with all speakers as a tuple of their name and gender, under a key of the show's code
    speakers_dict = dict()
    with open("{}speakers-to-edit.txt".format(path_base), "r", encoding = "UTF-8") as speaker_file:
        content = speaker_file.readlines()
    for code in select_codes:
        if code in codes:
        # initializes a list under every code currently being processed 
            speakers_dict[code] = list()
    for line in content:
        data = line.split("\t")
        # speaker data are saved in a tab-separated format of length three
        try:
            code_speaker = data[0].strip().split("/", maxsplit = 1)
            code = code_speaker[0]
            speaker = code_speaker[1]
            gender = data[2].strip()
            words = int(data[1].split(", ")[2].split("]")[0].strip())
            # extracts the name, code, and gender of every speaker
            if code in codes:
                speakers_dict[code].append((speaker, gender, words))
                # adds the speaker to the dictionary
        except Exception:
            print("Error in line: {}".format(line))
    return speakers_dict