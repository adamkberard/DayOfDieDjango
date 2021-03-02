from django.urls import path, register_converter

from tools.ids_encoder import converters

from .views import LitterViewDetail, LitterViewList

register_converter(converters.HashidsConverter, 'hashids')

urlpatterns = [
    path('', LitterViewList.as_view(), name='litter-list'),
    path('<hashids:litterId>/', LitterViewDetail.as_view(),
         name='litter-detail'),
]
