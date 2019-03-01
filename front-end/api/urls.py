from django.urls import path
from .views import VotesCountData, TransfersCountData, ClaimRewardsCountData, VotesSumData

urlpatterns = [
    path('votes/<slug:delta>', VotesCountData.as_view()),
    path('transfers/<slug:delta>', TransfersCountData.as_view()),
    path('claim_rewards/<slug:delta>', ClaimRewardsCountData.as_view()),
    path('analyses/votes/<slug:analyses>/<slug:resolution>', VotesSumData.as_view()),
]