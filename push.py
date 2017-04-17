#!/usr/bin/env python

# This tool updates a given Page on your Wordpress site.

# insert <!--zot_bib_web  COLLID1 COLLID2 --> into your page where you would like the
# bibliography to be inserted.
# COLLID1 is the ID (hex, 8 digits) of the top-level collection.
#     All sub-collections to this will be rendered.
# COLLID2 is the ID of a collection containing all records;
#     All records contained in COLLID2 minus the ones present
#     under COLLID1 will be rendered under a "Miscellaneous" heading.

# (C) 2013 David Reitter, The Pennsylvania State University
# Released under the GNU General Public License, V.3 or later.



wp_url = 'http://example.com/wp/xmlrpc.php'   # Wordpress XMLRPC URL
wp_username = 'pubpushuser'   # create a user.  Insert name here.
wp_password = 'xxxxxxxxxxxxxxx'   # password
wp_blogid = "0"  # typically 0, unless you have other blogs on the site

post_id = 225   # set the post_id to the page number (see page's URL)

infile = "zotero-bib.html"  # input file














#############################################################################
try:
    from settings import *
except ImportError:
    pass
#############################################################################


import datetime, xmlrpclib
import codecs
import sys

status = 'publish'

server = xmlrpclib.ServerProxy(wp_url)


from subprocess import call

def get_bibliography (coll):
    global infile

    if coll:
        infile = 'zotero-bib.html'
        # to do: why call as a sub-process when we can just import it?
        call(["./zot.py", coll, infile, '--div'])

    if infile:
        file = codecs.open(infile, "r", "utf-8")
        if file:
            return file.read()
    return ""

# let's get the

rawpost = server.wp.getPost(wp_blogid, wp_username, wp_password, post_id)

import re

m = re.match(r'(.*)(<!--\s*zot_bib_web\s*(\w*)\s*(\w*)\s*-->)(.*)', rawpost['post_content'], re.DOTALL|re.IGNORECASE)

if m:
    newpost = m.group(1) + m.group(2)

    coll = m.group(3)
    #  catchall = m.group(4)  (legacy)

    contents = get_bibliography(coll)
    if contents:
        newpost += contents + "\n<!--zot_bib_end_of_bibliography-->"


    m2 = re.match(r'.*<!--\s*zot_bib_end_of_bibliography\s*-->(.*)', m.group(5), re.DOTALL|re.IGNORECASE)
    if m2:
        newpost += m2.group(1)
    else:
        newpost += m.group(5)  # all of the remainder

    if rawpost['post_content'].strip() == newpost.strip():
        print("Content unchanged")
    else:

        data = { 'post_content' : newpost}

        post_id = server.wp.editPost(wp_blogid, wp_username, wp_password, post_id, data)

        print "post update ",
        if post_id:
            print "successful."
        else:
            print "NOT successful."
            sys.exit(1)
else:
    print "No shortcode found in post %s."%post_id
    print " Need  <!--zot_bib_web--> or <!--zot_bib_web COLLECTIONID--> or <!--zot_bib_web COLLECTIONID -->"
