import urllib3
import bs4
import json

def get_cases():
    url = "https://www.newegg.com/p/pl?N=100007583%20600545969&cm_sp=Cat_Computer-Cases_4_-VisNav-_-ATX-Mid-Tower"
    
    cases = urllib3.request("GET", url).data
    case_site = bs4.BeautifulSoup(str(cases), features="html.parser")
    
    case_dict = {}
    item_boxes = case_site.find_all(attrs={'class', 'item-cell'})
    for box in item_boxes:
        link = box.find(attrs={'class', 'item-title'})['href']
        name = box.find(attrs={'class', 'item-title'}).contents[1]
        price_label = box.find(attrs={'class', 'price-current'})
        price = int(price_label.strong.contents[0])
        explicit_data = urllib3.request("GET", link).data
        explicit_site = bs4.BeautifulSoup(str(explicit_data), features="html.parser")
        tables = explicit_site.find_all(attrs={'class', 'table-horizontal'})
        name = ""
        brand = ""
        model = ""
        for table in tables:
            if table.caption.contents == ["Model"]:
                rows = table.find_all('tr')
                brand = rows[0].td.contents[0]
                model = rows[2].td.contents[0]
                name = brand + " " + model
        case_dict[name] = {"link": link, "price": price}
    
    json.dump(case_dict, open("cases.json", "w"), indent=6)
    
    
        
def get_RAM():
    url = "https://www.newegg.com/p/pl?d=RAM&n=4841"
    
    RAM_data = urllib3.request("GET", url).data
    RAM_site = bs4.BeautifulSoup(str(RAM_data), features="html.parser")
    
    RAM_dict = {}
    def avoid_ads(tag):
        return len(tag.attrs) > 1
    
    item_boxes = RAM_site.find_all(avoid_ads)
    for box in item_boxes:
        try:
            item = box.find(attrs={'class', 'item-title'})
            if not item or not item.has_attr('href'):
                continue
            link = item['href']
            price_label = box.find(attrs={'class', 'price-current'})
            price = int(price_label.strong.contents[0]) 
            explicit_data = urllib3.request("GET", link).data
            explicit_site = bs4.BeautifulSoup(str(explicit_data), features="html.parser")
            tables = explicit_site.find_all(attrs={'class', 'table-horizontal'})
            name = ""
            brand = ""
            model = ""
            for table in tables:
                if table.caption.contents == ["Model"]:
                    rows = table.find_all('tr')
                    brand = rows[0].td.contents[0]
                    model = rows[2].td.contents[0]
                    name = brand + " " + model
            RAM_dict[name] = {"link": link, "price": price}
        except AttributeError:
            pass
    
    json.dump(RAM_dict, open("RAM.json", "w"), indent=6)
        
    
def get_power_supply():
    url = "https://www.newegg.com/p/pl?d=power+supply&n=4841"
    
    power_data = urllib3.request("GET", url).data
    power_site = bs4.BeautifulSoup(str(power_data), features="html.parser")
    
    power_dict = {}
    def avoid_ads(tag):
        return len(tag.attrs) > 1
    
    item_boxes = power_site.find_all(avoid_ads)
    for box in item_boxes:
        try:
            item = box.find(attrs={'class', 'item-title'})
            if not item or not item.has_attr('href'):
                continue
            link = item['href']
            price_label = box.find(attrs={'class', 'price-current'})
            price = int(price_label.strong.contents[0]) + float(price_label.sup.contents[0])
            explicit_data = urllib3.request("GET", link).data
            explicit_site = bs4.BeautifulSoup(str(explicit_data), features="html.parser")
            tables = explicit_site.find_all(attrs={'class', 'table-horizontal'})
            name = ""
            brand = ""
            model = ""
            wattage = 0
            for table in tables:
                if table.caption.contents == ["General"]:
                    rows = table.find_all('tr')
                    brand = rows[0].td.contents[0]
                    model = rows[2].td.contents[0]
                    name = brand + " " + model
                if table.caption.contents == ["Details"]:
                    rows = table.find_all('tr')
                    wattage = int(rows[1].td.contents[0])
            power_dict[name] = {"link": link, "wattage": wattage, "price": price}
            # power_list.append((name, link, wattage, price))
        except :
            pass
        
    json.dump(power_dict, open("power.json", "w"), indent=6)

def get_motherboard():
    
    AMD_url = "https://www.newegg.com/p/pl?N=4841%20100007625&d=motherboard&isdeptsrh=1"
    INTEL_url = "https://www.newegg.com/p/pl?N=4841%20100007627&d=motherboard&isdeptsrh=1"
    
    mother_dict = {}
    for url in [AMD_url, INTEL_url]:
        mother_data = urllib3.request("GET", url).data
        mother_site = bs4.BeautifulSoup(str(mother_data), features="html.parser")
        def avoid_ads(tag):
            return len(tag.attrs) > 1
        
        item_boxes = mother_site.find_all(avoid_ads)
        for box in item_boxes:
            try:
                item = box.find(attrs={'class', 'item-title'})
                if not item or not item.has_attr('href'):
                    continue
                link = item['href']
                price_label = box.find(attrs={'class', 'price-current'})
                price = int(price_label.strong.contents[0]) + float(price_label.sup.contents[0])
                explicit_data = urllib3.request("GET", link).data
                explicit_site = bs4.BeautifulSoup(str(explicit_data), features="html.parser")
                tables = explicit_site.find_all(attrs={'class', 'table-horizontal'})
                name = ""
                brand = ""
                model = ""
                Socket = ""
                for table in tables:
                    if table.caption.contents == ["Model"]:
                        rows = table.find_all('tr')
                        brand = rows[0].td.contents[0]
                        model = rows[1].td.contents[0]
                        name = brand + " " + model
                    if table.caption.contents == ["Supported CPU"]:
                        rows = table.find_all('tr')
                        Socket = rows[0].td.contents[0]
                mother_dict[name] = {"link": link, "chipset": Socket, "price": price}
                # mother_list.append((name, link, Socket, price))
            except :
                pass
            
    json.dump(mother_dict, open("mother.json", "w"))
    