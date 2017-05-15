## settings.example.py

## You must configure the authentication settings and one collection key.

#### AUTHENTICATION AND COLLECTIONS #############################################



group_collection(160464, collection='MGID93AS')

# user_collection(id='1366640', api_key='Y4oUU2c7P1nQWNPO3hvuEwzP')

# group_collection(id, api_key=None, collection=None, top_level=False)
# user_collection(id, api_key=None, collection=None, top_level=False)
#
#   Use group_collection for a group library, user_collection for a (private) user library.
#   ID specifies the group or user ID.
#
#   You may find your user ID for the library_id setting under
#   "Settings -> Feeds/API":
#        https://www.zotero.org/settings/keys
#
#   You may find your library ID by selecting the group on the Zotero website,
#   and then choose "Group Settings".  The URL in your browser
#   window will then show you a six-digit number,
#   e.g.,  .../groups/110233/settings
#
#   api_key
#       The secret key provided by Zotero.
#       If you want to retrieve non-public data from Zotero, you’ll need a
#       Zotero account (or group) at zotero.org.  Log into your account,
#       access the Settings page on the Zotero site and create an private
#       API key (under "Settings -> Feeds/API").  For the key, check "Allow
#       library access".  This key is used in the api_key setting.
#
#   collection
#       ID of the top-level collection to be included.
#       All sub-collections under this collection will be imported.
#       If not given (None), all available collections will be included.
#
#   top_level
#       If true, then the collection given be included as a level.
#       Otherwise (default, False), sub-collections and items will be included directly.


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

outputfile = 'zotero-bib.html'  # relative or absolute path name of output file
category_outputfile_prefix = 'zotero'  # relative or absolute path prefix

show_search_box = True  # show a Javascript/JQuery based search box to filter pubs by keyword.  Must define jquery_path.
jquery_path = "site/jquery.min.js"  # path to jquery file on the server
# jquery_path = "../wp-includes/js/jquery/jquery.js"  # wordpress location

# Show categories at the top of the bibliography for quick filtering
# 'collection', 'type', 'year', 'venue', 'venue_short' are supported
show_shortcuts = ['collection']
# To add specific rather than all available values for a field, use the shortcut function as follows.
# Note that for year, we support ranges.
# In the following, we tell the program to display despific entries for "year"
show_shortcuts += [shortcut('year', [2017,2016,2015,2014,2013,"2008-2012","2005-2008","-2004"])]
# Show the venues (conferences, journals) where we've published.
# the "shortcut" function offers some options:
# sort="asc" or "desc" instructs the program to sort the entries.  (Default is automatic.)
# sortBy indicates that we'd like to sort by how many items there are in each category
#   (Default is to sort by name.  'count' is the only other value possible at this time.)
# topN says to display only the 5 biggest categories.
# If there are several categories ranked 5, we're showing all of them.
# E.g.  topN=3 shows:  WIFN(8) FJJ(8) CLAM(5) CLEE(5)
# (Default is to show all for which bibliographic entries exist in the data.)
show_shortcuts += [shortcut('venue_short', sort='desc', sortBy='count', topN=5)]
# To add arbitrary search terms:
show_shortcuts += [shortcut('keyword', values=["model", "language", "entropy"])]  # define some search terms

number_bib_items = False  # show bibliographic items as numbered, ordered list
show_copy_button = True  # show clipbaord copy button.  Must define jquery_path.
clipboard_js_path = "site/clipboard.min.js"  # path to file on server
copy_button_path = "site/clippy.svg" # path to file on server

# unconditionally show these items if they are available for the item
# (don't set to obtain defaults)
# show_links = ['abstract', 'pdf', 'bib', 'wikipedia', 'ris']

# omit_COinS = False  # True to omit COINS metadata; useful to save space, but not recommended.

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
