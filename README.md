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
----------------------------------------
- Python 2.7 installation (Python 3 not yet supported by Pyzotero)
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
- run push.py regularly or on demand.  It will call zot.py automatically.

push.py can automatically update the Wordpress page with the
bibliography.


How it works
-----------------------------------------

Zot.py produces annotated, beautiful bibliographies for the web from a
Zotero collection.  It is designed for individuals and for research
groups.

This program will load settings.py for its configuration.
It will retrieve all publications for the given user or
group.  If subcollections are present, each subcollection will form a
separate section.  The top-level collection can be ignored (depending
on configuration.)

The output of zot.py consists of HTML: either a full document, or a snippet, as
configured.

Each bibliographic entry is annotated with a bib record and an abstract,
each of which can be revealed by the reader (client-side javascript).


Tips
-----------------------------------------

- To put collections in a certain order, just add a number to their
  names, like so:

10 Selected Publications
20 Refereed Works
30 Presentations

Zot.py will automatically remove the number for display.

- Use the push.py script to update a page in Wordpress.

Author
-----------------------------------------
David Reitter, Penn State
