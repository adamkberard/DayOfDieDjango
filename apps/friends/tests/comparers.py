from tools.helperFunctions.helperFuncs import listDiff


def checkFriendMatch(responseFriendData, friendModelData, both=True,
                     toAvoid=[]):

    errors = {}
    if 'friend' not in responseFriendData:
        errors['friend'] = ['No friend']
        return errors

    friendData = responseFriendData['friend']

    # Fields here
    fields = ['status', 'timeRequested', 'timeRespondedTo', 'id']
    fieldsToTest = listDiff(fields, toAvoid)

    # First I take care of the user part of it
    if both:
        fields.append('requested')
        fields.append('requester')
    else:
        if 'friend' in friendData:
            response = friendData['friend']
            model1 = friendModelData['requester']
            model2 = friendModelData['requested']
            if (response != model1) and (response != model2):
                estr = '{} != {} or {}'.format(response, model1, model2)
                errors['friend_friend'] = [estr]
        else:
            errors['friend_friend'] = ['No friend friend']

    for field in fieldsToTest:
        if field in friendData:
            response = friendData[field]
            model = friendModelData[field]
            if response != model:
                estr = '{} != {}'.format(response, model)
                errors['friend_{}'.format(field)] = [estr]
        else:
            errors['friend_{}'.format(field)] = ['No friend {}'.format(field)]

    if len(errors) == 0:
        return 'valid'
    else:
        return errors
