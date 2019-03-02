from django.urls import path
from .views import VotesCountData, TransfersCountData, ClaimRewardsCountData, VotesSumData

urlpatterns = [
    path('votes/<slug:delta>/<slug:period>', VotesCountData.as_view()),
    path('transfers/<slug:delta>/<slug:period>', TransfersCountData.as_view()),
    path('claim_rewards/<slug:delta>/<slug:period>', ClaimRewardsCountData.as_view()),
    path('table/votes/<slug:analyses>/<slug:resolution>', VotesSumData.as_view()),
]