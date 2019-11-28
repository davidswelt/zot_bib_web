Interactive web bibliographies with Zotero
=========================================================

Example Installations
---------------------

`Lab website at Penn State <http://acs.ist.psu.edu/wp/pub/>`__

`Personal website <http://david-reitter.com/pub/>`__

Documentation
-------------

http://zot-bib-web.readthedocs.io/


Author/Contact:
-------------

David Reitter -- david.reitter@gmail.com
http://www.david-reitter.com

Features
--------

This tool generates interactive web bibliographies based on one or more
collections in a Zotero repository. Collections can be maintained by
groups of people, using Zotero's web
interface or their desktop applications.

Bibliographies can be ordered by collection, by publication year, or
by publication type (e.g., journal articles first), are interactively
searchable, can be linked to PDF documents or other URLs, have records
for BibTex, EndNote and Wikipedia, and can be exported to HTML or pushed
to a Wordpress database.

Zot\_bib\_web does not depend on any third-party web server. The
generated bibliographies load quickly because they are stored as static
files along with the rest of your website. This makes a good source
for webcrawlers, including Google Scholar and CiteSeer.

Setup is easy for anyone who runs their own website and knows how
to use a command line (shell).
The easiest way to use it is to call zot.py with the key of a public
Zotero collection. It will make a zotero-bib.html file. Copy this, along
with the "site" and "files" (if any) directory to your webserver.


Demo
----

-  View the HTML files in the demo folder for some examples of
   bibliographies. Their respective settings files and CSS style files
   are included.

-  Run::

     ./zot.py --settings demo/settings3.py

   to see it in action.


License and Donations
---------------------

-  Use and modify this software free of charge.
-  No warranty is provided whatsoever.
-  Please e-mail david.reitter@gmail.com a link to the bibliography on
   your website if you decide to use zot\_bib\_web.

-  You may use this software for free.


Requirements
------------

-  Python 2.7 or 3.6+
-  Pyzotero. To install Pyzotero, a library for python::

       sudo pip install pyzotero

   or::

       sudo easy_install pyzotero

-  A Zotero collection with your bibliography (as user or as group)

-  Optional: dateutils package for Python (improves date parsing if present)


Setup
-----

-  Ensure zot.py is executable (chmod ug+x zot.py)

-  Try it out. From a unix-like command-line, do this::

       ./zot.py --group 160464 DTDTV2EP

Then view zotero-bib.html in a browser. If that looks good, move on to
the next steps for configuration.

-  In a new file called settings.py, add configuration as documented in
   the file settings\_example.py. Go to zotero.org to get your API
   secret key and your user or library IDs. It's easy: see the top of
   settings.example.py for details. If settings.py is set up, you can
   call zot.py without arguments.

Alternatively, you can use give the primary settings in arguments to the
program.

Bibliography in Zotero
----------------------

-  With Zotero, create a bibliography and note its ID (e.g., from the
   URL in the Zotero web interface). Example: ``MGID90AT``. This ID is
   what you need for the "toplevelfilter" variable in settings.py.

-  You can add sub-collections to your bibliography.

-  If you format ordered by collections, giving them an order may be
   helpful. You can name collections starting with a number: "10 Social
   Psychology".

Here's an example of a bibliography structure::

    My Publications [MGID90AT]
	10 Selected Works
	15 In Preparation / Under Review
	20 Refereed Works by Topic
	    Semantics
	    Parsing
	    Dialogue
	    Machine Learning
	30 Theses
	40 Talks (Without Paper)

To see this, use the provided settings.py as an example.

Overview of Configuration options
--------------------------------------

-  Configuration takes place in a settings file, by default named
   settings.py.

-  Call ./zot.py --help to see a list of command-line options.

-  Please refer to the documentation for information on the settings
   file, or read settings\_example.py.
   A few options are discussed in the following.

-  You can order our bibliography by sub-collection, by year, or by
   publication type (e.g., journal articles first, then conference
   papers). Even within the higher-level categories you can sort your
   bibliographic entries as you wish. Use the "sort\_criteria" and
   "show\_top\_section\_headings" settings.

-  You can choose a different formatting convention. Default is APA
   format.

-  At the top, a search box and a set of shortcuts may be displayed: for
   example, several years or spans of years, publication types, or
   subcollections that indicate topic areas. A visitor may click on
   these to quickly filter the bibliography.

-  Configure the shortcuts shown at the top using the show\_shortcuts
   variable. 'collection', 'type', 'year', 'venue', 'venue\_short', and
   'tags' are supported values, in addition to more fine-grained lists
   of values you can create using the shortcut() function. You can give
   the list of values or ranges (for years), their order, and some
   filtering to only show the most common ones. See settings.example.py
   for a detailed example.

-  There are several more options. Again, see settings\_example.py.

Deployment to a web site
------------------------

-  Upload the site folder or its contents to a public place on your web
   server. By default, /site/... is the assumed URL.

To generate HTML and include it in a website:

-  run zot.py once/on demand, or install as cron job or service on a
   server Do not run it more than once a day. Configure it directly in
   zot.py, or in a separate file settings.py to make upgrading simple.

-  include the resulting file zotero-bib.html (or as configured) in your
   website as you see fit. You may also include individual collection
   files, which are also generated. You can configure zot.py to generate
   a complete HTML document, or just a portion of it. Zot\_bib\_web
   generates HTML5 content.

-  Style your bibliography using CSS. An example style file is included
   (see site/ directory).

Wordpress Support
-----------------

This package can push directly to a Wordpress site. A separate program
"push.py" is included to do this.

Follow these steps:

1. Set up zot.py to generate a bibliography you like. Call zot.py --full
   to generate a complete zotero-bib.html file for debugging purposes.
   Configure settings.py to not generate the full HTML code.
2. Install the wpautop-control plugin (or a similar plugin) to make sure
   that WP will not insert paragraph breaks at various places in the
   bibliography. With this plugin, you will need to add a "custom field"
   to the page created in the next step (Choose "Screen Options" at the
   top of the page view, enable custom fields. Then find custom fields
   at the very bottom of the page and add a "wpautop" field with value
   "no".
3. Create a WP page or a post for the bibliography. Insert
   [zot\_bib\_web COLLECTION] where you'd like the bibliography
   inserted. Replace COLLECTION with the ID of the collection. (More
   options: see push.py)
4. Copy the style sheet contents (in site/) to your Wordpress theme
   (select "editor", or "Additional CSS").
5. Configure settings.py so that jquery and other files are available on
   the web server. Typically, this would be jquery\_path =
   "../wp-includes/js/jquery/jquery.js" clipboard.js and clippy.svg: You
   may refer to a public URL or serve the files yourself.
6. Configure push.py (at the top). You will need to know a few simple
   details about your WP installation.
7. Run push.py regularly or on demand. It will call zot.py automatically
   and then update the page in WP.
