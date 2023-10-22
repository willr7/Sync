import json
import urllib3
from html.parser import HTMLParser

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
        
def fetch_particular_score(type, name):
    gpu_url = "https://www.videocardbenchmark.net/gpu.php?gpu="
    cpu_url = "https://www.cpubenchmark.net/cpu.php?cpu="
    #urls don't include the memory at the end of GPUs, does include Company names though: AMD, INTEL, etc. 
    

def generate_benchmark_data():
    cpu_benchmark_url = "https://www.cpubenchmark.net/desktop.html"
    gpu_benchmark_url = "https://www.videocardbenchmark.net/common_gpus.html"
    
    try:
        f = open("cpu_benchmarks.json", "x")
        f = open("gpu_benchmarks.json", "x")
        
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
            price = int(price.strip("$").strip("*").replace(',', '').replace('.', '')) if price != 'NA' else 'NA'
            cpu_dict[name] = (score, price)
        
        parser.clear_scores() 
        
        parser = GPUParser()
        parser.feed(str(gpu_resp.data))
        
        gpu_dict = {}
        for elem in parser.scores:
            name, score, price = elem
            name = name[:name.find('@')].strip() if name.find('@') != -1 else name.strip()
            score = int(score.replace(',', ''))
            price = int(price.strip("$").strip("*").replace(',', '').replace('.', '')) if price != 'NA' else 'NA'
            gpu_dict[name] = (score, price)
        
        json.dump(cpu_dict, f, indent=6)
        json.dump(gpu_dict, f, indent=6)
    except FileExistsError:
        #no need to recreate the benchmark jsons
        pass

    