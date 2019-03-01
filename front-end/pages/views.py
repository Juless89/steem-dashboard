from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect

# Create your views here.
class IndexView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect('/votes')

class VotesView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'votes.html')

class TransfersView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'transfers.html')

class ClaimRewardsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'claim_rewards.html')