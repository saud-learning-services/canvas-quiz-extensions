# quiz_extension

A project that takes input in the form of CSV that extends a user's quiz access for given number of minutes.


## Getting Started

### Requirements

You need Python 3.4 or later to run **quiz_extensions.py.** You can have multiple Python versions (2.x and 3.x) installed on the same system without problems.

In Ubuntu, Mint and Debian you can install Python 3 like this:

```
$ sudo apt-get install python3 python3-pip
```

For Windows, Mac or other Linux, packages are available at

http://www.python.org/getit/


### Set up

To run this script, you will need a **Canvas API Access token.** Instructions on how to generate one can be found here

https://community.canvaslms.com/docs/DOC-10806-4214724194

Once you have a token, you will need to set up **canvas.cfg** with your token.

### Running the script

**extend_quiz.py** can either be run stand alone
```
python3 extend_quiz.py
```

or with an input file as an argument

```
python3 extend_quiz.py input.csv
```

If you are running the script on Windows, simply double clicking **extend_quiz.py** or drag-and-dropping an input file onto it.


## Example Input

**input.csv** has an example of input data that **quiz_extension.py** can read as input.  This data will extend access to quizzes 10000 and 10001 in courses 100 and 101 to Student Numbers 12345678 and 87654321 for 30 minutes.


## Settings

**settings.cfg** can be modified to change the behavior of **quiz_extension.py**. It currently supports three options:
* output_file: the name of the output file.  If none given, no output file will be created.
* prompt_to_close: prompts user with "Press enter to close..." if set to True
* input_has_headers: reads the first line of input data as a row of headers if set to True.

## Authors

* **Tyler Cinkant** - [Lannro](https://github.com/Lannro)
