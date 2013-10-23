#!/usr/bin/python2.7

# This will retrieve a set of collections and format an interactive bibliography in HTML5.
# The bibliography contains BibTeX records and abstracts that can be revealed upon clicking.
# The output is ready to be included in other websites (there are options), and it can be 
# easily styles using CSS (see style.css).

# Bibliographic style can be chosen (APA) is default.


# (C) 2013 David Reitter, The Pennsylvania State University
# Released under the GNU General Public License, V.3 or later.


####  Program arguments

# zot.py
# zot.py TOPLEVELFILTER
# zot.py TOPLEVELFILTER CATCHALLCOLLECTION
# zot.py TOPLEVELFILTER CATCHALLCOLLECTION OUTPUTFILE


#### You must configure the following items
# the values given here are mere examples

library_id = '160464' # your group or user ID (e.g., six numeric digits)
library_type ='group'  # or 'group' # group or userm
api_key = 'xxxxxxxxxxxxxxxxx'  # secret key (from Zotero)

toplevelfilter = 'MGID93AS'   # collection where to start retrieving
catchallcollection = '4KATF6MA'  # include "Miscellaneous" category at end containing all items not mentioend anywhere else

limit=5   # None, or set a limit (integer<100) for each collection for debugging


###### Special settings


bib_style =  'apa'     # bibliography style format (e.g., 'apa' or 'mla') - Any valid CSL style in the Zotero style repository

order_by = 'date'   # order in each category: e.g., 'dateAdded', 'dateModified', 'title', 'creator', 'type', 'date', 'publisher', 'publication', 'journalAbbreviation', 'language', 'accessDate', 'libraryCatalog', 'callNumber', 'rights', 'addedBy', 'numItems'

sort_order = 'desc'   # "desc" or "asc"

write_full_html_header = False   # False to not output HTML headers.  In this case, expect a file in UTF-8 encoding.

outputfile = 'zotero-bib.html'  # relative or absolute path name of output file
category_outputfile_prefix = 'zotero'  # relative or absolute path prefix

show_search_box = True  # show a Javascript/JQuery based search box to filter pubs by keyword.  Must define jquery_path.
jquery_path = "../wp-includes/js/jquery/jquery.js"  # path to jquery file on the server - default: wordpress location











#############################################################################
try:
    from settings import *
except ImportError:
    pass
#############################################################################

from pyzotero import zotero

import codecs
import sys
from texconv import tex2unicode
import re

script_html = """<style type="text/css" scoped>
.bibshowhide {display:none;}
.abstract {display:none;}
.blink {margin:0;margin-right:15px;padding:0;display:none;}
</style>
<script type="text/javascript">
function show(elem) {
  var elems = elem.parentNode.getElementsByTagName('*'), i;
    for (i in elems) {
        if((' ' + elems[i].className + ' ').indexOf(' ' + 'bibshowhide' + ' ') > -1) 
           { if (elems[i].style.display == 'block') {elems[i].style.display = 'none';} else {elems[i].style.display = 'block';}}}}
function changeCSS() {
	if (!document.styleSheets) return;
	var theRules = new Array();
    ss = document.styleSheets[document.styleSheets.length-1];
	if (ss.cssRules)
		theRules = ss.cssRules
	else if (ss.rules)
		theRules = ss.rules
	else return;
	theRules[theRules.length-2].style.display = 'inline';
    theRules[theRules.length-1].style.display = 'inline';}
changeCSS();</script>"""

if write_full_html_header:
    html_header = u'<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN"><html><head><meta charset="UTF-8"><title>Bibliography</title>'+script_html+u'</head><body>'
    html_header += '<h1 class="title">'+'Bibliography'+"</h1>\n";
    html_footer = u'</body></html>'
else:
    html_header = u'<div class="bibliography">'+script_html
    html_footer = u'</div>'

search_box = ""
if show_search_box and jquery_path:
    search_box= """<form id="pubSearchBox" name="pubSearchBox"><input id="pubSearchInputBox" type="text" name="keyword" />&nbsp;<input id="pubSearchButton" type="button" value="Search" onClick="searchFunction()" /></form><script type="text/javascript" src="%s"></script><script type="text/javascript">
  function getURLParameter(name) {
    return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null;
  }
  jQuery( document ).ready(function() {
    jQuery('#pubSearchInputBox').val(getURLParameter("keyword"));
    searchFunction();
  });
function searchFunction() {
  var searchTerms = document.pubSearchBox.keyword.value.split(" ");
  jQuery( ".bib-item").css( "display", "none" );
  var q = ".bib-item";
  jQuery.each(searchTerms, function(i,x) {q = q + ":contains('"+x+"')";});
  jQuery(q).css( "display", "block" );
}
  jQuery(function() {    // <== Doc ready  
  // stackoverflow q 3971524
    var inputVal = jQuery("#pubSearchInputBox").val(), 
        timer,
        checkForChange = function() {
            var self = this; // or just use .bind(this)
            if (timer) { clearTimeout(timer); }
            // check for change of the text field after each key up
            timer = setTimeout(function() {
                if(self.value != inputVal) {
                    searchFunction();
                    inputVal = self.value
                }
            }, 250);
        };
    jQuery("#pubSearchInputBox").bind('keyup paste cut', checkForChange);
});</script>
"""%(jquery_path)
    
        

def retrieve_bib (collection, content, style):
    global limit
    if limit:
        items = zot.collection_items(collection, content=content, style=style, limit=limit, order=order_by, sort=sort_order)
    else:
        items = zot.everything(zot.collection_items(collection, content=content, style=style, order=order_by, sort=sort_order))
    return items

def write_bib (items, outfile):
        
    file = codecs.open(outfile, "w", "utf-8")

    for item in items:
        file.write(item)

    file.close()


def retrieve_atom (collection):
    global limit
    if limit:
        items = zot.collection_items(collection, format='atom',content='csljson', limit=limit, order=order_by, sort=sort_order)
    else:
        items = zot.everything(zot.collection_items(collection, format='atom',content='csljson', order=order_by, sort=sort_order))

    return items


def format_bib(bib):
    return bib.replace("},","},\n")

def extract_abstract(bib):
    m = re.match(r'(.*)abstract\s*=\s*{?(.*?)}\s*(,|})(.*)', bib, re.DOTALL|re.IGNORECASE)
    if m:
        a = m.group(2)
        b = m.group(1)+m.group(4)
        a = a.replace("{","")
        a = a.replace("}","")
        a = a.replace("\?&", "&amp;")
        return tex2unicode(a),b
    return None,bib

def write_some_html (body, outfile, title=None):
    file = codecs.open(outfile, "w", "utf-8")
    file.write(html_header)
    if title:
        file.write('<h1 class="title">'+title+"</h1>")
    file.write(body)
    file.write(html_footer)
    file.close()

def cleanup_lines (string):
    "Remove double line feeds to protect from <P> insertion in Wordpress."
    # Wordpress likes to insert <P>, which is not a good idea here.
    return re.sub(r'\n\s*\n', '\n', string, flags=re.DOTALL)
    
def make_html (bibitems, htmlitems, items, exclude={}):

    string = ""
    for bibitem,htmlitem,item in zip(bibitems,htmlitems,items):
        if not exclude.has_key(item[u'id']):
            if item.has_key(u'title'):

                t =  item[u'title']
                u = None
                if item.has_key(u'URL'):
                    u = item[u'URL']
                elif item.has_key(u'url'):
                    u = item[u'url']

                if u:
                    new = htmlitem.replace(t, u"<a class=\"doctitle\" href=\"%s\">%s</a>"%(u,t))
                    if new == htmlitem:
                        # replacement not successful
                        htmlitem += u"<div class=\"blink\"><a class=\"doctitle\" href=\"%s\">PDF</a></div>"%u
                    else:
                        # remove "Retrieved from"
                        # URL detector from http://daringfireball.net/2010/07/improved_regex_for_matching_urls
                        new = re.sub(r"Retrieved from (?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?]))", "", new)
                        # this is the new item
                        htmlitem = new
                else:
                    htmlitem = htmlitem.replace(t, u"<span class=\"doctitle\">%s</span>"%(t))
                    
                if bibitem:

                    abstract,bibitem2 = extract_abstract(bibitem)

                    if abstract:
                        htmlitem += u"<div class=\"blink\"><a href=\"javascript:show(this);\" onclick=\"show(this);\">abstract</a><div class=\"bibshowhide\"><div class=\"abstract\">%s</div></div></div>"%(abstract)
                    
                    htmlitem += u"<div class=\"blink\"><a href=\"javascript:show(this);\" onclick=\"show(this);\">bib</a><div class=\"bibshowhide\"><div class=\"bib\">%s</div></div></div>"%(bibitem2)
    
                    
                string += "<div class=\"bib-item\">" + htmlitem + "</div>"

    return cleanup_lines(string)



    
zot = zotero.Zotero(library_id, library_type, api_key)

if len(sys.argv)>1:
    if not sys.argv[1] == "None":
        toplevelfilter = sys.argv[1]
if len(sys.argv)>2:
    if not sys.argv[2] == "None":
        catchallcollection =sys.argv[2]
if len(sys.argv)>3:
    if not sys.argv[3] == "None":
        outputfile =sys.argv[3]
if len(sys.argv)>4:
    if sys.argv[4] == "--div":
        write_full_html_header = False
        

    
collection_ids = {}
c=zot.collections()


collection_filter = {toplevelfilter:False}
lastsize = 0
while True:
    for x in c:
        if x.has_key(u'parent') and  x[u'parent'] in collection_filter:
            collection_filter[x[u'key']] = True  # allow children, include their items

        if x[u'key'] in collection_filter:
            collection_ids[x[u'name']] = x[u'key']  #[x[u'key']]

    size = len(collection_ids.keys())
    if size == lastsize:
        break
    lastsize = size
            

if lastsize>1:  # has sub-collections?
    # remove top level collection
    for n,k in collection_ids.items():
        if k == toplevelfilter:
            del collection_ids[n]
            print("(Top-level collection will be ignored.)")
            break
    
print("%s collections: "%lastsize)

if limit:
    print("Output limited to %s per collection."%limit)

sortedkeys = collection_ids.keys()
sortedkeys.sort()

# show at end
if catchallcollection:
    sortedkeys += ["Miscellaneous"]
    collection_ids['Miscellaneous'] = catchallcollection

# start with links to subsections
fullhtml = ""

fullhtml = '<ul class="bib-cat">'
for collection_name in sortedkeys:
    anchor = collection_ids[collection_name]
    fullhtml += "   <li class='link'><a href='#%s'>%s</a></li>\n"%(anchor,collection_name)
fullhtml += "</ul>"
fullhtml += search_box
item_ids = {}

def compile_data(collection_id, collection_name, exclude={}):
    global fullhtml
    global item_ids
    global bib_style

    print(collection_name + "...")
    
    b = retrieve_bib(collection_id,'bibtex', '')
    h = retrieve_bib(collection_id,'bib', bib_style)
    a = retrieve_atom(collection_id)

    if not exclude:
        for i in a:
            key = i[u'id']
            if item_ids.has_key(key):
                print("warning - item %s included additionally in collection %s"%(key, collection_name))
            item_ids[key] = True
    
    
    # write_html([None] * len(h), h, a, 'out.html')
    #html = "dummy"
    html = "<h3 id=\"%s\" class=\"collectiontitle\">%s</h3>\n"%(collection_id,collection_name)
    html += make_html(b, h, a, exclude=exclude)
    write_some_html(html, category_outputfile_prefix+"-%s.html"%collection_id)
    fullhtml += html


for collection_name in sortedkeys:
    if collection_ids[collection_name] == catchallcollection:
        # now for "Other"
        # Other has everything that isn't mentioned above
        compile_data(collection_ids[collection_name], collection_name, exclude=item_ids)
    else:
        compile_data(collection_ids[collection_name], collection_name)

write_some_html(fullhtml, outputfile)

