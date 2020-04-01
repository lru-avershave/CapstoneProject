# Checks the two parameters against set usernames and passwords
# Uses user inputted values as parameters
# Returns login status as true or false
def validate(username, password):
    login = True
    savedUsername = "Admin" #Can be changed to a database with logins
    savedPassword = "Password" 

    if not username == savedUsername:
        login = False
    if not password == savedPassword:
        login = False
    
    return login