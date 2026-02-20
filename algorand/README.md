Algorand / AlgoKit Quickstart

This folder contains a minimal PyTeal smart contract and a Python deploy script (uses `algosdk`).

Options:
- AlgoKit CLI: follow AlgoKit docs to initialize and manage deployments (recommended for production and CI).
- Python (below): quick local deployment using `algosdk` + `pyteal`.

Setup (Python):
1. Create a virtualenv and install:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. Set environment variables (example for PureStake or local algod):

- `ALGOD_ADDRESS` (e.g. https://testnet-algorand.api.purestake.io/ps2)
- `ALGOD_TOKEN` (PureStake token or local algod token)
- `DEPLOYER_MNEMONIC` (mnemonic of the account that will create the app)

On Windows (PowerShell):

```powershell
$env:ALGOD_ADDRESS = "https://testnet-algorand.api.purestake.io/ps2"
$env:ALGOD_TOKEN = "<your-purestake-token>"
$env:DEPLOYER_MNEMONIC = "your 25-word mnemonic here"
```

3. Deploy the contract:

```bash
python deploy.py
```

Notes:
- For CI or more advanced flows, use AlgoKit CLI (https://developer.algorand.org/docs/algokit/).
- The deploy script here is an example; adapt it to your needs and secure keys appropriately.
