#Check for prohibited words in response
def check_prohibited(response):

    prohibited_words = [
        "promise",
        "guarantee",
        "sue",
        "lawsuit",
        "fault",
        "responsible",
        "compensation",
        "refund",
        "liable",
        "always",
        "never"
    ]

    for word in prohibited_words:
        if word in response.lower():
            return {"passed": False, "reason": f"Prohibited word found: {word}"}
    
    return {"passed": True, "reason": "No prohibited words found"}
    

#Checks if response is empty, if prohibited word was found, and if risk was flagged
def safety_check(analysis, response):

    if not response:
        return {"passed": False, "reason": "Empty Response"}
    
    prohibited = check_prohibited(response)

    if not prohibited["passed"]:
        return prohibited

    if analysis['risk']:
        return {"passed": False, "reason": "Risk found - requires manual review"}
    
    return {"passed": True, "reason": "All checks passed"}