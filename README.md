# quiz_extension

A project that takes input in the form of CSV that extends a user's quiz access for given number of minutes


## Getting Started

First thing you will need to do is set up the **canvas.cfg** with a canvas token, then **quiz_extension.py** can be run stand alone, or with a csv file as input.


## Example

**input.csv** has an example of input data that **quiz_extension.py** can read as input.  This data will extend access to quizzes 10000 and 10001 in courses 100 and 101 to Student Numbers 12345678 and 87654321 for 30 minutes.


## Settings

**settings.cfg** can be modified to change the behavior of **quiz_extension.py**. It currently supports three options:
* output_file: the name of the output file.  If none given, no output file will be created.
* prompt_to_close: prompts user with "Press enter to close..." if set to True
* input_has_headers: reads the first line of input data as a row of headers if set to True.

## Authors

* **Tyler Cinkant** - [Lannro](https://github.com/Lannro)