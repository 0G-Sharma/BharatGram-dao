import os
from algosdk import mnemonic, account
from algokit_utils import (
    get_algod_client,
    get_account,
    ApplicationClient,
    ApplicationSpecification,
)
from contract import approval_program, clear_state_program
from pyteal import compileTeal, Mode

# Configuration
ALGOD_ADDRESS = os.environ.get("ALGOD_ADDRESS", "https://testnet-api.algonode.cloud")
ALGOD_TOKEN = os.environ.get("ALGOD_TOKEN", "")
DEPLOYER_MNEMONIC = os.environ.get("DEPLOYER_MNEMONIC")

if not DEPLOYER_MNEMONIC:
    print("WARNING: DEPLOYER_MNEMONIC not set. Deployment will fail if not using localnet.")

def deploy():
    client = get_algod_client() # Defaults to localhost if no params, but we can override
    
    # In a real hackathon delivery, we'd use environment variables
    # For now, let's assume we have a way to get the account
    if DEPLOYER_MNEMONIC:
        deployer = get_account(client, mnemonic=DEPLOYER_MNEMONIC)
    else:
        # Default for local development (AlgoKit LocalNet)
        from algokit_utils import get_localnet_default_account
        deployer = get_localnet_default_account(client)

    print(f"Deploying from: {deployer.address}")

    # Compile programs
    approval_teal = compileTeal(approval_program(), mode=Mode.Application, version=8)
    clear_teal = compileTeal(clear_state_program(), mode=Mode.Application, version=8)

    # Note: Modern AlgoKit uses ApplicationSpecification, but for simplicity here
    # we'll do a direct deployment or use a wrapper.
    
    from algosdk.v2client import algod
    from algosdk import transaction

    # Compile on-chain
    def compile_program(client, source_code):
        compile_response = client.compile(source_code)
        import base64
        return base64.b64decode(compile_response['result'])

    # Application deployment
    params = client.suggested_params()
    
    txn = transaction.ApplicationCreateTxn(
        sender=deployer.address,
        sp=params,
        on_complete=transaction.OnComplete.NoOpOC,
        approval_program=compile_program(client, approval_teal),
        clear_program=compile_program(client, clear_teal),
        global_schema=transaction.StateSchema(num_uints=1, num_byte_slices=1), # total_projects, admin
        local_schema=transaction.StateSchema(num_uints=0, num_byte_slices=0),
        extra_pages=0
    )

    signed_txn = txn.sign(deployer.private_key)
    txid = client.send_transaction(signed_txn)
    print(f"Deployment Transaction ID: {txid}")
    
    # Wait for confirmation
    from algosdk.transaction import wait_for_confirmation
    confirmed = wait_for_confirmation(client, txid, 4)
    app_id = confirmed['application-index']
    print(f"✅ Smart Contract Deployed! App ID: {app_id}")
    
    return app_id

if __name__ == "__main__":
    deploy()
