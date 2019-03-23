from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from .serializers import VotesCount, VotesSum, Blocks

from datetime import datetime, timedelta

import json

def get_start_day(period, end):
    switcher = {
        "ALL": None,
        "30D": end - timedelta(days=30),
        "90D": end - timedelta(days=90),
        "1Y": end - timedelta(days=365),
        "7D": end - timedelta(days=7),
        "24H": end - timedelta(days=1),
        "12H": end - timedelta(hours=12),
        "1H": end - timedelta(hours=1),
    }
    return switcher.get(period, "Invalid period")

# return count model for operation type
def get_model_count(operation):
    switcher = {
        "votes": votes_count_day,
        "transfers": transfers_count_day,
        "claim_rewards": claim_rewards_count_day,
        "delegate_vesting_shares_operation": delegate_vesting_shares_operation_count_day,
        "custom_json_operation": custom_json_operation_count_day,
        "comment_operation": comment_operation_count_day,
        "comment_options_operation": comment_options_operation_count_day,
        "account_update_operation": account_update_operation_count_day,
        "transfer_to_vesting_operation": transfer_to_vesting_operation_count_day,
        "account_witness_vote_operation": account_witness_vote_operation_count_day,
        "feed_publish_operation": feed_publish_operation_count_day,
        "limit_order_create_operation": limit_order_create_operation_count_day,
        "limit_order_cancel_operation": limit_order_cancel_operation_count_day,
        "delete_comment_operation": delete_comment_operation_count_day,
        "account_create_with_delegation_operation": account_create_with_delegation_operation_count_day,
        "withdraw_vesting_operation": withdraw_vesting_operation_count_day,
        "account_create_operation": account_create_operation_count_day,
        "transfer_from_savings_operation": transfer_from_savings_operation_count_day,
        "transfer_to_savings_operation": transfer_to_savings_operation_count_day,
        "cancel_transfer_from_savings_operation": cancel_transfer_from_savings_operation_count_day,
        "witness_update_operation": witness_update_operation_count_day,
        "account_witness_proxy_operation": account_witness_proxy_operation_count_day,
        "custom_operation": custom_operation_count_day,
        "set_withdraw_vesting_route_operation": set_withdraw_vesting_route_operation_count_day,
        "recover_account_operation": recover_account_operation_count_day,
        "request_account_recovery_operation": request_account_recovery_operation_count_day,
        "convert_operation": convert_operation_count_day,
        "escrow_release_operation": escrow_release_operation_count_day,
        "escrow_transfer_operation": escrow_transfer_operation_count_day,
        "escrow_approve_operation": escrow_approve_operation_count_day,
        "change_recovery_account_operation": change_recovery_account_operation_count_day,
    }
    return switcher.get(operation, "Invalid operation")

# return operation model for operation type
def get_model_operation(operation):
    switcher = {
        "votes": votes,
        "transfers": transfers,
        "claim_rewards": claim_rewards,
        "delegate_vesting_shares_operation": delegate_vesting_shares_operation,
        "custom_json_operation": custom_json_operation,
        "comment_operation": comment_operation,
        "comment_options_operation": comment_options_operation,
        "account_update_operation": account_update_operation,
        "transfer_to_vesting_operation": transfer_to_vesting_operation,
        "account_witness_vote_operation": account_witness_vote_operation,
        "feed_publish_operation": feed_publish_operation,
        "limit_order_create_operation": limit_order_create_operation,
        "limit_order_cancel_operation": limit_order_cancel_operation,
        "delete_comment_operation": delete_comment_operation,
        "account_create_with_delegation_operation": account_create_with_delegation_operation,
        "withdraw_vesting_operation": withdraw_vesting_operation,
        "account_create_operation": account_create_operation,
        "transfer_from_savings_operation": transfer_from_savings_operation,
        "transfer_to_savings_operation": transfer_to_savings_operation,
        "cancel_transfer_from_savings_operation": cancel_transfer_from_savings_operation,
        "witness_update_operation": witness_update_operation,
        "account_witness_proxy_operation": account_witness_proxy_operation,
        "custom_operation": custom_operation,
        "set_withdraw_vesting_route_operation": set_withdraw_vesting_route_operation,
        "recover_account_operation": recover_account_operation,
        "request_account_recovery_operation": request_account_recovery_operation,
        "convert_operation": convert_operation,
        "escrow_release_operation": escrow_release_operation,
        "escrow_transfer_operation": escrow_transfer_operation,
        "escrow_approve_operation": escrow_approve_operation,
        "change_recovery_account_operation": change_recovery_account_operation,
    }
    return switcher.get(operation, "Invalid operation")


# API for count chart data
class CountData(APIView):
    # Unused user authentication classes
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None, *args, **kwargs):
        # get resolution, period and operation type
        delta = kwargs['delta']
        period = kwargs['period']
        operation = kwargs['type']
        end = datetime.now()

        # get operation count model
        self.model = get_model_count(operation)

        # calculate start
        start = get_start_day(period, end)

        # ALL or specific periode
        if start:
            ticker = self.model.objects.filter(timestamp__range=(start, end)).order_by('timestamp')
        else:
            ticker = self.model.objects.all().order_by('timestamp')
        serializer = VotesCount(ticker, many=True)

        # datastruct for response
        data = []

        # Omit last result, append data into lists
        for row in serializer.data[:-1]:
            data.append({
                "date": row['timestamp'],
                "count": row['count'],
            })

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
        self.model = get_model_operation(operation)

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

        # filter for 0 values
        if previous_count == 0:
            delta = 'NaN'
        else:
            delta = '{:.2f}'.format((count-previous_count)/previous_count*100)

        if count_30d == 0:
            delta_30d = 'NaN'
        else:
            delta_30d = '{:.2f}'.format((count-count_30d)/count_30d*100)
        
        if count_365d == 0:
            delta_365d = 'NaN'
        else:
            delta_365d = '{:.2f}'.format((count-count_365d)/count_365d*100)


        # response datastruct
        data = {
            "operations": count,
            "block_num": block.data,
            "delta": delta,
            "delta_30d": delta_30d,
            "delta_365d": delta_365d,
        }

        return Response(data)