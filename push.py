#!/usr/bin/python

# insert <!--zot_bib_web--> into your page for this to work.
# set the post_id to the page number (see page's URL)

wp_url = 'https://cc.ist.psu.edu/wp/xmlrpc.php'
wp_username = 'pubpusher'
wp_password = 'push47293738zot'
wp_blogid = "0"

post_id = 225

infile = "zotero-bib.html"

#####

import datetime, xmlrpclib
import codecs
import sys

status = 'publish'

server = xmlrpclib.ServerProxy(wp_url)


from subprocess import call

def get_bibliography (coll, catchall):
    global infile
    
    if coll:
        infile = 'zotero-bib.html'
        call(["./zot.py", coll, catchall, infile, '--div'])
        
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
    catchall = m.group(4)

    contents = get_bibliography(coll, catchall)
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
    print " Need  <!--zot_bib_web--> or <!--zot_bib_web COLLECTIONID--> or <!--zot_bib_web COLLECTIONID CATCHALLID-->"
