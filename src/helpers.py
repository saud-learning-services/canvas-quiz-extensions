
## Functions I seem to use over and over

from canvasapi import Canvas
import getpass
import sys
import pandas as pd
import re
import ast
from src.util import shut_down, print_error, print_success
import requests
import json
#import re 

'''
CANVAS FUNCTIONS - GETTING OR SENDING DATA 
'''
# tries to create a canvas instance
# checks that it is valid by getting self information
def create_instance(API_URL, API_KEY):
    try:
        canvas = Canvas(API_URL, API_KEY)
        print_success("Token Valid: {}".format(str(canvas.get_user('self'))))
        return(canvas)
    except Exception as e:
        print("\nInvalid Token: {}\n{}".format(API_KEY, str(e)))
        sys.exit(1)
        #raise

def _get_course(canvas_obj, course_id):
    '''
    Get Canvas course using canvas object from canvasapi
    Parameters:
        course (Canvas): canvasapi instance
        course_id (int): Canvas course ID
    Returns:
        canvasapi.course.Course object
    '''
    try:
        course = canvas_obj.get_course(course_id)
        print_success(f'Entered id: {course_id}, Course: {course.name}.')
    except Exception:
        shut_down(f'ERROR: Could not find course [ID: {course_id}]. Please check course id.')

    return course

def _get_quiz(course_obj, quiz_id):
    '''
    Get Canvas course quiz using canvas.course.Course object from canvasapi
    Parameters:
        course (Canvas): canvasapi instance
        quiz_id (int): Canvas quiz ID
    Returns:
        canvasapi.quiz.Quiz object
    '''

    try:
        quiz = course_obj.get_quiz(quiz_id)
        return(quiz)
    except Exception as qe:
        print_error(f'ERROR: Could not find quiz [ID: {quiz_id}]. Please check course id.')
        raise

def _paginate_list(sub_list, auth_header):
    json_list = pd.read_json(sub_list.text)
    
    while sub_list.links['current']['url'] != sub_list.links['last']['url']:
        sub_list =  requests.get(sub_list.links['next']['url'],
                     headers=auth_header)
        admin_sub_table = pd.read_json(sub_list.text)
        json_list= pd.concat([json_list, admin_sub_table], sort=True)
        json_list=json_list.reset_index(drop=True)
    
    return json_list

def _get_students(course_id, AUTH_HEADER, API_URL):
    '''
    Function gets a list of students for a course
    Parameters:
        course_id (int): Canvas course id
        auth_header (dict): Authorization header for canvas API request. See top for format
    Returns:
        student_list (json): a list of students in json
    '''

    # Get students in course
    '''
    try:
        student_list = course.get_users()
    '''
    # Above code doesn't return student SIS ID, forced to use request lib temporarily
    try:
        url = "{}api/v1/courses/{}/users".format(API_URL, course_id)
        student_list = requests.get(url, headers=AUTH_HEADER, params={'enrollment_type[]':'student', 'per_page':50})
        student_list = _paginate_list(student_list, AUTH_HEADER)
        #student_list = json.loads(student_list.text)
        return(student_list)
    except Exception as se:
        # print(str(se))
        shut_down(f'{se}')
        #shut_down(f'ERROR: Could not find students for course [ID: {course_id}]. Please check course id.')