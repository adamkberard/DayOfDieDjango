# My additional testing methods
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
