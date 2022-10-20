import re, regex       #regex
import bz2      #bz2 compression reading
import pickle   #serialization util
import gc       #garbage collector
import logging 
from vinf_utils import *


def split_xml_into_pages(filename):
    with bz2.open(filename, "r") as file:
        lines = file.read().decode()
        pages_arr = lines.split("<page>")
        return pages_arr

def filter_records(records_arr ,filter_string):
    result_arr = []
    for record in records_arr:
        if filter_string in record:
            result_arr.append(record)
    return result_arr

def process_attribute_group(grp):
    #gets rid of the | attribute_name =
    attr_name_re = r"\|\s*(.)*?\s*="
    attr_name_search  = re.search(attr_name_re, grp)
    if attr_name_search != None:
        attr_name_end_idx = attr_name_search.span()[1]
        grp_str = grp[attr_name_end_idx:]
    else:
        grp_str = grp

    return grp_str.strip()

def process_date(date_str):
    curly_re = r"{{(.)*?[0-9](.)*?}}" #we are only interested in brackets with digits in them
    square_re = r"[[(.)*?[0-9](.)*?]]"




def parse_record(record):
    
    tl_re = r"(?<=<title>)(\n|.)*?(?=</title>)"                 #title 
    ct_re = r"(?<={{Infobox)\s+\S+"                             #categories 
    nm_re = r"\|\s*name(.)*?(\n|\|\s+\S+\s*=s*[^0-9])"          #name
    bd_re = r"\|\s*birth_date(.)*?(\n|\|\s+\S+\s*=s*[^0-9])"    #bith date 
    dd_re = r"\|\s*death_date(.)*?(\n|\|\s+\S+\s*=s*[^0-9])"    #death date
    bp_re = r"\|\s*birth_place(.)*?(\n|\|\s+\S+\s*=s*[^0-9])"   #birth place
    dp_re = r"\|\s*death_place(.)*?(\n|\|\s+\S+\s*=s*[^0-9])"   #death place

    tl_srch = re.search(tl_re, record)
    ct_srch = re.search(ct_re, record)
    nm_srch = re.search(nm_re, record)
    bd_srch = re.search(bd_re, record)   
    dd_srch = re.search(dd_re, record)   
    bp_srch = re.search(bp_re, record)   
    dp_srch = re.search(dp_re, record)

    tl_str = ""
    ct_str = ""
    nm_str = ""
    bd_str = ""   
    dd_str = ""   
    bp_str = ""   
    dp_str = ""
    
    if tl_srch != None:
        tl_str = process_attribute_group(tl_srch.group())
    if ct_srch != None:
        ct_str = process_attribute_group(ct_srch.group())
    if nm_srch != None:
        nm_str = process_attribute_group(nm_srch.group())
    if bd_srch != None:
        bd_str = process_attribute_group(bd_srch.group())
    if dd_srch != None:
        dd_str = process_attribute_group(dd_srch.group())
    if bp_srch != None:
        bp_str = process_attribute_group(bp_srch.group())
    if dp_srch != None:
        dp_str = process_attribute_group(dp_srch.group())

    print(f"title:\t\t{tl_str}")
    print(f"categories:\t{ct_str}")
    print(f"name:\t\t{nm_str}")
    print(f"birth date:\t{bd_str}")
    print(f"death date:\t{dd_str}")
    print(f"birth place:\t{bp_str}")
    print(f"death place:\t{dp_str}")
    print("----------------------------------------------------------------------")
    #create a dictionary
    record_dict = {
       
    }
    



#regex that matches closed {{}} - '\{\{(?:[^}{]+|(?R))*+\}\}' or '\{\{(?:[^}{]+|(?V1))*+\}\}' for python

logging.basicConfig(level=logging.INFO)

#infobox_regex = r"{{Infobox (\n|.)*?\n}}"
#box_regex = r"\{\{(?:[^}{]+|(?V1))*+\}\}"
pages = []
people = []
read_xml = False
serialize = False
serialization_file = "test.pickle"
input_xml = "D:/VINF_datasets/enwiki-latest-pages-articles-multistream1.xml-p1p41242.bz2"

if read_xml:
    pages = split_xml_into_pages(input_xml)
    
else:
    people = load_serialization(serialization_file)

if serialize:
    people = filter_records(records_arr=pages, filter_string="birth_date")
    serialize_array(serialization_file, people)

for p in people:
    parse_record(p)


