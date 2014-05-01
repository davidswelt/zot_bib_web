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

To generate HTML and include it in a website:
- run zot.py once/on demand, or install as cron job or service on a server
Do not run it more than once a day.  Configure it directly in zot.py,
or in a separate file settings.py to make upgrading simple.

- include the resulting file zotero-bib.html (or as configured) in
  your website as you see fit.  You may also include individual
  collection files, which are also generated.   You can configure
  zot.py to generate a complete HTML document, or just a portion of it.
  
- Style your bibliography using CSS.  An example style
  file is included.


Wordpress Support
-----------------------------------------

This package can push directly to a Wordpress site.  A separate
program "push.py" is included to do this.

Follow these steps:
1. Set up zot.py to generate a bibliography you like.
2. Create a WP page or a post for the bibliography. Insert
    [zot_bib_web COLLECTION] where you'd like the bibliography
    inserted.  Replace COLLECTION with the ID of the collection.
	(More options: see push.py)
3. Configure push.py (at the top).  You will need to know a few simple
   details about your WP installation.
4. Run push.py regularly or on demand.  It will call zot.py
   automatically and then update the page in WP.



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
