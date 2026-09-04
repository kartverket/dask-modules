# validate_data_contract

Dependencies for [validate_data_contract.py](validate_data_contract.py) are declared directly in the
script itself, using [PEP 723](https://peps.python.org/pep-0723/) inline script metadata (the
`# /// script ... # ///` block at the top of the file). There is no `requirements.txt`.

The script is run with [uv](https://docs.astral.sh/uv/), which reads that metadata and the
adjacent [validate_data_contract.py.lock](validate_data_contract.py.lock) lockfile to install an
exact, reproducible set of dependencies before running.

## Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

See the [uv installation docs](https://docs.astral.sh/uv/getting-started/installation/) for other
methods (Homebrew, pipx, pip, Windows, etc.).

## Add a new dependency

```bash
uv add --script validate_data_contract.py "some-package==1.2.3"
```

This updates the `dependencies` array in the script's metadata block and re-locks automatically.

## Update the lockfile

If you edit the `dependencies` list by hand, or want to refresh to the latest compatible
versions, regenerate the lock:

```bash
uv lock --script validate_data_contract.py
```

Commit the updated `validate_data_contract.py.lock` alongside your change.
