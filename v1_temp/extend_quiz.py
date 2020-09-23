from canvas_api import canvas
from canvas_api.quizzes import extend_quiz_access
from canvas_api.users import get_user_id_by_enrollment
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

def extend_user_access(input_list):
    output_content = [_HEADERS]
    output_content[0].append("status")
    for row in input_list:
        try:
            _status = ""            
            course_id = row['course_id']
            quiz_id = row['quiz_id']
            student_number = row['student_number']
            extra_time = row['extra_time']

            response = get_user_id_by_enrollment(canvas, student_number, course_id)

            if 'error' in response:
                _status = "FAILURE: " + response['error']      
            elif 'message' in response:
                _status = "FAILURE: " + response['message']
            else:            
                user_id = response['user_id']                
                response = extend_quiz_access(canvas,course_id, quiz_id, user_id, extra_time)
                
                if 'error' in response:
                    _status = "FAILURE: " + response['error']
                else:
                    _status = "SUCCESS"
                
            output = [course_id, quiz_id, student_number, extra_time, _status]
            if _status == "SUCCESS":
                logging.info(", ".join(str(x) for x in output))
            else:
                logging.warning(", ".join(str(x) for x in output))
            output_content.append(output)
            
        except KeyError as e:
            output = []
            for x in row:
                output.append(row[x])
            output.append("FAILURE: missing data header {}".format(e))
            logging.warning(", ".join(str(x) for x in output))
            break
        
        except Exception as e:
            output = []
            for x in row:
                output.append(row[x])
            output.append("FAILURE: unexpected error - {}: {}".format(type(e).__name__, e))
            logging.warning(", ".join(str(x) for x in output))
            
    if len(output_content) > 1 and _OUTPUT_FILE:
        write_to_csv(str(_OUTPUT_FILE), output_content)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        _input = read_from_csv(sys.argv[1], _HEADERS, _INPUT_HAS_HEADERS)
        extend_user_access(_input)
    else:
        _input = [{}]
        for header in _HEADERS:
            _input[0][header] = input("{header}: ".format(header=header))
        extend_user_access(_input)
    if _PROMPT:
        input("Press enter to close...")
