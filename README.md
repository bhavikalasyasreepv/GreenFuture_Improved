# GreenFuture — Quiz Application

A local-first Python 3.10+ quiz record, scoring and analytics application built from the GreenFuture Hack Project #3 brief.

## Features
- Modern Tkinter desktop interface and a menu-driven terminal interface
- Topic-wise quiz records, automatic scoring and defensive validation
- Local JSON + CSV persistence and audit logging
- Keyword search and topic filtering
- Executive summaries, topic-level metrics and threshold/overdue warnings
- Matplotlib topic performance charts (optional dependency)
- Markdown, TXT audit and CSV report exports
- Bulk CSV import with row-by-row validation and error reporting
- 35 demonstration records across seven categories
- Missing/corrupt JSON recovery with a `.corrupt.json` backup

## Run
Python 3.10 or newer is recommended.

```bash
python main.py
```

Terminal mode:

```bash
python cli.py
```

Optional charts:

```bash
pip install -r requirements.txt
```

No internet connection or external API is required. Data is saved under `data/`.

## CSV import format
Required columns: `student,topic,question,options,correct_answer`.
Separate options using ` | `. Optional columns: `id,student_answer,score,max_score,created_at,deadline,status`.

Example:

```csv
student,topic,question,options,correct_answer,student_answer
Aarav,Python Basics,Which keyword defines a function?,func | def | lambda,def,def
```

## Project structure

```text
GreenFuture_Quiz_Application/
├── main.py
├── cli.py
├── requirements.txt
├── quiz_app/
│   ├── gui.py
│   ├── engine.py
│   ├── storage.py
│   ├── reports.py
│   └── sample_data.py
└── data/
    ├── records.json
    ├── records.csv
    └── audit.log
```

## Notes
- The brief describes a quiz application and does not prescribe a specific question-bank schema or authentication model. This implementation records each learner's question attempt as a durable record.
- Threshold warnings use a default 60% completion score and identify past deadlines for records not marked Completed.
- Tkinter is included with most standard Python distributions. On some Linux systems, install the OS package `python3-tk`.
