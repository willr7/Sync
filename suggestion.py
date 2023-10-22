import json
import difflib

def suggestions(curr_title):
    game_titles = json.load(open("gpu_benchmarks.json")).keys()
    # print(cpu_name, gpu_name)
    closest = difflib.get_close_matches(curr_title, game_titles, cutoff=0)
    return closest