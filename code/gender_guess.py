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
                        speaker_split = re.split(r'( AND )|&|,', speaker)
                        for speaker in speaker_split:
                            if ((speaker) and not (speaker == " AND ")):
                                if ((code + "/" + speaker.strip()) not in speakers.keys()):
                                    speakers[code + "/" + speaker.strip()] = [0, 0, 0]
                                if (re.match(r'.*\[.*\].*', sentence)):
                                    male = 0
                                    female = 0
                                    male += len(re.findall(r'\[(.*[ ,\.!\?])?((he)|(him)|(his))([ ,\.!\?].*)?\]', sentence.lower()))
                                    female += len(re.findall(r'\[(.*[ ,\.!\?])?((she)|(her)|(hers))([ ,\.!\?].*)?\]', sentence.lower()))
                                    speakers[code + "/" + speaker.strip()][0] += male
                                    speakers[code + "/" + speaker.strip()][1] += female
                                    sentence = re.sub(r'\[.*\]', r'', sentence)
                                speakers[code + "/" + speaker.strip()][2] += len(sentence.split())
    return speakers

if __name__ == "__main__":
    show_paths = setup.initial_setup("txt_conversion/")
    with open(setup.path_base + "speakers.txt", "w", encoding = "UTF-8") as output:
        speakers = count_speakers(show_paths)
        male_tok = 0
        female_tok = 0
        for key in speakers.keys():
            if (speakers[key][2] > 100):
                output.write(key + "\t" + str(speakers[key]) + "\t")
                if (speakers[key][0] > speakers[key][1]):
                    output.write("MALE")
                    male_tok += speakers[key][2]
                elif (speakers[key][1] > speakers[key][0]):
                    output.write("FEMALE")
                    female_tok += speakers[key][2]
                output.write("\n")
        output.write("MALE TOKENS: {}\nFEMALE TOKENS: {}".format(str(male_tok), str(female_tok)))