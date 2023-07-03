from django.urls import path
from .views import *


urlpatterns = [
    path('newsletter/list', NewsletterListView.as_view()),
    path('newsletter/create', NewsletterCreateView.as_view()),
    path('newsletter/<int:pk>', NewsletterUpdateDeleteView.as_view()),
    path('client/list', ClientListView.as_view()),
    path('client/create', ClientCreateView.as_view()),
    path('client/<int:pk>', ClientUpdateDeleteView.as_view()),
    path('statistics/<int:pk>', StatistikDetail.as_view()),
    path('statistic', StatistickAllView.as_view()),
]
