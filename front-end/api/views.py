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

# return count model for operation type
def get_model_count(operation):
    if operation == 'votes':
        return votes_count_day
    elif operation == 'transfers':
        return transfers_count_day
    elif operation == 'claim_rewards':
        return claim_rewards_count_day
    elif operation == 'delegate_vesting_shares_operation':
        return delegate_vesting_shares_operation_count_day
    elif operation == 'custom_json_operation':
        return custom_json_operation_count_day
    elif operation == 'comment_operation':
        return comment_operation_count_day
    elif operation == 'comment_options_operation':
        return comment_options_operation_count_day
    elif operation == 'account_update_operation':
        return account_update_operation_count_day
    elif operation == 'transfer_to_vesting_operation':
        return transfer_to_vesting_operation_count_day
    elif operation == 'account_witness_vote_operation':
        return account_witness_vote_operation_count_day
    elif operation == 'feed_publish_operation':
        return feed_publish_operation_count_day
    elif operation == 'limit_order_create_operation':
        return limit_order_create_operation_count_day
    elif operation == 'limit_order_cancel_operation':
        return limit_order_cancel_operation_count_day
    elif operation == 'delete_comment_operation':
        return delete_comment_operation_count_day
    elif operation == 'account_create_with_delegation_operation':
        return account_create_with_delegation_operation_count_day
    elif operation == 'withdraw_vesting_operation':
        return withdraw_vesting_operation_count_day
    elif operation == 'account_create_operation':
        return account_create_operation_count_day
    elif operation == 'transfer_from_savings_operation':
        return transfer_from_savings_operation_count_day
    elif operation == 'transfer_to_savings_operation':
        return transfer_to_savings_operation_count_day
    elif operation == 'cancel_transfer_from_savings_operation':
        return cancel_transfer_from_savings_operation_count_day
    elif operation == 'witness_update_operation':
        return witness_update_operation_count_day
    elif operation == 'account_witness_proxy_operation':
        return account_witness_proxy_operation_count_day
    elif operation == 'custom_operation':
        return custom_operation_count_day
    elif operation == 'set_withdraw_vesting_route_operation':
        return set_withdraw_vesting_route_operation_count_day
    elif operation == 'recover_account_operation':
        return recover_account_operation_count_day
    elif operation == 'request_account_recovery_operation':
        return request_account_recovery_operation_count_day
    elif operation == 'convert_operation':
        return convert_operation_count_day
    elif operation == 'escrow_release_operation':
        return escrow_release_operation_count_day
    elif operation == 'escrow_transfer_operation':
        return escrow_transfer_operation_count_day
    elif operation == 'escrow_approve_operation':
        return escrow_approve_operation_count_day
    elif operation == 'change_recovery_account_operation':
        return change_recovery_account_operation_count_day

# return operation model for operation type
def get_model_operation(operation):
    if operation == 'votes':
        return votes
    elif operation == 'transfers':
        return transfers
    elif operation == 'claim_rewards':
        return claim_rewards
    elif operation == 'delegate_vesting_shares_operation':
        return delegate_vesting_shares_operation
    elif operation == 'custom_json_operation':
        return custom_json_operation
    elif operation == 'comment_operation':
        return comment_operation
    elif operation == 'comment_options_operation':
        return comment_options_operation
    elif operation == 'account_update_operation':
        return account_update_operation
    elif operation == 'delegate_vesting_shares_operation':
        return delegate_vesting_shares_operation
    elif operation == 'transfer_to_vesting_operation':
        return transfer_to_vesting_operation
    elif operation == 'account_witness_vote_operation':
        return account_witness_vote_operation
    elif operation == 'feed_publish_operation':
        return feed_publish_operation
    elif operation == 'limit_order_create_operation':
        return limit_order_create_operation
    elif operation == 'limit_order_cancel_operation':
        return limit_order_cancel_operation
    elif operation == 'delete_comment_operation':
        return delete_comment_operation
    elif operation == 'account_create_with_delegation_operation':
        return account_create_with_delegation_operation
    elif operation == 'withdraw_vesting_operation':
        return withdraw_vesting_operation
    elif operation == 'account_create_operation':
        return account_create_operation
    elif operation == 'transfer_from_savings_operation':
        return transfer_from_savings_operation
    elif operation == 'transfer_to_savings_operation':
        return transfer_to_savings_operation
    elif operation == 'cancel_transfer_from_savings_operation':
        return cancel_transfer_from_savings_operation
    elif operation == 'witness_update_operation':
        return witness_update_operation
    elif operation == 'account_witness_proxy_operation':
        return account_witness_proxy_operation
    elif operation == 'custom_operation':
        return custom_operation
    elif operation == 'set_withdraw_vesting_route_operation':
        return set_withdraw_vesting_route_operation
    elif operation == 'recover_account_operation':
        return recover_account_operation
    elif operation == 'request_account_recovery_operation':
        return request_account_recovery_operation
    elif operation == 'convert_operation':
        return convert_operation
    elif operation == 'escrow_release_operation':
        return escrow_release_operation
    elif operation == 'escrow_transfer_operation':
        return escrow_transfer_operation
    elif operation == 'escrow_approve_operation':
        return escrow_approve_operation
    elif operation == 'change_recovery_account_operation':
        return change_recovery_account_operation

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