# VINF - Leonard Puškáč 2022/23 Winter Semester - Documentation

This project was created in contribution to the VINF (Information Retrieval) course at FIIT STU - 2022/23

It deals with extracting data about people from wikipedia dumps - data such as their name, date of birth, date of death, and so on...
It aims to create an index on the extrated data, and allow for quick seaching of the records.
The output of the program is the answer to the question: "Could these two people have met?"

The project uses the Apache Spark for parallel/distributed data extraction from xml wiki dumps. Namely it uses dataframes - loads the xmls into the dataframe in a distributed manner, and transforms the dataframe using user defined funcitions. 

The user defined function in this case is a method from the VINF_Parser object called parse_record that extracts the relevant information from the wiki page. (name of the person, their date of birth and date of death).

Then the extraced data is written into a json file, and an index is created over these records using Lucene.


## User Interface

The user interface consists of a prompt in the terminal - e.i. its a console application, and all of the searching is done via console.

The user is usually given a set of options to choose from - the choice is always made by typing the number of the choice in the prompt and hitting Enter.

The main functionality looks for two people from the indexed records and compares their dates of birth and death. This is done by first searching for and selecting the first person, and then the second person (Separately).

The does this by typing in the name (or a part of the name) of the first person. And then selecting a person from the provided results. Then, unless the user opted not to pick any of the found results, the process happens for the second person. Once both are selected, the user is given the answer as well as some information about the selected people (like when they were born, and when they died).

## Project Structure

The project consists of multiple parts with their specific dependencies.
The parts being: 
  - Lucene (controller and handler) - indexing and searching
  - Apache Spark (Pyspark) - distributed computation (extraction of data)
  - Parser - parsing data from xml format to json objects

Unfortunately due to some package handling issues, the source files of the project are all clumped into one direcotry. However they are named according to their functionality, so it shouldn't be a problem to differentiate between them.
### Files with descriptions
[vinf_spark.py](https://github.com/Dewflio/vinf/blob/master/vinf_spark.py) - runs the distributed data extraction using Spark\
[vinf_lucene.py](https://github.com/Dewflio/vinf/blob/master/vinf_lucene.py) - the console application that allows the user to search for results\
[vinf_lucene_controller.py](https://github.com/Dewflio/vinf/blob/master/vinf_spark.py) - a class that handles all things lucene. If run as a script, it creates the index\
[vinf_parser.py](https://github.com/Dewflio/vinf/blob/master/vinf_spark.py) - a class that handles parsing the xml wiki dumps into a list of records in json format\
[vinf_date.py](https://github.com/Dewflio/vinf/blob/master/vinf_spark.py) - an extension of the datetime.datetime class that adds the option to store information about the date being AD or BC\
[vinf_utils.py](https://github.com/Dewflio/vinf/blob/master/vinf_spark.py) - some utility functions - serialization of arrays that was used during development - not really used in the final version of the application
[vinf_parse_pages.py](https://github.com/Dewflio/vinf/blob/master/vinf_parse_pages.py) - processes the input xml files - creates a json dict with the pages we are interested in (with all newlines converted to spaces).

## Setup guide

As stated above, each part of the project has its own dependancies, namely PyLucene and PySpark. This section describes how to setup the project so that the dependencies are satisfied.

### Lucene

The indexing and searching part of this project is implemented using the PyLucene API. This is done using docker.

**Using Windows Powershell or bash**
```
docker pull coady/pylucene
docker create --name vinf_pylucene_container -v path_to_project_directory:/VINF_project -i coady/pylucene
docker start vinf_pylucene_container
docker exec -it vinf_pylucene_container /bin/bash
```
Then in the bash of the container install the required python dependencies by running: 

```
pip install -r path_to_project/lucene_requirements.txt
```

### Spark

The distributed part of the project is built using the Spark API.
This was done using docker, early on in the project. However we later switched to using wsl (The Windows Subsystem for Linux)
We installed Ubuntu from the microsoft store. And on it we installed java using these commmands:
```
sudo apt update
sudo apt install openjdk-11-jdk
```
Then we installed python using commands:
```
sudo apt-get update
sudo apt-get install python3
```
we also installed pip with:
```
sudo apt-get update
apt install python3-pip
```
and then intalled the required packages using:
```
pip install -r path_to_project/spark_requirements.txt
```

## Running the Application

### Lucene

To run the application with the Lucene components we first start the lucene container using this command in powershell:
```
docker start vinf_lucene_container
```
and then we can start the script using:
```
docker exec -it vinf_pylucene_container /bin/bash
python3 path_to_project/vinf_lucene.py
```
This opens the console application that does the searching.

To create the index we can use (as of the time of writing this):
```
python3 path_to_project/vinf_lucene_controller.py
```

### Spark

The Spark portion of the project is run using the wsl environment. We attach a shell from the environment to our IDE and run the following command:
```
python3 path_to_project/vinf_spark.py
```
This runs the distributed data extraction. It does so by processing the data/parsed_pages.json file with xml pages written as json objects (each in one line).
We generate this file using:
```
python3 path_to_project/vinf_parse_pages.py
```

## Input Data

To test this project we used four compressed xml wiki dump files dowloaded from the dump repository https://dumps.wikimedia.org/enwiki/latest/

To be specific the files used were called:\
enwiki-latest-pages-articles-multistream1.xml-p1p41242.bz2\
enwiki-latest-pages-articles-multistream10.xml-p4045403p5399366.bz2\
enwiki-latest-pages-articles-multistream11.xml-p5399367p6899366.bz2\
enwiki-latest-pages-articles-multistream12.xml-p7054860p8554859.bz2

These files are stored in the /data/input_xmls directory (Which is not included in the github repository). These files were used to create the pre-processed data stored in json format.

However, we later implemented a spark script that works with xml files directly. These files however have to be unpacked from the bz2 format. (At least in the current version of the implementation) They are stored in the /data/input_xmls_unpacked (Which also is not included in the github repo).

All in all, the input files were about 1,1 GB when compressed with bz2, and about 6,7 GB when uncompressed.

These files contain wikipedia dumps in xml format.





## Encountered Problems

Some of the problems we encounted during the making of this project were the following:
 - The extratction of the dates proved to be a bit difficult because of all the different formats used in the xml.
 - Spark: At first we extracted the data not directly from the input xmls but from a json which included preprocessed pages. They were preprocessed by replacing newlines by whitespaces, and being written into one-line attributes of json objects. This might still be the case at the time of the final turn-in. 


