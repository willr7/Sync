import json
import urllib3
from html.parser import HTMLParser
import bs4
import difflib

class BenchmarkParser(HTMLParser):
    #Specifically designed for the common benchmarks site
    
    def __init__(self, *, convert_charrefs: bool = True) -> None:
        self.scores = [] #dictionary of parts to scores
        self.in_visible = False
        self.in_entry = False
        self.in_table = False
        self.done = False
        self.current_entry = {}
        self.current_attr = ""
        self.item_type = {"prdname", "count", "price-neww"}
        super().__init__(convert_charrefs=convert_charrefs)
        
    def handle_starttag(self, tag, attrs):
        if tag == 'div' and attrs == [('id', 'mark')]:
            self.in_visible = True
        elif tag == 'div' and attrs == [('id', 'value')]:
            self.in_visible = False
        elif tag == 'ul' and attrs == [('class', 'chartlist')]: #[tag, attrs] == ['ul', ('class', 'chartlist')]:
            self.in_table = True
        elif self.in_table and tag == 'a':
            self.in_entry = True
        elif self.in_entry and tag == 'span':
            self.current_attr = attrs[0][1] # second element of the first tuple
            
    
    def handle_endtag(self, tag):
        if tag == 'ul' and self.in_table:
            self.done = True
            self.in_table = False
        elif tag == 'a' and self.in_table and self.in_entry and not self.done:
            self.in_entry = False
            # print(self.current_entry)
            self.scores.append(dict(self.current_entry))

    def handle_data(self, data):
        if self.in_table and self.in_entry and self.current_attr in self.item_type:
            self.current_entry[self.current_attr] = data
            
    def clear_scores(self):
        self.scores = []
        
class GPUParser(HTMLParser):
    def __init__(self, *, convert_charrefs: bool = True) -> None:
        self.scores = [] #dictionary of parts to scores
        self.done = False
        self.in_table = False
        self.in_entry = False
        self.current_key = ""
        self.item_type = {"prdname", "count", "price-neww"}
        self.current_entry = []
        super().__init__(convert_charrefs=convert_charrefs)
        
    def handle_starttag(self, tag, attrs):   
        if tag == 'ul' and attrs == [('class', 'chartlist')]:
            self.in_table = True
        elif tag == 'li' and self.in_table:
            self.in_entry = True
        elif tag == 'span' and self.in_table and self.in_entry:
            self.current_key = attrs[0][1]
    
    def handle_endtag(self, tag):
        if tag == 'ul' and self.in_table:
            self.in_table = False
            self.done = True
        elif tag == 'li' and self.in_entry and self.current_entry:
            self.in_entry = False
            self.scores.append(self.current_entry)
            self.current_entry = []
        
    
    def handle_data(self, data):
        if self.current_key in self.item_type and not self.done:
            self.current_entry.append(data)
            self.current_key = ""
        
def fetch_particular_score_2(cpu_name: str, gpu_name: str):
    
    cpu_search = cpu_name.replace(" ", "+")
    gpu_search = gpu_name.strip("NVIDIA").strip("AMD").strip().lower()
    
    #remove gb
    if "gb" in gpu_search:
        index = gpu_search.find("gb")
        

    gpu_url = "https://www.videocardbenchmark.net/gpu_list.php"
    cpu_url = "https://www.cpubenchmark.net/cpu.php?cpu=" + cpu_search
    
    cpu_resp = urllib3.request("GET", cpu_url)
    gpu_resp = urllib3.request("GET", gpu_url)
    
    cpu_site = bs4.BeautifulSoup(str(cpu_resp.data), features="html.parser")
    gpu_site = bs4.BeautifulSoup(str(gpu_resp.data), features="html.parser")
    
    cpu_score = cpu_site.find(attrs={"class": "right-desc"}).findAll("span")[1].contents
    gpu_score = None
    
    #have to search for it
    entries = gpu_site.find('tbody').find_all('tr')
    for entry in entries:
        if entry.find('a').contents[0].lower() == gpu_search: #make this less strict matching
            gpu_score = entry.find_all('td')[1].contents
    
    #assumes that it works for all cpus
    assert gpu_score is not None, f"{gpu_search}"
        
    return int(cpu_score[0]), int(gpu_score[0])

def fetch_particular_score(cpu_name: str, gpu_name: str):
    cpu_dict = json.load(open("cpu_benchmarks.json"))
    gpu_dict = json.load(open("gpu_benchmarks.json"))
    closest_cpu = difflib.get_close_matches(cpu_name, cpu_dict, cutoff=0)[0]
    closest_gpu = difflib.get_close_matches(gpu_name, gpu_dict, cutoff=0)[0]
    
    return {"cpu_name": closest_cpu, "cpu_score": cpu_dict[closest_cpu][0], "gpu_name": closest_gpu, "gpu_score": gpu_dict[closest_gpu][0]}
    
def generate_data():
    
    cpu_url = "https://www.cpubenchmark.net/cpu_list.php"
    gpu_url = "https://www.videocardbenchmark.net/gpu_list.php"
    
    try:
        f_cpu = open("cpu_benchmarks.json", "x")
        f_gpu = open("gpu_benchmarks.json", "x")
        
        cpu = urllib3.request("GET", cpu_url).data
        gpu = urllib3.request("GET", gpu_url).data
        
        cpu_site = bs4.BeautifulSoup(str(cpu), features="html.parser")
        gpu_site = bs4.BeautifulSoup(str(gpu), features="html.parser")
        
        cpu_dict = {}
        gpu_dict = {}
        
        gpu_entries = gpu_site.find('tbody').find_all('tr')
        for entry in gpu_entries:
            name_td, score_td, _, _, price_td = entry.find_all('td')
            name = name_td.a.contents[0]
            score = int(score_td.contents[0].replace(",", ""))
            price = 'NA'
            if price_td.contents != ['NA']:
                price = float(price_td.a.contents[0].strip("*").strip("$").replace(",", ""))
            gpu_dict[name] = (score, price)
        
        cpu_entries = cpu_site.find('tbody').find_all('tr')
        for entry in cpu_entries:
            name_td, score_td, _, _, price_td = entry.find_all('td')
            name = name_td.a.contents[0]
            score = int(score_td.contents[0].replace(",", ""))
            price = 'NA'
            if price_td.contents != ['NA']:
                try:
                    price = float(price_td.contents[0].strip("*").strip("$").replace(",", ""))
                except AttributeError:
                    pass
            cpu_dict[name] = (score, price)
            
        json.dump(cpu_dict, f_cpu, indent=6)
        json.dump(gpu_dict, f_gpu, indent=6)
        
    except FileExistsError:
        pass
    

def generate_benchmark_data():
    cpu_benchmark_url = "https://www.cpubenchmark.net/desktop.html"
    gpu_benchmark_url = "https://www.videocardbenchmark.net/common_gpus.html"
    
    try:
        f_cpu = open("cpu_benchmarks.json", "x")
        f_gpu = open("gpu_benchmarks.json", "x")
        
        cpu_resp = urllib3.request("GET", cpu_benchmark_url)
        gpu_resp = urllib3.request("GET", gpu_benchmark_url)
        
        if cpu_resp.status != 200 or gpu_resp.status != 200:
            print("Error Getting Benchmark Url results")
            exit()
            
        parser = BenchmarkParser()
        parser.feed(str(cpu_resp.data))
        
        cpu_dict = {}
        for elem in parser.scores:
            name, score, price = elem['prdname'], elem['count'], elem['price-neww']
            name = name[:name.find('@')].strip() if name.find('@') != -1 else name.strip()
            score = int(score.replace(',', ''))
            price = float(price.strip("$").strip("*").replace(',', '')) if price != 'NA' else 'NA'
            cpu_dict[name] = (score, price)
        
        parser.clear_scores() 
        
        parser = GPUParser()
        parser.feed(str(gpu_resp.data))
        
        gpu_dict = {}
        for elem in parser.scores:
            name, score, price = elem
            name = name[:name.find('@')].strip() if name.find('@') != -1 else name.strip()
            score = int(score.replace(',', ''))
            price = float(price.strip("$").strip("*").replace(',', '')) if price != 'NA' else 'NA'
            gpu_dict[name] = (score, price)
        
        json.dump(cpu_dict, f_cpu, indent=6)
        json.dump(gpu_dict, f_gpu, indent=6)
        
    except FileExistsError:
        #no need to recreate the benchmark jsons
        pass

