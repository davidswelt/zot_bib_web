#!/usr/bin/env python
# coding: utf-8

class ZBWModule:

    def bibAdded (self, bibitem):
        "Called for each bibliographic item"
        return None
    def transformBibHtml (self, bibitem, html):
        "Return HTML (string) for a single bibliographic item.  Return html if no change desired."
        return html
    def makePreBibliography (self):
        "Return HTML (string) to be inserted before the bibliography."
        return ""
    def makePostBibliography (self):
        "Return HTML (string) to be inserted after the bibliography."
        return ""

zotbibweb_modules = []
def add_module (className):
    global zotbibweb_modules
    zotbibweb_modules += [className]


# MODULE CODE
# Can be in a separate file/package in the future

# Example module
from collections import Counter
class VenueStats (ZBWModule):

    def __init__(self):
        self.venueCount = Counter()
    
    def bibAdded (self, bibitem):
        if bibitem.venue() and bibitem.venue()!="":
            self.venueCount[bibitem.venue()] += 1
        
    def makePreBibliography (self):
        h = '<h3>Most frequent publication venues:</h3><table class="venueStats">\n'
        for v,c in self.venueCount.most_common(5):
            h += '<tr><td class="venue">%s</td><td class="count">%s</td></tr>\n'%(v,c)
        h += '</table>'
        return h

add_module(VenueStats)

# to enable a module, list it in modules_enabled, e.g. modules_enabled = ["modules.VenueStats"]
