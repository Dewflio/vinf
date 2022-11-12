import logging, pickle

def serialize_array(filename, array):
    logging.info("serializing an array into " + filename + " ...")
    with open(filename, "wb") as outfile:
        pickle.dump(array, outfile)
    logging.info("array serialized!")

def load_serialization(filename):
    logging.info("loading serialized objects from " + filename + " ...")
    load_result = []
    with open(filename, "rb") as infile:
        load_result = pickle.load(infile)
    logging.info("objects loaded!")
    return load_result

