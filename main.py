"""Entry point for the GreenFuture Quiz Application desktop interface."""


def main() -> None:
    try:
        from quiz_app.gui import launch
    except ImportError as exc:
        raise SystemExit(
            "The desktop interface could not be loaded. Ensure the quiz_app package "
            "and its gui.py module are present in the project directory."
        ) from exc
    launch()


if __name__ == "__main__":
    main()
