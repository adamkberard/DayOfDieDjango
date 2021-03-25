from tools.helperFuncs import listDiff


def checkTeamMatch(responseTeamData, teamModelData, both=True,
                   toAvoid=[]):

    errors = {}
    if 'team' not in responseTeamData:
        errors['team'] = ['No team']
        return errors

    teamData = responseTeamData['team']

    # Fields here
    fields = ['status', 'timeRequested', 'timeRespondedTo', 'id', 'league']
    fieldsToTest = listDiff(fields, toAvoid)

    # First I take care of the user part of it
    if both:
        fields.append('teamCaptain')
        fields.append('teammate')
    else:
        if 'teammate' in teamData:
            response = teamData['teammate']
            model1 = teamModelData['teamCaptain']
            model2 = teamModelData['teammate']
            if (response != model1) and (response != model2):
                estr = '{} != {} or {}'.format(response, model1, model2)
                errors['team_teammate'] = [estr]
        else:
            errors['team_teammate'] = ['No team teammate']

    for field in fieldsToTest:
        if field in teamData:
            response = teamData[field]
            model = teamModelData[field]
            if response != model:
                estr = '{} != {}'.format(response, model)
                errors['team_{}'.format(field)] = [estr]
        else:
            errors['team_{}'.format(field)] = ['No team {}'.format(field)]

    if len(errors) == 0:
        return 'valid'
    else:
        return errors
