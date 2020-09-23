
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

def all_dict_to_str(d):
    """
        Handles dictionaries returned from canvas.
        When data returned some items are not strings - changes all items to strings.
        Some data becomes string in DataFrames i.e. "{'a': 'string'}", transforms to dict.
        Returns Dict where all values are strings.
        """
    # if its a dict, change items to strings
    if isinstance(d, dict):
        new = {k:str(v) for k, v in d.items()}
        return(new)
    else:
        if pd.isnull(d):
            pass
        else:
            d = literal_eval(d)
            new = {k:str(v) for k, v in d.items()}
            return(new)

# Working with DataFrames and 
def list_to_df(df, col_to_expand):
    """
    Expands column that contains list to multiple rows (1/list item)
    Keeps original columns. 
    Requires df and col_to_expand (the column that contains lists)
    Returns DataFrame with original index
    """
    s = df.apply(lambda x: pd.Series(x[col_to_expand]),axis=1).stack().reset_index(level=1, drop=True)
    s.name = col_to_expand
    new_df = df.drop(col_to_expand, axis=1).join(s)
    return(new_df)
        

def dict_to_cols(df, col_to_expand, expand_name):
    """
    Expands column that contains dict to multiple columns (1/dict key)
    Handles transforming column specified to appropriate dict (where all items are strings)
    Returns DataFrame with original index
    """
    df[col_to_expand] = df[col_to_expand].apply(all_dict_to_str, axis=1)
    original_df = df.drop([col_to_expand], axis=1)
    extended_df = df[col_to_expand].apply(pd.Series)
    extended_df.columns = [i if bool(re.search(expand_name, i)) else "{}{}".format(str(expand_name), str(i))for i in extended_df.columns]
    new_df = pd.concat([original_df, extended_df], axis=1, ignore_index=False)
    return(new_df)






