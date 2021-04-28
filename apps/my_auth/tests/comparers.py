def checkLoginMatch(response, userData, gamesData, friendsData, toAvoid=[]):
    errors = {}
    if 'token' in response:
        # Can check maybe length or something honestly idk
        pass
    else:
        errors['token'] = ['No token']

    if 'user' in response:
        # Probably run user comparer
        pass
    else:
        errors['user'] = ['No user']

    if 'games' in response:
        # Probably run game comparer
        # Also make sure it's a list
        pass
    else:
        errors['games'] = ['No games']

    if 'friends' in response:
        # Probably run friend comparer
        # Also make sure it's a list
        pass
    else:
        errors['friends'] = ['No friends']

    # Other Fields that are much simpler
    fields = ['timeStarted', 'timeSaved', 'playerOne', 'playerTwo',
              'playerThree', 'playerFour', 'statType', 'id']
    fieldsToTest = listDiff(fields, toAvoid)

    for field in fieldsToTest:
        if field in gameData:
            response = gameData[field]
            model = gameModelData[field]
            if response != model:
                estr = '{} != {}'.format(response, model)
                errors['game_{}'.format(field)] = [estr]
        else:
            errors['game_{}'.format(field)] = ['No game {}'.format(field)]

    if len(errors) == 0:
        return 'valid'
    else:
        return errors
