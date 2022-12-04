from vinf_parser import VINF_Parser

import os, json, logging

logging.basicConfig(level=logging.INFO)
root_folder = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
page_parser = VINF_Parser()


paths = []
data_dir = root_folder + '/data'
xmls_dir = data_dir + '/input_xmls'

for file in os.listdir(xmls_dir):
    paths.append(xmls_dir + '/' + file)

all_people = {}
counter=0
for path in paths:
    logging.info(f"Parsing {path}")
    pages = page_parser.split_xml_into_pages(path)
    logging.info(f"Filtering pages for people")
    people = page_parser.filter_array_str(pages, "birth_date")
    for person in people:
        counter += 1
        person = person.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
        all_people[str(counter)] = person

logging.info("writing pages to json ...")
jsonFile = open(data_dir + "/parsed_pages.json", "w")
jsonString = json.dumps(all_people)
jsonFile.write(jsonString)
jsonFile.close()
logging.info("pages written into json")
