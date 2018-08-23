from canvas_api import canvas
from canvas_api.quizzes import extend_quiz_access
from canvas_api.users import get_user_id, get_user_id_by_enrollment
from canvas_api.util.file import read_from_csv, write_to_csv
import logging
import sys
from configparser import ConfigParser

config = ConfigParser(interpolation=None)
config.read('settings.cfg')

_OUTPUT_FILE = config['default']['output_file']
if _OUTPUT_FILE == "False":
    _OUTPUT_FILE = False
    
_PROMPT = config['default']['prompt_to_close']
if _PROMPT == "False":
    _PROMPT = False
    
_INPUT_HAS_HEADERS = config['default']['input_has_headers']
if _INPUT_HAS_HEADERS == "False":
    _INPUT_HAS_HEADERS = False

_HEADERS = ['course_id', 'quiz_id', 'student_number', 'extra_time']

_CHECK_BY_ENROLLMENTS = False

def extend_user_access(input_list):
    global _CHECK_BY_ENROLLMENTS
    output_content = [_HEADERS]
    output_content[0].append("status")
    for row in input_list:
        try:
            course_id = row['course_id']
            quiz_id = row['quiz_id']
            student_number = row['student_number']
            extra_time = row['extra_time']
            output = [str(course_id), str(quiz_id), str(student_number), str(extra_time)]

            if _CHECK_BY_ENROLLMENTS:
                response = get_user_id_by_enrollment(canvas, student_number, course_id)
            else:
                response = get_user_id(canvas, student_number)
                
            if 'unauthorized' in response:
                _CHECK_BY_ENROLLMENTS = True
                response = get_user_id_by_enrollment(canvas, student_number, course_id)
                
            if 'error' in response:
                output.append("FAILED: " + response['error'])
                logging.warning(", ".join(output))
                output_content.append(output)
                continue            
            if 'message' in response:
                output.append("FAILED: " + response['message'])
                logging.warning(", ".join(output))
                output_content.append(output)
                continue
            
            if _CHECK_BY_ENROLLMENTS:
                user_id = response['user_id']
            else:
                user_id = response['id']
                
            response = extend_quiz_access(canvas,course_id, quiz_id, user_id, extra_time)            
            if 'error' in response:
                output.append("FAILED: " + response['error'])
                logging.warning(", ".join(output))
                output_content.append(output)
                continue
            output.append("SUCCESS")
            logging.info(", ".join(output))
            output_content.append(output)
        except KeyError as e:
            logging.error("KeyError: {0}".format(e))
            logging.warning("unexpected data headers.  check input data.")
            break            
        except Exception as e:
            logging.error("{}: {}".format(type(e).__name__, e))
            
    if len(output_content) > 1 and _OUTPUT_FILE:
        write_to_csv(str(_OUTPUT_FILE), output_content)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        extend_user_access(read_from_csv(sys.argv[1], _HEADERS, _INPUT_HAS_HEADERS))
    else:
        _input = {}
        for header in _HEADERS:
            _input[header] = input("{header}: ".format(header=header))
        extend_user_access([_input])
    if _PROMPT:
        input("Press enter to close...")
