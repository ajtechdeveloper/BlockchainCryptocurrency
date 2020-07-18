import hashlib
import datetime
import json
import pprint


class Block:
    def __init__(self, timestamp, transaction, previous_block=''):
        self.timestamp = timestamp
        self.previousBlock = previous_block
        self.transaction = transaction
        self.difficultyIncrement = 7777
        self.hash = self.calculate_block_hash_key(transaction, timestamp, self.difficultyIncrement)

    def calculate_block_hash_key(self, data, timestamp, difficulty_increment):
        data = str(data) + str(timestamp) + str(difficulty_increment)
        data = data.encode()
        hash_key = hashlib.sha256(data)
        return hash_key.hexdigest()

    def mine_new_block(self, difficulty):
        difficulty_check = "3" * difficulty
        while self.hash[:difficulty] != difficulty_check:
            self.hash = self.calculate_block_hash_key(self.transaction, self.timestamp, self.difficultyIncrement)
            self.difficultyIncrement = self.difficultyIncrement + 1


class Blockchain:
    def __init__(self):
        self.chain = [self.genesis_block()]
        self.difficulty = 4
        self.pendingTransaction = []
        self.reward = 20

    def genesis_block(self):
        genesis_block = Block(str(datetime.datetime.now()), "This is the Genesis Block")
        return genesis_block

    def get_the_last_block(self):
        return self.chain[len(self.chain) - 1]

    def mine_pending_transaction(self, miner_reward_address):
        new_block = Block(str(datetime.datetime.now()), self.pendingTransaction)
        new_block.mine_new_block(self.difficulty)
        new_block.previousBlock = self.get_the_last_block().hash

        print("Previous Block's Hash key: " + new_block.previousBlock)
        transaction_chain = []
        for transaction in new_block.transaction:
            single_transaction = json.dumps(transaction.__dict__, indent=0, separators=(',', ': ')).replace("\n", "")
            transaction_chain.append(single_transaction)
        pprint.pprint(transaction_chain)

        self.chain.append(new_block)
        print("Block's Hash key: " + new_block.hash)
        print("New Block has been added"+ "\n")

        reward_transaction = Transaction("System", miner_reward_address, self.reward)
        self.pendingTransaction.append(reward_transaction)
        self.pendingTransaction = []

    def is_chain_valid(self):
        for x in range(1, len(self.chain)):
            current_block = self.chain[x]
            previous_block = self.chain[x - 1]

            if (current_block.previousBlock != previous_block.hash):
                return "\n"+"The Blockchain is not valid!"
        return "\n"+"The Blockchain is stable and valid"

    def create_transaction(self, transaction):
        self.pendingTransaction.append(transaction)

    def get_the_balance(self, wallet_address):
        balance = 0
        for block in self.chain:
            if block.previousBlock == "":
                continue
            for transaction in block.transaction:
                if transaction.fromWallet == wallet_address:
                    balance -= transaction.amount
                if transaction.toWallet == wallet_address:
                    balance += transaction.amount
        #Round Balance to 2 decimal places
        balance = round(balance,2)
        return balance


class Transaction:
    def __init__(self, fromWallet, toWallet, amount):
        self.fromWallet = fromWallet
        self.toWallet = toWallet
        self.amount = amount


alpha = Blockchain()
alpha.create_transaction(Transaction("Jane", "Jim", 7.4))
alpha.create_transaction(Transaction("Jane", "Mary", 3))

print("Frank started mining")

alpha.mine_pending_transaction("Frank")
alpha.create_transaction(Transaction("John", "Jim", 40.47))
alpha.create_transaction(Transaction("Steve", "Jane", 11))
alpha.create_transaction(Transaction("Mary", "John", 60))
alpha.create_transaction(Transaction("Jim", "Mary", 62.47))

print("Frank started mining")

alpha.mine_pending_transaction("Frank")
alpha.create_transaction(Transaction("John", "Steve", 15))
alpha.create_transaction(Transaction("John", "Jim", 16))
alpha.create_transaction(Transaction("Frank", "John", 15))

print("Frank started mining")
alpha.mine_pending_transaction("Frank")

# Frank earned 60 Alpha Coins by mining and gave 15 Alpha Coins to John. So Frank's balance is now 45 Alpha Coins
print("Frank has " + str(alpha.get_the_balance("Frank")) + " Alpha Coins on his account")
print("Jane has " + str(alpha.get_the_balance("Jane")) + " Alpha Coins on her account")
print("Jim has " + str(alpha.get_the_balance("Jim")) + " Alpha Coins on his account")
print("Mary has " + str(alpha.get_the_balance("Mary")) + " Alpha Coins on her account")
print("John has " + str(alpha.get_the_balance("John")) + " Alpha Coins on his account")
print("Steve has " + str(alpha.get_the_balance("Steve")) + " Alpha Coins on his account")
print(alpha.is_chain_valid())
