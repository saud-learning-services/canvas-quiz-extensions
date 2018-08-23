import logging

_GET_USER = "users/{user_id}"
_GET_USER_BY_ENROLLMENT = "/courses/{course_id}/enrollments?sis_user_id[]={student_number}"

def get_user_id(canvas, student_number):
    
    if not student_number:
        return {"error":"null student_number"}
    
    response = canvas.call_api(_GET_USER.format(user_id="sis_user_id:{}".format(str(student_number))))
    if not response:
        return {"error":"null response"}
    
    if 'errors' in response:
        if response['errors'][0]['message'] == "The specified resource does not exist.":
            return {"error":"user not found"}
        elif response['errors'][0]['message'] == "user not authorized to perform that action":
            return {"unauthorized":"user not authorized"}
        else:
            return {"error":response['errors'][0]['message']}

    return response

def get_user_id_by_enrollment(canvas, student_number, course_id):
    
    if not student_number:
        return {"error":"null student_number"}
    
    if not course_id:
        return {"error":"null course_id"}
    
    response = canvas.call_api(_GET_USER_BY_ENROLLMENT.format(course_id=course_id,
                                                              student_number=student_number))
    if not response:
        return {"error":"null response"}
    
    if 'errors' in response:
        if response['errors'][0]['message'] == "The specified resource does not exist.":
            return {"error":"user not found"}
        else:
            return {"error":response['errors'][0]['message']}

    if len(response) == 1:
        return response[0]

    return response
