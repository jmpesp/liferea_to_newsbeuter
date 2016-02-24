
This repository stores scripts necessary to move cached RSS content
from Liferea's DB to Newsbeuter's DB.

First, run `01-export-from-liferea.py` in `~/.local/share/liferea/` (or
where liferea.db is on your system). This will output JSON to stdout so
redirect it into a file named items.json. Move items.json into
`~/.newsbeuter/`.

Next, run `02-import-into-newsbeuter.py` in `~/.newsbeuter/`. This
script will verbosely log what it is doing so I recommend dumping the
output into a .log file.

