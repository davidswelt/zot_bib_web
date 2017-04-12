zot_bib_web 3.0.0
-----------------------------------------

- New interface to allow sorting of the bibliographic items not just
  by collection as in the Zotero library, but also by year or by
  publication type (e.g., journal article, conference paper), and
  arbitrary hierarchies thereof.  Extracting "selected works" or "in
  review" papers is possible.  Even if ordering chronologically,
  without showing thematic collections, the bibliography can be
  filtered according to area with the collection shortcuts at the top.
  
- Bibliographic entries can be numbered within their sections now.
  See the number_bib_items variable.
  
- full-bib-section and short-bib-section divs now contain their
  respective section headings.

- Added several worked examples with output in the demo folder.
  Run make-demo.sh to generate them.



zot_bib_web 2.0.0
-----------------------------------------
- Much simplified installation and setup.  Improved documentation.
- Items in top-level collection are no longer excluded
- Fix problem with nested collections that did not show in the correct location
- Improved warning messages for double entries
- More flexibility with the "catch-all collection", which can now be
under the top-level collection
- Nested collections can be indented or otherwise styled using CSS
  (new div.collection tags)
- Tested with Pyzotero 0.10.1 and Pyzotero 1.2.0
- Now compatible with Python 2.7 or Python 3.


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
