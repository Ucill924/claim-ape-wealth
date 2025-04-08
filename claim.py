from web3 import Web3
from eth_account import Account
from colorama import Fore, init
import time

init(autoreset=True)
rpc_url = "https://base-mainnet.public.blastapi.io/"
chain_id = 8453
w3 = Web3(Web3.HTTPProvider(rpc_url))

def claim(account_address, private_key):
    try:
        nonce = w3.eth.get_transaction_count(account_address)
        tx = {
            'to': "0x950349F1a3B155BE6ADD4684c67Fea46721B72Ed",
            'data': "0x4e71d92d",
            'value': 0,
            'gas': 300000,
            'maxFeePerGas': w3.to_wei(0.02, 'gwei'),
            'maxPriorityFeePerGas': w3.to_wei(0.02, 'gwei'),
            'nonce': nonce,
            'chainId': chain_id
        }
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(Fore.YELLOW + f"[{account_address}] ⏳ Menunggu receipt...")
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        if receipt.status == 1:
            print(Fore.GREEN + f"[{account_address}] ✅ Claim sukses! Tx: {tx_hash.hex()}")
        else:
            print(Fore.RED + f"[{account_address}] ❌ Claim gagal. Receipt status: {receipt.status}")
    except Exception as e:
        print(Fore.RED + f"[{account_address}] ⚠️ Error: {e}")

with open("pk.txt", "r") as f:
    private_keys = [line.strip() for line in f if line.strip()]
print(Fore.CYAN + f"🔍 Mulai claim untuk {len(private_keys)} wallet...\n")

for i, pk in enumerate(private_keys, 1):
    try:
        acct = Account.from_key(pk)
        address = acct.address
        print(Fore.BLUE + f"[{i}] 🔑 Wallet: {address}")
        claim(address, pk)
        time.sleep(2)
    except Exception as e:
        print(Fore.RED + f"[{i}] ⚠️ Gagal proses wallet: {e}")
