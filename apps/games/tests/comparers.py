# Just a bunch of helper funcs for testing games

def checkGameMatch(gameSetData, gameModelData, pointModelsData,
                   points=True, ids=True):
    errors = {}
    if 'game' not in gameSetData:
        errors['game'] = ['No game']
        return errors

    gameData = gameSetData['game']

    if points:
        if 'points' in gameData:
            if not pointsMatch(pointModelsData, gameData['points']):
                errors['game_points'] = ['Points do not match']
        else:
            errors['game_points'] = ['No game points']

    if 'timeStarted' in gameData:
        resp = gameData['timeStarted']
        mod = gameModelData['timeStarted']
        if resp != mod:
            estr = '{} != {}'.format(resp, mod)
            errors['game_timeStarted'] = [estr]
    else:
        errors['game_timeStarted'] = ['No game timeStarted']

    if 'timeSaved' in gameData:
        resp = gameData['timeSaved']
        mod = gameModelData['timeSaved']
        if resp != mod:
            estr = '{} != {}'.format(resp, mod)
            errors['game_timeSaved'] = [estr]
    else:
        errors['game_timeSaved'] = ['No game timeSaved']

    # Then I'll check the players
    fields = ['playerOne', 'playerTwo', 'playerThree', 'playerFour']
    for field in fields:
        if field in gameData:
            resp = gameData[field]
            mod = gameModelData[field]
            if resp != mod:
                estr = '{} != {}'.format(resp, mod)
                errors['game_{}'.format(field)] = [estr]
        else:
            errors['game_{}'.format(field)] = ['No {}'.format(field)]

    if ids:
        if 'id' in gameData:
            resp = gameData['id']
            mod = gameModelData['id']
            if resp != mod:
                estr = '{} != {}'.format(resp, mod)
                errors['game_id'.format()] = [estr]
        else:
            errors['game_id'] = ['No game id']

    if 'statType' in gameData:
        resp = gameData['statType']
        mod = gameModelData['statType']
        if resp != mod:
            estr = '{} != {}'.format(resp, mod)
    else:
        errors['game_statType'] = ['No game stat type']

    if len(errors) == 0:
        return 'valid'
    else:
        return errors


def pointsMatch(expectedPointsData, recievedPointsData):
    if len(expectedPointsData) != len(recievedPointsData):
        return False

    for expectedPointData in expectedPointsData:
        for recievedPointData in recievedPointsData:
            if (pointMatch(expectedPointData, recievedPointData)):
                recievedPointsData.remove(recievedPointData)
                break

    return len(recievedPointsData) == 0


def pointMatch(expectedData, recievedData):
    if expectedData['scorer'] != recievedData['scorer']:
        return False
    if expectedData['typeOfPoint'] != recievedData['typeOfPoint']:
        return False
    if expectedData['scoredOn'] != recievedData['scoredOn']:
        return False
    return True
