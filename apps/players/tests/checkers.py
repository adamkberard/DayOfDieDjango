from apps.core.checker import BaseChecker


class BasicUserTesting(BaseChecker):
    fields = ['username', 'uuid', 'wins', 'losses']


class PlayerTesting(BaseChecker):
    fields = ['email', 'username', 'uuid', 'wins', 'losses']
