import importlib


def test_import_app_module() -> None:
    module = importlib.import_module("app")
    assert module is not None
