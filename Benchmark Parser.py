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


if __name__ == "__main__":
    cpu_benchmark_url = "https://www.cpubenchmark.net/desktop.html"
    gpu_benchmark_url = "https://www.videocardbenchmark.net/common_gpus.html"
    
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
       
    # parser.clear_scores() 
    # parser.feed(str(gpu_resp.data))
    # gpu_dict = {}
    # for elem in parser.scores:
    #     name, score, price = elem['prdname'], elem['count'], elem['price-neww']
    #     name = name[:name.find('@')].strip() if name.find('@') != -1 else name.strip()
    #     score = int(score.replace(',', ''))
    #     price = int(price.strip("$").strip("*").replace(',', '').replace('.', '')) if price != 'NA' else 'NA'
    #     gpu_dict[name] = (score, price)
    
    print(cpu_dict)
    # print(resp.data)