#!/usr/bin/env python2.7
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

# For best results, configure this in a file called "settings.py".
# The values given here are mere examples

library_id = '160464' # your group or user ID (e.g., six numeric digits) - this is an example
library_type ='group'  # 'group' or 'user'
api_key = ''  # secret key (from Zotero)

toplevelfilter = None   #  collection where to start retrieving
# toplevelfilter = 'MGID93AS'  # (Try this for an example)

catchallcollection = None  # include "Miscellaneous" category for all remaining items
# catchallcollection = '4KATF6MA'  # (Try this for an example)

limit=5   # None, or set a limit (integer<100) for each collection for debugging


###### Special settings - no need to change these

titlestring = 'Bibliography'

bib_style =  'apa'     # bibliography style format (e.g., 'apa' or 'mla') - Any valid CSL style in the Zotero style repository

order_by = 'date'   # order in each category: e.g., 'dateAdded', 'dateModified', 'title', 'creator', 'type', 'date', 'publisher', 'publication', 'journalAbbreviation', 'language', 'accessDate', 'libraryCatalog', 'callNumber', 'rights', 'addedBy', 'numItems'

sort_order = 'desc'   # "desc" or "asc"

write_full_html_header = True   # False to not output HTML headers.  In this case, expect a file in UTF-8 encoding.
stylesheet_url = "site/style.css"  # If set and write_full_html_header is True, link to this style sheet (a URL)

outputfile = 'zotero-bib.html'  # relative or absolute path name of output file
category_outputfile_prefix = 'zotero'  # relative or absolute path prefix

jquery_path = "site/jquery.min.js"  # path to jquery file on the server
# jquery_path = "../wp-includes/js/jquery/jquery.js"  # wordpress location

show_copy_button = True  # show clipbaord copy button.  Must define jquery_path.
clipboard_js_path = "site/clipboard.min.js"
copy_button_path = "site/clippy.svg"
show_search_box = True  # show a Javascript/JQuery based search box to filter pubs by keyword.  Must define jquery_path.

show_links = ['abstract', 'pdf', 'bib', 'wikipedia', 'ris']   # unconditionally show these items if they are available.

smart_selections = True # Prevent viewers from selecting "bib", "pdf" etc for easier copy/paste of bibliography

#############################################################################

__version__ = "1.2.0"

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

from pyzotero import zotero,zotero_errors

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


###########

def cleanup_lines (string):
    "Remove double line feeds to protect from <P> insertion in Wordpress."
    # Wordpress likes to insert <P>, which is not a good idea here.
    return re.sub(r'\n\s*\n', '\n', string, flags=re.DOTALL)


# smart selections prevents viewers from copying certain buttons
# this way, a nice, clean bibliography can be copied right from a browser window
# this is achieved by displaying the buttons dynamically.
# caveat - are there accessibility implications?
if smart_selections:
    blinkitem_css = "".join(["a.%s::before {content:\"%s\"}\n"%(i,i) for i in show_links])
    blinkitem_css += "a.shortened::before {content:\"\\229E\"}\n"  # hex(8862)
else:
    blinkitem_css = "".join(["a.%s::before {}\n"%(i) for i in show_links])
    blinkitem_css += "a.shortened::before {}\n"

# note - the final two styles in the style sheet are manipulated by changeCSS
# these are selected (hack, hack) by index
# the .blink p style is a hack because Wordpress seems to insert <p> at times.
script_html = """<style type="text/css" id="zoterostylesheet" scoped>
.bibshowhide {display:none;}
"""+ blinkitem_css + """.blink p {display:inline;}
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
	var elems = elem.parentNode.parentNode.getElementsByTagName('*');
	for (i in elems) {
        if((' ' + elems[i].className + ' ').indexOf(' ' + 'bibshowhide' + ' ') > -1) 
	    { if (elems[i].parentNode != elem.parentNode)
		    elems[i].style.display = 'none';
	    }}
	elems = elem.parentNode.getElementsByTagName('*');
	for (i in elems) {
        if((' ' + elems[i].className + ' ').indexOf(' ' + 'bibshowhide' + ' ') > -1) 
	    { elems[i].style.display = (elems[i].style.display == 'block') ? 'none' : 'block';
	    }}}
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


if show_copy_button:
    if jquery_path:
        script_html += """<script type="text/javascript" src="%s"></script>
    <script type="text/javascript" src="%s"></script>
    <script type="text/javascript">
    jQuery(document).ready(function () {
    jQuery( "div.bib" ).append('\\n<button class="btn"><img src="%s" width=13 alt="Copy to clipboard"></button>');
        new Clipboard('.btn',{
text: function(trigger) {
var prevCol = trigger.parentNode.style.color;
trigger.parentNode.style.color="grey";
setTimeout(function(){trigger.parentNode.style.color=prevCol;}, 200);
return trigger.parentNode.childNodes[0].textContent;}});});</script>"""%(jquery_path,clipboard_js_path,copy_button_path)
    else:
        warning("show_search_box set, but jquery_path undefined.")

credits_html = u'<div name="zbw_credits" style="text-align:right;">A <a href="https://github.com/davidswelt/zot_bib_web">zot_bib_web</a> bibliography.</div>'

script_html = cleanup_lines(script_html)
        
html_header = u''
html_footer = u''
if write_full_html_header:
    style_html = u''
    if stylesheet_url:
        style_html = u"<link rel=\"stylesheet\" type=\"text/css\" href=\"%s\">"%stylesheet_url
    html_header += u'<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN"><html><head><meta charset="UTF-8"><title>'+titlestring+u'</title>'+style_html+u'</head><body>'
    html_header += u'<div class="bibliography">'+script_html
    html_footer += credits_html + u'</div>'
    html_header += '<h1 class="title">'+titlestring+"</h1>\n";
    html_footer += u'</body></html>'
else:
    html_header += u'<div class="bibliography">'+script_html
    html_footer += credits_html + u'</div>'

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
});</script>"""
    else:
        warning("show_search_box set, but jquery_path undefined.")
        

def retrieve_x (collection,**args):
    global limit
    if limit:
        items = zot.collection_items(collection, limit=limit, order=order_by, sort=sort_order, itemType='-attachment || note', **args)
    else:
        items = zot.everything(zot.collection_items(collection, order=order_by, sort=sort_order, itemType='-attachment || note', **args))
    return items

def retrieve_bib (collection, content, style):
    return retrieve_x(collection, content=content, style=style)

def retrieve_atom (collection):
    return retrieve_x(collection, content='csljson', format='atom')

def retrieve_coins (collection):
    return retrieve_x(collection, content='coins')

def retrieve_wikipedia (collection):
    return retrieve_x(collection, content='wikipedia')

def write_bib (items, outfile):
        
    file = codecs.open(outfile, "w", "utf-8")

    for item in items:
        file.write(item)

    file.close()


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

def tryreplacing (source, strings, repl):
    for s in strings:
        if s in source:
            repl2 = repl.replace("\\0", s)
            return source.replace(s, repl2)
    return source
    
def sortitems (data, sort_criteria):
    if not sort_criteria:
        return data
    zipped = zip(data,[[None for _i in sort_criteria] for _x in data])
    # the second item of each tuple in zipped
    # contains the values to sort by.
    for i,val in zipped:
        for num,c in enumerate(sort_criteria):
            # for each sort criterion, extract the value for the item
            if i[-1].has_key(c):
                # if available, write value into tuple
                if c==u'author' and isinstance(i[-1][c],list) and i[-1][c][0].has_key(u'family') and i[-1][c][0].has_key(u'given'):
                    val[num] = i[-1][c][0][u'family']+','+i[-1][c][0][u'given']
                elif c==u'page':
                    try:
                        val[num] = i[-1][c].split('-')[0]
                        val[num] = int(val[num])
                    except:
                        val[num] = i[-1][c]
                else:
                    val[num] = i[-1][c]
    zipped = sorted(zipped, key=lambda x:x[1])
    return [d for d,_sv in zipped]
# [u'issued',u'author']  (by date, then author)
# [u'page']  (just sort by page number)

def make_html (bibitems, htmlitems, risitems, coinsitems, wikiitems, items, exclude={}, shorten=False):
    def a_button (name,url=None,js=None,title=None,cls=None):
        global smart_selections
        if not js:
            js = "show(this)"
        if not url:
            url = "javascript:"+js+";"
        if not cls:
            cls = name
        title2 = ""
        if title:
            title2 = "title=\"%s\""%title
        return u"<a class=\"%s\" %s href=\"%s\" onclick=\"%s\">%s</a>"%(cls,title2,url,js,("" if smart_selections else name))

    sort_criteria = None   # [u'page']  # TODO - allow user to set this; document
    
    string = ""
    for bibitem,htmlitem,risitem,coinsitem,wikiitem,item in sortitems(zip(bibitems,htmlitems,risitems,coinsitems,wikiitems,items),sort_criteria):
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

                if coinsitem:
                    htmlitem += str(coinsitem).strip()
                    
                if bibitem:

                    abstract,bibitem2 = extract_abstract(bibitem)
                    blinkitem = u""
                    # we print the original item name as label so that capitalization may be chosen via the items list
                    for item in show_items:

                        if 'abstract' == item.lower() and abstract:
                            blinkitem += u'<div class="blink">'+a_button(item)+u'<div class="bibshowhide"><div class="abstract">%s</div></div></div>'%(abstract)
                        elif 'wikipedia' == item.lower() and wikiitem:
                            blinkitem += u'<div class="blink">'+a_button(item)+u'<div class="bibshowhide"><div class="bib" style="white-space:pre-wrap;">%s</div></div></div>'%(wikiitem)
                        elif 'bib' == item.lower() and bibitem2:
                            blinkitem += u'<div class="blink">'+a_button(item)+u'<div class="bibshowhide"><div class="bib">%s</div></div></div>'%(bibitem2)
                        elif 'pdf' == item.lower() and u:
                            blinkitem += u'<div class="blink">'+a_button(item,url=u)+u'</div>'
                        elif 'ris' == item.lower() and risitem:
                            blinkitem += u'<div class="blink">'+a_button(item,title="Download EndNote record",js="downloadFile(this)")+u'<div class="bibshowhide"><div class="ris">%s</div></div></div>'%(risitem)

                    if shorten:
                        blinkitem = u'<div style="padding-left:20px;">' + blinkitem + u'</div>'
                        
                    htmlitem += blinkitem

                string += u'<div class="bib-item">' + htmlitem + u'</div>'

    if len(string)==0:
        return ""  # avoid adding title for section later on

    if shorten:
        string = u'<div class="short-bib-section">' + string + u'</div>'
    else:
        string = u'<div class="full-bib-section">' + string + u'</div>'

    return cleanup_lines(string)


def shortcollection(st):
    return "*" in st.partition(' ')[0]

def strip(string):
    return string.lstrip("0123456789* ")

def coll_data(c):
    if not (u'key' in c and u'name' in c) and u'data' in c:
        c = c[u'data']
    return c

def coll_key(c):
    if u'key' in c:
        return c[u'key']
    return c[u'data'][u'key']


collection_filter = {}  # top-level nodes

try:
    zot = zotero.Zotero(library_id, library_type, api_key)
    
    collection_ids = {}  # collection names -> IDs
    collection_depths = {}  # collection names -> depth
    #c=[(x,0) for x in zot.collections_sub(toplevelfilter)]  # this will probably return a maximum of 25
    if toplevelfilter:
        c = zot.collections_sub(toplevelfilter)
        collection_filter[toplevelfilter] = False
    else:
        print("Fetching all collections:")
        c = []
        for col in zot.collections():
            name=""
            if col.has_key(u'data'):
                name = col[u'data'].get(u'name',"")
            print(col[u'key']+": "+name)
            c += zot.collections_sub(col[u'key'])
            collection_filter[col[u'key']] = False
        
        
except zotero_errors.UserNotAuthorised:
    print("UserNotAuthorised: Set Zotero API key in settings.py or zot.py.", file=sys.stderr)
    raise SystemExit(1)


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
    c = retrieve_coins(collection_id)
    if 'wikipedia' in show_links or 'WIKIPEDIA' in show_links or "Wikipedia" in show_links:
        w = retrieve_wikipedia(collection_id)
    else:
        w = [None for _x in h]
        
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

    corehtml = make_html(b, h, r, c, w, a, exclude=exclude, shorten=shorten)
    
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
        c = compile_data(collection_ids[collection_name], strip(collection_name), exclude=copy.copy(item_ids), shorten=s)
    else:
        c = compile_data(collection_ids[collection_name], strip(collection_name), shorten=s)

    if c>0:
        anchor = collection_ids[collection_name]
        headerhtml += "   <li class='link'><a style='white-space: nowrap;' href='#%s'>%s</a></li>\n"%(anchor,strip(collection_name))

headerhtml += "</ul>"
headerhtml += search_box

        
write_some_html(headerhtml+fullhtml, outputfile)

