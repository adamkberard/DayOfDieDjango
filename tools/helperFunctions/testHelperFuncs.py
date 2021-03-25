# My additional testing methods


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
    temp1 = model.requester.username == friend['friend']
    temp2 = model.requested.username == friend['friend']
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
    if model.requester.username != friend['requester']:
        return False
    if model.requested.username != friend['requested']:
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


def teamsMatch(models, teams):
    if len(models) != len(teams):
        return False

    for model in models:
        for team in teams:
            if (teamMatch(model, team)):
                teams.remove(team)
                break

    return len(teams) == 0


def teamMatch(model, team):
    temp1 = model.teamCaptain.username == team['partner']
    temp2 = model.teammate.username == team['partner']
    if temp1 or temp2:
        dateFormatString = '%Y-%m-%d %H:%M:%S'
        temp = model.timeRequested.strftime(dateFormatString)
        if temp != team['timeRequested']:
            return False
        temp = model.timeRespondedTo.strftime(dateFormatString)
        if temp != team['timeRespondedTo']:
            return False

        # Now check the status
        if team['status'] != model.status:
            return False

        # Now check the league
        if team['league'] != model.league:
            return False

        # Then make sure we got an ID back
        if len(team['id']) < 8:
            return False

        return True
    else:
        return False


def fullTeamsMatch(models, teams):
    if len(models) != len(teams):
        return False

    for model in models:
        for team in teams:
            if (fullTeamMatch(model, team)):
                teams.remove(team)
                break

    return len(teams) == 0


def fullTeamMatch(model, team):
    if model.teamCaptain.username != team['teamCaptain']:
        return False
    if model.teammate.username != team['teammate']:
        return False

    dateFormatString = '%Y-%m-%d %H:%M:%S'
    temp = model.timeRequested.strftime(dateFormatString)
    if temp != team['timeRequested']:
        return False
    temp = model.timeRespondedTo.strftime(dateFormatString)
    if temp != team['timeRespondedTo']:
        return False

    # Now check the status
    if model.status != team['status']:
        return False

    # Now check the league
    if team['league'] != model.league:
        return False

    # Then make sure we got an ID back
    if len(team['id']) < 8:
        return False

    return True
