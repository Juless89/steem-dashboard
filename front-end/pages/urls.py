from django.urls import path

from .views import VotesView, TransfersView, ClaimRewardsView, IndexView

urlpatterns = [
    path('', IndexView.as_view()),
    path('votes', VotesView.as_view()),
    path('transfers', TransfersView.as_view()),
    path('claim_rewards', ClaimRewardsView.as_view()),
]