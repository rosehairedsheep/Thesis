import utils.setup as setup
import statistics

episode_lengths = dict()

if __name__ == "__main__":
    show_paths = setup.initial_setup("txt_conversion/")
    for code in setup.codes:
        episode_lengths[code] = list()
    absolutely_all_tokens = 0
    all_episodes = list()
    for code in show_paths.keys():
        total_tokens = 0
        for episode in show_paths[code]:
            with open(episode, encoding = "UTF-8") as episode_file:
                content = episode_file.read()
            tokens = len(content.split())
            episode_lengths[code].append(tokens)
            all_episodes.append(tokens)
            total_tokens += tokens
        average_tokens = statistics.mean(episode_lengths[code])
        standard_deviation = statistics.stdev(episode_lengths[code])
        absolutely_all_tokens += total_tokens
        print("Show: {}\nTotal number of tokens: {}\nAverage number of tokens: {}\nStandard deviation: {}\n"
        .format(code, total_tokens, average_tokens, standard_deviation))
    print(absolutely_all_tokens)
    print(statistics.mean(all_episodes))
    print(statistics.stdev(all_episodes))