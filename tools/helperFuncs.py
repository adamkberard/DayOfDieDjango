from apps.my_auth.models import Player


def convertToPK(data):
    terms = ['playerOne', 'playerTwo', 'playerThree', 'playerFour',
             'scorer', 'scoredOn']

    for term in terms:
        if term in data:
            username = data[term]
            if username is not None:
                data[term] = Player.objects.get(username=username, is_staff=False).id

    return data


def listDiff(list1, list2):
    return [item for item in list1 if item not in list2]
