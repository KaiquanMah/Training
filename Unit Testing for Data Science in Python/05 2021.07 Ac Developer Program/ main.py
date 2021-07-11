import re 

# Question 1: -----------------------------------
regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$' 
      
def check_email(email):  
    if(re.search(regex,email)):  
        return True          
    else:  
        return False 
      
def check_psw_upper(psw):
  result = any(char.isupper() for char in psw)
  return result

def check_psw_digit(psw):
  result = any(char.isdigit() for char in psw)
  return result


"""original wrong code
def check_psw_lower(psw):
  result = any(char.isupper() for char in psw)
  return result
"""
#fixed code
def check_psw_lower(psw):
  result = any(char.islower() for char in psw)
  return result



"""original code
def check_psw(psw):
  if(check_psw_digit(psw)
            and check_psw_upper(psw)
            and check_psw_lower(psw)
            and check_psw_digit(psw)  
            and len(psw) >= 7):
    print("Valid password")
    return True
  else:
    print("Invalid password")    
    return False    
"""




"""dont need this newly created fn
def check_psw_symbols(psw):
  result = any((not char.isalphanum()) for char in psw)
  return result
"""



#fix
def check_psw(psw):
  if(check_psw_digit(psw)
            and check_psw_upper(psw)
            and check_psw_lower(psw)
            and len(psw) >= 7):
    print("Valid password")
    return True
  else:
    print("Invalid password")    
    return False    





# New functions: ------------------------------------
def check_psw_equal(psw1, psw2):
  return psw1 == psw2

def check_credentials(email, psw1, psw2):
  return check_email(email) and check_psw(psw1) and check_psw_equal(psw1, psw2)

