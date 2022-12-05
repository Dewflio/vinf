# VINF - Leonard Puškáč 2022/23 Winter Semester - Documentation

This project was created in contribution to the VINF (Information Retrieval) course at FIIT STU - 2022/23

It deals with extracting data about people from wikipedia dumps - data such as their name, date of birth, date of death, and so on...
It aims to create an index on the extrated data, and allow for quick seaching of the records.
The output of the program is the answer to the question: "Could these two people have met?"

## User Interface

The user interface consists of a prompt in the terminal - e.i. its a console application, and all of the searching is done via console.


## Project Structure

The project consists of multiple parts with their specific dependencies.
The parts being: 
  - Lucene (controller and handler) - indexing and searching
  - Apache Spark (Pyspark) - distributed computation (extraction of data)
  - Parser - parsing data from xml format to json objects

Unfortunately due to some package handling issues, the source files of the project are all clumped into one direcotry. However they are named according to their functionality, so it shouldn't be a problem to differentiate between them.

TODO: ADD descriptions of each file
  
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



