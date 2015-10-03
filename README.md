usage: citeulike.py [-h] -u USER [-j] [-b] [-o OUTPUT]

Simple CiteULike operations. Access granded through Firefox cookies.

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  CiteULike username [required]
  -j, --json            Save CiteULike JSON file [default:./${user}.json]
  -b, --bibtex          Save CiteULike JSON file [default:./${user}.json]
  -o OUTPUT, --output OUTPUT
                        Path to save CiteULike BibTeX/JSON file
                        [default:./${user}.{json,bib}]
