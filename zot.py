#!/usr/bin/env python
# coding: utf-8

# zot_bib_web

# The simple way to add a fast, interactive Zotero bibiography in your website.

# This tool will retrieve a set of collections and format an interactive
# bibliography in HTML5.  The bibliography contains BibTeX records and
# abstracts that can be revealed upon clicking.  The output is ready
# to be included in other websites (there are options), and it can be
# easily styles using CSS (see style.css).

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

library_id = None
library_id = None
library_type ='group'
api_key = None
toplevelfilter = None
limit=None   # None, or set a limit (integer<100) for each collection for debugging
catchallcollection = None
titlestring = 'Bibliography'
catchall_title = 'Miscellanous'
bib_style =  'apa'
write_full_html_header = True
stylesheet_url = "site/style.css"
outputfile = 'zotero-bib.html'
category_outputfile_prefix = 'zotero'
jquery_path = "site/jquery.min.js"
# jquery_path = "../wp-includes/js/jquery/jquery.js"  # wordpress location
number_bib_items = False
show_copy_button = True
clipboard_js_path = "site/clipboard.min.js"
copy_button_path = "site/clippy.svg"
show_search_box = True
show_shortcuts = ['collection']
show_links = ['abstract', 'PDF', 'BIB', 'Wikipedia', 'EndNote', 'COINS']
smart_selections = True
content_filter = {'bib' : 'fix_bibtex_reference'}  # currently, only this function is supported.

sort_criteria = ['collection', '-year', 'type']
show_top_section_headings = 1

language_code = 'en'
sortkeyname_order = {}
# Define label for article types and their ordering
# types may occur in libraryCatalog or itemType
# use libraryCatalog to override it in special cases (e.g., archival Conference papers)
sortkeyname_order['en']={}
sortkeyname_order['en']['type'] = [
    ('journalArticle', 'Journal Articles'),
    ('archivalConferencePaper', 'Archival Conference Papers'),
    ('conferencePaper', 'Conference and Workshop Papers'),
    ('book', 'Books'),
    ('bookSection', 'Book Chapters'),
    ('edited-volume', "Edited Volumes"),
    ('thesis', 'Theses'),
    ('report', 'Tech Reports'),
    ('presentation', 'Talks')]

sortkeyname_order['en']['date'] = sortkeyname_order['en']['year'] = [
    (None, None), # sort all other values here
    ('in preparation', None),
    ('submitted', None),
    ('in review', None),
    ('accepted', None),
    ('to appear', None),
    ('in press', None)]

sortkeyname_order['de']={}
sortkeyname_order['de']['type'] = [
    ('journalArticle', 'Journal-Artikel'),
    ('archivalConferencePaper', u'Konferenz-Veröffentlichungen'),
    ('conferencePaper', 'Konferenz- und Workshop-Papiere'),
    ('book', u'Bücher'),
    ('bookSection', 'Kapitel'),
    ('edited-volume', "Sammlungen (als Herausgeber)"),
    ('thesis', 'Dissertationen'),
    ('report', 'Technische Mitteilungen'),
    ('presentation', u'Vorträge')]

# Basic translations
link_translations = {}
link_translations['de'] = {'abstract':'Abstrakt', 'pdf':'Volltext'}


##### legacy settings
order_by = None   # order in each category: e.g., 'dateAdded', 'dateModified', 'title', 'creator', 'type', 'date', 'publisher', 'publication', 'journalAbbreviation', 'language', 'accessDate', 'libraryCatalog', 'callNumber', 'rights', 'addedBy', 'numItems'
# Note: this does not seem to work with current the Zotero API.
# If set, overrides sort_criteria
sort_order = 'desc'   # "desc" or "asc"


#############################################################################

__version__ = "3.0.0"


#############################################################################
import sys
import re
import copy
def warning(*objs):
    print("WARNING: ", *objs, file=sys.stderr)
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
logging.captureWarnings(False)

import codecs
from texconv import tex2unicode
import base64


def load_settings(file="settings.py"):
    try:
        import imp

        # from settings import *
        settings = imp.load_source("settings", file)
        # import settings into local namespace:
        for k,v in settings.__dict__.items():
            if k in globals() and not "__" in k:  # only if default is defined
                globals()[k]=v
                # print(k,v)
        print("Loaded settings from %s."%file)

    except ImportError:
        pass

def fetch_tag (tag, default=None):
    result = default
    if tag in sys.argv:
        i = sys.argv.index(tag)
        if len(sys.argv)>i+1:
            result = sys.argv[i+1]
            sys.argv=sys.argv[:i]+sys.argv[i+2:]
        else:
            warn("%s needs a value."%tag)
    return result

def print_usage ():
    print("""Usage:   zot.py {--div|--full|--limit|--test|--group GID|--user UID} [TOPLEVEL_COLLECTION_ID] [CATCHALL_COLLECTION_ID [OUTPUTFILE]]
Example: ./zot.py --group 160464 DTDTV2EP

--settings FILE.py  load settings from FILE

--group GID          set a group library              [library_id; library_type='group']
--user UID           set a user library               [library_id; library_type='user']
--limit              sets limit to 5 for fast testing [limit=5]
--div                output an HTML fragment          [write_full_html_header=False]
--full               output full html                 [write_full_html_header=True]
--apikey KEY         set Zotero API key               [api_key]
--test               implies --full and uses site/ directory

These and additional settings can be loaded from settings.py.
""")

print_usage_and_exit = False

x = fetch_tag ("--settings")
if x:
    load_settings(x)
else:
    load_settings()

# Parase remaining arguments

if "--div" in sys.argv:
    write_full_html_header = False
    sys.argv.remove('--div')
if "--full" in sys.argv:
    write_full_html_header = True
    sys.argv.remove('--full')
if "--test" in sys.argv:
    write_full_html_header = True
    stylesheet_url = "site/style.css"
    outputfile = 'zotero-bib.html'
    jquery_path = "site/jquery.min.js"
    clipboard_js_path = "site/clipboard.min.js"
    copy_button_path = "site/clippy.svg"
    sys.argv.remove('--test')
    print("Test mode.  Forcing settings for local testing.")

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

x = fetch_tag ("--user")
if x:
    library_id = x
    library_type = 'user'
    # When a different user library is set, we expect new collections
    toplevelcollection=None
    catchallcollection=None

x = fetch_tag ("--group")
if x:
    library_id = x
    library_type = 'group'
    toplevelcollection=None
    catchallcollection=None

api_key = fetch_tag ("--apikey", api_key)

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

if len(sys.argv)<=1 and not library_id:  # if no settings file loaded and no args given
    print_usage_and_exit = True

if not library_id:
    warn("You must give --user or --group, or set library_id and library_type in settings.py.")
    print_usage_and_exit = True

if print_usage_and_exit:
    print_usage()
    sys.exit(1)



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
          return(void(0));
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
    if jquery_path and clipboard_js_path and copy_button_path:
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
        warning("show_search_box set, but jquery_path, clipboard_js_path or copy_button_path undefined.")

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
if show_search_box or show_shortcuts or show_copy_button:
    search_box += '<script type="text/javascript" src="'+jquery_path+'</script>'

if show_search_box or show_shortcuts:
    if jquery_path:
        search_box = ''
        if show_search_box:
            search_box += '<form id="pubSearchBox" name="pubSearchBox"><input id="pubSearchInputBox" type="text" name="keyword">&nbsp;<input id="pubSearchButton" type="button" value="Search" onClick="searchF()"></form><h2 id="searchTermSectionTitle" class="collectiontitle"></h2>'

        if show_search_box or show_shortcuts:
            search_box += """<script type="text/javascript">
  function getURLParameter(name) {
    return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null;
  }
  jQuery( document ).ready(function() {
    var kw = getURLParameter("keyword");
    if (kw) {
        jQuery('#pubSearchInputBox').val(kw);
        searchF([kw]);
    }
  });
  jQuery.expr[":"].icontains = jQuery.expr.createPseudo(function(arg) {
    return function( elem ) {
        return jQuery(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
    };});
function searchF(searchTerms, shown, disjunctive) {
  var i=document.pubSearchBox.keyword.value;
  searchTerms = searchTerms || (i!=""&&i.split(" "));
  shown = shown || searchTerms;
  jQuery(".bib-item").css("display", "none");
  var q = ".bib-item";
  if (disjunctive)
  { for (x in searchTerms) {jQuery(".bib-item:icontains('"+searchTerms[x]+"')").css("display", "block");}
  }
  else
  { jQuery.each(searchTerms, function(i,x) {q = q + ":icontains('"+x+"')";});
    jQuery(q).css("display", "block");}
  jQuery("#searchTermSectionTitle").html(searchTerms.length>0?"<a href='#' onclick='searchF([]);'>&#x2715;</a> "+shown:"");
  jQuery(".collectiontitle").parent(".full-bib-section,.short-bib-section").css("display", "block");
  jQuery(".collectiontitle").parent(".full-bib-section,.short-bib-section").each(function(){
    var y = jQuery(this).find(".bib-item:visible");
    if (y.length==0) {jQuery(this).css("display","none");}
  });
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
                    searchF();
                    inputVal = self.value
                }
            }, 250);
        };
    jQuery("#pubSearchInputBox").bind('keyup paste cut', checkForChange);
});</script>"""
    else:
        warning("show_search_box or show_shortcut are True, but jquery_path undefined.")

def sortkeyname(field, value):
    global sortkeyname_dict
    # field may be a single field, or a list of fields
    # value corresponds to field

    sort_prefix = ""

    if not is_string(value):  #isinstance(value, list):
        # it's a path of something
        # sorting by all the numbers (if available).
        # e.g., 10.13, and displaying the last entry
        if 'collection'==field:
            return ".".join([str(sortkeyname(field, value2)[0]) for value2 in value]), sortkeyname(field, value[-1])[1]
        else:
            return ".".join([str(sortkeyname(field2, value2)[0]) for field2,value2 in zip(field,value)]), sortkeyname(field[-1], value[-1])[1]

    if field == "collection":
        name = collection_names[value] # value is an ID
        m = re.match(r'([0-9]+)[\s*\-!]*\s(.*)', name)
        if m:
            sort_prefix,value = m.group(1),m.group(2)
        else:
            sort_prefix,value = "", name

    if field in sortkeyname_dict:
        if value in sortkeyname_dict[field]:
            s, value = sortkeyname_dict[field][value]   # this is (sort_number, label)
            sort_prefix = str(s) + " " + sort_prefix
        elif None in sortkeyname_dict[field]:  # default for unknown values
            sort_prefix = str(sortkeyname_dict[field][None][0]) + " " + sort_prefix

    return " ".join([sort_prefix,value.lower()]),value  # sort by value

def import_legacy_configuration():
    global order_by
    global sort_criteria
    global sort_reverse
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

def sort_crit_in_reversed_order(field):
    global sort_criteria
    if field in sort_criteria:
        return sort_reverse[sort_criteria.index(field)]
    if field=='date' and 'year' in sort_criteria:
        return sort_reverse[sort_criteria.index('year')]
    if field=='year' and 'date' in sort_criteria:
        return sort_reverse[sort_criteria.index('date')]
    return False

def index_configuration():
    global sortkeyname_order
    global sortkeyname_dict
    global language_code
    # Not using OrderedDict (Python 2.7), because it does not actually
    # indicate the index of an item by itself
    if not language_code in sortkeyname_order:
        language_code = 'en' # fallback - should be present.

    # use val as default if it is given as None
    sortkeyname_dict = {key:{val:(idx,mappedVal or val) for idx,(val,mappedVal) in enumerate(list(the_list))} for key,the_list in sortkeyname_order[language_code].items()}

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

class ZotItem:
    def __init__(self, entries):
        self.publicationTitle = None
        self.journalAbbreviation = None
        self.event = None
        self.section_keyword = None
        self.url = None
        self.collection = []
        self.type = None
        self.libraryCatalog = None  # special setting, overrides u'itemType' for our purposes
        self.note = None

        self.__dict__.update(entries)

        # Will be set later - None is a good default
        self.bib = None
        self.ris = None
        self.html = None
        self.coins = None
        self.wikipedia = None

        # allow libraryCatalog to override itemType
        self.type = self.libraryCatalog or self.itemType

    def access(self, key, default=""):
        if key in self.__dict__:
            return self.__dict__[key]
        if key=='year' and self.date:
            m = re.search('[0-9][0-9][0-9][0-9]', self.date)
            if m:
                return m.group(0)
            return self.date  # fallback

        return default  # default
        # raise RuntimeError("access: field %s not found."%key)


def retrieve_data(collection_id, exclude=None):

    global item_ids

    def check_show(s):
        global show_links
        s = s.lower()
        for x in show_links:
            if x.lower()==s:
                return True
        return False
    def cfilter(atom, type, content):
        if content_filter and type in content_filter:
            fun = content_filter[type]
            return [globals()[fun](item, thisatom, atom) for item, thisatom in zip(content,atom)]
        return content

    # ii = zot.everything(zot.collection_items(collection_id))
    ii = retrieve_x(collection_id)

    a = [ZotItem(i['data']) for i in ii]

    # PyZotero can retrieve different formats at once,
    # but this does not seem to work with current versions of the library or API

    b = cfilter(a, 'bib', retrieve_bib(collection_id,'bibtex', ''))
    h = cfilter(a, 'html', retrieve_bib(collection_id,'bib', bib_style))
    if check_show('EndNote') or check_show('RIS'):
        r = cfilter(a, 'ris', retrieve_bib(collection_id,'ris', ''))
    else:
        r = [None for _x in h]
    if check_show('coins'):
        c = cfilter(a, 'coins', retrieve_coins(collection_id))
    else:
        c = [None for _x in h]
    if check_show('wikipedia'):
        w = cfilter(a, 'wikipedia', retrieve_wikipedia(collection_id))
    else:
        w = [None for _x in h]

    for i in a:
        # we store by key (ID) and also by title hash
        for key in [i.key, hash(i.title.lower())]:
            if key not in item_ids:
                item_ids[key] = []
            # if not shorten:
            item_ids[key] += [(i, collection_id)]

    for bi,hi,ri,ci,wi,ai in zip(b,h,r,c,w,a):

        ai.bib = bi
        ai.html = hi
        ai.ris = ri
        ai.coins = ci
        ai.wikipedia = wi


    return a


def write_bib (items, outfile):

    file = codecs.open(outfile, "w", "utf-8")

    for item in items:
        file.write(item)

    file.close()

#  Atom bib entry:
# {u'publisher': u'Routledge Psychology Press', u'author': [{u'given': u'David', u'family': u'Reitter'}], u'collection-title': u'Frontiers of Cognitive Psychology', u'issued': {u'raw': u'January 2017'}, u'title': u'Alignment in Web-based Dialogue: Who Aligns, and how Automatic is it? Studies in Big-Data Computational Psycholinguistics', u'editor': [{u'given': u'Michael N.', u'family': u'Jones'}], u'container-title': u'Big Data in Cognitive Science', u'type': u'chapter', u'id': u'1217393/IVR7H8TD'}





def format_bib(bib):
    return bib.replace("},","},\n")

def format_ris(bib):
    return bib.replace("\n","\\n").replace("\r","\\r")


def fix_bibtex_reference(bib, _thisatom, _allatoms):
    "Fix reference style for BIB entries: use authorYEARfirstword convention."
    sub = re.sub(r'(?<=[a-z\s]{)(?P<name>[^_\s,]+)_(?P<firstword>[^_\s,]+)_(?P<year>[^_\s,]+)(?=\s*,\s*[\r\n])', "\g<name>\g<year>\g<firstword>", bib, count=1)
    return sub or bib


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
    print("Output written to %s."%outfile)

def tryreplacing (source, strings, repl):
    for s in strings:
        if s in source:
            repl2 = repl.replace("\\0", s)
            return source.replace(s, repl2)
    return source

from six import string_types
def is_string (s):
    return isinstance(s, string_types)


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


def is_short_collection(section_code):
    "Show abbreviated entries for items in this collection"
    return is_special_collection(section_code, "*")
# def is_exclusive_collection(section_code):
#     "Show item in this collection, and do not show them in regular collections"
#     return is_special_collection(section_code, "-")
def is_featured_collection(section_code):
    """Regardless of sort_criteria, show this collection
at the top of the bibliography"""
    return is_special_collection(section_code, "!")
def is_hidden_collection(section_code):
    "Hide items in this collection."
    return is_special_collection(section_code, "-")

def is_special_collection(section_code, special):
    if not is_string(section_code):
        return any([is_special_collection(x, special) for x in section_code])
    if section_code in collection_names:  # it's a collection key
        name = collection_names[section_code] # value is an ID
        return special in name.partition(' ')[0]
    # if it's not a section key, then it doesn't indicate a short section
    return False

def get_featured_collections(section_code):
    return filter(lambda x: is_featured_collection(x), section_code)


def strip(string):
    stripped = string.lstrip("0123456789*!- ")
    if stripped == "":
        return string
    return stripped


def last(string_or_list):
    if not is_string(string_or_list):
        return string_or_list[-1]
    return string_or_list

def js_strings(string_or_list):
    if is_string(string_or_list):
        return '"%s"'%string_or_list
    return ",".join(map(js_strings, string_or_list))


def make_header_htmls(all_items):
    # filters for criteria

    # ordering:
    # sort collections as they are normally sorted (sortkeyname)

    headerhtmls = [] # {'collection':u"", 'year':u"", 'type':u""}
    for complex_crit in show_shortcuts:
        vals = None
        crit = complex_crit
        if crit == 'date':
            crit = 'year'
        if isinstance(crit, tuple):  # e.g., ('type', [v1,v2,v3])
            crit, vals = crit
            l = [(sortkeyname(crit, str(value))[0], str(value), value) for value in vals]
        else:
            l = [sortkeyname(crit, value) + (value,) for value in (vals or set([i.access(crit) for i in all_items]))]
        l.sort(key=lambda x: x[0], reverse=sort_crit_in_reversed_order(crit))

        html = ""
        for _,section_print_title,section_code in l:
            last_section_id=last(section_code) if crit=="collection" else str(section_code)  # if collection, get its ID
            allyears = True # keep by default
            if crit == 'year':
                # Allow for range specification in years
                # We will search for all appropriate years using the JS search function.
                m = re.match(r'([0-9]*)-([0-9]*)', last_section_id)
                if m and (m.group(1) or m.group(2)):
                    fromyear = m.group(1) or 0
                    toyear = m.group(2) or 3000
                    allyears = set([i.access('year') for i in all_items])
                    allyears = filter(lambda y: (y>=fromyear and y<=toyear), allyears)
                    last_section_id = map(lambda y: "year__%s"%y, allyears)
                    section_print_title = "%s&ndash;%s"%(m.group(1),m.group(2))
                else:
                    # Currently, we're only filtering for the years, because that is were it is practically relevant
                    allyears = list(filter(lambda y: (str(y) == str(last_section_id)), [i.access(crit) for i in all_items]))
                    last_section_id = 'year__'+last_section_id

            if crit == 'type':
                allyears = list(filter(lambda y: (str(y) == str(last_section_id)), [i.access(crit) for i in all_items]))
                last_section_id = 'type__'+last_section_id

            if not allyears:  # empty result set (no items for this search, if type or year search)
                print("Warning: %s %s not found, but mentioned in shortcuts. Skipping."%(crit,last_section_id))
            else:
                # collection does not need to be marked
                html += "   <li class='link'><a style='white-space: nowrap;' href='#' onclick='searchF([%s],\"%s\",1);return false;'>%s</a></li>\n"%(js_strings(last_section_id), section_print_title,section_print_title)
        headerhtmls += [html]

    return headerhtmls

entry_count=0
def make_html (all_items, exclude={}, shorten=False):
    def a_button (name,url=None,js=None,title=None,cls=None):
        global smart_selections
        global language_code
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
        if language_code in link_translations:
            name = link_translations[language_code].get(name.lower(), name)
        return u"<a class=\"%s\" %s %s onclick=\"%s\">%s</a>"%(cls,title2,url,js,("" if smart_selections else name))

    sort_criteria = None   # [u'page']  # TODO - allow user to set this; document

    count = 0
    string = ""
    for item in all_items:
        if item.key not in exclude:
            if item.title:

                count += 1

                htmlitem = item.html

                global show_links
                show_items = show_links
                t =  item.title
                u = None
                if item.url:
                    u = item.url

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

                # Insert searchable keywords (not displayed)
                search_tags = ''
                if item.section_keyword:
                    search_tags += item.section_keyword  # no special tag for collections
                search_tags += " year__" + item.access('year')  # no search by date
                if item.type:
                    search_tags += " type__" + item.type
                htmlitem += "<span class='bib-kw' style='display:none;'>%s</span>"%search_tags

                htmlitem = u'<div class="bib-details">' + htmlitem + u'</div>'

                if shorten:

                    ct = item.publicationTitle or item.journalAbbreviation or item.event or u""
                    if item.note and (len(item.note) < len(ct) or ct==u""):
                        ct = item.note

                    y = ""
                    if item.date:
                        y = "(%s)"%item.date

                if item.bib:
                    abstract,bibitem2 = extract_abstract(item.bib)
                    blinkitem = u""
                    # we print the original item name as label so that capitalization may be chosen via the items list
                    for show in show_items:

                        if 'abstract' == show.lower() and abstract:
                            blinkitem += u'<div class="blink">'+a_button(show)+u'<div class="bibshowhide"><div class="abstract">%s</div></div></div>'%(abstract)
                        elif 'wikipedia' == show.lower() and item.wikipedia:
                            blinkitem += u'<div class="blink">'+a_button(show)+u'<div class="bibshowhide"><div class="bib" style="white-space:pre-wrap;">%s</div></div></div>'%(item.wikipedia)
                        elif 'bib' == show.lower() and bibitem2:
                            blinkitem += u'<div class="blink">'+a_button(show)+u'<div class="bibshowhide"><div class="bib">%s</div></div></div>'%(bibitem2)
                        elif 'pdf' == show.lower() and u:
                            blinkitem += u'<div class="blink">'+a_button(show,url=u)+u'</div>'
                        elif ('ris' == show.lower() or 'endnote' == show.lower()) and item.ris:
                            blinkitem += u'<div class="blink">'+'<a class="%s" title="Download EndNote record" onclick="dwnD(\'%s\');return false;"></a></div>'%(show,base64.b64encode(item.ris.encode('utf-8')).decode('utf-8'))
                        elif 'coins' == show.lower() and item.coins:
                            blinkitem += str(item.coins).strip()

                    if shorten: # to do - consider moving this to the CSS
                        blinkitem = u'<div style="padding-left:20px;">' + blinkitem + u'</div>'

                    htmlitem += u'<div class="blinkitems">' + blinkitem + u'</div>'

                if shorten:
                    htmlitem = u"<a href=\"#\" onclick=\"show(this);\">&#8862;</a> <span class=\"doctitle-short\">%s</span> <span class=\"containertitle\">%s</span> %s"%(t,ct,y) + "<div class=\"bibshowhide\" style=\"padding-left:20px;\">"+htmlitem+"</div>"
                    htmlitem = u"<div>" + htmlitem + "</div>" # to limit was is being expanded

                tag = "li" if number_bib_items else "div"
                string += u'<%s class="bib-item">'%tag + htmlitem + u'</%s>'%tag

    if len(string)==0:
        return "",0  # avoid adding title for section later on

    if number_bib_items:
        string = u'<ol>' + string + u'</ol>'


    global entry_count
    entry_count += count

    return cleanup_lines(string),count


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
                at_end += [(catchallcollection, 0, catchall_title, [])]
            items = [e for e in items if e[0]!=catchallcollection] + at_end

        return items


    except zotero_errors.UserNotAuthorised:
        print("UserNotAuthorised: Set correct Zotero API key in settings.py and allow access.", file=sys.stderr)
        raise SystemExit(1)

def traverse(agenda, depth=0, parents=[]):
    global zot
    result = []
    # sort agenda by name
    for collitem in sorted(agenda, key=coll_name):
        c = zot.collections_sub(coll_key(collitem))
        result += [(coll_key(collitem), depth, coll_data(collitem)[u'name'], parents)]
        result += traverse(c, depth+1, parents+[coll_key(collitem)])
    return result



def filter_items(quaditems, exclude):
    def fil(a):
        return not (a.key in item_ids)
    return filter(fil, quaditems)

def merge_doubles(items):
    iids = {}
    def rd(a):
        key = a.key
        if key in iids:
            # depending on sort criteria, even the short collection ones
            # can show up elsewhere.
            #  and not (u'collection' in iids[key] and is_short_collection(iids[key].collection))
            # print("Merging ", a.title)

            # merge "section keywords"
            if a.section_keyword:
                iids[key].section_keyword += " "+a.section_keyword
            return False
        else:
            iids[key] = a
            return True

    return filter(rd, items)

from datetime import datetime, timedelta
import pickle
def retrieve_all_items(sortedkeys):

    global toplevelfilter, limit
    try:
        sklen, date, tlc, l, items = pickle.load(open("retrieve.cache", 'rb'))
        if date > datetime.now()-timedelta(days=1):
            if sklen == hash(str(sortedkeys)) and tlc==toplevelfilter and l==limit:
                print("Using cached Zotero items (retrieve.cache).")
                return items
    except IOError:
        pass

    all_items = []
    for key,depth,collection_name,collection_parents in sortedkeys:
        c = 0
        print(" "+" "*len(collection_parents) + collection_name + "...")

        i2 = retrieve_data(key)
        if key == catchallcollection:  # Miscellaneous
            # This has everything that isn't mentioned above
            # so we'll filter what's in item_ids
            i2 = filter_items(i2, item_ids)

        i2 = list(i2)
        # add IDs to the list with the collection name
        #### collect_ids(i2, collection_name, item_ids)

        print("%s Items."%len(list(i2)))

        parent_path = tuple(collection_parents + [key])
        for atuple in i2:  # for sorting by collection
            atuple.collection = parent_path

        # if sort_criteria[0] != 'collection':
        for atuple in i2:
            atuple.section_keyword = " ".join(collection_parents + [key]) # will be added HTML so the entry can be found

        if len(i2)>0:
            all_items += i2


    pickle.dump((hash(str(sortedkeys)), datetime.now(), toplevelfilter, limit, all_items), open("retrieve.cache", 'wb'))

    return all_items

def compile_data(all_items, section_code, crits, exclude={}, shorten=False):
    global item_ids
    global bib_style
    global show_top_section_headings

    corehtml,count = make_html(all_items, exclude=exclude, shorten=shorten)

    # empty categories shouldn't actually be passed to compile_data

    html = ""
    if section_code:
        section_print_title = sortkeyname(crits, section_code)[1]
        last_section_id=last(section_code)  # if collection, get its ID
        last_crit=last(crits)
    else:
        section_print_title = "Empty"
        last_section_id = last_crit = None
        section_code=['A']
        print(all_items)
        raise RuntimeException("compile_data called with empty section_code")


    if last_section_id:

        html += "<a id='%s' style='{display: block; position: relative; top: -150px; visibility: hidden;}'></a>"%last_section_id
        if section_code and show_top_section_headings:
            depth=0
            if not is_string(section_code):
                depth = len(section_code)-1 # it's a path
            # do not show headings deeper than this
            # if depth<=show_top_section_headings:
            html += "<h%s class=\"collectiontitle\">%s</h3>\n"%(2+depth,section_print_title)
    html += corehtml
    html = u'<div class="%s-bib-section">'%(u'short' if shorten else u'full') + html + u'</div>'

    # write_some_html(html, category_outputfile_prefix+"-%s.html"%last_section_id)
    return html

def show_double_warnings ():
    global item_ids

    def itemref(i):
        auth = (i.title and i.title[:30]) or u""
        year = i.date or u""
        ref = "%s (%s)"%(auth, year)
        return ref

    for key,itemcolls in item_ids.items():
        if len(itemcolls)>1:
            uniqueitems = set([i.key for i,_c in itemcolls])
            if len(uniqueitems)>1:
                # This only applies to different items with the same title
                warning("%s items sharing the same title included:"%len(itemcolls))
                for i,c in itemcolls:
                    warn(" %s [%s] (collection: %s)"%(itemref(i), i.key, c))
            else:
                # if item is the same, it may still be included in several collections:
                uniquecolls = set([c for _i,c in itemcolls])
                if len(uniquecolls)>1:
                    # we know that every item here has the same ID (because of the previous check)
                    # itemcolls is a list
                    warning('Item "%s" included in %s collections:\n %s'%(itemref(itemcolls[0][0]), len(uniquecolls), "\n ".join(uniquecolls)))


from collections import defaultdict
def pull_up_featured_remove_hidden_items (all_items):
    # split up into featured and other sections
    visible_items = list(filter(lambda it: not is_hidden_collection(it.collection), all_items))
    featured_items = filter(lambda it: is_featured_collection(it.collection), visible_items)
    other_items = filter(lambda it: not is_featured_collection(it.collection), visible_items)

    # if a hidden item is available elsewhere, transfer its category so that it
    # can be searched for using the category shortcuts.
    # E.g., "selected works" might not be shown at the top of the bibliography,
    # but you still might filter for it.

    hidden_item_categories = defaultdict(str)
    for it in all_items:
        if is_hidden_collection(it.collection):
            hidden_item_categories[it.key] += it.section_keyword + " "
    for it in visible_items:
        id = it.key
        if id in hidden_item_categories:
            it.section_keyword += " " + hidden_item_categories[id]

    return featured_items, other_items

def sort_items(all_items, sort_criteria, sort_reverse):
    # sort the items (in place)
    if sort_criteria:
        all_items = list(all_items)
        # sort is stable, so we will sort several times,
        # from the last to the first criterion
        for crit,rev in reversed(list(zip(sort_criteria, sort_reverse))):
            # print("Sorting by",crit, rev)
            # all_items contains 4-tuples, the last one is the atom representation
            all_items.sort(key=lambda x: sortkeyname(crit, x.access(crit))[0], reverse=rev)

        # prioritize featured collections
        # all_items.sort(key=lambda x: is_featured_collection(x.collection))
    return all_items


from itertools import islice,chain
try:
    from itertools import zip_longest
except ImportError:
    # Python 2
    from itertools import izip_longest as zip_longest


def section_generator (items, crits):
    "Iterate over all items, return them section by section"

    collect = []
    prev_section = ""
    prev_crits_sec = ""
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


    for item_tuple in items:
        item = item_tuple
        # construct section path identifier
        # also, make matching criterion identifier

        section = []
        crits_sec = []

        if is_featured_collection(item.collection):
            section=list(get_featured_collections(item.collection))
            crits_sec += ['collection'] * len(section)
        else:
            # Then, everything is organized according to the sort criteria
            for crit in crits[:show_top_section_headings]:
                val = item.access(crit)
                if is_string(val):  # basic fields
                    section += [val]
                    crits_sec += [crit]
                else: # collection paths (val is a list)
                    section += val # flat concat
                    crits_sec += [crit] * len(val)

        #section = item.access(crit)
        if section != prev_section:
            changed_sections = list(changed_section_headings(prev_section, section))
            if changed_sections:
                if len(collect)>0:
                    yield prev_section, prev_crits_sec, collect
                # new section, show a section header.  add as separate item.
                # add a header for every level that has changed
                # except for the last one - that'll come with the next set of items
                for s in changed_sections: #[:-1]:
                    if not s == section:  # because that would be the heading for the next set of items.
                        yield s, crits_sec[:len(s)], []

                collect = []
            prev_section, prev_crits_sec = section, crits_sec

        collect += [item_tuple]
    if collect:
        yield prev_section, prev_crits_sec, collect


def main():

    global item_ids
    global catchallcollection
    global collection_names

    import_legacy_configuration()
    index_configuration()

    sortedkeys = get_collections()
    item_ids = {}
    collection_names = {key:name for key,_,name,_ in sortedkeys}
    fullhtml = ""

    if limit:
        print("Output limited to %s per collection."%limit)

    all_items = []
    section_items = []

    all_items = retrieve_all_items(sortedkeys)


    if 'collection' in sort_criteria:
        show_double_warnings()
        # If collection doesn't feature in sort criteria,
        # double entries are likely to get filtered out anyway,
        # or they are desired (e.g., Selected Works)

    featured_items, regular_items = pull_up_featured_remove_hidden_items(all_items)
    featured_items = sort_items(featured_items, ['collection']+sort_criteria, [False]+sort_reverse)
    regular_items = sort_items(regular_items, sort_criteria, sort_reverse)

    # don't use chain - we will iterate over all_items several times, so
    # we need a list
    all_items = list(featured_items) + list(regular_items)

    headerhtmls = make_header_htmls(all_items)

    fullhtml = u""
    for section_code, crits, items in list(section_generator(all_items, sort_criteria)):
        # remove double entries within one section
        items = list(merge_doubles(items))
        fullhtml += compile_data(items, section_code, crits, shorten=is_short_collection(section_code))


    headerhtml = '<div id="bib-preamble">'
    for crit,h in zip(show_shortcuts, headerhtmls):
        if isinstance(crit,tuple):
            crit = crit[0]
        headerhtml += '<ul id="bib-cat-%s" class="bib-cat">'%crit + h + "</ul>"
    headerhtml += search_box + "</div>" #preamble

    write_some_html(headerhtml+fullhtml, outputfile)


init_db()

if interactive_debugging:
    import code
    code.interact(local=locals())
else:
    main()
