from django.urls import path
from .views import VotesCountData, TransfersCountData, ClaimRewardsCountData, VotesSumData, GeneralStats

urlpatterns = [
    path('votes/<slug:delta>/<slug:period>', VotesCountData.as_view()),
    path('transfers/<slug:delta>/<slug:period>', TransfersCountData.as_view()),
    path('claim_rewards/<slug:delta>/<slug:period>', ClaimRewardsCountData.as_view()),
    path('table/votes/<slug:analyses>/<slug:resolution>', VotesSumData.as_view()),
    path('stats/<slug:operation>', GeneralStats.as_view())
]