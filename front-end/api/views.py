from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from .serializers import *

from datetime import datetime, timedelta

import json

# convert string to time delta
def get_start_day(period, end):
    if period == 'ALL':
        return None
    if period == '30D':
        return end - timedelta(days=30)
    elif period == '90D':
        return end - timedelta(days=90)
    elif period == '1Y':
        return end - timedelta(days=365)
    elif period == '7D':
        return end - timedelta(days=7)
    elif period == '24H':
        return end - timedelta(days=1)
    elif period == '12H':
        return end - timedelta(hours=12)
    elif period == '1H':
        return end - timedelta(hours=1)

# API for vote count chart data
class VotesCountData(APIView):
    # Unused user authentication classes
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None, *args, **kwargs):
        # get resolution and period
        delta = kwargs['delta']
        period = kwargs['period']
        end = datetime.now()

        # retrieve correct model
        if delta == 'minute':
            self.model = votes_count_minute
        elif delta == 'hour':
            self.model = votes_count_hour
        elif delta == 'day':
            self.model = votes_count_day

        # calculate start
        start = get_start_day(period, end)

        # ALL or specific periode
        if start:
            ticker = self.model.objects.filter(timestamp__range=(start, end)).order_by('timestamp')
        else:
            ticker = self.model.objects.all().order_by('timestamp')
        serializer = VotesCount(ticker, many=True)


        x = []
        y = []

        # Omit last result, append data into lists
        for row in serializer.data[:-1]:
            x.append(row['timestamp'])
            y.append(row['count'])

        # datastruct for response
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

    def get(self, request, format=None, *args, **kwargs):
        # get resolution and period
        delta = kwargs['delta']
        period = kwargs['period']
        end = datetime.now()

        # retrieve correct model
        if delta == 'minute':
            self.model = transfers_count_minute
            start = end - timedelta(hours=1)
        elif delta == 'hour':
            self.model = transfers_count_hour
            start = end - timedelta(days=14)
        elif delta == 'day':
            self.model = transfers_count_day
            start = end - timedelta(days=60)

        # calculate start
        start = get_start_day(period, end)

        # ALL or specific period
        if start:
            ticker = self.model.objects.filter(timestamp__range=(start, end)).order_by('timestamp')
        else:
            ticker = self.model.objects.all().order_by('timestamp')
        serializer = TransfersCount(ticker, many=True)

        x = []
        y = []

        # Omit last result, append data into lists
        for row in serializer.data[:-1] :
            x.append(row['timestamp'])
            y.append(row['count'])

        # datastruct for response
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

    def get(self, request, format=None, *args, **kwargs):
        # get resolution and period
        delta = kwargs['delta']
        period = kwargs['period']
        end = datetime.now()

        # retrieve correct model
        if delta == 'minute':
            self.model = claim_rewards_count_minute
            start = end - timedelta(hours=1)
        elif delta == 'hour':
            self.model = claim_rewards_count_hour
            start = end - timedelta(days=7)
        elif delta == 'day':
            self.model = claim_rewards_count_day
            start = end - timedelta(days=60)

        # calculate start
        start = get_start_day(period, end)


        # ALL or specific period
        if start:
            ticker = self.model.objects.filter(timestamp__range=(start, end)).order_by('timestamp')
        else:
            ticker = self.model.objects.all().order_by('timestamp')
        serializer = TransfersCount(ticker, many=True)
        
        x = []
        y = []

        # Omit last result, append data into lists
        for row in serializer.data[:-1]:
            x.append(row['timestamp'])
            y.append(row['count'])

        # datastruct for response
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

    def get(self, request, format=None, *args, **kwargs):
        # resolution and type of analysis
        resolution = kwargs['resolution']
        analytics = kwargs['analytics']
        self.model = votes_count_sum

        # retrieve data from db and serialze
        ticker = self.model.objects.filter(resolution=resolution, analyses=analytics).order_by('-timestamp')[:1]
        serializer = VotesSum(ticker, many=True)

        return Response(serializer.data)

class GeneralStats(APIView):
    # Unused user authentication classes
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None, *args, **kwargs):
        # operation type
        operation = kwargs['operation']

        # retrieve correct model 
        if operation == 'votes':
            self.model = votes
        elif operation == 'transfers':
            self.model = transfers
        elif operation == 'claim_rewards':
            self.model = claim_rewards

        # timne period
        end = datetime.now()
        start = end - timedelta(days=1)

        # Retrieve all period and caculate changes
        count = self.model.objects.filter(timestamp__range=(start, end)).count()
        previous_count = self.model.objects.filter(
            timestamp__range=(start - timedelta(days=1), start)).count(
        )
        count_30d = self.model.objects.filter(
            timestamp__range=(end - timedelta(days=30), end - timedelta(days=29))).count(
        )
        count_365d = self.model.objects.filter(
            timestamp__range=(end - timedelta(days=365), end - timedelta(days=364))).count(
        )

        # retrieve latest block_num
        self.model = blocks 
        ticker = self.model.objects.all().order_by('-block_num')[:1]
        block = Blocks(ticker, many=True)

        # response datastruct
        data = {
            "operations": count,
            "block_num": block.data,
            "delta": '{:.2f}'.format((count-previous_count)/previous_count*100),
            "delta_30d": '{:.2f}'.format((count-count_30d)/count_30d*100),
            "delta_365d": '{:.2f}'.format((count-count_365d)/count_365d*100),
        }

        return Response(data)