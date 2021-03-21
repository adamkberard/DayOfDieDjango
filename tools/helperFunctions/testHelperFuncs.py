# My additional testing methods
def pointsMatch(models, points):
    if len(models) != len(points):
        return False

    for model in models:
        for point in points:
            if (pointMatch(model, point)):
                points.remove(point)
                break

    return len(points) == 0


def pointMatch(model, point):
    if model.scorer.username != point['scorer']:
        return False
    if model.typeOfPoint != point['typeOfPoint']:
        return False
    if model.scoredOn is not None:
        if model.scoredOn.username != point['scoredOn']:
            return False
    return True


def friendsMatch(models, friends):
    if len(models) != len(friends):
        return False

    for model in models:
        for friend in friends:
            if (friendMatch(model, friend)):
                friends.remove(friend)
                break

    return len(friends) == 0


def friendMatch(model, friend):
    temp1 = model.friendOne.username == friend['friend']
    temp2 = model.friendTwo.username == friend['friend']
    if temp1 or temp2:
        dateFormatString = '%Y-%m-%d %H:%M:%S'
        temp = model.timeRequested.strftime(dateFormatString)
        if temp != friend['timeRequested']:
            return False
        temp = model.timeRespondedTo.strftime(dateFormatString)
        if temp != friend['timeRespondedTo']:
            return False

        # Now check the status
        if friend['status'] != model.status:
            return False

        # Then make sure we got an ID back
        if len(friend['id']) < 8:
            return False

        return True
    else:
        return False


def fullFriendsMatch(models, friends):
    if len(models) != len(friends):
        return False

    for model in models:
        for friend in friends:
            if (fullFriendMatch(model, friend)):
                friends.remove(friend)
                break

    return len(friends) == 0


def fullFriendMatch(model, friend):
    if model.friendOne.username != friend['friendOne']:
        return False
    if model.friendTwo.username != friend['friendTwo']:
        return False

    dateFormatString = '%Y-%m-%d %H:%M:%S'
    temp = model.timeRequested.strftime(dateFormatString)
    if temp != friend['timeRequested']:
        return False
    temp = model.timeRespondedTo.strftime(dateFormatString)
    if temp != friend['timeRespondedTo']:
        return False

    # Now check the status
    if model.status != friend['status']:
        return False

    # Then make sure we got an ID back
    if len(friend['id']) < 8:
        return False

    return True
