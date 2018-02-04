Changes to Zot_bib_web

https://github.com/davidswelt/zot_bib_web

Author/Contact:
	Dr. David Reitter, College of Information Sciences & Technology,
	Penn State
	reitter@psu.edu


zot_bib_web 2.1.0
-----------------------------------------

- Add --quiet and --verbose arguments and a `verbosity' configuration
  variable.  Output is now primarily made to stderr.  Other improvements
  to progress output.

- Links in bib entries are now clickable.

- Fix bugs in connection with empty author and title fields.

- Fix problems with Windows in connection with non-ASCII characters

- Various bugfixes.

-- David Reitter <reitter@psu.edu> 2018-01-04


zot_bib_web 2.0.4
-----------------------------------------

The program's configuration has been redesigned, and many more
options for displaying and sorting the interactive bibliography are available.


- Much simplified installation and setup.  Improved documentation.
  Settings files can now load multiple collections from different
  libraries.  Use user_collection(...) and group_collection(...)
  statements.  See settings_example.py for documentation.
  Previous settings file are imported (with exception of the next item).

- Documentation is now available at http://zot-bib-web.readthedocs.io .

- You can sort the bibliographic items not just
  by collection as in the Zotero library, but also by year or by
  publication type (e.g., journal article, conference paper), and
  arbitrary hierarchies thereof.   "Selected works" or "in
  review" papers can be extracted at the top.  Even if ordering chronologically,
  without showing thematic collections, the bibliography can be
  filtered according to area with the collection shortcuts at the top.

- Shortcuts at the top of the generated webpage can filter by years,
  collections, venues, publication type.

- Files (like PDF files) stored in the Zotero library can now be
  written out and linked to.

- Additional settings have become available.  See settings_example.py.

- Citations can be viewed in additional formats (see show_links
  configuration variable).  For example, we can show the full entry in
  APA or MLA format (or any other style available).

- Files attached to entries in Zotero can now be saved for upload to
  the server. (Requested by Selcuk Bilmis.)  HTML archives are also
  supported. Notes are supported in
  a similar way, but are not functional until some bugs in PyZotero or
  the Zotero API are fixed.

- Bibliographic entries can be numbered within their sections now.
  See the number_bib_items variable.

- Added several worked examples with output in the demo folder.
  Run make-demo.sh to re-generate them.

- Caching of Zotero retrieval makes repeated runs much faster.

- Tested with Pyzotero 1.2.11.
- Now compatible with Python 2.7 or Python 3.6.

Compatibility-breaking Changes:

- Catchallcollection is no longer available in program arguments or
the settings file.  Specify a "catch-all collection" via the &
modifier directly in the name of the respective collection,
e.g. "9999& Miscellaneous" (9999 if sorting at the end is desired).

- Output file is not longer a positional argument to the program.
  Use -o <outfile> instead.  '-' is permissible for stdout.

- Items in top-level collection are no longer excluded

- Limit has been removed (replaced with caching)



CSS  and HTML Changes:

- Search keywords are now prominently displayed when active

- full-bib-section and short-bib-section divs now contain their
respective section headings.

- Nested collections can be indented or otherwise styled using CSS
  (new div.collection tags)

- Several new class and id attributes to allow for more styling.

- Buttons (e.g., Wikipedia, EndNote, BIB) have standard capitalization
now.  Style using CSS.


Selected bug fixes:

- Fix problem with nested collections that did not show in the correct location
- Improved warning messages for double entries


zot_bib_web 1.2.2
-----------------------------------------
- Fix bug that prevented RIS downloads from showing
  (and potentially other elements included in show_links depending on capitalization)
- Improved instructions in settings example file
- Tested with Pyzotero 1.2.0 and Python 2.7


zot_bib_web 1.2.0
-----------------------------------------

- A "show to clipboard" button is shown for bib and wikipedia code (configure with show_copy_button entry)
- COINS information is now included.  This means Zotero's browser plugins will work with the generated bibliographies
- Wikipedia markup is included in the bibliography (configure with show_links setting)
- The shortened section (e.g., "Selected Works") now shows the journal or conference title  (to hide, use CSS style sheet)
- Visitors can now select text for copy/paste without also copying the meaningless buttons (configure with smart_selections setting)
- Style and js files necessary on the webserver are now in the "site" directory
- toplevelfilter may be None now, in which case the entire library is used.
- Many improvements to the generated HTML and supplied stylesheets
- Better IE11 support
- Tested with pyzotero 1.1.21

-- David Reitter <reitter@psu.edu> 2017-01-28
