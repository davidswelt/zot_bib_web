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

additional_collections = []  # additional collections to be added from outside of the toplevelfilter

#### SPECIAL OPTIONS: STYLE ####################################################
# Special settings - configure only if needed.

# The sort_criteria determine the structure of the bibliography.
# Allowable values: 'type' (category of publication, e.g., journal article),
# 'date' (full date)
# 'year' (year of publication)
# 'collection' (the subcollection the article is placed in).
# Collection works best at the beginning of the list.
# add - in front of the field name to sort in descending order (e.g., -date will show the newest entries first).

# sort_criteria = ['collection','-date']   # First by collection, then type, then by date, latest first.
sort_criteria = ['type','-date']   # we have date and type: First by date ("issued"), then by type.
#sort_criteria = ['-year','type']   # Ordered by year.



# bibliography title
titlestring = 'Bibliography'

# show section headings for the primary search criterion
show_top_section_headings = True

# bibliography style format (e.g., 'apa' or 'mla') - Any valid CSL style in the Zotero style repository
bib_style =  'apa'

# Limit - for fast testing and debugging
# None, or set a limit (integer<100) for each collection for debugging
# You may also give the --limit argument to zot.py
limit=None

#### SPECIAL OPTIONS: HTML AND FILE CONFIGURATION ##############################
# Special settings - configure only if needed.


no_cache = True  # Do not use cache; retrieve items from Zotero database every time (slow)

write_full_html_header = True   # False to not output HTML headers.  In this case, expect a file in UTF-8 encoding.
stylesheet_url = "style.css"  # If set and write_full_html_header is True, link to this style sheet (a URL)

# If set, include "Miscellaneous" category at end containing all items from this
# collection that were not mentioend anywhere else.
# You can use the toplevel collection here
catchallcollection = None # e.g., '4KATF6MA', or simply toplevelcollection
# Title for the catch-all collection (shown at end)
catchall_title = 'Miscellanous'

outputfile = 'zotero-bib.html'  # relative or absolute path name of output file
category_outputfile_prefix = 'zotero'  # relative or absolute path prefix

show_search_box = True  # show a Javascript/JQuery based search box to filter pubs by keyword.  Must define jquery_path.
jquery_path = "site/jquery.min.js"  # path to jquery file on the server
# jquery_path = "../wp-includes/js/jquery/jquery.js"  # wordpress location

# Show categories at the top of the bibliography for quick filtering
# 'collection', 'type', 'year' are supported
show_shortcuts = ['collection']
# To add specific rather than all available values for a field, use a tuple as follows.
# Note that for year, we support ranges. 
show_shortcuts += [('year', [2017,2016,2015,2014,2013,"2008-2012","2005-2008","-2004"])]
# To add arbitrary search terms:
show_shortcuts += [('keyword', ["model", "language", "entropy"])]  # define some search terms

number_bib_items = False  # show bibliographic items as numbered, ordered list
show_copy_button = True  # show clipbaord copy button.  Must define jquery_path.
clipboard_js_path = "site/clipboard.min.js"  # path to file on server
copy_button_path = "site/clippy.svg" # path to file on server

# unconditionally show these items if they are available for the item
# (don't set to obtain defaults)
# show_links = ['abstract', 'pdf', 'bib', 'wikipedia', 'ris', 'coins']

# Prevent viewers from selecting "bib", "pdf" etc for easier copy/paste of bibliography
# (don't set to obtain default)
# smart_selections = True

# Output in this language
language_code = 'en'

# Define labels for article types and their ordering
# types may occur in libraryCatalog or itemType
# use libraryCatalog to override it in special cases (e.g., archival Conference papers)
sortkeyname_order['en']['type'] = [('journalArticle', 'Journal Articles'),
                            ('archivalConferencePaper', 'Archival Conference Papers'),
                            ('conferencePaper', 'Conference and Workshop Papers'),
                            ('book','Books'),
                            ('bookSection', 'Book Chapters'),
                            ('edited-volume', "Edited Volumes"),
                            ('thesis', 'Theses'),
                            ('report', 'Tech Reports'),
                            ('presentation', 'Talks')]

# Translations for links
# Provide additional languages like so:
# link_translations['de'] = {'abstract':'Abstrakt', 'pdf':'Volltext'}




#### SPECIAL OPTIONS: WORDPRESS ##############################
# Special settings - configure only if needed.
# These settings are used by push.py

wp_url = 'https://example.com/wp/xmlrpc.php'   # Wordpress XMLRPC URL
wp_username = 'pubpusherusername'
wp_password = 'password'
wp_blogid = "0"

post_id = 225

infile = "zotero-bib.html"
