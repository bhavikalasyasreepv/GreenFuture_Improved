"""Menu-driven terminal interface for the GreenFuture Quiz Application."""
from __future__ import annotations

from datetime import date

from quiz_app.storage import load_records, save_records
from quiz_app.engine import create_record, summary, warnings, filtered
from quiz_app.reports import export_report
from quiz_app.sample_data import seed

MENU = """\n====================================================
       GREENFUTURE | QUIZ APPLICATION
====================================================
1. Create quiz result
2. View executive summary
3. Search records
4. View warnings
5. Export reports
6. Load sample records
0. Exit
"""


def ask(label: str, *, allow_blank: bool = False) -> str:
    """Prompt until a non-empty value is entered (unless blank is allowed)."""
    while True:
        try:
            value = input(label).strip()
        except EOFError:
            raise KeyboardInterrupt from None
        if value or allow_blank:
            return value
        print("This field cannot be blank. Please try again.")


def ask_deadline() -> str:
    """Accept an optional deadline and validate its ISO date format."""
    while True:
        value = ask("Deadline YYYY-MM-DD (optional): ", allow_blank=True)
        if not value:
            return ""
        try:
            date.fromisoformat(value)
            return value
        except ValueError:
            print("Please enter a valid date in YYYY-MM-DD format, or leave blank.")


def create_quiz(records: list[dict]) -> None:
    student = ask("Student name: ")
    topic = ask("Topic: ")
    question = ask("Question: ")
    options = [ask(f"Option {i}: ") for i in range(1, 5)]
    correct = ask("Correct answer (exact option text): ")
    chosen = ask("Student answer (exact option text): ")
    deadline = ask_deadline()

    record = create_record(student, topic, question, options, correct, chosen, deadline)
    records.append(record)
    save_records(records)
    print(f"\nSaved successfully. Score: {record['score']}/{record['max_score']}")


def show_summary(records: list[dict]) -> None:
    data = summary(records)
    print(f"\nRecords: {data['records']} | Score: {data['score']}/{data['possible']} | Average: {data['percentage']}%")
    if not data.get("topics"):
        print("No topic data available yet.")
        return
    print("\nTopic performance:")
    for topic, values in sorted(data["topics"].items()):
        percent = 100 * values["score"] / max(1, values["max"])
        print(f"  {topic}: {values['score']}/{values['max']} ({percent:.1f}%)")


def search_records(records: list[dict]) -> None:
    keyword = ask("Keyword (student/question/topic): ", allow_blank=True)
    topic = ask("Topic (blank for all): ", allow_blank=True) or "All"
    results = filtered(records, keyword, topic)
    if not results:
        print("No matching records found.")
        return
    print("\nID | Student | Topic | Score")
    print("-" * 72)
    for record in results:
        print(f"{record.get('id', '—')} | {record.get('student', '—')} | {record.get('topic', '—')} | {record.get('score', 0)}/{record.get('max_score', 0)}")


def show_warnings(records: list[dict]) -> None:
    items = warnings(records)
    print("\n" + ("\n".join(items) if items else "No warnings."))


def export(records: list[dict]) -> None:
    folder = ask("Export folder [reports]: ", allow_blank=True) or "reports"
    paths = export_report(records, folder)
    if not paths:
        print("No reports were generated.")
    else:
        for path in paths:
            print("Created:", path)


def load_samples() -> list[dict]:
    seed()
    updated = load_records()
    print(f"Loaded sample data. Total records: {len(updated)}")
    return updated


def main() -> None:
    records = load_records()
    actions = {
        "1": lambda: create_quiz(records),
        "2": lambda: show_summary(records),
        "3": lambda: search_records(records),
        "4": lambda: show_warnings(records),
        "5": lambda: export(records),
        "6": lambda: None,
    }

    while True:
        print(MENU)
        try:
            choice = ask("Select an option: ", allow_blank=True)
            if choice == "0":
                print("Goodbye!")
                return
            if choice == "6":
                records = load_samples()
                # Rebind the actions that close over the records list.
                actions = {
                    "1": lambda: create_quiz(records),
                    "2": lambda: show_summary(records),
                    "3": lambda: search_records(records),
                    "4": lambda: show_warnings(records),
                    "5": lambda: export(records),
                }
                continue
            action = actions.get(choice)
            if action is None:
                print("Please choose one of the menu options (0–6).")
                continue
            action()
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except (ValueError, OSError) as exc:
            print(f"\nCould not complete action: {exc}")
        except Exception as exc:
            print(f"\nUnexpected error: {exc}")
            print("The application is still running; please try again.")


if __name__ == "__main__":
    main()
