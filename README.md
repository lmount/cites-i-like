cites-i-like
============
Simple command line CiteULike operations. Access granted through Firefox cookies.

```javascript

usage: cites-i-like.py [-h] -u USER [-j] [-b] [-p] [-o OUTPUT]

Simple CiteULike operations. Access granted through Firefox cookies.

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  CiteULike username [required]
  -j, --json            Save CiteULike JSON file [default:./${user}.json]
  -b, --bibtex          Save CiteULike JSON file [default:./${user}.json]
  -p, --pdf             Save PDF files of a CiteULike account (requires
                        Firefox cookies). [default:./${user}_pdf/]
  -o OUTPUT, --output OUTPUT
                        Path to save CiteULike BibTeX/JSON file
                        [default:./${user}{.json,.bib,_pdf}]
```
