def validate(username, password):
    login = True
    if not username == "Admin":
        login = False
    if not password == "Password":
        login = False
    return login