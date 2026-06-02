# Contributing

Contributions are welcome. The project is currently in an early research-prototype stage.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,analysis]"
pytest
```

## Design principles

1. Prefer transparent and reproducible metrics.
2. Keep Arabic preprocessing decisions explicit.
3. Avoid releasing identifiable student data.
4. Add tests for every new metric.
5. Document assumptions in the function docstring and in `docs/SCHEMA.md`.
