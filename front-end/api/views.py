from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import votes_count_minute, votes_count_hour, votes_count_day
from .serializers import VotesCount

# APIview for coinmarketcap STEEM and SBD ticker prices.
class VotesCountData(APIView):
    # Unused user authentication classes
    authentication_classes = []
    permission_classes = []

    # Retrieve STEEM and SBD market prices, return a dict
    def get(self, request, format=None, *args, **kwargs):
        type = kwargs['type']
        delta = kwargs['delta']

        if type == 'votes':
            self.model = votes_count_hour

        ticker = self.model.objects.all()
        serializer = VotesCount(ticker, many=True)
        x = []
        y = []

        for row in serializer.data:
            x.append(row['timestamp'])
            y.append(row['count'])

        data = {
            "labels": x,
            "data": y,
        }

        return Response(data)