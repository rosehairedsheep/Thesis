import utils.setup as setup
import re

def convert_all(show_paths, path = setup.codes):
    speakers_dict = setup.initialize_speakers(path)
    for code in show_paths.keys():
        if code in path:
        # handles all codes as default, can be set to only handle some
            show_output = ""
            pair = [0, 0, 0, 0]
            # the pairs go as follows: M > M, M > F, F > M, F > F
            print(code)
            for episode in show_paths[code]:
            # makes stats for each episode
                result = convert_single(episode, code, speakers_dict, pairs = pair)
                show_output += result[0]
                pair = result[1]
                # updates the pairs values and feeds it into the next loop
            show_output = "STATS:\n{}\n\n{}".format(str(pair), show_output)
            # creates a stats block before printing the individual pairs
            with open("{}coref_analysis/{}.txt".format(setup.path_base, code), "w", encoding = "UTF-8") as output_file:
                output_file.write(show_output.strip())
    return

def convert_single(path, code, speakers_dict, pairs = [0, 0, 0, 0]):
    with open(path, encoding = "UTF-8") as episode_file:
    # gathers data from an individual episode coreference
        raw_content = episode_file.readlines()
    findings = dict()
    # the keys are line numbers, the values are an ordered list of the speaker and addressee tuples
    for line in raw_content:
        if re.match(r'(.*)?\([1-9]+,(.*)?, that is: "you(rs?)?"(.*)?', line.lower().strip()):
        # identifies coreference lines
            line_number = int(line.split(",")[0].split("(")[1])
            # identifies the line number
            if (line_number not in findings.keys()):
                findings[line_number] = [[], []]
            addressee = ("", "")
            for speaker in speakers_dict[code]:
            # searches addressee in the coreference, updates if the speaker has a longer name than the last addressee assigned
                if ((len(speaker[0]) > len(addressee[0])) & (speaker[0] in line.upper())):
                    addressee = speaker
            findings[line_number][1] = addressee
    collect_speakers = False
    last_linenumber = -1
    assigned_speaker = ("", "")
    for line in raw_content:
        if (line.strip() == ""):
            collect_speakers = False
        if (collect_speakers & (last_linenumber in findings.keys())):
            if (re.match(r'[A-Za-z0-9]+ says:.*', line.strip())):
            # identifies a line said by a speaker of the specified line number
                this_speaker = line.split(" says:")[0].strip()
                for speaker in speakers_dict[code]:
                # searches speaker in the coreference, updates if the speaker has a longer name than the last speaker assigned
                    if ((len(speaker[0]) > len(assigned_speaker[0])) &
                    ((this_speaker.upper() in speaker[0])) | (speaker[0] in this_speaker.upper())):
                        assigned_speaker = speaker
                findings[last_linenumber][0] = assigned_speaker
        if(re.match(r'Sentence #[1-9]+.*', line)):
        # identifies the current line number
            last_linenumber = int(line.split("Sentence #")[1].split("(")[0].strip())
            collect_speakers = True
            assigned_speaker = ("", "")
    text = ""
    for key in findings.keys():
        if ((len(findings[key][0]) != 0) & (len(findings[key][1]) != 0)):
            if ((findings[key][0] != findings[key][1]) & (findings[key][0][0].strip() != "")
            & (findings[key][1][0].strip() != "")):
            # removes incomplete pairs
                text += "\n\nspeaker: " + findings[key][0][0]
                text += "\naddressee: " + findings[key][1][0]
                if ((findings[key][0][1] == "MALE") & (findings[key][1][1] == "MALE")):
                    pairs[0] += 1
                elif ((findings[key][0][1] == "MALE") & (findings[key][1][1] == "FEMALE")):
                    pairs[1] += 1
                elif ((findings[key][0][1] == "FEMALE") & (findings[key][1][1] == "MALE")):
                    pairs[2] += 1
                elif ((findings[key][0][1] == "FEMALE") & (findings[key][1][1] == "FEMALE")):
                    pairs[3] += 1
                # updates pairs values for the episode
    return [text, pairs]

if __name__ == "__main__":
    show_paths = setup.initial_setup("coref_finished/")
    convert_all(show_paths)