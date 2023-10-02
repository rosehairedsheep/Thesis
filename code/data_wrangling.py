import utils.setup as setup
from bs4 import BeautifulSoup as bs
import os
import re

def convert_all(show_paths, path = setup.codes):
    for code in show_paths.keys():
        if code in path:
        # handles all codes as default, can be set to only handle some
            if not os.path.exists(setup.path_base + "txt_conversion/" + code):
            # checks if a folder exists, otherwise makes one
                os.makedirs(setup.path_base + "txt_conversion/" + code)
            for episode in show_paths[code]:
            # converts each episode
                convert_single(episode, code)

def convert_single(episode, code):
    with open(episode, encoding = "UTF-8") as epi:
    # converts the HTML format to text
        soup = bs(epi, features="lxml")
        raw_content = soup.get_text()
    raw_content = wrangle(raw_content, code)
    # wrangles the text
    with open(episode.replace("html_source", "txt_conversion") + ".txt", "w", encoding = "UTF-8") as output_file:
    # writes down the wrangled text
        output_file.write(raw_content)

def wrangle(content, code):
    def group0(content, colon):
    # default group
        return content

    def group1(content, colon):
    # ('ATL', 'KOR')
        content = max(content.split("\n\n\n\n\n\n"), key = len)
        # strips the beginning of the transcript
        content = content.split("\nCast\n")[0].strip()
        # strips the end of the transcript
        if colon:
            return colonize(content)
        else:
            return content.strip()

    def group2(content, colon):
    # ('ADV', 'CLW', 'DUC', 'FUT', 'OWL', 'PPG', 'SHE', 'SPO', 'VOL')
        content = content.split("Retrieved from \"")[0].strip()
        if (len(re.split(r'Futurama transcripts', content)) > 1):
            content = (re.split(r'Futurama transcripts', content))[0].strip()
        if (content.endswith("See Also: Episode Transcript List")):
            content = content.split("See Also: Episode Transcript List")[0].strip()
        if (len(content.split("Play Sound")) > 1):
            content = content.split("Play Sound")[1].strip()
        if (len(content.split("The Neutral Planet")) > 1):
            content = content.split("The Neutral Planet")[1].strip()
        if (len(re.split(r'Next: "[a-zA-Z0-9,\' !\/]*"', content, re.M)) > 1):
            content = re.split(r'Next: "[a-zA-Z0-9,\' !\/]*"', content, re.M)[1].strip()
        if (len(re.split(r'\nTranscripts?\n', content, re.M)) > 2):
            content = re.split(r'\nTranscripts?\n', content, re.M)[2].strip()
        if (len(re.split(r'This article is a transcript of the SpongeBob SquarePants episode .+\n', content)) > 1):
            content = re.split(r'This article is a transcript of the SpongeBob SquarePants episode .+\n', content)[1].strip()
        if (len(re.split(r'\(Opening shot: .+\n', content)) > 1):
            content = re.split(r'\(Opening shot: .+\n', content)[1].strip()
        if (len(re.split(r'\n([A-Z]+: )', content, re.M)) > 2):
            content = re.split(r'\n([A-Z]+: )', content, maxsplit = 1)[1] + re.split(r'\n([A-Z]+:)', content, maxsplit = 1)[2].strip()
        if colon:
            return colonize(content)
        else:
            return content.strip()

    def group3(content, colon):
    # ('GRA', 'GUM', 'MLP', 'RAM', 'STU')
        content = content.split("\nSite navigation\n")[0]
        content = content.split("\nv ")[0]
        content = content.split("v • d")[0]
        if (len(content.split("all transcripts on a single page")) > 1):
            content = content.split("all transcripts on a single page")[1]
        if (len(content.split("\nDialogue\n")) > 1):
            content = content.split("\nDialogue\n")[1]
        if (len(re.split(r'Next: "[a-zA-Z0-9,\' !\/]*"', content, re.M)) > 1):
            content = re.split(r'Next: "[a-zA-Z0-9,\' !\/]*"', content, re.M)[1].strip()
        if (len(re.split(r'\nTranscripts?\n', content, re.M)) > 1):
            content = max(re.split(r'\nTranscripts?\n', content, re.M), key = len).strip()
        content = content = max(content.split("\n\n"), key = len)
        if colon:
            return colonize(content)
        else:
            return content.strip()

    def colonize(content):
    # converts columns to "<speaker>: <sentence>"
        lines = content.splitlines()
        lines = list(filter(None, lines))
        content = ""
        for line in lines:
            if re.match(r'(.*)?(([a-z:])|(b\.o\.y\.d\.))$', line.lower().strip()):
                content += line.strip() + ": "
            else:
                content += line.strip() + "\n"
        return content.strip()
    
    switcher = {
        'ADV': [group2, False],
        'ATL': [group1, True],
        'CLW': [group2, False],
        'DUC': [group2, True],
        'FUT': [group2, False],
        'GRA': [group3, True],
        'GUM': [group3, False],
        'KOR': [group1, True],
        'MLP': [group3, False],
        'OWL': [group2, False],
        'PPG': [group2, False],
        'RAM': [group3, False],
        'SHE': [group2, False],
        'SPO': [group2, False],
        'STU': [group3, True],
        'VOL': [group2, False],
    }

    return switcher.get(code, group0)[0](content, switcher[code][1])

if __name__ == "__main__":
    show_paths = setup.initial_setup("html_source/")
    convert_all(show_paths, path = ())