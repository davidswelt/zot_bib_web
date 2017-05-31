#!/usr/bin/env python

# This tool updates a given Page on your Wordpress site with
# a bibliography produced by zot_bib_web.

# insert <!--zot_bib_web  COLLID1 --> into your page where you would like the
# bibliography to be inserted.
# COLLID1 is the ID (hex, 8 digits) of the top-level collection.
#     All sub-collections to this will be rendered.

# To use a more complex configuration, define settings.py.

# (C) 2013, 2017 David Reitter, The Pennsylvania State University
# Released under the GNU General Public License, V.3 or later.






#############################################################################

def noop(*args,**kwargs):
    pass

def push_wordpress(url, blogID, user, password, postID):
    global wp_url, wp_username, wp_password, wp_blogid, post_id
    wp_url = url
    wp_username = user
    wp_password = password
    wp_blogid = blogID
    post_id = postID

#############################################################################

# Configuration example
# push_wordpress(url='https://example.com/wp/xmlrpc.php', blogID=0, user='pubpushername', password='pass', postID=200)

# If no collection is given, we read from what is specified as outfile in settings.py, or fro mzotero-bib.html



try:
    import __builtin__
except ImportError:
    # Python 3
    import builtins as __builtin__

__builtin__.shortcut = noop
__builtin__.user_collection = noop
__builtin__.group_collection = noop
__builtin__.exclude_collection = noop
__builtin__.rename_collection = noop
__builtin__.exclude_items = noop
__builtin__.push_wordpress = push_wordpress

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
    global outputfile

    if coll:
        outputfile = 'zotero-bib.html'
        # to do: why call as a sub-process when we can just import it?
        call(["./zot.py", coll, '-o', outputfile, '--div'])

    if outputfile:
        file = codecs.open(outputfile, "r", "utf-8")
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
    #  catchall = m.group(4)  (legacy - ignored)

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
