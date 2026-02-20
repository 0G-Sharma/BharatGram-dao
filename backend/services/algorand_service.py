import os
import hashlib
import json

# Configuration from environment
ALGOD_ADDRESS = os.environ.get("ALGOD_ADDRESS", "https://testnet-api.algonode.cloud")
ALGOD_TOKEN = os.environ.get("ALGOD_TOKEN", "")
DEPLOYER_MNEMONIC = os.environ.get("DEPLOYER_MNEMONIC")
APP_ID = int(os.environ.get("ALGORAND_APP_ID", 0))


class AlgorandService:
    def __init__(self):
        self.app_id = APP_ID
        self.client = None
        self.deployer_sk = None
        self.deployer_address = None

        try:
            from algosdk.v2client import algod
            self.client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)
            print(f"[Algorand] Connected to node: {ALGOD_ADDRESS}")
        except Exception as e:
            print(f"[Algorand] Could not connect to node: {e}")

        if DEPLOYER_MNEMONIC:
            try:
                from algosdk import mnemonic, account
                self.deployer_sk = mnemonic.to_private_key(DEPLOYER_MNEMONIC)
                self.deployer_address = account.address_from_private_key(self.deployer_sk)
                print(f"[Algorand] Deployer loaded: {self.deployer_address}")
            except Exception as e:
                print(f"[Algorand] Could not load deployer wallet: {e}")

    def generate_project_hash(self, project_data: dict) -> bytes:
        """SHA256 hash of project details for on-chain integrity check."""
        data_str = json.dumps(project_data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).digest()

    def sync_project(self, project_id: int, budget: int, spent: int, project_data: dict, is_new=True):
        """Sync project data to Algorand Box Storage."""
        if not self.deployer_sk or self.app_id == 0 or not self.client:
            print(f"[Algorand] Skipping sync for project {project_id} (no credentials or App ID configured)")
            return None

        try:
            from algosdk import transaction
            params = self.client.suggested_params()
            status_hash = self.generate_project_hash(project_data)

            project_id_bytes = project_id.to_bytes(8, 'big')
            budget_bytes = budget.to_bytes(8, 'big')
            spent_bytes = spent.to_bytes(8, 'big')

            if is_new:
                app_args = [b"register", project_id_bytes, budget_bytes, spent_bytes, status_hash]
            else:
                app_args = [b"update", project_id_bytes, spent_bytes, status_hash]

            boxes = [(self.app_id, project_id_bytes)]
            txn = transaction.ApplicationNoOpTxn(
                sender=self.deployer_address,
                sp=params,
                index=self.app_id,
                app_args=app_args,
                boxes=boxes
            )
            signed_txn = txn.sign(self.deployer_sk)
            txid = self.client.send_transaction(signed_txn)
            print(f"[Algorand] Project {project_id} synced — TxID: {txid}")
            return txid
        except Exception as e:
            print(f"[Algorand] Sync error for project {project_id}: {e}")
            return None

    def get_on_chain_data(self, project_id: int):
        """Reads project data from Algorand Box Storage."""
        if self.app_id == 0 or not self.client:
            return None
        try:
            import base64
            project_id_bytes = project_id.to_bytes(8, 'big')
            box_response = self.client.application_box_by_name(self.app_id, project_id_bytes)
            raw = base64.b64decode(box_response['value'])
            budget = int.from_bytes(raw[0:8], 'big')
            spent = int.from_bytes(raw[8:16], 'big')
            status_hash = raw[16:48].hex()
            return {"budget": budget, "spent": spent, "hash": status_hash, "verified": True}
        except Exception as e:
            print(f"[Algorand] Read error for project {project_id}: {e}")
            return None


# Singleton — always succeeds even if blockchain is unavailable
algo_service = AlgorandService()
