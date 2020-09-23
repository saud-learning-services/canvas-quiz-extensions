import getpass, requests, json

from canvasapi import Canvas
from helpers import createInstance

FOLDER = "canvas_course_settings"
INPUT = "{}/input".format(FOLDER)
OUTPUT = "{}/output".format(FOLDER)
LOGS = "{}/complete".format(FOLDER)

API_URL = "https://ubc.test.instructure.com/"

# WARNING: Using Ctrl + V for getpass on windows on console seems to cause wonky issues. 
# Not a problem on UI though, only when using console.
API_KEY = getpass.getpass("Enter Token: ")
#API_KEY = input("Enter token: ")
canvas = createInstance(API_URL, API_KEY)
auth_header = {'Authorization': f'Bearer {API_KEY}'}

# Current code works on 1:1 student basis, because the CSV is unsorted, hopefully in future,
# we will not need to get quiz object and course object multiple times in most cases.
# More comprehensive Error checking will have to be done as well.

'''
	Extend time limit for a given user in a given course taking a given quiz for a specified time
	Parameters:
		course_id (int): Canvas course ID
		quiz_id (int): Canvas quiz ID
		student_id (int): Student SIS ID
		time (int): minutes of time to be added for quiz
	Returns:
		0 (int): Extension failed
		1 (int): Extension succeeded 
'''

def extend_quiz(course_id, quiz_id, student_id, time):
	# Get Canvas Course from id
	try:
		course = canvas.get_course(course_id)
	except Exception as e:
		print(str(e))
		sys.exit(1)

	# Get Quiz from course
	try:
		quiz = course.get_quiz(quiz_id)
	except Exception as qe:
		print(str(qe))
		sys.exit(1)

	# Get students in course
	'''
	try:
		student_list = course.get_users()
	'''
	# Above code doesn't return student SIS ID, forced to use request lib temporarily
	try:
		url = "{}api/v1/courses/{}/users".format(API_URL,course_id)
		student_list = requests.get(url, headers=auth_header, params={'enrollment_type[]':'student'})
	except Exception as se:
		print(str(se))
		sys.exit(1)

	student_list = json.loads(student_list.text)
	canvas_student_id = -1
	for student in student_list:
		if(student['sis_user_id'] == str(student_id)):
			print(student)
			canvas_student_id = int(student['id'])
			break

	# If no SIS student ID found, no student exists. Exit failure
	# Have to log failure somewhere
	if(canvas_student_id == -1):
		return 0

	# Extend Quiz:
	student_dict = {'user_id': canvas_student_id, 'extra_time': time}
	try:
		quiz_extensions = quiz.set_extensions([student_dict])
	except Exception as exe:
		print(str(exe))
		sys.exit(1)

	return 1

if __name__ == '__main__':
	# Test values
	code = extend_quiz(10751, 91041, 0, 10)
	if(code == 1):
		print("Success")
	else:
		print("Fail")
		# Have to add logging for success and fail cases




