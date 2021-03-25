# Just a bunch of helper funcs for testing friends

def checkFriendMatch(responseFriendData, modelFriendData, points=True,
                     ids=True, both=True, times=True):
    errors = {}
    if 'friend' not in responseFriendData:
        errors['friend'] = ['No friend']
        return errors

    friendData = responseFriendData['friend']

    if 'status' in friendData:
        resp = friendData['status']
        mod = modelFriendData['status']
        if resp != mod:
            estr = '{} != {}'.format(resp, mod)
            errors['friend_status'] = [estr]
    else:
        errors['friend_status'] = ['No friend status']

    if times:
        if 'timeRequested' in friendData:
            resp = friendData['timeRequested']
            mod = modelFriendData['timeRequested']
            if resp != mod:
                estr = '{} != {}'.format(resp, mod)
                print("ESTR: {}".format(estr))
                errors['friend_timeRequested'] = [estr]
        else:
            errors['friend_timeRequested'] = ['No friend timeRequested']

        if 'timeRespondedTo' in friendData:
            resp = friendData['timeRespondedTo']
            mod = modelFriendData['timeRespondedTo']
            if resp != mod:
                estr = '{} != {}'.format(resp, mod)
                errors['friend_timeRespondedTo'] = [estr]
        else:
            errors['friend_timeRespondedTo'] = ['No friend timeRespondedTo']

    if both:
        if 'requester' in friendData:
            resp = friendData['requester']
            mod = modelFriendData['requester']
            if resp != mod:
                estr = '{} != {}'.format(resp, mod)
                errors['friend_requester'] = [estr]
        else:
            errors['friend_requester'] = ['No friend requester']

        if 'requested' in friendData:
            resp = friendData['requested']
            mod = modelFriendData['requested']
            if resp != mod:
                estr = '{} != {}'.format(resp, mod)
                errors['friend_requested'] = [estr]
        else:
            errors['friend_requested'] = ['No friend requested']
    else:
        if 'friend' in friendData:
            resp = friendData['friend']
            mod2 = modelFriendData['requester']
            mod1 = modelFriendData['requested']
            if (resp != mod1) and (resp != mod2):
                estr = '{} != {} or {}'.format(resp, mod1, mod2)
                errors['friend_friend'] = [estr]
        else:
            errors['friend_friend'] = ['No friend friend']

    if ids:
        if 'id' in friendData:
            resp = friendData['id']
            mod = modelFriendData['id']
            if resp != mod:
                estr = '{} != {}'.format(resp, mod)
                errors['friend_id'.format()] = [estr]
        else:
            errors['friend_id'] = ['No friend id']

    if len(errors) == 0:
        return 'valid'
    else:
        return errors
