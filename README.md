# VINF - Leonard Puškáč 2022/23 Winter Semester

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



