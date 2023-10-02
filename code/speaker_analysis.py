import utils.setup as setup
import re

def count_speakers(show_paths):
    speakers = dict()
    for code in setup.codes:
        for episode in show_paths[code]:
            with open(episode, encoding = "UTF-8") as epi:
                content = epi.readlines()
                for line in content:
                    splits = line.split(": ", maxsplit = 1)
                    if ((len(splits) > 1) and not (len(splits[0].split()) > 5)):
                        speaker = splits[0].strip()
                        speaker = re.sub(r'[\[\(].*[\]\)]', "", speaker).strip().upper()
                        speaker = re.sub(r'\".*\"', "", speaker)
                        if re.match(r'.*[\[\]\(\)\#0-9].*', speaker):
                            continue
                        if (len(speaker.split("⨂")) > 1):
                            speaker = speaker.split("⨂")[0]
                        sentence = splits[1].strip()
                        speaker_split = re.split(r'(AND)|&|,', speaker)
                        for speaker in speaker_split:
                            if ((speaker) and not (speaker == "AND")):
                                if ((code + "/" + speaker.strip()) not in speakers.keys()):
                                    speakers[code + "/" + speaker.strip()] = 0
                                speakers[code + "/" + speaker.strip()] += len(sentence.split())
    return speakers

if __name__ == "__main__":
    show_paths = setup.initial_setup("txt_conversion/")
    with open(setup.path_base + "speakers.txt", "w", encoding = "UTF-8") as output:
        speakers = count_speakers(show_paths)
        for key in speakers.keys():
            if (speakers[key] > 10):
                output.write(key + ": " + str(speakers[key]) + ", \n")