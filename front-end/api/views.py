from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from .serializers import *

from datetime import datetime, timedelta

def get_start_day(period, end):
    if period == 'ALL':
        return None
    if period == '30D':
        return end - timedelta(days=30)
    elif period == '7D':
        return end - timedelta(days=7)
    elif period == '24H':
        return end - timedelta(days=1)
    elif period == '12H':
        return end - timedelta(hours=12)
    elif period == '1H':
        return end - timedelta(hours=1)

class VotesCountData(APIView):
    # Unused user authentication classes
    authentication_classes = []
    permission_classes = []

    # Retrieve STEEM and SBD market prices, return a dict
    def get(self, request, format=None, *args, **kwargs):
        delta = kwargs['delta']
        period = kwargs['period']
        end = datetime.now()

        if delta == 'minute':
            self.model = votes_count_minute
        elif delta == 'hour':
            self.model = votes_count_hour
        elif delta == 'day':
            self.model = votes_count_day

        start = get_start_day(period, end)

        if start:
            ticker = self.model.objects.filter(timestamp__range=(start, end)).order_by('timestamp')
        else:
            ticker = self.model.objects.all().order_by('timestamp')
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
        period = kwargs['period']
        end = datetime.now()

        if delta == 'minute':
            self.model = transfers_count_minute
            start = end - timedelta(hours=1)
        elif delta == 'hour':
            self.model = transfers_count_hour
            start = end - timedelta(days=14)
        elif delta == 'day':
            self.model = transfers_count_day
            start = end - timedelta(days=60)

        start = get_start_day(period, end)

        if start:
            ticker = self.model.objects.filter(timestamp__range=(start, end)).order_by('timestamp')
        else:
            ticker = self.model.objects.all().order_by('timestamp')
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
        period = kwargs['period']
        end = datetime.now()

        if delta == 'minute':
            self.model = claim_rewards_count_minute
            start = end - timedelta(hours=1)
        elif delta == 'hour':
            self.model = claim_rewards_count_hour
            start = end - timedelta(days=7)
        elif delta == 'day':
            self.model = claim_rewards_count_day
            start = end - timedelta(days=60)

        start = get_start_day(period, end)

        if start:
            ticker = self.model.objects.filter(timestamp__range=(start, end)).order_by('timestamp')
        else:
            ticker = self.model.objects.all().order_by('timestamp')
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

class VotesSumData(APIView):
    # Unused user authentication classes
    authentication_classes = []
    permission_classes = []

    # Retrieve STEEM and SBD market prices, return a dict
    def get(self, request, format=None, *args, **kwargs):
        resolution = kwargs['resolution']
        analyses = kwargs['analyses']
        self.model = votes_count_sum

        ticker = self.model.objects.filter(resolution=resolution, analyses=analyses).order_by('-timestamp')[:1]
        serializer = VotesSum(ticker, many=True)

        return Response(serializer.data)