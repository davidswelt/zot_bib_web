Zot/Bib/Web
===========

This tool generates interactive HTML bibliographies based on one or
more collections in the Zotero database.

Bibliographies are automatically sorted by collection.  BibTeX records
are provided for visitors to see, and PDF files are automatically
available via weblink.

The content generated is static.

Available on Github.


Requirements
-----------------------------------------
- Python installation
- Pyzotero
- Bibliographic entries in Zotero (as user or as group)


Installation
-----------------------------------------

- Install Pyzotero, a library for python:
  sudo pip install pyzotero
  
- At the top of zot.py, add configuration as documented.
  Go to zotero.org to get your API secret key.

- ensure zot.py is executable (chmod ug+x zot.py)
- run once/on demand, or install as cron job or service on a server
  Do not run it more than once a day. 

- include the resulting file zotero-bib.html (or as configured) in
  your website as you see fit.  You may also include individual
  collection files, which are also generated.
- You may want to style your bibliography using CSS.  An example style
  file is included.


Planned for future versions
-----------------------------------------

- writing to MySQL database for wordpress (so integration is easier -
  run it as cron job and you're done)



Author
-----------------------------------------
David Reitter, Penn State
