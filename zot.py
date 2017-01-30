#!/usr/bin/env python
# coding: utf-8

# zot_bib_web

# This will retrieve a set of collections and format an interactive
# bibliography in HTML5.  The bibliography contains BibTeX records and
# abstracts that can be revealed upon clicking.  The output is ready
# to be included in other websites (there are options), and it can be
# easily styles using CSS (see style.css).

# Bibliographic style can be chosen (APA) is default.


# (C) 2014,2015,2016,2017 David Reitter, The Pennsylvania State University
# Released under the GNU General Public License, V.3 or later.

from __future__ import print_function

####  Program arguments

# zot.py
# zot.py TOPLEVELFILTER
# zot.py TOPLEVELFILTER CATCHALLCOLLECTION
# zot.py TOPLEVELFILTER CATCHALLCOLLECTION OUTPUTFILE

#############################################################################

## See settings.example.py for configuration information
## Create settings.py to supply your configuration.

#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################

## The following items are defaults.

library_id = '160464'
library_type ='group'
api_key = None
toplevelfilter = None
limit=None   # None, or set a limit (integer<100) for each collection for debugging
catchallcollection = None
titlestring = 'Bibliography'
catchall_title = 'Miscellanous'
bib_style =  'apa'
order_by = 'date'
sort_order = 'desc'
write_full_html_header = True
stylesheet_url = "site/style.css"
outputfile = 'zotero-bib.html'
category_outputfile_prefix = 'zotero'
jquery_path = "site/jquery.min.js"
# jquery_path = "../wp-includes/js/jquery/jquery.js"  # wordpress location
show_copy_button = True
clipboard_js_path = "site/clipboard.min.js"
copy_button_path = "site/clippy.svg"
show_search_box = True
show_links = ['abstract', 'PDF', 'BIB', 'Wikipedia', 'EndNote', 'COINS']
smart_selections = True

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
    print("Warning: ", *objs, file=sys.stderr)
def warn(*objs):
    print(*objs, file=sys.stderr)

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
import base64


def print_usage ():
    print("Usage:  zot.py [--div|--full||--limit|-i] TOPLEVEL_COLLECTION_ID [CATCHALL_COLLECTION_ID [OUTPUTFILE]]")

if "--div" in sys.argv:
    write_full_html_header = False
    sys.argv.remove('--div')
if "--full" in sys.argv:
    write_full_html_header = True
    sys.argv.remove('--full')
if "-i" in sys.argv:
    interactive_debugging = True
    sys.argv.remove('-i')
else:
    interactive_debugging = False
if "--limit" in sys.argv:
    limit=5
    sys.argv.remove('--limit')
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

# note - the final style in the style sheet is manipulated by changeCSS
# this is selected (hack, hack) by index
script_html = """<style type="text/css" id="zoterostylesheet" scoped>
.bibshowhide {display:none;}
"""+ blinkitem_css + """
.blink {margin:0;margin-right:15px;padding:0;display:none;}
</style>
<script type="text/javascript">
function dwnD(data) {
  filename = "article.ris"
  var pom = document.createElement('a');
  var isSafari = navigator.vendor && navigator.vendor.indexOf('Apple') > -1 && navigator.userAgent && !navigator.userAgent.match('CriOS');
  var mime = (isSafari?"text/plain":"application/x-research-info-systems");
  pom.href = window.URL.createObjectURL(new Blob([atob(data)], {type: mime+";charset=utf-8"}));
  pom.download = filename;
  document.body.appendChild(pom);
  pom.click();
  setTimeout(function(){document.body.removeChild(pom);}, 100); 
  return(void(0));}
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

credits_html = u'<div id="zbw_credits" style="text-align:right;">A <a href="https://github.com/davidswelt/zot_bib_web">zot_bib_web</a> bibliography.</div>'

script_html = cleanup_lines(script_html)

html_header = u''
html_footer = u''
if write_full_html_header:
    style_html = u''
    if stylesheet_url:
        style_html = u"<link rel=\"stylesheet\" type=\"text/css\" href=\"%s\">"%stylesheet_url
    html_header += u'<!DOCTYPE HTML><html><head><meta charset="UTF-8"><title>'+titlestring+u'</title>'+style_html+u'</head><body>'
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
        search_box= '<form id="pubSearchBox" name="pubSearchBox"><input id="pubSearchInputBox" type="text" name="keyword">&nbsp;<input id="pubSearchButton" type="button" value="Search" onClick="searchFunction()"></form><script type="text/javascript" src="'+jquery_path+""""></script><script type="text/javascript">
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
        a = a.replace("&", "&amp;")
        a = a.replace("<","&lt;")
        a = a.replace(">","&gt;")
        a = a.replace("\\textless","&lt;")
        a = a.replace("\\textgreater","&gt;")
        a = a.replace("\\textbar","|")
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
            if c in i[-1]:
                # if available, write value into tuple
                if c==u'author' and isinstance(i[-1][c],list) and u'family' in i[-1][c][0] and u'given' in i[-1][c][0]:
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

entry_count=0
def make_html (bibitems, htmlitems, risitems, coinsitems, wikiitems, items, exclude={}, shorten=False):
    def a_button (name,url=None,js=None,title=None,cls=None):
        global smart_selections
        if not js:
            js = "show(this)"
        if not url:
            url = ""
        else:
            url = 'href=\"%s\"'%url
        if not cls:
            cls = name
        title2 = ""
        if title:
            title2 = "title=\"%s\""%title
        return u"<a class=\"%s\" %s %s onclick=\"%s\">%s</a>"%(cls,title2,url,js,("" if smart_selections else name))

    sort_criteria = None   # [u'page']  # TODO - allow user to set this; document

    count = 0
    string = ""
    for bibitem,htmlitem,risitem,coinsitem,wikiitem,item in sortitems(zip(bibitems,htmlitems,risitems,coinsitems,wikiitems,items),sort_criteria):
        if item[u'id'] not in exclude:
            if u'title' in item:

                count += 1

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

                if shorten:
                    ct = None
                    if u'container-title' in item:
                        ct = item[u'container-title']
                    if u'event' in item:
                        ct = item[u'event']
                    if u'journalAbbreviation' in item:
                        ct = item[u'journalAbbreviation']
                    if u'note' in item:
                        if len(item[u'note']) < len(ct):
                            ct = item[u'note']

                    y = ""
                    if u'date' in item:
                        y = "(%s)"%item[u'date']
                    elif u'issued' in item:
                        i = item[u'issued']
                        if u'raw' in i:
                            y = "(%s)"%i[u'raw']  # to do: get year from more complex date?

                    htmlitem = u"<a href=\"#\" onclick=\"show(this);\">&#8862;</a> <span class=\"doctitle-short\">%s</span> <span class=\"containertitle\">%s</span> %s"%(t,ct,y) + "<div class=\"bibshowhide\" style=\"padding-left:20px;\">"+htmlitem+"</div>"
                    htmlitem = u"<div>" + htmlitem + "</div>" # to limit was is being expanded


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
                        elif ('ris' == item.lower() or 'endnote' == item.lower()) and risitem:
                            blinkitem += u'<div class="blink">'+'<a class="%s" title="Download EndNote record" onclick="dwnD(\'%s\');return false;"></a></div>'%(item,base64.b64encode(risitem.encode('utf-8')))
                        elif 'coins' == item.lower() and coinsitem:
                            blinkitem += str(coinsitem).strip()

                    if shorten:
                        blinkitem = u'<div style="padding-left:20px;">' + blinkitem + u'</div>'

                    htmlitem += blinkitem

                string += u'<div class="bib-item">' + htmlitem + u'</div>'

    if len(string)==0:
        return "",0  # avoid adding title for section later on

    if shorten:
        string = u'<div class="short-bib-section">' + string + u'</div>'
    else:
        string = u'<div class="full-bib-section">' + string + u'</div>'

    global entry_count
    entry_count += count

    return cleanup_lines(string),count


def is_shortcollection(st):
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

def coll_name(c):
    return coll_data(c)[u'name']

def init_db ():
    global zot

    try:
        zot = zotero.Zotero(library_id, library_type, api_key)
    except zotero_errors.UserNotAuthorised:
        print("UserNotAuthorised: Set correct Zotero API key in settings.py.", file=sys.stderr)
        raise SystemExit(1)

def get_collections ():
    global zot
    global catchallcollection
    try:
        if toplevelfilter:
            items= traverse (zot.collections_sub(toplevelfilter))
        else:
            print("Fetching all collections:")
            items= traverse (zot.collections())

        if catchallcollection:
            # move catchallcollection to the end
            at_end = [e for e in items if e[0]==catchallcollection]
            if len(at_end)==0:
                at_end += [(catchallcollection, 0, catchall_title)]
            items = [e for e in items if e[0]!=catchallcollection] + at_end

        return items


    except zotero_errors.UserNotAuthorised:
        print("UserNotAuthorised: Set correct Zotero API key in settings.py and allow access.", file=sys.stderr)
        raise SystemExit(1)

def traverse(agenda, depth=0):
    global zot
    result = []
    # sort agenda by name
    for item in sorted(agenda, key=coll_name):
        c = zot.collections_sub(coll_key(item))
        result += [(coll_key(item), depth, coll_data(item)[u'name'])]
        result += traverse(c, depth+1)
    return result


def compile_data(collection_id, collection_name, depth=0, exclude={}, shorten=False):
    global fullhtml
    global item_ids
    global bib_style


    def check_show(s):
        global show_links
        s = s.lower()
        for x in show_links:
            if x.lower()==s:
                return True
        return False

    print(" "+" "*depth + collection_name + "...", end='')

    a = retrieve_atom(collection_id)
    b = retrieve_bib(collection_id,'bibtex', '')
    h = retrieve_bib(collection_id,'bib', bib_style)
    if check_show('EndNote') or check_show('RIS'):
        r = retrieve_bib(collection_id,'ris', '')
    else:
        r = [None for _x in h]
    if check_show('coins'):
        c = retrieve_coins(collection_id)
    else:
        c = [None for _x in h]
    if check_show('wikipedia'):
        w = retrieve_wikipedia(collection_id)
    else:
        w = [None for _x in h]


    counter = 0
    if not exclude:
        for i in a:
            # we store by key (ID) and also by title hash
            for key in [i[u'id'], hash(i[u'title'.lower()])]:
                if key not in item_ids:
                    item_ids[key] = []
                if not shorten:
                    item_ids[key] += [(i, collection_name)]

            counter += 1

    corehtml,count = make_html(b, h, r, c, w, a, exclude=exclude, shorten=shorten)
    print(count) # number of items

    if collection_id != catchallcollection or (corehtml and len(corehtml)>0):

        # write_html([None] * len(h), h, a, 'out.html')
        #html = "dummy"
        html = "<a id='%s' style='{display: block; position: relative; top: -150px; visibility: hidden;}'></a>"%collection_id
        d = 2+depth
        html += '<div class="collection"><h%s class="collectiontitle">%s</h%s>\n'%(d,collection_name,d)
        html += corehtml + '</div>'
        write_some_html(html, category_outputfile_prefix+"-%s.html"%collection_id)
        fullhtml += html

    return counter # number of items included


def show_double_warnings ():
    global item_ids

    def itemref(i):
        auth = ""
        if u'title' in i:
            auth = i[u'title'][:30]
        year = ""
        if u'issued' in i and u'raw' in i[u'issued']:
            year = i[u'issued'][u'raw']
        ref = "%s (%s)"%(auth, year)
        return ref

    for key,itemcolls in item_ids.items():
        if len(itemcolls)>1:
            uniqueitems = set([i[u'id'] for i,_c in itemcolls])
            if len(uniqueitems)>1:
                # This only applies to different items with the same title
                warning("%s items sharing the same title included:"%len(itemcolls))
                for i,c in itemcolls:
                    warn(" %s [%s] (collection: %s)"%(itemref(i), i[u'id'], c))
            else:
                # if item is the same, it may still be included in several collections:
                uniquecolls = set([c for _i,c in itemcolls])
                if len(uniquecolls)>1:
                    # we know that every item here has the same ID (because of the previous check)
                    # itemcolls is a list
                    warning('Item "%s" included in %s collections:\n %s'%(itemref(itemcolls[0][0]), len(uniquecolls), "\n ".join(uniquecolls)))

# to do - maybe give option to automatically exclude double entries?
# would have to be done in compile_data, via exclude mechanism


def main():

    global item_ids
    global fullhtml
    global catchallcollection

    sortedkeys = get_collections()
    # start with links to subsections
    headerhtml = '<ul class="bib-cat">'
    item_ids = {}
    fullhtml = ""

    if limit:
        print("Output limited to %s per collection."%limit)

    for key,depth,name in sortedkeys:
        c = 0
        s=is_shortcollection(name)
        if key == catchallcollection:
            # now for "Other"
            # Other has everything that isn't mentioned above
            # this key is guaranteed to be at the end of the list
            c = compile_data(key, strip(name), depth=depth, exclude=copy.copy(item_ids), shorten=s)
        else:
            c = compile_data(key, strip(name), depth=depth, shorten=s)

        if c>0:
            anchor = key
            headerhtml += "   <li class='link'><a style='white-space: nowrap;' href='#%s'>%s</a></li>\n"%(anchor,strip(name))
    show_double_warnings()
    print("%s items included."%entry_count)

    headerhtml += "</ul>"
    headerhtml += search_box


    write_some_html(headerhtml+fullhtml, outputfile)

init_db()

if interactive_debugging:
    import code
    code.interact(local=locals())
else:
    main()
