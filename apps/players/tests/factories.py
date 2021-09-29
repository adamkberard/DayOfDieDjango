import factory

from apps.players.models import Player

# Common variable
DEFAULT_PASSWORD = 'pass4user'


class PlayerFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Player

    email = factory.Sequence(lambda n: '%d@example.com' % n)
    password = DEFAULT_PASSWORD

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Create an instance of the model, and save it to the database."""
        return Player.objects.create_user(email=kwargs['email'], password=kwargs['password'])
