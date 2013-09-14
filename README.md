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

For HTML generation or inclusion in any website:
- run once/on demand, or install as cron job or service on a server
  Do not run it more than once a day. 
- include the resulting file zotero-bib.html (or as configured) in
  your website as you see fit.  You may also include individual
  collection files, which are also generated.
- You may want to style your bibliography using CSS.  An example style
  file is included.

For Wordpress inclusion:
- create a page or a post for the bibliography. Insert
  [zot_bib_web COLLECTION] where you'd like the bibliography
  inserted. (More options: see push.py)
- configure push.py (at the top) and make sure it is executable
- run push.py regularly or on demand

push.py can automatically update the Wordpress page with the
bibliography.


Planned for future versions
-----------------------------------------

- show abstract similar to .bib


Author
-----------------------------------------
David Reitter, Penn State
