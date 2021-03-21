import datetime

import factory
import factory.fuzzy
import pytz

from apps.my_auth.factories import CustomUserFactory

from .models import Friend


class FriendFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Friend

    friendOne = factory.SubFactory(CustomUserFactory)
    friendTwo = factory.SubFactory(CustomUserFactory)
    status = Friend.PENDING

    timeRequested = factory.fuzzy.FuzzyDateTime(datetime.datetime(2021, 3, 12,
                                                tzinfo=pytz.utc))
    timeRespondedTo = factory.LazyAttribute(lambda o: o.timeRequested +
                                            datetime.timedelta(minutes=25))
