#!/usr/bin/env python2.7
# coding: utf-8

# This will retrieve a set of collections and format an interactive bibliography in HTML5.
# The bibliography contains BibTeX records and abstracts that can be revealed upon clicking.
# The output is ready to be included in other websites (there are options), and it can be 
# easily styles using CSS (see style.css).

# Bibliographic style can be chosen (APA) is default.


# (C) 2014, 2015, 2016, 2017 David Reitter, The Pennsylvania State University
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

titlestring = 'Bibliography'

bib_style =  'apa'     # bibliography style format (e.g., 'apa' or 'mla') - Any valid CSL style in the Zotero style repository


sort_criteria = ['collection', '-year', 'type']   # we have subcollection, date, year and type

#sort_criteria = ['-year', 'type']   # we have date, year and type: First by year, then by type.
# sort_criteria = ['type', '-year']   # also common: order by publication type first, then by year

show_top_section_headings = 1  # show section headings for the first N sort criteria

write_full_html_header = True   # False to not output HTML headers.  In this case, expect a file in UTF-8 encoding.
stylesheet_url = "style.css"  # If set and write_full_html_header is True, link to this style sheet (a URL)

outputfile = 'zotero-bib.html'  # relative or absolute path name of output file
category_outputfile_prefix = 'zotero'  # relative or absolute path prefix

show_search_box = True  # show a Javascript/JQuery based search box to filter pubs by keyword.  Must define jquery_path.
jquery_path = "jquery_min.js"  # path to jquery file on the server
# jquery_path = "../wp-includes/js/jquery/jquery.js"  # wordpress location

show_links = ['abstract', 'pdf', 'bib', 'ris']   # unconditionally show these items if they are available.


#### Even more special settings
    
# sortkeyname_order defines the order and the display names of some fields.
# This is used in section headings when show_top_section_headings is >0
# we're not primarily sorting by collection.

sortkeyname_order = {}
# Define label for article types and their ordering
sortkeyname_order['type'] = {'article-journal':(0,'Journal Articles'),
                           'paper-conference':(2, 'Conference and Workshop Papers'),
                           'book':(5,'Books and Collections'),
                           'chapter':(7,'Book Chapters'),
                           'thesis':(10,'Theses'),
                           'speech':(15,'Talks')}


##### legacy settings

    
order_by = None   # order in each category: e.g., 'dateAdded', 'dateModified', 'title', 'creator', 'type', 'date', 'publisher', 'publication', 'journalAbbreviation', 'language', 'accessDate', 'libraryCatalog', 'callNumber', 'rights', 'addedBy', 'numItems'
# Note: this does not seem to work with current the Zotero API.
# If set, overrides sort_criteria
sort_order = 'desc'   # "desc" or "asc"




#############################################################################

__version__ = "2.0.0"

#############################################################################


try:
    from settings import *
except ImportError:
    pass

#############################################################################
import sys
import re
import copy
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
  pom.href = window.URL.createObjectURL(new Blob([ee.innerHTML], {type: 'text/plain;charset=utf-8'}));
  pom.download = filename;
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
    html_header += u'<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN"><html><head><meta charset="UTF-8"><title>'+titlestring+u'</title>'+style_html+u'</head><body>'
    html_header += u'<div class="bibliography">'+script_html
    html_footer += u'</div>'
    html_header += '<h1 class="title">'+titlestring+"</h1>\n";
    html_footer += u'</body></html>'
else:
    html_header += u'<div class="bibliography">'+script_html
    html_footer += u'</div>'

search_box = ""
if show_search_box:
    if jquery_path:
        search_box= '<form id="pubSearchBox" name="pubSearchBox"><input id="pubSearchInputBox" type="text" name="keyword" />&nbsp;<input id="pubSearchButton" type="button" value="Search" onClick="searchFunction()" /></form><h2 id="searchTermSectionTitle" class="collectiontitle"></h2><script type="text/javascript" src="'+jquery_path+""""></script><script type="text/javascript">
  function getURLParameter(name) {
    return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1])||null;
  }
  jQuery( document ).ready(function() {
    jQuery('#pubSearchInputBox').val(getURLParameter("keyword"));
    searchFunction(getURLParameter("keyword"));
  });
  jQuery.expr[":"].icontains = jQuery.expr.createPseudo(function(arg) {
    return function( elem ) {
        return jQuery(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
    };});
function searchFunction(searchTerms) {
  var i = document.pubSearchBox.keyword.value;
  var searchTerms = searchTerms || (i!=""&&i.split(" "));
  jQuery( ".bib-item").css( "display", "none" );
  var q = ".bib-item";
  jQuery.each(searchTerms, function(i,x) {q = q + ":icontains('"+x+"')";});
  jQuery(q).css("display", "block");
  jQuery("#searchTermSectionTitle").html(searchTerms.length>0?"<a href='#' onclick='searchFunction([]);'>&#x2715;</a> "+searchTerms:"");
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


if order_by:  # set by user (legacy setting)
    sort_critera = ['collection', order_by]
else:
    order_by = 'date'

# find sort order for each criterion
sort_reverse = []
for i, c in enumerate(sort_criteria):
    if c[0] == '-':
        sort_criteria[i] = c[1:]
        sort_reverse += [True]
    else:
        sort_reverse += [False]


    
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

#  Atom bib entry:
# {u'publisher': u'Routledge Psychology Press', u'author': [{u'given': u'David', u'family': u'Reitter'}], u'collection-title': u'Frontiers of Cognitive Psychology', u'issued': {u'raw': u'January 2017'}, u'title': u'Alignment in Web-based Dialogue: Who Aligns, and how Automatic is it? Studies in Big-Data Computational Psycholinguistics', u'editor': [{u'given': u'Michael N.', u'family': u'Jones'}], u'container-title': u'Big Data in Cognitive Science', u'type': u'chapter', u'id': u'1217393/IVR7H8TD'}

def retrieve_atom (collection):
    global limit
    if limit:
        items = zot.collection_items(collection, format='atom',content='csljson', limit=limit, order=order_by, sort=sort_order, itemType='-attachment || note')
    else:
        items = zot.everything(zot.collection_items(collection, format='atom',content='csljson', order=order_by, sort=sort_order, itemType='-attachment || note'))
    return items


def access(atom_item, key, default=""):
    key = u"%s"%key
    if key in atom_item:
        return atom_item[key]
    if key=='year' and u'issued' in atom_item:
        fulldate = atom_item[u'issued'][u'raw']
        m = re.search('[0-9][0-9][0-9][0-9]', fulldate)
        if m:
            return m.group(0)
        return fulldate  # fallback
        
    if key=='date' and u'issued' in atom_item:
        return atom_item[u'issued'][u'raw']

    return default  # default
    # raise RuntimeError("access: field %s not found."%key)

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
    for s in strings:
        if s in source:
            repl2 = repl.replace("\\0", s)
            return source.replace(s, repl2)
    return source
    
def make_html (all_items, exclude={}, shorten=False):

    # bibitems, htmlitems, risitems, items
    
    string = ""
    for bibitem,htmlitem,risitem,item in all_items:
        if bibitem != "HEADER" and not item[u'id'] in exclude:
            if u'title' in item:
                global show_links
                show_items = show_links
                t =  item[u'title']
                u = None
                if u'URL' in item:
                    u = item[u'URL']
                elif u'url' in item:
                    u = item[u'url']

                t2 = t.replace(u"'",u'’') # technically, we're going to have to do much more (or do a flexible match)
                t_to_replace = ["<i>"+t+"</i>.","<i>"+t2+"</i>.","<i>"+t+"</i>","<i>"+t2+"</i>",t+".",t2+".",t,t2]
                if u:
                    new = tryreplacing(htmlitem, t_to_replace, u"<span class=\"doctitle\"><a class=\"doctitle\" href=\"%s\">%s</a></span>"%(u,"\\0"))

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
                    htmlitem = tryreplacing(htmlitem, t_to_replace, u"<span class=\"doctitle\">%s</span>"%("\\0"))
                    
                if u'section_keyword' in item:
                    htmlitem += "<span style='display:none;'>%s</span>"%item[u'section_keyword']
                    
                if shorten:
                    y = ""
                    if u'date' in item:
                        y = "(%s)"%item[u'date']
                    elif u'issued' in item:
                        i = item[u'issued']
                        if u'raw' in i:
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


def is_short_collection(st):
    if not isinstance(st, basestring):
        return any([is_short_collection(x) for x in st])
    return "*" in st.partition(' ')[0]

def strip(string):
    stripped = string.lstrip("0123456789* ")
    if stripped == "":
        return string
    return stripped
    
    
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
collection_parents = {}  # collection names -> list of collection parents
#c=[(x,0) for x in zot.collections_sub(toplevelfilter)]  # this will probably return a maximum of 25
c=zot.collections_sub(toplevelfilter)

collection_filter = {toplevelfilter:False}
for coll in c:  # for each collection
    # pyzotero or Zotero API has changed at some point, so...
    data = coll_data(coll)
    key = data[u'key']
    name = data[u'name']
    
    if not name in collection_parents:
        collection_parents[name] = []
    parents = collection_parents[name]  # read depth

    if (u'parentCollection' in data and data[u'parentCollection'] in collection_filter) or (u'parent' in data and data[u'parent'] in collection_filter):
        collection_filter[key] = True  # allow children, include their items
        for coll2 in zot.collections_sub(key):  # get children
            key2 = coll_key(coll2)
            if not key2 in c:
                name2 = coll_data(coll2)[u'name']
                c += [coll2]  # add child to agenda for crawling
                collection_parents[name2] = parents + [name]

    if key in collection_filter:
        collection_ids[name] = key  #[x[u'key']]


if collection_parents.values().count(0)==1:  # only one top-level collection?
    # remove top level collection
    for n,k in collection_ids.items():
        if k == toplevelfilter:
            del collection_ids[n]
            print("(Top-level collection will be ignored.)")
            break

print("%s collections: "%len(collection_ids.items()))
if 0==len(collection_ids.items()) and catchallcollection != toplevelfilter:
    print("Warning: Items in the top level collections are excluded.")
    print("Move your items into subcollections or use the catchallcollection setting.")
if limit:
    print("Output limited to %s per collection."%limit)

sortedkeys = collection_ids.keys()
sortedkeys.sort()

# show at end
if catchallcollection:
    sortedkeys += ["Miscellaneous"]
    collection_ids['Miscellaneous'] = catchallcollection
    collection_parents['Miscellaneous'] = []

fullhtml = ""
item_ids = {}

def retrieve_data(collection_id, exclude=None):
    
    global item_ids

    # all = retrieve_bib(collection_id,'bibtex,bib,ris', '')
    # print(all)
    # sys.exit(1)
    
    b = retrieve_bib(collection_id,'bibtex', '')
    h = retrieve_bib(collection_id,'bib', bib_style)
    if 'ris' in show_links or "RIS" in show_links or "EndNote" in show_links:
        r = retrieve_bib(collection_id,'ris', '')
    else:
        r = [None for _x in h]
    a = retrieve_atom(collection_id)
    return zip(b,h,r,a)

def collect_ids (quaditems, collection_name, items_ids):
    c=0
    for _,_,_,i in quaditems:
        if key in item_ids:
            auth = ""
            if u'title' in i:
                auth = access(i,'title')[:14]
            year = access(i, 'year')
            ref = "%s (%s)"%(auth, year)
            print("Warning: item %s also included in collection %s"%(ref, item_ids[key]))
        else:
            item_ids[i[u'id']] = collection_name
            c+=1
    return c


        
def filter_items(quaditems, exclude):
    def fil(qi):
        _,_,_,a = qi
        # print(a)
        return not (a[u'id'] in item_ids)
    return filter(fil, quaditems)

def merge_doubles(items):
    iids = {}
    def rd(it):
        _,_,_,a = it
        key = a[u'id']
        if ksi in iids and not (u'collection' in iids[key] and is_short_collection(iids[key][u'collection']))
            # merge "section keywords"
            if u'section_keyword' in a:
                if not u'section_keyword' in iids[key]:
                    iids[key][u'section_keyword'] = ""
                iids[key][u'section_keyword'] += " "+a[u'section_keyword']
            return False
        else:
            iids[key] = a
            return True

    return filter(rd, items)


def sortkeyname(field, value):
    global sortkeyname_order
    # field may be a single field, or a list of fields
    # value corresponds to field
    if not isinstance(value, basestring):
        # it's a path of something
        # sorting by all the numbers (if available).e.g. 10-13, and displaying the last entry
        
        return ".".join([str(sortkeyname(field2, value2)[0]) for field2,value2 in zip(field,value)]), sortkeyname(field[-1], value[-1])[1]
    if field in sortkeyname_order:
        if value in sortkeyname_order[field]:
            return sortkeyname_order[field][value]
        return 100,value  # sort at the end
    if field == "collection":

        m = re.match(r'([0-9]+)\s*\*?\s(.*)', value)
        if m:
            return m.group(1), m.group(2)  # like "strip"
        
    return value,value  # sort by value

def last(string_or_list):
    if not isinstance(string_or_list, basestring):
        return string_or_list[-1]
    return string_or_list


def compile_data(all_items, section_code, crits, exclude={}, shorten=False):
    global fullhtml
    global item_ids
    global bib_style
    global show_top_section_headings


    corehtml = make_html(all_items, exclude=exclude, shorten=shorten)

    # empty categories shouldn't actually be passed to compile_data
    # if len(all_items)>0 and corehtml:   # if corehtml and len(corehtml)>0:  # was anything found in this category?
    html = ""
    section_print_title = sortkeyname(crits, section_code)[1]
    collection_id=collection_ids.get(last(section_code), None) # if collection, get its ID
    if collection_id:
        html += "<a id='%s' style='{display: block; position: relative; top: -150px; visibility: hidden;}'></a>"%collection_id
    if section_code and show_top_section_headings:
        depth=0
        if not isinstance(section_code, basestring):
            depth = len(section_code)-1 # it's a path
        # do not show headings deeper than this
        # if depth<=show_top_section_headings:
        html += "<h%s class=\"collectiontitle\">%s</h3>\n"%(2+depth,section_print_title)
    html += corehtml
    write_some_html(html, category_outputfile_prefix+"-%s.html"%(section_print_title or ""))
    fullhtml += html

    return None


# start with links to subsections
headerhtml = '<ul class="bib-cat">'

all_items = []
section_items = []
for collection_name in sortedkeys:
    c = 0
    id = collection_ids[collection_name]
    print(" "+" "*len(collection_parents.get(collection_name,[])) + collection_name + "...")

    i2 = retrieve_data(id)
    if id == catchallcollection:  # Miscellaneous
        # This has everything that isn't mentioned above
        # so we'll filter what's in item_ids
        i2 = filter_items(i2, item_ids)

    # add IDs to the list with the collection name
    collect_ids(i2, collection_name, item_ids)
        
    print("%s Items."%len(i2))

    parent_path = tuple(collection_parents[collection_name] + [collection_name])
    for _,_,_,a in i2:  # for sorting by collection
        a[u'collection'] = parent_path
        
    # if sort_criteria[0] != 'collection':
    for _,_,_,a in i2:
        a[u'section_keyword'] = strip(collection_name) # will be added HTML so the entry can be found

    if len(i2)>0:
        all_items += i2
        if show_search_box:  # search box is necessary for this to work
            # Keyword filter
            headerhtml += "   <li class='link'><a style='white-space: nowrap;' href='#' onclick='searchFunction([\"%s\"]);return false;'>%s</a></li>\n"%(strip(collection_name),strip(collection_name))
                


all_items = merge_doubles(all_items)
            

# remove double entries
# sorting the items
if sort_criteria:
    # sort is stable, so we will sort several times, from the last to the first criterion
    for crit,rev in reversed(zip(sort_criteria, sort_reverse)):
        # all_items contains 4-tuples, the last one is the atom representation
        all_items.sort(key=lambda x: sortkeyname(crit, access(x[3],crit))[0], reverse=rev)


try:
    from itertools import zip_longest, islice
except ImportError:
    # Python 2
    from itertools import izip_longest as zip_longest
    from itertools import islice
    
def section_generator (all_items, crits):
    
    collect = []
    prev_section = ""
    #crit = crits[0]  ## TO DO:  section headings for all sort criteria
    crits_sec = []
    section = []
    def changed_section_headings(prev_section, section):
        cum_new_section = []
        do_rem = False
        for p,n in zip_longest(prev_section, section, fillvalue=None):
            cum_new_section = cum_new_section + [n]  # make copy to preserve previous entries
            if n and (p != n or do_rem):  # level is different
                yield cum_new_section
                do_rem = True

    
    for item_quad in all_items:
        first,_,_,item = item_quad

        # construct section path identifier
        # also, make matching criterion identifier
        section = []
        crits_sec = []
        for crit in crits[:show_top_section_headings]:
            val = access(item, crit)
            if isinstance(val, basestring):
                section += [val]
                crits_sec += [crit]
            else:
                section += val # flat concat
                crits_sec += [crit] * len(val)
                
        #section = access(item, crit)
        if section != prev_section:
            changed_sections = list(changed_section_headings(prev_section, section))
            if changed_sections:
                if len(collect)>0:
                    yield prev_section, crits_sec, collect
                # new section, show a section header.  add as separate item.
                # add a header for every level that has changed
                # except for the last one - that'll come with the next set of items
                for s in changed_sections: #[:-1]:
                    if not s == section:  # because that would be the heading for the next set of items.
                        yield s, crits_sec[:len(s)], []

                collect = []
            prev_section = section
        collect += [item_quad]
    yield prev_section, crits_sec, collect

for section_code, crits, items in section_generator(all_items, sort_criteria):
    print (section_code, crits, len(items), "items")
    compile_data(items, section_code, crits, shorten=is_short_collection(section_code))



# Note: all of this needs a major rewrite to be more flexible
# we should be able to do sort_criteria = [ 'year', 'collection']

    
            
headerhtml += "</ul>"
headerhtml += search_box

        
write_some_html(headerhtml+fullhtml, outputfile)

