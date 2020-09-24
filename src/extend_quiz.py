import getpass, requests, json, os, sys
import pandas as pd

from canvasapi import Canvas

imported = 0

try:
	from helpers import createInstance
except:
	from src.helpers import createInstance
	imported = 1

FOLDER = os.path.abspath(os.getcwd())
if imported:
	INPUT = "{}\\src\\input".format(FOLDER)
	OUTPUT = "{}\\src\\output".format(FOLDER)
	LOGS = "{}\\src\\complete".format(FOLDER)
else:
	INPUT = "{}\\src\\input".format(FOLDER)
	OUTPUT = "{}\\src\\output".format(FOLDER)
	LOGS = "{}\\src\\complete".format(FOLDER)

if imported == 0:
	API_URL = "https://ubc.test.instructure.com/"
else:
	API_URL = input("Enter Canvas URL instance: ")

# WARNING: Using Ctrl + V for getpass on windows on console seems to cause wonky issues. 
# Not a problem on UI though, only when using console.
API_KEY = getpass.getpass("Enter Token: ")
# API_KEY = ''
canvas = createInstance(API_URL, API_KEY)
AUTH_HEADER = {'Authorization': f'Bearer {API_KEY}'}

'''
	Get Canvas course using canvas object from canvasapi
	Parameters:
		course (Canvas): canvasapi instance
		course_id (int): Canvas course ID
	Returns:
		canvasapi.course.Course object
'''
def getCourse(canvas_obj, course_id):
	try:
		course = canvas_obj.get_course(course_id)
	except Exception as e:
		print(str(e))
		sys.exit(1)
	return course

'''
	Get Canvas course quiz using canvas.course.Course object from canvasapi
	Parameters:
		course (Canvas): canvasapi instance
		quiz_id (int): Canvas quiz ID
	Returns:
		canvasapi.quiz.Quiz object
'''
def getQuiz(course_obj, quiz_id):
	try:
		quiz = course_obj.get_quiz(quiz_id)
	except Exception as qe:
		print(str(qe))
		sys.exit(1)
	return quiz

'''
	Download list of quizzes in a given course, and puts it into a CSV for users to edit
	Parameters:
		course (canvas.course.Course): Canvas course object from canvasapi
	Returns:
		None. But a CSV is created under input folder called 'quiz_inputs.csv'
'''
def dl_quizzes(course_obj):
	try:
		quiz_list = course_obj.get_quizzes()
	except Exception as qle:
		print(str(qle))
		sys.exit(1)

	df = pd.DataFrame(columns=['quiz_name','id'])
	for quiz in quiz_list:
		df = df.append({
			'quiz_name': quiz.title,
			'id': quiz.id
			}, ignore_index=True)
	path = os.path.join(INPUT, 'quiz_input.csv')
	df.to_csv(path, index=False)

'''
	Documentation to be created
'''
def getStudents(course_id, auth_header):
	# Get students in course
	'''
	try:
		student_list = course.get_users()
	'''
	# Above code doesn't return student SIS ID, forced to use request lib temporarily
	try:
		url = "{}api/v1/courses/{}/users".format(API_URL, course_id)
		student_list = requests.get(url, headers=auth_header, params={'enrollment_type[]':'student'})
	except Exception as se:
		print(str(se))
		sys.exit(1)

	student_list = json.loads(student_list.text)

	df = pd.DataFrame(columns=['name','SIS_id','canvas_id','extra_time'])
	for student in student_list:
		df = df.append({
			'name':student['name'],
			'SIS_id': student['sis_user_id'],
			'canvas_id': student['id'],
			'extra_time': 0
			}, ignore_index=True)
	path = os.path.join(INPUT, 'student_input.csv')
	df.to_csv(path, index=False)

'''
	Extend time limit for a given user in a given course taking a given quiz for a specified time
	Parameters:
		course (Canvas.course.Course): Canvas course object from canvasapi
		quiz_id (int): Canvas quiz ID
		student_id (int): Canvas student ID (not SIS ID)
		time (int): minutes of time to be added for quiz
	Returns:
		0 (int): Extension failed
		1 (int): Extension succeeded 
'''
def extend_quiz_s(course, quiz_id, student_id, time):

	# Get Quiz from course
	quiz = getQuiz(course, quiz_id)

	# Extend Quiz for given canvas student_id:
	student_dict = {'user_id': student_id, 'extra_time': time}
	try:
		quiz_extensions = quiz.set_extensions([student_dict])
	except Exception as exe:
		print(str(exe))
		sys.exit(1)

	return 1

def extend_quiz_a():
	# Test values
	course_id = input("\nEnter your desired Canvas course id: ")
	# course_id = 10751
	course = getCourse(canvas, course_id)

	print("\nFor first time use on a machine, the following two steps are mandatory.")
	cr_csv = input("\nDo you want to create a Quiz List CSV to edit as input (Y/N): ")
	cr_csv = cr_csv.strip().upper()

	if(cr_csv == "Y"):
		dl_quizzes(course)

	cr_csv = input("\nDo you want to create a Student List CSV to edit as input (Y/N): ")
	cr_csv = cr_csv.strip().upper()

	if(cr_csv == "Y"):
		getStudents(course_id, AUTH_HEADER)

	input("This is the time to edit the input CSVs under, src/inputs. Press any key to continue: ")

	# Read Input CSVs
	path_a = os.path.join(INPUT, 'student_input.csv')
	st_df = pd.read_csv(path_a)

	path_b = os.path.join(INPUT, 'quiz_input.csv')
	qz_df = pd.read_csv(path_b)

	# Create Progress Tracker
	x = len(st_df['canvas_id'])
	y = len(qz_df['id'])
	total = x*y
	count = 0
	print("\nPlease Wait...")
	sys.stdout.write("0/{}".format(total))
	sys.stdout.flush()

	for i, student in enumerate(st_df['canvas_id']):
		extra_time = st_df['extra_time'][i]
		for quiz in qz_df['id']:
			extend_quiz_s(course, quiz, student, extra_time)
			count+=1
			sys.stdout.write("\r{}/{}".format(count,total))
			sys.stdout.flush()

	print("\nCompleted!")
	
	# Should add some sort of logging here

if imported:
	extend_quiz_a()

if __name__ == '__main__':
	extend_quiz_a()