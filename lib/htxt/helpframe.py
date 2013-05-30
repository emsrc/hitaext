#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007-2010 by 
# Erwin Marsi and TST-Centrale
#
#
# This file is part of the Hitaext program.
#
# The Hitaext program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# The Hitaext program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
provides the class HelpViewFrame, a subclass of wx.TreeCtrl,
for displaying help as an HTML file 
'''

__version__ = "1.0"
__author__ = "Erwin Marsi"

import wx
import wx.html

from os import getcwd, getenv
from os.path import dirname, exists, join as pathjoin


class HelpViewFrame(wx.Frame):
    
    def __init__(self, parent, title): 
        wx.Frame.__init__(self, parent, -1, title=title, size=(600,600))
        html = wx.html.HtmlWindow(self)
        
        (path, tried) = self.findDocs()
        
        if path:
            html.LoadFile(path)
        else:
            html.SetPage("<b>Error: cannot find documentation at any of the following locations</b><br><br>" +
                         tried) 
        
        self.Show()
        
    def findDocs(self): 
        paths = [getcwd(), 
                 pathjoin(getcwd(), 'doc'), 
                 getenv("RESOURCEPATH",""), # are we a Mac OS X application bundle?
                 pathjoin(getenv("DAESO_BASE",""), "trunk/software/intern/doc/hitaext") # dev tree
                 ] 
        tried = ''
        print
        
        for p in paths:
#            if type(p) == type(None):
#                continue
            p = pathjoin(p, "index.htm")
            if exists(p):
                return (p, None)
            tried += p + '<br>'
        else:
            return (None, tried)
        
