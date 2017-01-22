#dr-settings.py


#### You must configure the following items

library_id = '160464' # your group or user ID (e.g., six numeric digits)
library_type ='group'  # or 'group' # group or userm
api_key = ''  # secret key (from Zotero)

toplevelfilter = 'MGID93AS'   # top-collection that is going to be ignored (as a level), or None
catchallcollection = '4KATF6MA'  # include "Miscellaneous" category at end containing all items not mentioend anywhere else, or None



###### Special settings - configure if needed.

limit=None   # None, or set a limit (integer<100) for each collection for debugging

bib_style =  'apa'     # bibliography style format (e.g., 'apa' or 'mla') - Any valid CSL style in the Zotero style repository

order_by = 'date'   # order in each category: e.g., 'dateAdded', 'dateModified', 'title', 'creator', 'type', 'date', 'publisher', 'publication', 'journalAbbreviation', 'language', 'accessDate', 'libraryCatalog', 'callNumber', 'rights', 'addedBy', 'numItems'

sort_order = 'desc'   # "desc" or "asc"

write_full_html_header = True   # False to not output HTML headers.  In this case, expect a file in UTF-8 encoding.
stylesheet_url = "style.css"  # If set and write_full_html_header is True, link to this style sheet (a URL)

outputfile = 'zotero-bib.html'  # relative or absolute path name of output file
category_outputfile_prefix = 'zotero'  # relative or absolute path prefix

show_search_box = True  # show a Javascript/JQuery based search box to filter pubs by keyword.  Must define jquery_path.
jquery_path = "site/jquery.min.js"  # path to jquery file on the server
# jquery_path = "../wp-includes/js/jquery/jquery.js"  # wordpress location

show_copy_button = True  # show clipbaord copy button.  Must define jquery_path.
clipboard_js_path = "site/clipboard.min.js"  # path to file on server
copy_button_path = "site/clippy.svg" # path to file on server




## 


wp_url = 'https://example.com/wp/xmlrpc.php'   # Wordpress XMLRPC URL
wp_username = 'pubpusherusername'
wp_password = 'password'
wp_blogid = "0"

post_id = 225

infile = "zotero-bib.html"






