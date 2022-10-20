import logging, pickle, bz2, re, regex

def serialize_array(filename, array):
    logging.info("serializing the infoboxes array...")
    with open(filename, "wb") as outfile:
        pickle.dump(array, outfile)
    logging.info("array serialized!")

def load_serialization(filename):
    logging.info("loading serialized objects...")
    load_result = []
    with open(filename, "rb") as infile:
        load_result = pickle.load(infile)
    logging.info("objects loaded!")
    return load_result

def regex_from_xml(filename, regex_term):
    logging.info("reading the xml file into memory...")
    regex_groups = []
    with bz2.open(filename, "r") as file: 
        lines = file.read().decode()
        logging.info("file read into memory!")
        logging.info("searching the file with regex")
        count = 0
        for x in regex.finditer(regex_term, lines, re.MULTILINE):
            regex_group = x.group()
            if regex_group.startswith("{{Infobox"):
                count+=1
                regex_groups.append(regex_group)
                print(count)
            else:
                if "{{Infobox" in regex_group:
                    print("HITTTTTTTT")
    return regex_groups