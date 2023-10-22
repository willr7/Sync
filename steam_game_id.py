import json
import urllib3
from html.parser import HTMLParser


class SpecParser(HTMLParser):
    #state machine to get the specs from HTML
    def __init__(self, *, convert_charrefs: bool = True) -> None:
        self.in_spec = False #whether or not the next data option should be added to the dictionary
        self.in_items = False
        self.current_key = ""
        self.spec_dict = {}
        super().__init__(convert_charrefs=convert_charrefs)
        
    def handle_starttag(self, tag, attrs):
        if tag == "strong":
            self.in_spec = True

    def handle_endtag(self, tag):
        if tag == "strong":
            self.in_spec = False
            self.in_items = True
        elif self.in_items:
            self.in_items = False

    def handle_data(self, data):
        if self.in_spec:
            self.current_key = data.strip(':')
        elif self.in_items and self.current_key != "Minimum" and self.current_key != "Recommended":
            if self.current_key == "Processor" or self.current_key == "Graphics":
                text = data.strip()
                self.spec_dict[self.current_key] = text.split(" or ")
            else:
                self.spec_dict[self.current_key] = data.strip()

def fetch_specs(game_name):    
    game_dict = {}
    source_filename = "ids.json"
    dest_filename = "game_ids.json"
    
    try:    
        f = open(dest_filename, "x", encoding='utf-8')
        json_dict = json.load(open(source_filename, encoding='utf-8'))
        #I want a set of all names, dictionary name : id
        for pair in json_dict['applist']['apps']:
            game_dict[pair['name']] = pair['appid']
        json.dump(game_dict, f, indent=6)
    except FileExistsError:
        game_dict = json.load(open(dest_filename))
    
    # game_name = "Rocket League" #will be gotten from user
    game_id = game_dict[game_name]
    
    # App details API: 
    app_url = "http://store.steampowered.com/api/appdetails?appids="
    resp = urllib3.request("GET", app_url + str(game_id) + "&l=english")
    OK = 200 #error code
    if resp.status == OK:
        print("request: success")
    
    game_data_json = resp.data
    game_data = json.loads(game_data_json)
    game_specs_dict = game_data[str(game_id)]['data']['pc_requirements']
    
    parser = SpecParser()
    parser.feed(game_specs_dict['minimum'])
    minimum_specs = dict(parser.spec_dict)
    parser.feed(game_specs_dict['recommended'])
    recommened_specs = parser.spec_dict
    
    Specifications = {"Minimum": minimum_specs,
                    "Recommended": recommened_specs}
    # print(recommened_specs)
    return recommened_specs