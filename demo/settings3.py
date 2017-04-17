#dr-settings.py


#### You must configure the following items

library_id = '160464' # your group or user ID (e.g., six numeric digits)
library_type ='group'  # or 'group' # group or userm
api_key = None

toplevelfilter = 'MGID93AS'   # collection where to start retrieving

# The sort_criteria determine the structure of the bibliography.
# Allowable values: 'type' (category of publication, e.g., journal article),
# 'date' (full date)
# 'year' (year of publication)
# 'collection' (the subcollection the article is placed in).
# Collection works best at the beginning of the list.
# add - in front of the field name to sort in descending order (e.g., -date will show the newest entries first).

# See also: show_top_section_headings setting below.

# Two typical variants are shown:
# Thematic, by collection
sort_criteria = ['collection','-date']   # First by collection, then type, then by date, latest first.
# By type (journal, conference, etc.), then chronologically
# sort_criteria = ['type','-date']   # we have date and type: First by date ("issued"), then by type.
# By year, then with journal articles first
# sort_criteria = ['-year']   # we have date and type: First by date ("issued"), then by type.
# By date only, newest first
#sort_criteria = ['-date']   # we have date and type: First by date ("issued"), then by type.



###### Special settings


limit=None   # None, or set a limit (integer<100) for each collection for debugging
    
bib_style =  'apa'     # bibliography style format (e.g., 'apa' or 'mla') - Any valid CSL style in the Zotero style repository

show_top_section_headings = 1  # show section headings for the first N sort criteria

catchallcollection = '4KATF6MA'  # include "Miscellaneous" category at end containing all items not mentioend anywhere else

write_full_html_header = True   # False to not output HTML headers.  In this case, expect a file in UTF-8 encoding.

outputfile = 'demo/example3.html'  # relative or absolute path name of output file
category_outputfile_prefix = 'zotero'  # relative or absolute path prefix

show_search_box = True  # show a Javascript/JQuery based search box to filter pubs by keyword.  Must define jquery_path.
jquery_path = "site/jquery.min.js"  # path to jquery file on the server - default: wordpress location

number_bib_items = False  # show bibliographic items as numbered, ordered list
    
show_copy_button = True
clipboard_js_path = "site/clipboard.min.js"
copy_button_path = "site/clippy.svg" # path to file on server

show_links = ['abstract', 'pdf', 'bib','ris']   # unconditionally show these items if they are available.

show_shortcuts = ['collection', ('year', [2019,2018,2017,2016,2015,2014,'2010-2013','2000-2009','-1999']), 'type']

stylesheet_url = "style3.css"


