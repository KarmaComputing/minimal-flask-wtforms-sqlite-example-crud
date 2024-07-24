# Flask WTforms Minimal example (CRUD)

Minimal example using WTforms with Fask + Sqlite database.

**WARNING** This project is vulnerable to SQL injection.
# Video

[![Video Minimal example using WTforms with Fask and Sqlite database ](https://img.youtube.com/vi/9fV1U6rwISA/0.jpg)](https://www.youtube.com/watch?v=9fV1U6rwISA)


# How to use

Read `__init__.py`

Install `rye` https://rye.astral.sh/
Activate the rye python environment
`rye sync`

Seed database
```
flask --app forms shell
from forms import init_db

init_db
```

Run flask
`flaks --app forms run --port 5000 --debug`

Observe app
http://127.0.0.1:5000

