import importlib


def test_app_entrypoint_has_main() -> None:
    module = importlib.import_module("app")
    assert hasattr(module, "main")
    assert callable(module.main)
