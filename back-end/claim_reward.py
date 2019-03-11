import operation


class Claim_rewards(operation.Operation):
    def __init__(self, table, storage, lock, scraping=False):
        operation.Operation.__init__(self, table, storage, lock, scraping)

    def process_operation(self, operation):
        account = operation['value']['account']
        reward_steem = operation['value']['reward_steem']['amount']
        reward_sbd = operation['value']['reward_sbd']['amount']
        reward_vests = operation['value']['reward_vests']['amount']
        self.db.add_claim_reward(
            account, reward_steem, reward_sbd,
            reward_vests, self.timestamp)

        # Allow for multiple resolutions
        hour = self.timestamp.hour
        minute = self.timestamp.minute

        steem = float(reward_steem)
        sbd = float(reward_sbd)
        vests = float(reward_vests)

        data = {
            "count": 1,
            "steem": steem,
            "sbd": sbd,
            "vests": vests,
        }
        
        self.counter.set_resolutions(hour, minute, **data)