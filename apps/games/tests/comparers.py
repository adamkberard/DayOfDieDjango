# Just a bunch of helper funcs for testing games

def checkGameMatch(gameSetData, gameModelData, pointModelsData,
                   toAvoid=[]):
    errors = {}
    if 'game' not in gameSetData:
        errors['game'] = ['No game']
        return errors

    gameData = gameSetData['game']

    if 'points' not in toAvoid:
        if 'points' in gameData:
            if not pointsMatch(pointModelsData, gameData['points']):
                errors['game_points'] = ['Points do not match']
        else:
            errors['game_points'] = ['No game points']

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


def listDiff(list1, list2):
    out = [item for item in list1 if item not in list2]
    return out
