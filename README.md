# Quiz Extensions

A project that takes input in the form of two CSVs and adds extra time or attempts for students on a list of quizzes

1. List of students with corresponding extra attempts and time to change are entered in ./src/input/student_input.csv
2. List of quizzes to change for students are entered in ./src/input/quiz_list.csv
3. Jupyter Notebook interface will guide user through script, asking for relevant user input when necessary
4. Errors will be shown when necessary by the interface, and failed attempts will be logged in ./src/log

## To Run

1. Open up Anaconda Prompt
2. `$ conda env create -f environment.yml`
3. `$ conda activate quiz_extension`
4. `$ jupyter notebook`
5. The previous command will have opened up a tab in your browser, select 'Canvas Batch Change Dates.ipynb' and follow the instructions listed.

## Inputs for Module

1. Canvas API Token
2. Canvas Course ID
4. Student and Quiz CSVs

## Contribution Guidelines:
**These guidelines assume you have a basic understanding of Git. If you do not please look at this resource here.**
1. If you wish to contribute, clone the repository.
2. Switch the branch to **dev** or make your own branch if you prefer.
3. Make your changes. Commit them with a proper message.
4. Make a pull request from your branch or dev branch into the master branch. Someone will review these changes. If anything needs to be changed, you will be contacted through GitHub.

**Contributions are always welcomed, but please follow the guidelines**

## Acknowledgement :star2:
This adapatation was forked from https://github.com/ubccapico/quiz-extension where the original author acknowledgements were:

> ###  Author
> * **Tyler Cinkant** - [Lannro](https://github.com/Lannro)
