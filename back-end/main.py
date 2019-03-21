from operations_account import *
from operations_comment import *
from operations_custom import *
from operations_escrow import *
from operations_orderbook import *
from operations_vote import *
from operations_wallet import *
from operations_witness import *
from steem_node import Node

from database import Database

import threading
import sys

if __name__ == "__main__":
    scraping = False
    valid = 0
    settings = {}

    # check for correct system arguments
    if len(sys.argv) == 4:
        block_num = sys.argv[1]
        block_count = sys.argv[2]
        n_threads = sys.argv[3]
        if block_num.isdigit():
            settings['block_num'] = int(block_num)
            settings['block_count'] = int(block_count)
            settings['n_threads'] = int(n_threads)
            settings['scraping'] = True
            scraping = True
            valid = 1
        else:
            print('User a number')
    elif len(sys.argv) == 1:
        valid = 1
    else:
        print('For scraping: python main.py <start_block> <blocks> <threads>')

    if valid:
        # queues for each different operation type
        arrays = {
            "vote_operation": [],
            "transfer_operation": [],
            "claim_reward_balance_operation": [],
            "custom_json_operation": [],
            "comment_operation": [],
            "comment_options_operation": [],
            "account_update_operation": [],
            "delegate_vesting_shares_operation": [],
            "transfer_to_vesting_operation": [],
            "account_witness_vote_operation": [],
            "feed_publish_operation": [],
            "limit_order_create_operation": [],
            "limit_order_cancel_operation": [],
            "delete_comment_operation": [],
            "account_create_with_delegation_operation": [],
            "withdraw_vesting_operation": [],
            "account_create_operation": [],
            "transfer_from_savings_operation": [],
            "transfer_to_savings_operation": [],
            "cancel_transfer_from_savings_operation": [],
            "witness_update_operation": [],
            "account_witness_proxy_operation": [],
            "custom_operation": [],
            "set_withdraw_vesting_route_operation": [],
            "recover_account_operation": [],
            "request_account_recovery_operation": [],
            "convert_operation": [],
            "escrow_release_operation": [],
            "escrow_transfer_operation": [],
            "escrow_approve_operation": [],
            "change_recovery_account_operation": [],
        }
        # shared lock between all operation threads
        lock = threading.Lock()

        # STEEM blockchain node api
        node = Node(arrays, lock, **settings)

        # processing threads for each operation type
        votes = Votes(
            'api_votes',
            arrays['vote_operation'],
            lock,
            scraping
        )

        transfers = Transfers(
            'api_transfers',
            arrays['transfer_operation'],
            lock,
            scraping
        )

        claim_rewards = Claim_rewards(
            'api_claim_rewards',
            arrays['claim_reward_balance_operation'],
            lock,
            scraping
        )

        custom_json_operations = Custom_json_operation(
            'api_custom_json_operation',
            arrays['custom_json_operation'],
            lock,
            scraping
        )

        comment_operations = Comment_operation(
            'api_comment_operation',
            arrays['comment_operation'],
            lock,
            scraping
        )

        comment_options_operations = Comment_options_operation(
            'api_comment_options_operation',
            arrays['comment_options_operation'],
            lock,
            scraping
        )

        account_update_operations = Account_update_operation(
            'api_account_update_operation',
            arrays['account_update_operation'],
            lock,
            scraping
        )

        delegate_vesting_shares_operations = Delegate_vesting_shares_operation(
            'api_delegate_vesting_shares_operation',
            arrays['delegate_vesting_shares_operation'],
            lock,
            scraping
        )

        transfer_to_vesting_operations = Transfer_to_vesting_operation(
            'api_transfer_to_vesting_operation',
            arrays['transfer_to_vesting_operation'],
            lock,
            scraping
        )

        account_witness_vote_operations = Account_witness_vote_operation(
            'api_account_witness_vote_operation',
            arrays['account_witness_vote_operation'],
            lock,
            scraping
        )

        feed_publish_operations = Feed_publish_operation(
            'api_feed_publish_operation',
            arrays['feed_publish_operation'],
            lock,
            scraping
        )

        limit_order_create_operations = Limit_order_create_operation(
            'api_limit_order_create_operation',
            arrays['limit_order_create_operation'],
            lock,
            scraping
        )

        limit_order_cancel_operations = Limit_order_cancel_operation(
            'api_limit_order_cancel_operation',
            arrays['limit_order_cancel_operation'],
            lock,
            scraping
        )

        delete_comment_operations = Delete_comment_operation(
            'api_delete_comment_operation',
            arrays['delete_comment_operation'],
            lock,
            scraping
        )

        account_create_with_delegation_operations = Account_create_with_delegation_operation(
            'api_account_create_with_delegation_operation',
            arrays['account_create_with_delegation_operation'],
            lock,
            scraping
        )

        account_create_operations = Account_create_operation(
            'api_account_create_operation',
            arrays['account_create_operation'],
            lock,
            scraping
        )

        withdraw_vesting_operations = Withdraw_vesting_operation(
            'api_withdraw_vesting_operation',
            arrays['withdraw_vesting_operation'],
            lock,
            scraping
        )

        transfer_from_savings_operations = Transfer_from_savings_operation(
            'api_transfer_from_savings_operation',
            arrays['transfer_from_savings_operation'],
            lock,
            scraping
        )

        transfer_to_savings_operations = Transfer_to_savings_operation(
            'api_transfer_to_savings_operation',
            arrays['transfer_to_savings_operation'],
            lock,
            scraping
        )

        cancel_transfer_from_savings_operations = Cancel_transfer_from_savings_operation(
            'api_cancel_transfer_from_savings_operation',
            arrays['cancel_transfer_from_savings_operation'],
            lock,
            scraping
        )

        witness_update_operations = Witness_update_operation(
            'api_witness_update_operation',
            arrays['witness_update_operation'],
            lock,
            scraping
        )

        account_witness_proxy_operations = Account_witness_proxy_operation(
            'api_account_witness_proxy_operation',
            arrays['account_witness_proxy_operation'],
            lock,
            scraping
        )

        custom_operations = Custom_operation(
            'api_custom_operation',
            arrays['custom_operation'],
            lock,
            scraping
        )

        set_withdraw_vesting_route_operations = Set_withdraw_vesting_route_operation(
            'api_set_withdraw_vesting_route_operation',
            arrays['set_withdraw_vesting_route_operation'],
            lock,
            scraping
        )

        recover_account_operations = Recover_account_operation(
            'api_recover_account_operation',
            arrays['recover_account_operation'],
            lock,
            scraping
        )

        request_account_recovery_operations = Request_account_recovery_operation(
            'api_request_account_recovery_operation',
            arrays['request_account_recovery_operation'],
            lock,
            scraping
        )

        convert_operations = Convert_operation(
            'api_convert_operation',
            arrays['convert_operation'],
            lock,
            scraping
        )

        escrow_release_operations = Escrow_release_operation(
            'api_escrow_release_operation',
            arrays['escrow_release_operation'],
            lock,
            scraping
        )

        escrow_approve_operations = Escrow_approve_operation(
            'api_escrow_approve_operation',
            arrays['escrow_approve_operation'],
            lock,
            scraping
        )

        escrow_transfer_operations = Escrow_transfer_operation(
            'api_escrow_transfer_operation',
            arrays['escrow_transfer_operation'],
            lock,
            scraping
        )

        change_recovery_account_operations = Change_recovery_account_operation(
            'api_change_recovery_account_operation',
            arrays['change_recovery_account_operation'],
            lock,
            scraping
        )

        # check for start block
        db = Database()
        data = db.get_last_block()
        if len(data) > 0 or settings.pop('block_num', None):
            # start all threads
            node.start()
            votes.start()
            claim_rewards.start()
            custom_json_operations.start()
            comment_operations.start()
            comment_options_operations.start()
            account_update_operations.start()
            delegate_vesting_shares_operations.start()
            transfer_to_vesting_operations.start()
            account_witness_vote_operations.start()
            feed_publish_operations.start()
            limit_order_create_operations.start()
            limit_order_cancel_operations.start()
            delete_comment_operations.start()
            account_create_with_delegation_operations.start()
            account_create_operations.start()
            withdraw_vesting_operations.start()
            transfer_from_savings_operations.start()
            transfer_to_savings_operations.start()
            cancel_transfer_from_savings_operations.start()
            witness_update_operations.start()
            account_witness_proxy_operations.start()
            custom_operations.start()
            set_withdraw_vesting_route_operations.start()
            recover_account_operations.start()
            request_account_recovery_operations.start()
            convert_operations.start()
            escrow_release_operations.start()
            escrow_approve_operations.start()
            escrow_transfer_operations.start()
            change_recovery_account_operations.start()
            transfers.start()
        else:
            print('Set start block')
