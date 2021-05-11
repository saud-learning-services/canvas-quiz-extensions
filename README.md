# Canvas Quiz Extensions

> - name: canvas-quiz-extensions
> - ops-run-with: jupyter
> - python>=3.7
> - canvasapi>=2.0.0
> - supports universal environment 🌎

A project that takes input in the form of two CSVs and adds extra time or attempts for students on a list of quizzes.

* Terminal (or Jupyter) will prompt user and generate input .csv templates:
   * Edit `input/student_input.csv` with a list of students with corresponding extra attempts and time
   * Edit `input/quiz_input.csv` to specify quizzes to affect
* Terminal (or Jupyter) will ask for inputs and confirmations
* Errors will be shown when necessary by the interface, and failed attempts will be logged in `/src/log` (a log is generated any time the script is run)

## :warning: Important Caveats

* This script only works with **Canvas Classic Quizzes**
* The attempt and time extensions will be overwritten when you run this script (does not add extra attempts or time, replaces them)
* The script assumes that you want to extend the time and/or attempts for each student for each quiz listed
* We have not tested the behaviour of this script for non-published or past-due quizzes

## Inputs

You will need
1. Canvas API Token
1. Canvas Course ID
2. Student and Quiz CSVs *(Templates generated when run)*


## To Run

### Sauder Operations

_Are you Sauder Operations Staff? Please go [here](https://github.com/saud-learning-services/instructions-and-other-templates/blob/main/docs/running-instructions.md) for detailed instructions to run in Jupyter. ("The Project", or "the-project" is "canvas-quiz-extensions" or "Canvas Quiz Extensions")._

### General (terminal instructions)

#### First Time

You will need to create the quiz_extension environment. We use conda to manage our projects.
`$ conda env create -f environment.yml`

#### Every Time

1. `$ conda activate canvas-quiz-extensions`
1. `$ python extend_quiz.py`

---

## Acknowledgement

This adapatation was forked from https://github.com/ubccapico/quiz-extension where the original author acknowledgements were:

> - **Tyler Cinkant** - [Lannro](https://github.com/Lannro)
