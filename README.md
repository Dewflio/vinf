# VINF

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
  
## Setup guide



