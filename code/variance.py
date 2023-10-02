import utils.setup as setup
import statistics

variance = dict()
percentage_variance = dict()

def count_single(path, code, speakers_dict, variance):
    gender_words = [0, 0]
    with open(path, encoding = "UTF-8") as episode_file:
        content = episode_file.readlines()
        for line in content:
            splits = line.split(" says:", maxsplit = 1)
            if ((len(splits) > 1) and not (len(splits[0].split()) > 5)):
                current_speaker = splits[0].strip().upper()
                sentence = splits[1].strip()
                guessed_speaker = ["", "", 0]
                for speaker in speakers_dict[code]:
                    if (((speaker[0] in current_speaker) | (current_speaker in speaker[0])) & (len(speaker[0]) > len(guessed_speaker[0]))):
                        guessed_speaker = speaker
                if guessed_speaker[1] == 'MALE':
                    gender_words[0] += len(sentence.split())
                elif guessed_speaker[1] == 'FEMALE':
                    gender_words[1] += len(sentence.split())
        variance[code].append(gender_words)
    return variance

if __name__ == "__main__":
    show_paths = setup.initial_setup("coref_source/")
    for code in setup.codes:
        variance[code] = list()
    speakers_dict = setup.initialize_speakers()
    for code in show_paths.keys():
        for episode in show_paths[code]:
            variance = count_single(episode, code, speakers_dict, variance)
    for code in variance:
        ratio = list()
        for item in variance[code]:
            if ((item[0] != 0) & (item[1] != 0)):
                ratio.append(item[0]/(item[0] + item[1]))
        ratio.sort()
        percentage_variance[code] = ratio
    for key in percentage_variance:
        print("{}\n{}".format(key, percentage_variance[key]))
