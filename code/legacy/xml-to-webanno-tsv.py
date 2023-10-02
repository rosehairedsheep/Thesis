import glob


def extract_from_xml(filename):

    with open(filename, encoding="utf8") as f:

        file = f.readlines()
        file_len = file.__len__()
        line_number = 0
        document = list()
        coreferences = list()

        while line_number < file_len:

            if file[line_number].strip().startswith("<sentence id"):
                # found a sentence start
                sentence = list()

                # start sentence loop
                line_start = line_number
                for j in range(line_start, file_len):
                    if file[j].strip().startswith("<token id"):
                        # found a token start
                        token = list()

                        # start token loop
                        for k in range(1, 7):
                            if k == 1:
                                # word
                                word = file[j+k].strip()[6:-7]
                                token.append(word)
                            if k == 3:
                                # CharacterOffsetBegin
                                char_begin = file[j+k].strip()[22:-23]
                                token.append(char_begin)
                            if k == 4:
                                # CharacterOffsetEnd
                                char_end = file[j+k].strip()[20:-21]
                                token.append(char_end)
                            if k == 6:
                                # NER
                                ner = file[j+k].strip()[5:-6]
                                token.append(ner)
                        # set the line number to current line
                        line_number += 6
                        sentence.append(token)

                    if file[j].strip().startswith("</tokens>"):
                        # found end of tokens
                        line_number += 1
                        document.append(sentence)
                        break

            if file[line_number].strip().startswith("<coreference") \
                    and file[line_number+1].strip().startswith("<mention"):
                # found a coreference chain start
                coreference = list()

                # start coreference loop
                line_start = line_number
                for i in range(line_start, file_len):
                    if file[i].strip().startswith("<mention"):
                        # found a mention start
                        mention = list()

                        # start mention loop
                        for m in range(1, 4):
                            if m == 1:
                                # sentence
                                sent_num = file[i + m].strip()[10:-11]
                                mention.append(sent_num)
                            if m == 2:
                                # start
                                start = file[i + m].strip()[7:-8]
                                mention.append(start)
                            if m == 3:
                                # end
                                end = file[i + m].strip()[5:-6]
                                mention.append(end)
                        # set the line number to current line
                        line_number += 3
                        coreference.append(mention)

                    if file[i].strip().startswith("</coreference"):
                        # found end of coreference chain
                        line_number += 1
                        coreferences.append(coreference)
                        break
            line_number += 1
    return document, coreferences


def write_tsv(document, coreferences, filename):
    with open(filename, "w", encoding="utf8") as f:
        # write header
        f.write("#FORMAT=WebAnno TSV 3.2\n")
        f.write("#T_SP=de.tudarmstadt.ukp.dkpro.core.api.ner.type.NamedEntity|identifier|value\n")
        f.write("#T_CH=de.tudarmstadt.ukp.dkpro.core.api.coref.type.CoreferenceLink|referenceRelation|referenceType\n")
        f.write("\n")
        f.write("\n")

        sentence_number = 0
        current_char = 0
        for sentence in document:
            sentence_number += 1
            token_number = 0
            # write the sentence header
            sentence_header = "#Text="
            for token in sentence:
                sentence_header += token[0]
                sentence_header += " "
            sentence_header += "\n"
            f.write(sentence_header)

            for token in sentence:
                token_number += 1
                f.write(str(sentence_number)+"-"+str(token_number)+"\t")
                f.write(str(current_char)+"-")
                current_char += token[0].__len__()
                f.write(str(current_char)+"\t"+token[0]+"\t")
                current_char += 1
                if token[3] == "PERSON" or token[3] == "TITLE":
                    f.write("*"+"\t"+"PER"+"\t")
                else:
                    f.write("_"+"\t"+"_"+"\t")
                found_coref = False
                for i in range(0, coreferences.__len__()):
                    if not found_coref:
                        for j in range(0, coreferences[i].__len__()):
                            if int(coreferences[i][j][0]) == sentence_number:
                                if token_number in range(int(coreferences[i][j][1]), int(coreferences[i][j][2])):
                                    # coreference found
                                    f.write("*->"+str(i+1)+"-"+str(j+1)+"\t*["+str(i+1)+"]\n")
                                    found_coref = True
                                    break
                            if int(coreferences[i][j][0]) > sentence_number:
                                break
                if not found_coref:
                    f.write("_\t_\n")
            if sentence_number < document.__len__():
                f.write("\n")


if __name__ == "__main__":
    path = "C:/Users/charl/PycharmProjects/LCA-miniproject/scenes/atla/xml/*"
    files = glob.glob(path)
    for file in files:
        tsv = file[63:] + ".tsv"
        doc, coref = extract_from_xml(file)
        write_tsv(doc, coref, tsv)
