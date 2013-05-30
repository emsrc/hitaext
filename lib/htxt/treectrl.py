#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007-2013 by 
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
provides the class HitaextTreeCtrl, a subclass of wx.TreeCtrl
as used in Hitaext
'''

__version__ = "1.0"
__author__ = "Erwin Marsi"

import wx


class HitaextTreeCtrl(wx.TreeCtrl):
    '''

    * elemTree: element tree of associated XML file
    
    * filename: filename of associated XML file 
    
    * focused: list of focused items, that is, items which are visually
    highlight because they are aligned with the selected item in the other
    tree
    
    '''
    def __init__(self, parent, elemTree):
        wx.TreeCtrl.__init__(self, parent, id=-1, 
                             style=wx.TR_DEFAULT_STYLE|wx.TR_HAS_BUTTONS)
        self.makeImages()

        self.focused = []
        
        self.elemTree = elemTree
        
        self.Bind(wx.EVT_TREE_KEY_DOWN, self.onKeyDown)
        
        
    def makeImages(self):
        '''
        create the small icons used in the TreeCtrl
        '''
        imageSize = (16,16)
        self.imageList = wx.ImageList(imageSize[0], imageSize[1])
        
        self.imageTerminal = self.imageList.Add(
            wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, imageSize))
        self.imageNonTerminal = self.imageList.Add(
            wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, imageSize)) 
        self.imageOpenNonTerminal = self.imageList.Add( 
            wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, imageSize)) 
        self.imageFocus = self.imageList.Add(
            wx.ArtProvider_GetBitmap(wx.ART_ERROR, wx.ART_OTHER, imageSize))
        #self.imageBack = self.imageList.Add(
        #    wx.ArtProvider_GetBitmap(wx.ART_GO_BACK, wx.ART_OTHER, imageSize))
        #self.imageForward = self.imageList.Add(
        #    wx.ArtProvider_GetBitmap(wx.ART_GO_FORWARD, wx.ART_OTHER, imageSize))
        
        self.AssignImageList(self.imageList)
        
    # ------------------------------------------------------------------------
    # element methods
    # ------------------------------------------------------------------------
    
    def processElemTree(self, pseudoRoot=None, ignoreTags=[], skipTags=[]):
        '''
        process element tree to produce a matching TreeCtrl
        '''
        self.skipTags = skipTags
        self.ignoreTags = ignoreTags
        
        rootElem = self.elemTree.getroot()
        
        # If pseudoRoot tag is equal to document root, then find will return None!
        # So we have to check explicitly that pseudoRoot tag is not equal to rootElem tag. 
        if pseudoRoot and pseudoRoot != rootElem.tag:        
            rootElem = self.elemTree.find('.//' + pseudoRoot)
            assert rootElem, 'document contains no (pseudo)root element "%s"' % pseudoRoot

        rootItemId = self.addRootElem(rootElem)
        self.appendElem(rootItemId, rootElem)
        # must set focus to get icons
        # after processing of children
        # child items are required for correct icon
        self.setItemFocus(rootItemId)
    
    def addRootElem(self, rootElem):
        rootItemId = self.addRootItem(rootElem.tag)
        # store back-pointer to item id in element
        rootElem.set("_item", rootItemId)
        self.setElemAlign(rootElem)
        self.SetItemPyData(rootItemId, rootElem)
        return rootItemId

    def appendElem(self, parentItemId, parentElem):
        for childElem in parentElem.getchildren():
            if childElem.tag in self.skipTags:
                # skipping this element means that we do not create an item for it
                # but we do continue processing its children
                self.appendElem(parentItemId, childElem)
            elif childElem.tag not in self.ignoreTags:
                childItemId = self.appendItem(parentItemId, childElem.tag)
                # store back-pointer to item id in element
                childElem.set("_item", childItemId)
                self.setElemAlign(childElem)
                # attach element as item data
                self.SetItemPyData(childItemId, childElem)
                self.appendElem(childItemId, childElem)
                # must set focus to get icons
                # after processing of children because we need to know if the
                # item has any children
                self.setItemFocus(childItemId)
            # other child elements are in self.ignoreTags
            # and they as well as their children are left unprocessed
                
    def getSelectedElem(self):
        # Returns the selection, or an invalid item if there is no selection
        # On MSW the TreeCtrl has no selection on initialisation.
        item = self.GetSelection()
        if item.IsOk():
            return self.GetItemPyData(self.GetSelection())
        else:
            self.SelectItem(self.GetRootItem())
            return self.GetItemPyData(self.GetRootItem())
                
    def setElemFocus(self, elem, focused=False):
        self.setItemFocus(elem.get("_item"), focused)
        
    def setElemAlign(self, elem):
        self.setItemAlign(elem.get("_item"), 
                          elem.get("_alignments"))
        
    def selectElem(self, elem):
        self.SelectItem(elem.get("_item"))
        
    # ------------------------------------------------------------------------
    # item methods
    # ------------------------------------------------------------------------
    
    def addRootItem(self, label):
        return wx.TreeCtrl.AddRoot(self, '<%s>' % label)
    
    def appendItem(self, itemId, label):
        return wx.TreeCtrl.AppendItem(self, itemId, '<%s>' % label)
                
    def setItemFocus(self, itemId, focused=False):
        if focused:
            wx.TreeCtrl.SetItemImage(self, itemId, self.imageFocus,
                                     wx.TreeItemIcon_Normal)
            wx.TreeCtrl.SetItemImage(self, itemId, self.imageFocus,
                                     wx.TreeItemIcon_Expanded)
            self.focused.append(itemId)
        else:
            if self.ItemHasChildren(itemId):
                wx.TreeCtrl.SetItemImage(self, itemId, self.imageNonTerminal,
                                         wx.TreeItemIcon_Normal)
                wx.TreeCtrl.SetItemImage(self, itemId, self.imageOpenNonTerminal,
                                         wx.TreeItemIcon_Expanded)
            else:
                wx.TreeCtrl.SetItemImage(self, itemId, self.imageTerminal,
                                         wx.TreeItemIcon_Normal)
                
            try:
                self.focused.remove(itemId)
            except ValueError:
                pass

    def setItemAlign(self, itemId, aligned=False): 
        if aligned:
            self.SetItemTextColour(itemId, "forest green")
        else:
            self.SetItemTextColour(itemId, "orange")
            
                
    def clearFocus(self):
        for item in self.focused[:]:
            self.setItemFocus(item, focused=False)
        
    # ------------------------------------------------------------------------
    # event methods
    # ------------------------------------------------------------------------

    def onKeyDown(self, evt):
        keycode = evt.GetKeyCode()
        
        if keycode == wx.WXK_LEFT:
            # why does this fail?
            #item = evt.GetItem()
            item = self.GetSelection()
            if item.IsOk():
                parentItem = self.GetItemParent(item)
                if parentItem.IsOk():
                    print self.GetItemText(parentItem)
                    self.SelectItem(parentItem)
                    self.Collapse(parentItem)
        else:
            # skip other keys strokes, e.g. TAB and SPACE,
            # which are handled by parent AlignFrame 
            evt.Skip()



if __name__ == '__main__':
    from ielemtree import IndexElemTree
    from sys import argv
    
    tree = IndexElemTree(file=argv[1])
    tree.update()

    class TestFrame(wx.Frame):
        
        def __init__(self): 
            wx.Frame.__init__(self, None)
            
            tc = HitaextTreeCtrl(self, tree)        
            tc.processElemTree(pseudoRoot='div')

        
    app = wx.PySimpleApp() 
    frame = TestFrame() 
    frame.Show() 
    app.MainLoop() 

