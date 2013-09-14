#!/usr/bin/python

# David Reitter, Penn State
# 2013
# License: GNU General Public License version 3 or higher




# You must configure the following items

library_id = '160464' # your group or user ID (e.g., six numeric digits)
library_type ='group'  # or 'group' # group or userm
api_key = '3JsK6ixlKIK1YFgRklj021S1'  # secret key (from Zotero)

toplevelfilter = 'MGID93AS'   # collection where to start retrieving
catchallcollection = '4KATF6MA'  # include "Miscellaneous" category at end - all items not mentioend anywhere else



###### Special settings

limit=None   # None, or set a limit (integer<100) for each collection for debugging

bib_style =  'apa'     # bibliography style format (e.g., 'apa' or 'mla') - Any valid CSL style in the Zotero style repository

order_by = 'date'   # order in each category: e.g., 'dateAdded', 'dateModified', 'title', 'creator', 'type', 'date', 'publisher', 'publication', 'journalAbbreviation', 'language', 'accessDate', 'libraryCatalog', 'callNumber', 'rights', 'addedBy', 'numItems'

sort_order = 'desc'   # "desc" or "asc"

write_full_html_header = True   # False to not output HTML headers.  In this case, expect a file in UTF-8 encoding.

outputfile = 'zotero-bib.html'  # relative or absolute path name of output file
category_outputfile_prefix = 'zotero'  # relative or absolute path prefix



















#############################################################################

import codecs
import sys


from pyzotero import zotero


script_html = """
<style type='text/css'>
.bib {display:none;}
.blink {display:none;}
</style>
<script type="text/javascript">

function show_parent(elem) {

for (var i = 0; i < elem.parentNode.childNodes.length; ++i) {
   elem.parentNode.childNodes[i].style.display = 'block';
}

}

function changeCSS() {
	if (!document.styleSheets) return;
	var theRules = new Array();
    ss = document.styleSheets[document.styleSheets.length-1];
	if (ss.cssRules)
		theRules = ss.cssRules
	else if (ss.rules)
		theRules = ss.rules
	else return;
	theRules[theRules.length-1].style.display = 'inline';
}

changeCSS();

    </script>
"""

if write_full_html_header:
    html_header = u'<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN"><html><head><meta charset="UTF-8"><title>Bibliography</title>'+script_html+u'</head><body>'
    html_header += '<h1 class="title">'+'Bibliography'+"</h1>\n";
    html_footer = u'</body></html>'
else:
    html_header = u'<div class="bibliography">'+script_html
    html_footer = u'</div>'
        

def retrieve_bib (collection, content, style):
    global limit
    if limit:
        items = zot.collection_items(collection, content=content, style=style, limit=limit, order=order_by, sort=sort_order)
    else:
        items = zot.everything(zot.collection_items(collection, content=content, style=style, order=order_by, sort=sort_order))
    return items

def write_bib (items, outfile):
        
    file = codecs.open(outfile, "w", "utf-8")

    # print items
    for item in items:
        print item
        file.write(item)
        #print item
        #print('Item Type: %s | Key: %s') % (item['itemType'], item['key'])

    file.close()


def retrieve_atom (collection):
    global limit
    if limit:
        items = zot.collection_items(collection, format='atom',content='csljson', limit=limit, order=order_by, sort=sort_order)
    else:
        items = zot.everything(zot.collection_items(collection, format='atom',content='csljson', order=order_by, sort=sort_order))

    return items


def write_some_html (body, outfile, title=None):
    file = codecs.open(outfile, "w", "utf-8")
    file.write(html_header)
    if title:
        file.write('<h1 class="title">'+title+"</h1>")
    file.write(body)
    file.write(html_footer)
    file.close()
    
def make_html (bibitems, htmlitems, items, title, exclude={}):
    
    string = '<h3 class="collectiontitle">'+title+"</h3>\n\n"

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
                    new = htmlitem.replace(t, u"<a class=\"doclink\" href=\"%s\">%s</a>"%(u,t))
                    if new == htmlitem:
                        # replacement not successful
                        htmlitem += u"<span class=\"blink\"><a class=\"doclink\" href=\"%s\">PDF</a></span>"%u
                    else:
                        htmlitem = new    
                if bibitem:
                    htmlitem += u"<span class=\"blink\"><a href=\"javascript:show_parent(this);\" onclick=\"show_parent(this);\">bib</a><div class=\"bib\">%s</div></span>"%(bibitem)

                string += "<div class=\"bib-item\">" + htmlitem + "</div>\n\n"


            #        print item[u'title']
            #        file.write(item)
            #print item
            #print('Item Type: %s | Key: %s') % (item['itemType'], item['key'])

    return string



    
zot = zotero.Zotero(library_id, library_type, api_key)

if len(sys.argv)>1:
    toplevelfilter =sys.argv[1]


    
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
            print "(Top-level collection will be ignored.)"
            break
    
print "%s collections: "%lastsize

sortedkeys = collection_ids.keys()
sortedkeys.sort()

# show at end
if catchallcollection:
    sortedkeys += ["Miscellaneous"]
    collection_ids['Miscellaneous'] = catchallcollection

# start with links to subsections
fullhtml = ""

fullhtml = "<ul>"
for collection_name in sortedkeys:
    anchor = collection_ids[collection_name]
    fullhtml += "   <li class='link'><a href='#%s'>%s</a></li>\n"%(anchor,collection_name)
fullhtml += "</ul>"

item_ids = {}

def compile_data(collection_id, collection_name, exclude={}):
    global fullhtml
    global item_ids
    global bib_style

    print collection_name + "..."
    
    b = retrieve_bib(collection_id,'bibtex', '')
    h = retrieve_bib(collection_id,'bib', bib_style)
    a = retrieve_atom(collection_id)

    if not exclude:
        for i in a:
            key = i[u'id']
            if item_ids.has_key(key):
                print "warning - item %s included additionally in collection %s"%(key, collection_name)
            item_ids[key] = True
    
    
    # write_html([None] * len(h), h, a, 'out.html')
    #html = "dummy"
    html = make_html(b, h, a, collection_name, exclude=exclude)
    write_some_html(html, category_outputfile_prefix+"-%s.html"%collection_id)
    fullhtml += "<a name='%s'></a>\n"%collection_id
    fullhtml += html


for collection_name in sortedkeys:
    if collection_ids[collection_name] == catchallcollection:
        # now for "Other"
        # Other has everything that isn't mentioned above
        compile_data(collection_ids[collection_name], collection_name, exclude=item_ids)
    else:
        compile_data(collection_ids[collection_name], collection_name)

write_some_html(fullhtml, outputfile)


    
# [{u'collectionVersion': 108, u'updated': 'Thu, 12 Sep 2013 14:38:14 EST', u'collectionKey': u'7SR3CBEH', u'name': u'Other', u'parent': u'MGID93AS', u'etag': '0928cd904548f0ba5ab00b719a517660', u'key': u'7SR3CBEH', u'group_id': u'160464'}, {u'collectionVersion': 108, u'updated': 'Thu, 12 Sep 2013 14:38:31 EST', u'collectionKey': u'GJW55P4X', u'name': u'David', u'parent': False, u'etag': 'f56e0d7d3588029226c25eede18321c5', u'key': u'GJW55P4X', u'group_id': u'160464'}, {u'collectionVersion': 108, u'updated': 'Thu, 12 Sep 2013 14:38:37 EST', u'collectionKey': u'MIR96Q4W', u'name': u'Frank', u'parent': False, u'etag': '50b91a48abe1186eecfb9aac285a26d1', u'key': u'MIR96Q4W', u'group_id': u'160464'}, {u'collectionVersion': 108, u'updated': 'Thu, 12 Sep 2013 14:38:33 EST', u'collectionKey': u'D3K3EDFS', u'name': u'Martin', u'parent': False, u'etag': '5d9eecd133dfb2d04f024fefc15be1a8', u'key': u'D3K3EDFS', u'group_id': u'160464'}, {u'collectionVersion': 102, u'updated': 'Wed, 11 Sep 2013 21:27:33 EST', u'collectionKey': u'CXXK8XEU', u'name': u'Social Cognition', u'parent': u'MGID93AS', u'etag': '47eba66a923d91c3405f989dc0ec20db', u'key': u'CXXK8XEU', u'group_id': u'160464'}, {u'collectionVersion': 107, u'updated': 'Thu, 12 Sep 2013 14:37:35 EST', u'collectionKey': u'9WF9BDUW', u'name': u'General', u'parent': u'DTDTV2EP', u'etag': '720740d7f5774845a85786af973c3f51', u'key': u'9WF9BDUW', u'group_id': u'160464'}, {u'collectionVersion': 94, u'updated': 'Wed, 11 Sep 2013 21:19:27 EST', u'collectionKey': u'VKCEE7SG', u'name': u'Soar', u'parent': u'DTDTV2EP', u'etag': 'ca6dce702d760a3ac1374b2bf9dcbe33', u'key': u'VKCEE7SG', u'group_id': u'160464'}, {u'collectionVersion': 94, u'updated': 'Wed, 11 Sep 2013 21:19:37 EST', u'collectionKey': u'MWXM72N2', u'name': u'ACT-R', u'parent': u'DTDTV2EP', u'etag': '1505496b75d52f76db49098fd4aef0f7', u'key': u'MWXM72N2', u'group_id': u'160464'}, {u'collectionVersion': 108, u'updated': 'Thu, 12 Sep 2013 14:37:59 EST', u'collectionKey': u'55G4P6RA', u'name': u'Human-Computer Interaction', u'parent': u'MGID93AS', u'etag': 'bb3d409d788a632010ff55d6e6347ed7', u'key': u'55G4P6RA', u'group_id': u'160464'}, {u'collectionVersion': 77, u'updated': 'Wed, 11 Sep 2013 20:19:00 EST', u'collectionKey': u'DTDTV2EP', u'name': u'Cognitive Architecture', u'parent': u'MGID93AS', u'etag': '677e35466e7dce02920f1d8e13a5204c', u'key': u'DTDTV2EP', u'group_id': u'160464'}, {u'collectionVersion': 104, u'updated': 'Wed, 11 Sep 2013 21:29:32 EST', u'collectionKey': u'4KATF6MA', u'name': u'All', u'parent': u'MGID93AS', u'etag': '4e8749634935f16969b8eff0bd5bc4f1', u'key': u'4KATF6MA', u'group_id': u'160464'}, {u'collectionVersion': 93, u'updated': 'Wed, 11 Sep 2013 21:18:17 EST', u'collectionKey': u'6Q5U5REX', u'name': u'Language', u'parent': u'MGID93AS', u'etag': '6fae6f1dd5442223830e4c769de0de5a', u'key': u'6Q5U5REX', u'group_id': u'160464'}, {u'collectionVersion': 113, u'updated': 'Fri, 13 Sep 2013 11:03:57 EST', u'collectionKey': u'XV6KXZ93', u'name': u'Decision-Making', u'parent': u'55G4P6RA', u'etag': 'b3edea36e0f6e945ae7129d0ae4720d6', u'key': u'XV6KXZ93', u'group_id': u'160464'}, {u'collectionVersion': 106, u'updated': 'Thu, 12 Sep 2013 14:36:46 EST', u'collectionKey': u'XQMGSSEH', u'name': u'Physiology', u'parent': u'MGID93AS', u'etag': '059b3532936beff8612121ca2d5fc7f9', u'key': u'XQMGSSEH', u'group_id': u'160464'}, {u'collectionVersion': 106, u'updated': 'Thu, 12 Sep 2013 14:36:07 EST', u'collectionKey': u'MGID93AS', u'name': u'website', u'parent': False, u'etag': 'e6f8e8dece3076fe53eb7fbac0a879ec', u'key': u'MGID93AS', u'group_id': u'160464'}]
