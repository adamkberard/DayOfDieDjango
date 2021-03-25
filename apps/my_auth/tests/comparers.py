# Helper functions for testing

def checkLoginMatch(responseData, modelData):
    errors = {}
    if 'token' not in responseData:
        errors['token'] = ['No token']
    elif responseData['token'] is None:
        errors['token'] = ['Token is none']

    if 'username' not in responseData:
        errors['username'] = ['No username']
    elif responseData['username'] != modelData['username']:
        estr = '{} doesnt match {}'
        estr.format(responseData['username'], modelData['username'])
        errors['username'] = [estr]

    if len(errors) == 0:
        return 'valid'
    else:
        return errors


def checkRegisterMatch(responseData):
    errors = {}
    if 'token' not in responseData:
        errors['token'] = ['No token']
    elif responseData['token'] is None:
        errors['token'] = ['Token is none']

    if 'username' not in responseData:
        errors['username'] = ['No username']
    elif responseData['username'] is None:
        errors['username'] = ['Username is none']

    if len(errors) == 0:
        return 'valid'
    else:
        return errors
