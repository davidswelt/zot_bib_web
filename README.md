Zot/Bib/Web
A program to export Zotero bibliographies to interactive HTML
===========

This tool generates interactive web bibliographies based on one or
more collections in a Zotero repository.

Collections can be maintained by groups of people, using Zotero's web
interface or their desktop applications.


Bibliographies
- are grouped by collection
- editable in Zotero by one or more users
- are interactively searchable
- linked to PDF documents or other URLs
- have BibTeX records
- and can be exported to HTML or pushed to a Wordpress database

The content generated is static.  This program is meant to 
be run regularly.  

Zot_bib_web is available on Github.


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
