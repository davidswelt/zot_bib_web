Pyzotero 1.3.0
-----------------------------------------
- Improved instructions in settings example file
- Tested with Pyzotero 1.2.0 and Python 2.7


Pyzotero 1.2.0
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
