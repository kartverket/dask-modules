# validate_data_contract

Dependencies are declared inline in [validate_data_contract.py](validate_data_contract.py) (PEP 723
script metadata) and locked in [validate_data_contract.py.lock](validate_data_contract.py.lock). No `requirements.txt`.

- **Install uv:** `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Add a dependency:** `uv add --script validate_data_contract.py "some-package==1.2.3"`
- **Update the lockfile:** `uv lock --script validate_data_contract.py`
