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
[vinf_spark.py](https://github.com/Dewflio/vinf/blob/master/vinf_spark.py) - runs the distributed data extraction using Spark - NOT USED ANYMORE\
[vinf_spark_new.py](https://github.com/Dewflio/vinf/blob/master/vinf_spark.py) - runs the distributed data extraction using Spark\
[vinf_lucene.py](https://github.com/Dewflio/vinf/blob/master/vinf_lucene.py) - the console application that allows the user to search for results\
[vinf_lucene_controller.py](https://github.com/Dewflio/vinf/blob/master/vinf_spark.py) - a class that handles all things lucene. If run as a script, it creates the index\
[vinf_parser.py](https://github.com/Dewflio/vinf/blob/master/vinf_spark.py) - a class that handles parsing the xml wiki dumps into a list of records in json format\
[vinf_date.py](https://github.com/Dewflio/vinf/blob/master/vinf_spark.py) - an extension of the datetime.datetime class that adds the option to store information about the date being AD or BC\
[vinf_utils.py](https://github.com/Dewflio/vinf/blob/master/vinf_spark.py) - some utility functions - serialization of arrays that was used during development - not really used in the final version of the application
[vinf_parse_pages.py](https://github.com/Dewflio/vinf/blob/master/vinf_parse_pages.py) - processes the input xml files - creates a json dict with the pages we are interested in (with all newlines converted to spaces). - NOT USED ANYMORE


[/data](https://github.com/Dewflio/vinf/tree/master/data) - a directory that contains the relevan data - in the github repo most of this directory is not included. Only the resulting indexes are. This directory needs to include subfolders called "input_xmls" and/or "input_xmls_unpacked" with the relevant input data to work properly\
[/data/index_final](https://github.com/Dewflio/vinf/tree/master/data/index_final) - contains the final version of the index


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
python3 path_to_project/vinf_spark_new.py
```
This runs the distributed data extraction. It does so by processing the xmls in the /data/input_xmls_unpacked directory. It creates a directory called spark_output_new into which Spark 
will write multiple json files (the number of these files depends on how the spark work is distrubuted). 


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





## The Process of Work on this Project

First I created a simple parser that extracted the data from the xmls into records. These records were written into a file called "records.json" and it contained an array of json objects. 

Later I created an index using Lucene from this "records.json" file. This was done via a class called VINF_Lucene_Controller, designed to handle writing and searching. The final version of the class isn't much different from how it was initially. Only the method that creates the index was changed to handle a different input file format (produced by the spark distributed extraction).

A script called vinf_lucene is the script that utilizes VINF_Lucene_Controller and serves as the console application. 

I later began working on the Spark distributed extraction of data. At first I was using Spark incorrectly - I had to preprocess data using the [vinf_parse_pages.py](https://github.com/Dewflio/vinf/blob/master/vinf_parse_pages.py) script. This produced a list of json objects that each contained the whole page in one line. And the [vinf_spark.py](https://github.com/Dewflio/vinf/blob/master/vinf_spark.py) script was used to process it.

In order to utilise Spark correctly I then later created [vinf_spark_new.py](https://github.com/Dewflio/vinf/blob/master/vinf_spark_new.py) which works with the input xmls directly and does not need the preprocessed data. 

### Encountered Problems

Some of the problems I encountered during the making of this project were the following:
 - The extratction of the dates proved to be a bit difficult because of all the different formats used in the xml.
 - Spark: At first I extracted the data not directly from the input xmls but from a json which included preprocessed pages. They were preprocessed by replacing newlines by whitespaces, and being written into one-line attributes of json objects.

Overall, the biggest hurdle during development was probably figuring out how to properly run the APIs that I was suppposed to work with (like using docker or wsl).

Other than that, handling date formats was a pain, as none of the available python libraries can handle dates Before Christ (BC), and there are some issues with reading years with a different number of digits than four.

And the final hurdle was figuring out how to read xmls directly into Spark dataframes, because this is not natively possible in Spark, and you have to utilise an external library. The proper usage of which was not really apparent (at least to me at first).

## Evaluation

After properly implementing the distributed data extraction in Spark, I can conclude that creating an index from mulitple large xml files is much faster that if it was done using other/regular means. The data we processed was about 6.7 GB (when uncompressed) and Spark loaded and read these files into a dataframe in a matter of seconds. The longest part (in terms of computation time) of the extraction was that last part of the spark script - the writing of the results from the dataframe.

Compared to an undistributed version of this program the Spark implementation is much faster. Without it, the program would one by one open the input files and parse them, which (at least on my machine) would take a much longer time. 

### Improvements 

I could improve the effectiveness of this project by mainly:
- refactoring the [vinf_parser.py](https://github.com/Dewflio/vinf/blob/master/vinf_parser.py)
- (Maybe) using other methods of representing and storing the data when extracting records.

The Parser class has a lot of issues. Some of which are: 
- The regexes to search each record are not precompiled
- There are some errors, that result in the date of birth or death not being loaded properly. This is mainly due to date formats that I have probably not accounted for.

Other than that, it might be possible that using something like RDDs instead of a normal dataframe could be better. And maybe using something else in place of UDFs (user defined functions), would also help speed up the process of extraction. That being said, on our data (about 6.7 GB) it works reasonably fast.

Finally, some more customisation to the VINF_Lucene_Controller could be beneficial - such as ensuring that the user can seach for parts of the words for example. 

