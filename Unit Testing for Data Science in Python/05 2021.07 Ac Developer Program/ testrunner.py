import pytest
from main import check_psw
from main import check_email
from main import check_psw_equal
from main import check_credentials

#Tests to question 1: -------------------------------
def test_email1():
  email = "myname326@gmail.com"
  assert check_email(email) is True

def test_email2():
  email = "my.ownsite@acc.org"
  assert check_email(email) is True

def test_email3():
  email = "myname326.com"
  assert check_email(email) is False

#TRUE because letters, upper case, lower case, numbers
def test_check_psw1():
  psw = "Qwert1234"
  assert check_psw(psw) is True

#FALSE because no numbers
def test_check_psw2():
  psw = "qwert"
  assert check_psw(psw) is False




#this unit test failed initially, #6
def test_check_psw3():
  psw = "QWERT55"
  assert check_psw(psw) is False
  
#FALSE because no numbers  
def test_check_psw4():
  psw = "Qwerty"
  assert check_psw(psw) is False

#FALSE because no letters  
def test_check_psw5():
  psw = "551234"
  assert check_psw(psw) is False

#TRUE because letters, upper case, lower case, numbers +- symbols
def test_check_psw6():
  psw = "Qwerty$£@55"
  assert check_psw(psw) is True

#FALSE because no numbers
def test_check_psw7():
  psw = "Qwerty$£@"
  assert check_psw(psw) is False



#this unit test failed initially, #11
#this password has letters, upper case, lower case, numbers, symbols
#it is a valid password
#not sure why the unit test assert is FALSE?!
#unit test 11 in testrunner seems wrong, yet the instructions tell us not to modify the testrunner file
def test_check_psw8():
  psw = "Qwert5@"
  assert check_psw(psw) is False     




# TODO write the unit tests for the new functions, remove the comment notation and replace assert False with your code: ---------------------------- 
# 1. Test that two equal passwords return true
def test_psw_equal1():
  psw1 = "abc"
  psw2 = "abc"
  assert check_psw_equal(psw1, psw2) is True

# 2. Test that the function is case sensitive
def test_psw_equal2():
  psw1 = "abc"
  psw2 = "Abc"
  assert check_psw_equal(psw1, psw2) is False

# 3. Test that two inequal passwords return false
def test_psw_equal3():
  psw1 = "abc1"
  psw2 = "0bc2"
  assert check_psw_equal(psw1, psw2) is False

# 4. Test that two equal passwords in the correct format and a correct email return true
def test_check_credentials1():
  email = "myname326@gmail.com"
  psw1 = "Abc12//" 
  psw2 = "Abc12//" 
  assert check_credentials(email, psw1, psw2) is True


# 5. Test that two inequal passwords in the correct format and a correct email return false
def test_check_credentials2():
  email = "myname326@gmail.com"
  psw1 = "Abc12//" 
  psw2 = "Abc13//" 
  assert check_credentials(email, psw1, psw2) is False


# 6. Test that two equal passwords in the correct format and an incorrect email return false
def test_check_credentials3():
  email = "myname326.com"
  psw1 = "Abc12//" 
  psw2 = "Abc12//" 
  assert check_credentials(email, psw1, psw2) is False
