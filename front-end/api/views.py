from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from .serializers import *

from datetime import datetime

class VotesCountData(APIView):
    # Unused user authentication classes
    authentication_classes = []
    permission_classes = []

    # Retrieve STEEM and SBD market prices, return a dict
    def get(self, request, format=None, *args, **kwargs):
        delta = kwargs['delta']

        if delta == 'minute':
            self.model = votes_count_minute
        elif delta == 'hour':
            self.model = votes_count_hour
        elif delta == 'day':
            self.model = votes_count_day

        start = '2019-01-01'
        end = '2019-01-31'
        ticker = self.model.objects.filter(timestamp__range=(start, end)).order_by('timestamp')
        serializer = VotesCount(ticker, many=True)
        x = []
        y = []

        for row in serializer.data:
            x.append(row['timestamp'])
            y.append(row['count'])

        data = {
            "label": '# of Votes',
            "labels": x,
            "data": y,
        }

        return Response(data)

class TransfersCountData(APIView):
    # Unused user authentication classes
    authentication_classes = []
    permission_classes = []

    # Retrieve STEEM and SBD market prices, return a dict
    def get(self, request, format=None, *args, **kwargs):
        delta = kwargs['delta']

        if delta == 'minute':
            self.model = transfers_count_minute
        elif delta == 'hour':
            self.model = transfers_count_hour
        elif delta == 'day':
            self.model = transfers_count_day

        start = '2019-01-01'
        end = '2019-01-31'
        ticker = self.model.objects.filter(timestamp__range=(start, end)).order_by('timestamp')
        serializer = TransfersCount(ticker, many=True)
        x = []
        y = []

        for row in serializer.data:
            x.append(row['timestamp'])
            y.append(row['count'])

        data = {
            "label": '# of Transfers',
            "labels": x,
            "data": y,
        }

        return Response(data)

class ClaimRewardsCountData(APIView):
    # Unused user authentication classes
    authentication_classes = []
    permission_classes = []

    # Retrieve STEEM and SBD market prices, return a dict
    def get(self, request, format=None, *args, **kwargs):
        delta = kwargs['delta']

        if delta == 'minute':
            self.model = claim_rewards_count_minute
        elif delta == 'hour':
            self.model = claim_rewards_count_hour
        elif delta == 'day':
            self.model = claim_rewards_count_day

        start = '2019-01-01'
        end = '2019-01-31'
        ticker = self.model.objects.filter(timestamp__range=(start, end)).order_by('timestamp')
        serializer = TransfersCount(ticker, many=True)
        x = []
        y = []

        for row in serializer.data:
            x.append(row['timestamp'])
            y.append(row['count'])

        data = {
            "label": '# of Claim rewards',
            "labels": x,
            "data": y,
        }

        return Response(data)