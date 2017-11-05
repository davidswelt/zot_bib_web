#!/usr/bin/env python
# coding: utf-8

## settings.example.py

## You must configure the authentication settings and one collection key.

verbosity = 0
# Print more or less output during execution
# -2: print errors
# -1: print warnings and errors
# 0: print progress information, warnings and errors
# 1: print log information and everything else.

#### AUTHENTICATION AND COLLECTIONS ######################################

group_collection(160464, collection='MGID93AS')

# user_collection(id='1366640', api_key='Y4oUU2c7P1nQWNPO3hvuEwzP')

# group_collection(id, api_key=None, collection=None, top_level=False)
# user_collection(id, api_key=None, collection=None, top_level=False)
#
#   Use group_collection for a group library, user_collection for a
#   (private) user library.
#   ID specifies the group or user ID.
#
#   You may find your user ID for the library_id setting under
#   "Settings -> Feeds/API":
#        https://www.zotero.org/settings/keys
#
#   You may find your library ID by selecting the group on the Zotero
#   website, and then choose "Group Settings".  The URL in your browser
#   window will then show you a six-digit number,
#   e.g.,  .../groups/110233/settings
#
#   api_key
#       The secret key provided by Zotero.
#       If you want to retrieve non-public data from Zotero, you'll need a
#       Zotero account (or group) at zotero.org.  Log into your account,
#       access the Settings page on the Zotero site and create an private
#       API key (under "Settings -> Feeds/API").  For the key, check
#       "Allow library access".  This key is used in the api_key setting.
#
#   collection
#       ID of the top-level collection to be included.
#       All sub-collections under this collection will be imported.
#       If not given (None), all available collections will be included.
#
#   top_level
#       If true, then the collection given be included as a level.
#       Otherwise (default, False), sub-collections and items will be
#       included directly.


#### COLLECTIONS TO BE RENDERED ##########################################

# In your library, you may create a collection, for example, "website".
# Within it, create titled sub-collections, like so:

# toRead
# thesis
# website
#    10 Selected Works
#    20 Journal Articles
#    30 Conference Proceedings
#    40 Theses

# Now, find the IDs of the top-level collection called "website".
# When you click on it on the Zotero website, your browser will show you
# an alphanumeric key in the URL, e.g., items/collectionKey/FCQM2AY6.
# The portion 'FCQM2AY6' is what you would use in 'collection' for
# the user_collection or group_collection directives.


# To cause zot_bib_web to format a sub-collection in special ways, you
# may add some statements here.  For these statements, supply either
# the name (title) or the key associated with a collection.

# exclude_collection (C)
# Remove sub-collection C.

# rename_collection (C, N)
# Rename collection C to N.
# This may be used to merge collections by giving them the same name.

# hidden_collection (C)
# Hide sub-collection C.  We still add a shortcut at the top
# to unhide its contents if they are available elsewhere.
# You may also use a '-' before the name of the collection in the library.

# short_collection (C)
# Short mode.  This sub-collection will be shown using titles,
# journal and years only, which can then be expanded.  Journal or
# conference titles can be kept short.  Specify the "journal abbr or
# "conference title" fields, or a short "note" if necessary.  You may
# want to copy bibliographic items from other parts of the bibliography
# into this sub-collection.
# You may also use a '*' before the name of the collection in the library.

short_collection("Selected Works")

# featured_collection (C)
# Feature this:  Extract this sub-collection and show at the beginning of
# the bibliography, regardless of whether the rest of the bibliography is
# sorted by, e.g., year, and ignores the collections otherwise. In the
# collection shown below, it prevents "in review" articles to show up as
# regular journal articles (which might give the impression you're
# taking credit for not-yet-reviewed/published material!)
# You may also use a '!' before the name of the collection in the library.

featured_collection("Selected Works")

# misc_collection (C)
# Show the items in this collection, but exclude those items that
# are already included in another regular collection.  A regular
# collection is one that is not hidden, not short, and not featured.
# This is useful to add a "Miscellaneous" category at the end for
# additional items without duplicating anything.
# You may also use a '&' before the name of the collection in the library.

misc_collection("Miscellaneous")


#### SPECIAL OPTIONS: STYLE ##############################################
# Special settings - configure only if needed.

# The sort_criteria determine the structure of the bibliography.
# Allowable values: 'type' (category of pub., e.g., journal article),
# 'date' (full date)
# 'year' (year of publication)
# 'collection' (the subcollection the article is placed in).
# Collection works best at the beginning of the list.
# add - in front of the field name to sort in descending order
# (e.g., -date will show the newest entries first).

# sort_criteria = ['collection','-date']   # collection, then by date.
sort_criteria = ['type','-date']   # by type, then by date ("issued").
#sort_criteria = ['-year','type']   # Ordered by year, then type.



titlestring = 'Bibliography'
""" bibliography title """

show_top_section_headings = True
""" show section headings for the primary search criterion"""

bib_style =  'apa'
""" bibliography style format (e.g., 'apa' or 'mla') - Any valid CSL style
 in the Zotero style repository"""

#### SPECIAL OPTIONS: HTML AND FILE CONFIGURATION ########################
# Special settings - configure only if needed.


write_full_html_header = True
# False to not output HTML headers.
# In this case, expect a file in UTF-8 encoding.

stylesheet_url = "site/style.css"
# If set and write_full_html_header is True,
# link to this style sheet (a URL)

outputfile = 'zotero-bib.html'
# relative or absolute path name of output file

show_search_box = True
# show a Javascript/JQuery based search box to filter pubs by keyword.
# Must define jquery_path.

jquery_path = "site/jquery.min.js"
# path to jquery file on the server
# jquery_path = "../wp-includes/js/jquery/jquery.js"  # wordpress location

# Show categories at the top of the bibliography for quick filtering
# 'collection', 'type', 'year', 'venue', 'venue_short', or 'tags'
show_shortcuts = ['collection']
# To add specific rather than all available values for a field, use the
# shortcut function as follows.
# Note that for year, we support ranges.

# In the following, we tell the program
# to display despific entries for "year":

show_shortcuts += [shortcut('year', [2017,2016,2015,2014,2013,
                                     "2008-2012","2005-2008","-2004"])]

# Show the venues (conferences, journals) where we've published.
# the "shortcut" function offers some options:
# sortDir="asc" or "desc" instructs the program to sort the entries.
# (Default is automatic.)
# sortBy indicates that we'd like to sort by how many items there are
# in each category
#   (Default is to sort by name.  'count' is the only other value possible
#    at this time.)
# topN says to display only the 5 biggest categories.
# If there are several categories ranked 5, we're showing all of them.
# E.g.  topN=3 shows:  WIFN(8) FJJ(8) CLAM(5) CLEE(5)
# (Default is to show all for which bibliographic entries exist in the data.)

show_shortcuts += [shortcut('venue_short', sortDir='desc',
                            sortBy='count', topN=5)]

# To add arbitrary search terms:

show_shortcuts += [shortcut('keyword',
                            values=["model", "language", "entropy"])]
# define some search terms

number_bib_items = False
# show bibliographic items as numbered, ordered list

show_copy_button = True
# show clipbaord copy button.  Must define jquery_path.

clipboard_js_path = "site/clipboard.min.js"
# path to file on server

copy_button_path = "site/clippy.svg"
# path to file on server

# Attachments
file_outputdir = 'files/'
# Location to save attached files.

file_output_path = "files/"
# relative URL on server, corresponding to file_outputdir

# unconditionally show these items if they are available for the item
# (don't set to obtain defaults)
# show_links = ['abstract', 'url', 'bib', 'wikipedia',
#               'ris', 'cite.apa', 'file']
#
# URL       - the URL field for the item; button is displayed as
#             PDF/DOC/PS/LINK as detected.
# file      - each file associated with the item in the library.
#             Files are saved to file_outputdir and expected to appear
#             on the web server in file_output_path (which see)
#             Button is displayed as PDF/DOC/PS/LINK as detected.
# RIS or EndNote - download of the file containing the bibliographic data
# BIB       - bibliographic data for LaTeX
# Wikipedia - bibliographic data in Wikipedia format
# Abstract  - the abstract
# cite.APA  - Citation in APA format
# cite.MLA  - Citation in MLA format
# cite.<XXX> - Citation in <XXX> format (as supported by Zotero)



# omit_COinS = False
# True to omit COINS metadata; useful to save space, but not recommended.

# no_cache = True
# True means do not use cache;
# retrieve items from Zotero database every time (slow)


# smart_selections = True
# Prevent viewers from selecting "bib", "pdf" etc
# for easier copy/paste of bibliography
# (don't set to obtain default, which is True)

# Output in this language
language_code = 'en'

# Define labels for article types and their ordering
# types may occur in libraryCatalog or itemType
# use libraryCatalog to override it in special cases
# (e.g., archival Conference papers)
# sortkeyname_order['en']['type'] = [('journalArticle', 'Journal Articles'),
#                             ('archivalConferencePaper', 'Archival Conference Papers'),
#                             ('conferencePaper', 'Conference and Workshop Papers'),
#                             ('book','Books'),
#                             ('bookSection', 'Book Chapters'),
#                             ('edited-volume', "Edited Volumes"),
#                             ('thesis', 'Theses'),
#                             ('report', 'Tech Reports'),
#                             ('attachment', 'Document'),
#                             ('webpage', 'Web Site'),
#                             ('presentation', 'Talks')]

# Translations for links
# Provide additional languages like so:
# link_translations['de'] = {'abstract':'Abstrakt', 'pdf':'Volltext'}




#### SPECIAL OPTIONS: WORDPRESS ##############################
# Special settings - configure only if needed.
# These settings are used by push.py

push_wordpress(url='https://example.com/wp/xmlrpc.php', blogID=0,
               user='pubpushername', password='pass', postID=200)

infile = "zotero-bib.html"
