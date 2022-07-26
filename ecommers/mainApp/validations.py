import re


# for cheacking mobile number lenght 10 and is digit or not 


def mobileNumber_validate(mobile):

    if len(mobile)==10:
        if mobile.isdigit():
            return True
        
        else:

            return False
    
    else:

        return False








#  if student name does not contains any digit True otherwise return false!




def check_name(name):
    a=re.findall("\d",name)
    if not a:
        return True
    else:
        return False



def email_validation(email):

    pattern = '^[a-z0-9]+[\._]?[ a-z0-9]+[@]\w+[. ]\w{2,3}$'

    if re.search(pattern,email):

        return True
    
    else:

        return False