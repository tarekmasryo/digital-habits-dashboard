"""Streamlit entrypoint.

We keep side effects behind a main-guard so the module can be imported in unit
tests (and by tooling) without starting the Streamlit runtime.
"""

from hip.web.app import run


def main() -> None:
    run()


if __name__ == "__main__":
    main()
