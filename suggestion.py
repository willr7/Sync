import json
import difflib

game_titles = json.load(open("game_ids.json")).keys()

def suggestions(curr_title):
    closest = difflib.get_close_matches(curr_title, game_titles, cutoff=0)
    print(closest)
    return closest