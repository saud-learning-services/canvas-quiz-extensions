import logging

_GET_USER = "users/{user_id}"

def get_user_id(canvas, student_number):
    
    if not student_number:
        return {"error":"null student_number"}
    
    response = canvas.call_api(_GET_USER.format(user_id="sis_user_id:{}".format(str(student_number))))
    if not response:
        return {"error":"null response"}
    
    if 'errors' in response:
        if response['errors'][0]['message'] == "The specified resource does not exist.":
            return {"error":"user not found"}
        else:
            return {"error":response['errors'][0]['message']}

    return response
