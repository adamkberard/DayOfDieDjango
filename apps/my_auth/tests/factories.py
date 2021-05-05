import factory

from ..models import CustomUser


class CustomUserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = CustomUser

    email = factory.Sequence(lambda n: '%d@example.com' % n)
    password = "pass4user"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Create an instance of the model, and save it to the database."""
        return CustomUser.objects.create_user(kwargs['email'], password=kwargs['password'])
