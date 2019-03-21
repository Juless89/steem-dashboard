from django.urls import path
from .views import VotesSumData, GeneralStats, CountData

urlpatterns = [
    path('<slug:type>/<slug:delta>/<slug:period>', CountData.as_view()),
    path('table/votes/<slug:analytics>/<slug:resolution>', VotesSumData.as_view()),
    path('stats/<slug:operation>', GeneralStats.as_view())
]