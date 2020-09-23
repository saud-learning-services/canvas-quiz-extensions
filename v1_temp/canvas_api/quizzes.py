import logging

_QUIZ_ACCESS = "courses/{course_id}/quizzes/{quiz_id}/extensions"

def extend_quiz_access(canvas, course_id, quiz_id, user_id, extra_time):
    if not user_id:
        return {"error":"null user_id"}
    if not extra_time:
        return {"error":"null extra_time"}
    if not str(extra_time).isdigit():
        return {"error":"null extra_time is not an integer"}
        
    response = canvas.call_api(_QUIZ_ACCESS.format(course_id=course_id,
                                                       quiz_id=quiz_id),
                               method="POST",
                               post_fields={"quiz_extensions[][user_id]":user_id,
                                            "quiz_extensions[][extra_time]":extra_time})
    if not response:
        return {"error":"null response"}

    if 'errors' in response:
        return {"error":"course/quiz not found OR user not a student in course"}

    return response
