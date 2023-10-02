import glob
import sys
import re

# function to remove brackets and everything inside of them
def remove_text_inside_brackets(text, brackets="()[]<>"):
    count = [0] * (len(brackets) // 2) # count open/close brackets
    saved_chars = []
    for character in text:
        for i, b in enumerate(brackets):
            if character == b: # found bracket
                kind, is_close = divmod(i, 2)
                count[kind] += (-1)**is_close # `+1`: open, `-1`: close
                if count[kind] < 0: # unbalanced bracket
                    count[kind] = 0  # keep it
                else:  # found bracket to remove
                    break
        else: # character is not a [balanced] bracket
            if not any(count): # outside brackets
                saved_chars.append(character)
    return ''.join(saved_chars)

if __name__ == "__main__":
    path = '/Users/emma/Documents/University/Linguistic Corpus Annotation/Project/LCA-miniproject/subtitles/*.srt'
    files = glob.glob(path)
    for name in files:
        with open(name, encoding = "ISO-8859-1") as f:
        # opens the source file

            aList = f.readlines()

            name = name[:len(name) - 4]
            nameList = name.split("subtitles/")
            newName = nameList[0] + "formatted_subtitles/" + nameList[1] + ".txt"
            # adjusts the file name to be put in a separate folder

            with open(newName, 'w', encoding = "ISO-8859-1",) as f2:
            # opens the write file

                for sentence in aList:
                    sentence = remove_text_inside_brackets(sentence)
                    # removes brackets and text inside

                    sentence = re.sub('[A-Z\']*? ?[A-Z\']*:', '', sentence)
                    # removes speaker annotation as in "SOMEONE:"

                    if sentence:
                        if (not sentence[0].isdigit() and not re.match(r'^\s*$', sentence) and not "www." in sentence):
                        # removes timestamps, sentence numbers, whitespace sentences, and website links

                            if (sentence.startswith("-")):
                                sentence = sentence[1:]
                            # removes dashes from the beginning of lines

                            sentence = sentence.strip()

                            if not sentence == "":
                                f2.write(sentence + "\n")
                            # prints output to f2