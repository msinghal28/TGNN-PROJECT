import asyncio
import json
import os
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from datetime import datetime, timezone

# ------------------------- CONFIG ------------------------- #
ETH_WS = "wss://mainnet.infura.io/ws/v3/65aeaa5ff07340e38fc51789e05391a5"
BNB_WS = "wss://bsc-mainnet.blastapi.io/6e5f7b45-fc8e-4a89-a9ed-60db2513c3eb"

ETH_JSON_FILE = "ethereum_transactions.json"
BNB_JSON_FILE = "bnb_transactions.json"

# ------------------------- JSON SETUP ------------------------- #
def init_json(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump([], f)
        print(f"Created new JSON: {file_path}")

def append_to_json(file_path, row_dict):
    with open(file_path, 'r+') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []
        data.append(row_dict)
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()
    print(f"Appended: {row_dict['Blockchain Type']} Tx {row_dict['Transaction Hash'][:10]}...")

# ------------------------- ETHEREUM LISTENER ------------------------- #
async def ethereum_listener(json_path, poll_interval=10):
    try:
        w3 = Web3(Web3.LegacyWebSocketProvider(ETH_WS))
        if not w3.is_connected():
            print("[Ethereum] Failed to connect.")
            return

        last_block = w3.eth.block_number
        print(f"[Ethereum] Listening from block: {last_block}")

        while True:
            latest = w3.eth.block_number
            if latest > last_block:
                print(f"[Ethereum] New blocks: {last_block + 1} to {latest}")
                for bn in range(last_block + 1, latest + 1):
                    try:
                        block = w3.eth.get_block(bn, full_transactions=True)
                        for tx in block.transactions:
                            gas_fee = float(Web3.from_wei(tx.gas * (tx.gasPrice or 0), 'ether')) \
                                if hasattr(tx, 'gasPrice') and tx.gasPrice is not None else 0.0

                            append_to_json(json_path, {
                                "Timestamp": datetime.fromtimestamp(block.timestamp, timezone.utc).isoformat(),
                                "Blockchain Type": "Ethereum",
                                "Transaction Hash": tx.hash.hex(),
                                "Sender Address": tx['from'],
                                "Receiver Address": tx.to,
                                "Amount": float(Web3.from_wei(tx.value, 'ether')),
                                "Token Type": "ETH",
                                "Gas Fee": gas_fee,
                                "Smart Contract Address": tx.to if tx.to and tx.input != '0x' else None
                            })
                    except Exception as block_err:
                        print(f"[Ethereum] Block error {bn}: {block_err}")
                last_block = latest
            await asyncio.sleep(poll_interval)
    except Exception as e:
        print(f"[Ethereum] Listener error: {e}")
        await asyncio.sleep(5)
        asyncio.create_task(ethereum_listener(json_path, poll_interval))

# ------------------------- BNB LISTENER ------------------------- #
async def bnb_listener(json_path, poll_interval=10):
    try:
        w3 = Web3(Web3.LegacyWebSocketProvider(BNB_WS))
        w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

        if not w3.is_connected():
            print("[BNB Chain] Failed to connect.")
            return

        last_block = w3.eth.block_number
        print(f"[BNB Chain] Listening from block: {last_block}")

        while True:
            latest = w3.eth.block_number
            if latest > last_block:
                print(f"[BNB Chain] New blocks: {last_block + 1} to {latest}")
                for bn in range(last_block + 1, latest + 1):
                    try:
                        block = w3.eth.get_block(bn, full_transactions=True)
                        for tx in block.transactions:
                            gas_fee = float(Web3.from_wei(tx.gas * (tx.gasPrice or 0), 'ether')) \
                                if hasattr(tx, 'gasPrice') and tx.gasPrice is not None else 0.0

                            append_to_json(json_path, {
                                "Timestamp": datetime.fromtimestamp(block.timestamp, timezone.utc).isoformat(),
                                "Blockchain Type": "BNB Chain",
                                "Transaction Hash": tx.hash.hex(),
                                "Sender Address": tx['from'],
                                "Receiver Address": tx.to,
                                "Amount": float(Web3.from_wei(tx.value, 'ether')),
                                "Token Type": "BNB",
                                "Gas Fee": gas_fee,
                                "Smart Contract Address": tx.to if tx.to and tx.input != '0x' else None
                            })
                    except Exception as block_err:
                        print(f"[BNB Chain] Block error {bn}: {block_err}")
                last_block = latest
            await asyncio.sleep(poll_interval)
    except Exception as e:
        print(f"[BNB Chain] Listener error: {e}")
        await asyncio.sleep(5)
        asyncio.create_task(bnb_listener(json_path, poll_interval))

# ------------------------- MAIN ------------------------- #
async def main():
    init_json(ETH_JSON_FILE)
    init_json(BNB_JSON_FILE)
    print("Starting listeners...")
    await asyncio.gather(
        ethereum_listener(ETH_JSON_FILE),
        bnb_listener(BNB_JSON_FILE)
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down listeners...")
    except Exception as e:
        print(f"Main error: {e}")
