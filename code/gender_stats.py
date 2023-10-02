import utils.setup as setup

speakers_dict = dict()
stats = dict()

if __name__ == "__main__":
    speakers_dict = setup.initialize_speakers(setup.codes)
    for code in setup.codes:
        stats[code] = dict()
        stats[code]["total_speakers"] = 0
        stats[code]["total_words"] = 0
        stats[code]["male_speakers"] = 0
        stats[code]["female_speakers"] = 0
        stats[code]["male_words"] = 0
        stats[code]["female_words"] = 0
    for code in speakers_dict.keys():
        for speaker in speakers_dict[code]:
            if not (speaker[1] == "NB"):
                stats[code]["total_speakers"] += 1
                stats[code]["total_words"] += speaker[2]
                if (speaker[1] == "MALE"):
                    stats[code]["male_speakers"] += 1
                    stats[code]["male_words"] += speaker[2]
                elif (speaker[1] == "FEMALE"):
                    stats[code]["female_speakers"] += 1
                    stats[code]["female_words"] += speaker[2]