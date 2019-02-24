from django.urls import path
from .views import VotesCountData

urlpatterns = [
    path('<slug:type>/<slug:delta>', VotesCountData.as_view()),
]