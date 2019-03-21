from django.urls import path

from .views import VotesView, TransfersView, ClaimRewardsView, IndexView, OperationView

urlpatterns = [
    path('', IndexView.as_view()),
    path('<slug:operation>', OperationView.as_view()),
]