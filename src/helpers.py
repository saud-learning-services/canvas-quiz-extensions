
## Functions I seem to use over and over

from canvasapi import Canvas
import getpass
import sys
import pandas as pd
import re
import ast
#import re 


def createCSV(df, output_name):
    print(df.head())

    while True:
        confirmation = input("Your csv will be called: {}\nDo you want to generate this csv from with the data above? (y/n): ".format(output_name))
        
        if confirmation == "y":
            df.to_csv(output_name, index=False)
            print("\n{} created.\nBye!".format(output_name))
            break
        elif confirmation =="n":
            print("\nCsv not created. You can run the script again or exit for no further action.\n")
            break
        else:
            print("Please enter 'y' to accept or 'n' to exit\n")
            continue

# tries to create a canvas instance
# checks that it is valid by getting self information
def createInstance(API_URL, API_KEY):
    try:
        canvas = Canvas(API_URL, API_KEY)
        print("Token Valid: {}".format(str(canvas.get_user('self'))))
        return(canvas)
    except Exception as e:
        print("\nInvalid Token: {}\n{}".format(API_KEY, str(e)))
        sys.exit(1)
        #raise

# get course id
def getCourseFromID(canvas):
    course_id = input("Enter Course ID: ")
    try:            
        course = canvas.get_course(course_id)
        print("Course ID: {}\nCourse Name: {}\n".format(course.id, course.name))
        return(course_id, course)
    except Exception as e:
        print(str(e))
        sys.exit(1)
