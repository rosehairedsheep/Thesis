import utils.setup as setup
import os
import re

def convert_all(show_paths, path = setup.codes):
    for code in show_paths.keys():
        if code in path:
        # handles all codes as default, can be set to only handle some
            if not os.path.exists(setup.path_base + "coref_source/" + code):
            # checks if a folder exists, otherwise makes one
                os.makedirs(setup.path_base + "coref_source/" + code)
            for episode in show_paths[code]:
            # converts each episode
                convert_single(episode, code)

def convert_single(episode, code):
    with open(episode, encoding = "UTF-8") as epi:
    # converts the HTML format to text
        raw_content = epi.readlines()
    raw_content = wrangle(raw_content, code)
    # wrangles the text
    with open(episode.replace("txt_conversion", "coref_source") + ".txt", "w", encoding = "UTF-8") as output_file:
    # writes down the wrangled text
        output_file.write(raw_content)

def wrangle(content, code):
    final = ""
    for line in content:
        lineparts = line.split(":", maxsplit = 1)
        if (len(lineparts) == 2):
            if (lineparts[1].strip() != ""):
                lineparts[0] = re.sub(r'[\[\(].*[\]\)]', "", lineparts[0])
                lineparts[1] = re.sub(r'[\[\(].*[\]\)]', "", lineparts[1])
                sentences = re.split(r'(\.\.?\.?)|(\?+(!+)?)|(!+)|(—)', lineparts[1])
                adder = False
                first = ""
                speaker_split = re.split(r'( and )|&|,', lineparts[0])
                for sentence in sentences:
                    if not (sentence == None):
                        if not (re.match(r'[(\.\.?\.?)(\?+(!+)?)(!+)—]', sentence.strip())):
                            first = sentence.strip()
                        else:
                            first += sentence.strip()
                            for speaker in speaker_split:
                                if ((speaker) and not (speaker.strip() == "and")):
                                    final += "\n{} says: \"{}\"".format(speaker.strip(), first.strip())
                            first = ""
        else:
            line = re.sub(r'[\[\(]', "", line)
            line = re.sub(r'[\]\)]', "", line.strip())
            if not line.endswith("."):
                if not line.endswith("!"):
                    if not line.endswith("?"):
                        line += "."
            if re.match(r'[A-Z].*', line):
                final += "\n" + line.strip()

    return final.strip()

if __name__ == "__main__":
    show_paths = setup.initial_setup("txt_conversion/")
    convert_all(show_paths)