## settings.example.py

## You must configure the authentication settings and one collection key.

#### AUTHENTICATION ############################################################

# Group/User:  You may either display a library for a Zotero user,
# or for a group.

# User:
# You may find your user ID for the library_id setting under
# "Settings -> Feeds/API":
#    https://www.zotero.org/settings/keys
# library_type is 'user'.

# Group:
# Find your library_id by selecting the group on the Zotero website,
# and then choose "Group Settings".  The URL in your browser
# window will then show you a six-digit number,
# e.g.,  .../groups/110233/settings
# library_type is 'group'.

library_id = '160464' # your group or user ID (e.g., six numeric digits)
library_type ='group'  # 'group' or 'user'

# Data from private Zotero accounts:

# If you want to retrieve non-public data from Zotero, you’ll need a
# Zotero account (or group) at zotero.org.  Log into your account,
# access the Settings page on the Zotero site and create an private
# API key (under "Settings -> Feeds/API").  For the key, check "Allow
# library access".  This key is used in the api_key setting.

api_key = None  # secret key (from Zotero)

#### COLLECTIONS TO BE RENDERED ################################################

# In your library, you may create a collection, for example, "website".
# Within it, create titled sub-collections, like so:

# toRead
# thesis
# website
#    *10 Selected Works
#    20 Journal Articles
#    30 Conference Proceedings
#    40 Theses

# Now, find the IDs of the top-level collection called "website".
# When you click on it on the Zotero website, your browser will show you an alphanumeric
# key in the URL, e.g., items/collectionKey/FCQM2AY6.  The portion 'FCQM2AY6' is what you
# would use in toplevelfilter.

# To display the whole library with all its collections,
# leave toplevelfilter set to None.  You may use that to see a list of all collections
# when zot_bib_web runs.

# ID string of the top-collection that is going to be ignored (as a level), or None
# If set, we will display the items available underneath this collection.
# otherwise, all collections available will be displayed.
toplevelfilter = None # e.g., 'MGID93AS'


#### SPECIAL OPTIONS: STYLE ####################################################
# Special settings - configure only if needed.

# bibliography title
titlestring = 'Bibliography'


# bibliography style format (e.g., 'apa' or 'mla') - Any valid CSL style in the Zotero style repository
bib_style =  'apa'

# order within each category
# e.g., 'dateAdded', 'dateModified', 'title', 'creator', 'type', 'date', 'publisher', 'publication', 'journalAbbreviation', 'language', 'accessDate', 'libraryCatalog', 'callNumber', 'rights', 'addedBy', 'numItems'
order_by = 'date'

# sorting direction
sort_order = 'desc'   # "desc" or "asc"

# Limit - for fast testing and debugging
# None, or set a limit (integer<100) for each collection for debugging
# You may also give the --limit argument to zot.py
limit=None

#### SPECIAL OPTIONS: HTML AND FILE CONFIGURATION ##############################
# Special settings - configure only if needed.

write_full_html_header = True   # False to not output HTML headers.  In this case, expect a file in UTF-8 encoding.
stylesheet_url = "style.css"  # If set and write_full_html_header is True, link to this style sheet (a URL)

# If set, include "Miscellaneous" category at end containing all items from this
# collection that were not mentioend anywhere else.
catchallcollection = None # e.g., '4KATF6MA'
# Title for the catch-all collection (shown at end)
catchall_title = 'Miscellanous'

outputfile = 'zotero-bib.html'  # relative or absolute path name of output file
category_outputfile_prefix = 'zotero'  # relative or absolute path prefix

show_search_box = True  # show a Javascript/JQuery based search box to filter pubs by keyword.  Must define jquery_path.
jquery_path = "site/jquery.min.js"  # path to jquery file on the server
# jquery_path = "../wp-includes/js/jquery/jquery.js"  # wordpress location

show_copy_button = True  # show clipbaord copy button.  Must define jquery_path.
clipboard_js_path = "site/clipboard.min.js"  # path to file on server
copy_button_path = "site/clippy.svg" # path to file on server

# unconditionally show these items if they are available for the item
# (don't set for default)
# show_links = ['abstract', 'pdf', 'bib', 'wikipedia', 'ris', 'coins']

# Prevent viewers from selecting "bib", "pdf" etc for easier copy/paste of bibliography
# (don't set for default)
# smart_selections = True



#### SPECIAL OPTIONS: WORDPRESS ##############################
# Special settings - configure only if needed.
# These settings are used by push.py

wp_url = 'https://example.com/wp/xmlrpc.php'   # Wordpress XMLRPC URL
wp_username = 'pubpusherusername'
wp_password = 'password'
wp_blogid = "0"

post_id = 225

infile = "zotero-bib.html"
