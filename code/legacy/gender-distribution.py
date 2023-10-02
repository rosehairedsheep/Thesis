if __name__ == "__main__":
    path = "/Users/emma/Documents/University/Linguistic Corpus Annotation/Project/LCA-miniproject/scenes/speakers-labelled.txt"
    male = 0
    female = 0
    with open(path, encoding = "UTF-8") as f:
        lines = f.readlines()
        for line in lines:
            first_split = line.split(": ")
            second_split = first_split[1].split(", ")
            if second_split[1].strip() == "m":
                male += int(second_split[0])
            elif second_split[1].strip() == "f":
                female += int(second_split[0])
    print("Male tokens: " + str(male) + "\nFemale tokens: " + str(female))

        