#!/usr/bin/python2.7
# coding: utf-8

# This will retrieve a set of collections and format an interactive bibliography in HTML5.
# The bibliography contains BibTeX records and abstracts that can be revealed upon clicking.
# The output is ready to be included in other websites (there are options), and it can be 
# easily styles using CSS (see style.css).

# Bibliographic style can be chosen (APA) is default.


# (C) 2014,2015 ,2016 David Reitter, The Pennsylvania State University
# Released under the GNU General Public License, V.3 or later.

from __future__ import print_function

####  Program arguments

# zot.py
# zot.py TOPLEVELFILTER
# zot.py TOPLEVELFILTER CATCHALLCOLLECTION
# zot.py TOPLEVELFILTER CATCHALLCOLLECTION OUTPUTFILE


#### You must configure the following items
# the values given here are mere examples
# You may, alternatively, configure this in a file called "settings.py"

library_id = '160464' # your group or user ID (e.g., six numeric digits)
library_type ='group'  # 'group' or 'user'
api_key = 'xxxxxxxxxxxxxxxxx'  # secret key (from Zotero)

toplevelfilter = 'MGID93AS'   # collection where to start retrieving
catchallcollection = '4KATF6MA'  # include "Miscellaneous" category at end containing all items not mentioend anywhere else

limit=5   # None, or set a limit (integer<100) for each collection for debugging


###### Special settings


bib_style =  'apa'     # bibliography style format (e.g., 'apa' or 'mla') - Any valid CSL style in the Zotero style repository

order_by = 'date'   # order in each category: e.g., 'dateAdded', 'dateModified', 'title', 'creator', 'type', 'date', 'publisher', 'publication', 'journalAbbreviation', 'language', 'accessDate', 'libraryCatalog', 'callNumber', 'rights', 'addedBy', 'numItems'

sort_order = 'desc'   # "desc" or "asc"

write_full_html_header = True   # False to not output HTML headers.  In this case, expect a file in UTF-8 encoding.
stylesheet_url = "style.css"  # If set and write_full_html_header is True, link to this style sheet (a URL)

outputfile = 'zotero-bib.html'  # relative or absolute path name of output file
category_outputfile_prefix = 'zotero'  # relative or absolute path prefix

show_search_box = True  # show a Javascript/JQuery based search box to filter pubs by keyword.  Must define jquery_path.
jquery_path = "jquery_min.js"  # path to jquery file on the server
# jquery_path = "../wp-includes/js/jquery/jquery.js"  # wordpress location

show_links = ['abstract', 'pdf', 'bib', 'ris']   # unconditionally show these items if they are available.








#############################################################################

__version__ = "1.1.0"

#############################################################################


try:
    from settings import *
except ImportError:
    pass

#############################################################################
import sys
import re
def warning(*objs):
    print("WARNING: ", *objs, file=sys.stderr)

from pyzotero import zotero

try:
    v = float("%d.%02d%02d"%tuple(map(int,zotero.__version__.split(r'.'))))
    if v>=1 and v<1.0103:
        warning("Pyzotero version may be incompatible.  Upgrade to 1.1.3 or later.")
except:
        warning("Pyzotero version could not be validated. 1.1.3 or later recommended.")

# redirect warnings (needed for InsecurePlatformWarning on Macs with standard Python)
import logging
logging.basicConfig(filename='zot_warnings.log',level=logging.NOTSET)
logging.captureWarnings(True)
    
import codecs
from texconv import tex2unicode


def print_usage ():
    print("Usage:  zot.py [--div|--full] TOPLEVEL_COLLECTION_ID [CATCHALL_COLLECTION_ID [OUTPUTFILE]]")

if "--div" in sys.argv:
    write_full_html_header = False
    sys.argv.remove('--div')
if "--full" in sys.argv:
    write_full_html_header = True
    sys.argv.remove('--full')
        
if "-h" in sys.argv:
    sys.argv.remove('-h')
    print_usage()
if "--help" in sys.argv:
    sys.argv.remove('--help')
    print_usage()

if len(sys.argv)>1:
    if not sys.argv[1] == "None":
        toplevelfilter = sys.argv[1]
if len(sys.argv)>2:
    if not sys.argv[2] == "None":
        catchallcollection =sys.argv[2]
if len(sys.argv)>3:
    if not sys.argv[3] == "None":
        outputfile =sys.argv[3]


script_html = """<style type="text/css" id="zoterostylesheet" scoped>
.bibshowhide {display:none;}
.abstract {display:none;}
.blink {margin:0;margin-right:15px;padding:0;display:none;}
</style>
<script type="text/javascript">
 function downloadFile(elem) {
  filename = "article.ris"
  if (elem.parentNode) {
    var elems = elem.parentNode.getElementsByTagName('*');
    for (i in elems) {
        if((' ' + elems[i].className + ' ').indexOf(' ' + 'bibshowhide' + ' ') > -1) 
           {
  var ee = elems[i]
  if (ee.childNodes[0]) { ee = ee.childNodes[0] } 
  var pom = document.createElement('a');
  pom.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(ee.innerHTML));
  pom.setAttribute('download', filename);
  document.body.appendChild(pom);
  pom.click();
  document.body.removeChild(pom);
}}}}
function show(elem) {
  if (elem.parentNode) {
   var elems = elem.parentNode.getElementsByTagName('*'), i;
    for (i in elems) {
        if((' ' + elems[i].className + ' ').indexOf(' ' + 'bibshowhide' + ' ') > -1) 
           { if (elems[i].style.display == 'block') {elems[i].style.display = 'none';} else {elems[i].style.display = 'block';}}}}
  return(void(0));}
function changeCSS() {
	if (!document.styleSheets) return;
	var theRules = new Array();
    //ss = document.styleSheets[document.styleSheets.length-1];
    var ss = document.getElementById('zoterostylesheet');
    if (ss) {
    ss = ss.sheet
	if (ss.cssRules)
		theRules = ss.cssRules
	else if (ss.rules)
		theRules = ss.rules
	else return;
	theRules[theRules.length-2].style.display = 'inline';
    theRules[theRules.length-1].style.display = 'inline';
    }
    }
changeCSS();</script>"""

html_header = u''
html_footer = u''
if write_full_html_header:
    style_html = u''
    if stylesheet_url:
        style_html = u"<link rel=\"stylesheet\" type=\"text/css\" href=\"%s\">"%stylesheet_url
    html_header += u'<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN"><html><head><meta charset="UTF-8"><title>Bibliography</title>'+style_html+u'</head><body>'
    html_header += u'<div class="bibliography">'+script_html
    html_footer += u'</div>'
    html_header += '<h1 class="title">'+'Bibliography'+"</h1>\n";
    html_footer += u'</body></html>'
else:
    html_header += u'<div class="bibliography">'+script_html
    html_footer += u'</div>'

search_box = ""
if show_search_box:
    if jquery_path:
        search_box= '<form id="pubSearchBox" name="pubSearchBox"><input id="pubSearchInputBox" type="text" name="keyword" />&nbsp;<input id="pubSearchButton" type="button" value="Search" onClick="searchFunction()" /></form><script type="text/javascript" src="'+jquery_path+""""></script><script type="text/javascript">
  function getURLParameter(name) {
    return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null;
  }
  jQuery( document ).ready(function() {
    jQuery('#pubSearchInputBox').val(getURLParameter("keyword"));
    searchFunction();
  });
  jQuery.expr[":"].icontains = jQuery.expr.createPseudo(function(arg) {
    return function( elem ) {
        return jQuery(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
    };});
function searchFunction() {
  var searchTerms = document.pubSearchBox.keyword.value.split(" ");
  jQuery( ".bib-item").css( "display", "none" );
  var q = ".bib-item";
  jQuery.each(searchTerms, function(i,x) {q = q + ":icontains('"+x+"')";});
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
"""
    else:
        warning("show_search_box set, but jquery_path undefined.")
        

def retrieve_bib (collection, content, style):
    global limit
    if limit:
        items = zot.collection_items(collection, content=content, style=style, limit=limit, order=order_by, sort=sort_order, itemType='-attachment || note')
    else:
        items = zot.everything(zot.collection_items(collection, content=content, style=style, order=order_by, sort=sort_order, itemType='-attachment || note'))
    return items

def write_bib (items, outfile):
        
    file = codecs.open(outfile, "w", "utf-8")

    for item in items:
        file.write(item)

    file.close()


def retrieve_atom (collection):
    global limit
    if limit:
        items = zot.collection_items(collection, format='atom',content='csljson', limit=limit, order=order_by, sort=sort_order, itemType='-attachment || note')
    else:
        items = zot.everything(zot.collection_items(collection, format='atom',content='csljson', order=order_by, sort=sort_order, itemType='-attachment || note'))

    return items


def format_bib(bib):
    return bib.replace("},","},\n")

def format_ris(bib):
    return bib.replace("\n","\\n").replace("\r","\\r")

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
    global html_header
    global html_footer
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

def tryreplacing (source, strings, repl):
    new = None
    for s in strings:
        repl2 = repl.replace("\\0", s)
    	new = source.replace(s, repl2)
	if not new == source:
	   return new
   
    return source

    
def make_html (bibitems, htmlitems, risitems, items, exclude={}, shorten=False):

    string = ""
    for bibitem,htmlitem,risitem,item in zip(bibitems,htmlitems,risitems,items):
        if not exclude.has_key(item[u'id']):
            if item.has_key(u'title'):

                global show_links
                show_items = show_links
                t =  item[u'title']
                u = None
                if item.has_key(u'URL'):
                    u = item[u'URL']
                elif item.has_key(u'url'):
                    u = item[u'url']

                if u:

                    new = tryreplacing(htmlitem, ["<i>"+t+"</i>.",t+".",t], u"<a class=\"doctitle\" href=\"%s\">%s</a>"%(u,"\\0"))
                    
                    if new == htmlitem:
                        # replacement not successful
                        if not 'pdf' in show_items and not 'PDF' in show_items:
                            show_items += ['pdf']
                    else:
                        # remove "Retrieved from"
                        # URL detector from http://daringfireball.net/2010/07/improved_regex_for_matching_urls
                        new = re.sub(r"Retrieved from (?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?]))", "", new)
                        # this is the new item
                        htmlitem = new
                else:
                    htmlitem = tryreplacing(htmlitem, ["<i>"+t+"</i>.",t+".",t], u"<span class=\"doctitle\">%s</span>"%("\\0"))

                if shorten:
                    y = ""
                    if item.has_key(u'date'):
                        y = "(%s)"%item[u'date']
                    elif item.has_key(u'issued'):
                        i = item[u'issued']
                        if i.has_key(u'raw'):
                            y = "(%s)"%i[u'raw']  # to do: get year from more complex date?
                    htmlitem = u"<a href=\"javascript:show(this);\" onclick=\"show(this);\">&#8862;</a> <span class=\"doctitle-short\">%s</span> %s"%(t,y) + "<div class=\"bibshowhide\" style=\"padding-left:20px;\">"+htmlitem+"</div>"
                    htmlitem = u"<div>" + htmlitem + "</div>" # to limit was is being expanded
                    
                if bibitem:

                    abstract,bibitem2 = extract_abstract(bibitem)
                    blinkitem = u""
                    # we print the original item name as label so that capitalization may be chosen via the items list
                    for item in show_items:
                        if 'abstract' == item.lower() and abstract:
                            blinkitem += u"<div class=\"blink\"><a href=\"javascript:show(this);\" onclick=\"show(this);\">%s</a><div class=\"bibshowhide\"><div class=\"abstract\">%s</div></div></div>"%(item,abstract)

                        elif 'bib' == item.lower() and bibitem2:
                            blinkitem += u"<div class=\"blink\"><a href=\"javascript:show(this);\" onclick=\"show(this);\">%s</a><div class=\"bibshowhide\"><div class=\"bib\">%s</div></div></div>"%(item,bibitem2)
                        elif 'pdf' == item.lower() and u:
                            blinkitem += u"<div class=\"blink\"><a href=\"%s\">%s</a></div>"%(u,item)
                        elif 'ris' == item.lower() and risitem:
                            # blinkitem += u"<div class=\"blink\"><a href=\"javascript:show(this);\" onclick=\"show(this);\">%s</a><div class=\"bibshowhide\"><div class=\"bib\">%s</div></div></div>"%(item,risitem)
                            blinkitem += u"<div class=\"blink\"><a title=\"Download EndNote record\" href=\"javascript:downloadFile(this);\" onclick=\"downloadFile(this);\">%s</a><div class=\"bibshowhide\"><div class=\"ris\">%s</div></div></div>"%(item,risitem)

                    if shorten:
                        blinkitem = "<div style=\"padding-left:20px;\">" + blinkitem + "</div>"
                        
                    htmlitem += blinkitem

                string += "<div class=\"bib-item\">" + htmlitem + "</div>"

    if shorten:
        string = "<div class=\"short-bib-section\">" + string + "</div>"
    else:
        string = "<div class=\"full-bib-section\">" + string + "</div>"

    return cleanup_lines(string)


def shortcollection(st):
    return "*" in st.partition(' ')[0]

def strip(string):
    return string.lstrip("0123456789* ")


    
zot = zotero.Zotero(library_id, library_type, api_key)

def coll_data(c):
    if not (u'key' in c and u'name' in c) and u'data' in c:
        c = c[u'data']
    return c

def coll_key(c):
    if u'key' in c:
        return c[u'key']
    return c[u'data'][u'key']

    
collection_ids = {}  # collection names -> IDs
collection_depths = {}  # collection names -> depth
#c=[(x,0) for x in zot.collections_sub(toplevelfilter)]  # this will probably return a maximum of 25
c=zot.collections_sub(toplevelfilter)

collection_filter = {toplevelfilter:False}
for coll in c:  # for each collection
    # pyzotero or Zotero API has changed at some point, so...
    data = coll_data(coll)
    key = data[u'key']

    if not collection_depths.has_key(key):
        collection_depths[key] = 0
    depth = collection_depths[key]

    if (data.has_key(u'parentCollection') and data[u'parentCollection'] in collection_filter) or (data.has_key(u'parent') and data[u'parent'] in collection_filter):
        collection_filter[key] = True  # allow children, include their items
        for coll2 in zot.collections_sub(key):  # get children
            key2 = coll_key(coll2)
            if not key2 in c:
                c += [coll2]  # add child to agenda for crawling
                collection_depths[key2] = depth + 1

    if key in collection_filter:
        collection_ids[data[u'name']] = key  #[x[u'key']]


if collection_depths.values().count(0)==1:  # only one top-level collection?
    # remove top level collection
    for n,k in collection_ids.items():
        if k == toplevelfilter:
            del collection_ids[n]
            print("(Top-level collection will be ignored.)")
            break
    
print("%s collections: "%len(collection_ids.items()))

if limit:
    print("Output limited to %s per collection."%limit)

sortedkeys = collection_ids.keys()
sortedkeys.sort()

# show at end
if catchallcollection:
    sortedkeys += ["Miscellaneous"]
    collection_ids['Miscellaneous'] = catchallcollection


fullhtml = ""
item_ids = {}

def compile_data(collection_id, collection_name, exclude={}, shorten=False):
    global fullhtml
    global item_ids
    global bib_style

    print(" "+" "*collection_depths.get(collection_id,0) + collection_name + "...")
    
    b = retrieve_bib(collection_id,'bibtex', '')
    h = retrieve_bib(collection_id,'bib', bib_style)
    if 'ris' in show_links or "RIS" in show_links or "EndNote" in show_links:
        r = retrieve_bib(collection_id,'ris', '')
    else:
        r = [None for _x in h]
    a = retrieve_atom(collection_id)

    counter = 0
    if not exclude:
        for i in a:
            key = i[u'id']
            if item_ids.has_key(key):
                auth = ""
                # if u'author' in i:
                #     a += ",".join(i[u'author'].values())
                # elif u'editor' in i:
                #     a +=  ",".join(i[u'editor'])
                if u'title' in i:
                    auth = i[u'title'][:14]

                year = ""
                if u'issued' in i and u'raw' in i[u'issued']:
                    year = i[u'issued'][u'raw']
                    
                ref = "%s (%s)"%(auth, year)
                print("Warning: item %s also included in collection %s"%(ref, item_ids[key]))
            item_ids[key] = collection_name
            counter += 1

    corehtml = make_html(b, h, r, a, exclude=exclude, shorten=shorten)
    
    if corehtml and len(corehtml)>0:  # was anything found in this category?
        # write_html([None] * len(h), h, a, 'out.html')
        #html = "dummy"
        html = "<a id='%s' style='{display: block; position: relative; top: -150px; visibility: hidden;}'></a>"%collection_id
        d = 2+collection_depths.get(collection_id,0)
        html += "<h%s class=\"collectiontitle\">%s</h3>\n"%(d,collection_name)
        html += corehtml
        write_some_html(html, category_outputfile_prefix+"-%s.html"%collection_id)
        fullhtml += html

    return counter # number of items included


# start with links to subsections
headerhtml = '<ul class="bib-cat">'

for collection_name in sortedkeys:
    c = 0
    s=shortcollection(collection_name)
    if collection_ids[collection_name] == catchallcollection:
        # now for "Other"
        # Other has everything that isn't mentioned above
        c = compile_data(collection_ids[collection_name], strip(collection_name), exclude=item_ids, shorten=s)
    else:
        c = compile_data(collection_ids[collection_name], strip(collection_name), shorten=s)

    if c>0:
        anchor = collection_ids[collection_name]
        headerhtml += "   <li class='link'><a style='white-space: nowrap;' href='#%s'>%s</a></li>\n"%(anchor,strip(collection_name))

headerhtml += "</ul>"
headerhtml += search_box

        
write_some_html(headerhtml+fullhtml, outputfile)

