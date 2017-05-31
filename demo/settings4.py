

#### You must configure the collection(s) to be loaded

group_collection(160464, collection='MGID93AS')

# 160464 #  group ID (e.g., six numeric digits)
# 'MGID93AS'  # collection where to find the bibliographic items.
# (You can load a user collection with user_collection().)

# Load an additional collection from a different library:
user_collection('1366641', api_key = 'X4iUU2a7P5mQWNTO7hvuQwzB', collection='FCQK6PT6')
exclude_collection('FCQK6PT6', top_level_only=True) # Do not keep top-level items from this collection

# One could also include the top level collections
#exclude_collection('FCQK6PT6', top_level_only=True)  # exclude items at the top level (redundant)
exclude_collection('Selected Works') # Selected Works ZJFRZTCB
exclude_collection('AWMEXUV2') # In Review and to appear
exclude_collection('HZHSMP74') # Theses
rename_collection('BQUUP5PR', "Language")

exclude_items(lambda i: 'Reitter' in i.html and i.year<2011)  # This is a function that returns True for every item to be excluded

#### Optional Settings

# No sort_critera specified here - use default.

# sort_criteria = ['collection', '-year', 'type']
# The sort_criteria determine the structure of the bibliography.
# Allowable values: 'type' (category of publication, e.g., journal article),
# 'date' (full date)
# 'year' (year of publication)
# 'collection' (the subcollection the article is placed in).
# Collection works best at the beginning of the list.
# add - in front of the field name to sort in descending order (e.g., -date will show the newest entries first).


###### Special settings

bib_style = 'mla'     # bibliography style format (e.g., 'apa' or 'mla') - Any valid CSL style in the Zotero style repository

write_full_html_header = True   # False to not output HTML headers.  In this case, expect a file in UTF-8 encoding.

outputfile = 'demo/example4.html'  # relative or absolute path name of output file

show_search_box = True  # show a Javascript/JQuery based search box to filter pubs by keyword.  Must define jquery_path.
jquery_path = "site/jquery.min.js"  # path to jquery file on the server - default: wordpress location


show_copy_button = True  # show clipbaord copy button.  Must define jquery_path.
clipboard_js_path = "site/clipboard.min.js"  # path to file on server
copy_button_path = "site/clippy.svg" # path to file on server

show_links = ['abstract', 'pdf', 'bib', 'wikipedia', 'endnote', 'coins']

show_shortcuts = ['type',shortcut('collection', sortBy='name')]

stylesheet_url = "style4.css"
