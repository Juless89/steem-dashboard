from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect

# redirect to /votes
class IndexView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect('/votes')

# vote operations
class VotesView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'votes.html')

# transfer operations
class TransfersView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'transfers.html')

# claim_rewards operations
class ClaimRewardsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'claim_rewards.html')