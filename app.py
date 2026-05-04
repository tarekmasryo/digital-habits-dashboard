"""Streamlit entrypoint.

Side effects stay behind ``main`` so unit tests and tooling can import this
module without requiring the Streamlit runtime to start immediately.
"""

from __future__ import annotations


def main() -> None:
    from hip.web.app import run

    run()


if __name__ == "__main__":
    main()
