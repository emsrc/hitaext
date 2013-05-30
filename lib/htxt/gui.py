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
Hitaext: hierarchical text aligment tool
'''

__version__ = "1.0"
__author__ = "Erwin Marsi"

import wx

from xml.parsers.expat import ExpatError
from os import getcwd, getenv
from os.path import basename, dirname, isabs, realpath, join as joinpaths
from platform import system

#from htxt.ielemtree import IndexElemTree
from daeso.ptc.ielemtree import IndexElemTree
from htxt.treectrl import HitaextTreeCtrl
from htxt.helpframe import HelpViewFrame

from daeso.ptc.document import HitaextDoc


class HitaextException(Exception):
    pass

class HitaextError(HitaextException):
    pass

class HitaextWarning(HitaextException):
    pass



class AlignFrame(wx.Frame):
    '''
    a frame containing the two HitaextElemTreeCtrl's
    representing the ElementTrees for two XML documents
    '''
    
    def __init__(self, parent, docTrees, alignTree): 
        wx.Frame.__init__(self, parent, -1, title=basename(alignTree.filename),
                          style=wx.MINIMIZE_BOX|wx.MAXIMIZE_BOX|wx.RESIZE_BORDER|wx.CAPTION)
        self.log = parent.log
        self.isChanged = False
        self.docTrees = docTrees
        self.sync = False
        self.blockSync = False
        
        sizer = wx.BoxSizer(wx.VERTICAL) 
        
        self.makeTreeCtrls(sizer, alignTree)
        self.makeOptionCtrls(sizer)
        self.makeTextFrame()
        
        #self.Bind(wx.EVT_CHAR, self.onKeyDown)
        
        self.SetSizer(sizer)
        self.Show()

    def makeTreeCtrls(self, sizer, alignTree):
        treeSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.treeCtrls = {}
        
        for side in ("from", "to"):
            self.treeCtrls[side] = HitaextTreeCtrl(self, self.docTrees[side])
            self.treeCtrls[side].processElemTree(alignTree.get_pseudo_root(side),
                                                 alignTree.get_tags(side, "ignore"),
                                                 alignTree.get_tags(side, "skip"))
            treeSizer.Add(self.treeCtrls[side], 1, wx.EXPAND) 
            self.Bind(wx.EVT_TREE_KEY_DOWN, self.onKeyDown, self.treeCtrls[side])
        
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.onFromTreeSelChanged,
                  self.treeCtrls["from"])
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.onToTreeSelChanged,
                  self.treeCtrls["to"])                
        
        sizer.Add(treeSizer, 1, wx.EXPAND)
        
    def makeOptionCtrls(self, sizer):
        optionSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        syncCheckBox = wx.CheckBox(self, -1, "sync")
        optionSizer.Add(syncCheckBox, 0, wx.ALL, 8)
        self.Bind(wx.EVT_CHECKBOX, self.onSync, syncCheckBox)
        
        sizer.Add(optionSizer)

    def makeTextFrame(self):
        title = ( basename(self.docTrees['from'].filename) + 
                  ' | ' + 
                  basename(self.docTrees['to'].filename) )
        self.textFrame = TextFrame(self, title)
        
        self.updateText('from')
        self.updateText('to')
        
        # binding slider events
        self.Bind(wx.EVT_SCROLL_THUMBRELEASE, 
                  self.onFromSliderChanged,
                  self.textFrame.sliders["from"])
        self.Bind(wx.EVT_SCROLL_THUMBRELEASE, 
                  self.onToSliderChanged,
                  self.textFrame.sliders["to"])
        
    # ------------------------------------------------------------------------
    # event methods
    # ------------------------------------------------------------------------
   
    # treeCtrl events

    def onFromTreeSelChanged(self, evt):
        self.updateText("from")
        self.updateFocus(self.treeCtrls["from"], 
                         self.treeCtrls["to"])

    def onToTreeSelChanged(self, evt):
        self.updateText("to")
        self.updateFocus(self.treeCtrls["to"], 
                         self.treeCtrls["from"])
   
    # slider events
               
    def onFromSliderChanged(self, evt):
        self.updateText("from")
        
    def onToSliderChanged(self, evt):
        self.updateText("to")
        
    # options
    
    def onSync(self, evt):
        checkBox = evt.GetEventObject()
        self.sync = checkBox.GetValue()
        
    # key events
    
    def onKeyDown(self, evt):
        keycode = evt.GetKeyCode()
        
        if keycode == wx.WXK_TAB:
            # if one of the TreeCtrls is selected,
            # evt is wxTree_Event, so get to the wxKey_Event first 
            if evt.GetKeyEvent().ControlDown():
                self.selectNextAlignedItem()
            else:
                self.changeTreeCtrlFocus()
        elif keycode == wx.WXK_SPACE:
            self.toggleAlignSelection()
        else:
            evt.Skip()    
            
    # ------------------------------------------------------------------------
    # GUI update methods
    # ------------------------------------------------------------------------
                    
    def updateText(self, side):
        elem = self.treeCtrls[side].getSelectedElem()
        start, end = elem.get("_start"), elem.get("_end")
        
        # prevent empty elements from triggering scrolling
        if start < end:
            text = self.docTrees[side].text
            context = self.textFrame.sliders[side].GetValue()
            # prevent out of bounds
            viewStart = max(0, start - context)
            viewEnd = min(len(text), end + context)
            
            textCtrl = self.textFrame.texts[side]
            textCtrl.Clear()
            
            textCtrl.SetDefaultStyle(wx.TextAttr("grey", "white"))
            textCtrl.AppendText(text[viewStart:start])
            
            if elem.get("_alignments"):
                textCtrl.SetDefaultStyle(wx.TextAttr("forest green", "white"))
            else:
                textCtrl.SetDefaultStyle(wx.TextAttr("orange", "white"))
            
            # TODO: upper limit should come from setting in <render> section
            if end - start < 10000:
                textCtrl.AppendText(text[start:end])
            else:
                textCtrl.AppendText(text[start:start + 5000])
                textCtrl.AppendText("\n[...]\n")
                textCtrl.AppendText(text[end - 5000:end])

            textCtrl.SetDefaultStyle(wx.TextAttr("grey", "white"))
            textCtrl.AppendText(text[end:viewEnd])

            # this works on MSW, but it not convenient,
            # because you have to scroll upwards all the time 
            # to see the right context
            #textStart = start - viewStart
            #textCtrl.ShowPosition(textStart)

            # instead, simply do this (works fine on MSW)
            textCtrl.ShowPosition(0)

            # no way to enforce the right positioning at OS X ...  :-(
 
    def updateFocus(self, thisTree, otherTree):
        # Called after the selected item in one tree has changed
        # to focus the aliged item(s) in other tree
        otherTree.clearFocus()

        thisElem = thisTree.getSelectedElem()
        
        otherAlignElems = thisElem.get("_alignments")
        
        if otherAlignElems:
            for otherElem in otherAlignElems:
                item = otherElem.get("_item")
                otherTree.setItemFocus(item, focused=True)
                otherTree.EnsureVisible(item)
                
            if self.sync:
                # When "sync" is checked, the aligned item in the
                #  other tree is automatically selected. However, on
                #  MSW, this fires another EVT_TREE_SEL_CHANGED, which
                #  causes selection of the aligned item in *this*
                #  tree, etc, ad inifintum. Introduced a
                #  self.blockSync boolean to break this endless loop.
                if system() == "Windows":
                    if self.blockSync:
                        self.blockSync = False
                    else:
                        self.blockSync = True
                        otherTree.selectElem(otherAlignElems[0])
                else:
                    otherTree.selectElem(otherAlignElems[0])

    def changeTreeCtrlFocus(self):
        if self.FindFocus() is self.treeCtrls['from']:
            self.treeCtrls['to'].SetFocus()
        else:
            self.treeCtrls['from'].SetFocus()
            
    def selectNextAlignedItem(self):
        if self.FindFocus() is self.treeCtrls['from']:
            thisTree = self.treeCtrls['from']
            otherTree = self.treeCtrls['to']
        elif self.FindFocus() is self.treeCtrls['to']:
            thisTree = self.treeCtrls['to']
            otherTree = self.treeCtrls['from']
        else:
            # another control has focus
            # should never happen
            return
            
        thisSelElem = thisTree.getSelectedElem()
        otherSelElem = otherTree.getSelectedElem()
        
        # alignments are assumed to be in text order
        otherAlignedElems = thisSelElem.get("_alignments")
        
        if not otherAlignedElems:
            # shortcut
            return
        
        try:
            i = otherAlignedElems.index(otherSelElem)
            otherSelElem = otherAlignedElems[i+1]
        except (IndexError, ValueError):
            # Incase of a ValueError, the selected element of the other tree
            # is not aligned to the selected element of this tree.
            # In case of an IndexError, the selected element of the other tree
            # is the last of aligned elements.
            # In both cases, we fall back to the first aligned element.
            otherSelElem = otherAlignedElems[0]
            
        otherTree.selectElem(otherSelElem)

    # ------------------------------------------------------------------------
    # alignment methods
    # ------------------------------------------------------------------------

    def toggleAlignSelection(self):
        fromElem = self.treeCtrls["from"].getSelectedElem()
        toElem = self.treeCtrls["to"].getSelectedElem()
        
        try:
            # disalign
            fromElem.get("_alignments").remove(toElem)
            self.treeCtrls["from"].setElemAlign(fromElem)
            self.treeCtrls["from"].setElemFocus(fromElem, False)
            
            toElem.get("_alignments").remove(fromElem)
            self.treeCtrls["to"].setElemAlign(toElem)
            self.treeCtrls["to"].setElemFocus(toElem, False)
            
            self.log("Disaligning <%s> #%s to <%s> #%s" % (
                fromElem.tag, 
                fromElem.get("_n"),
                toElem.tag, 
                toElem.get("_n") ))
            
        except ValueError, inst:
            # align
            fromAlignments = fromElem.get("_alignments")
            toAlignments = toElem.get("_alignments")
            
            fromAlignments.append(toElem)
            toAlignments.append(fromElem)
            
            # keep alignments sorted in text order
            fromAlignments.sort(lambda e1, e2: int(e1.get("_start")) - int(e2.get("_start")))
            toAlignments.sort(lambda e1, e2: int(e1.get("_start")) - int(e2.get("_start")))
            
            self.treeCtrls["from"].setElemAlign(fromElem)
            self.treeCtrls["to"].setElemAlign(toElem)
            
            #if self.FindFocus() is self.treeCtrls["from"]:
            self.treeCtrls["to"].setElemFocus(toElem, True)
            #else:
            self.treeCtrls["from"].setElemFocus(fromElem, True)
                
            self.log("Aligning <%s> #%s to <%s> #%s" % (
                fromElem.tag, 
                fromElem.get("_n"),
                toElem.tag, 
                toElem.get("_n") ))
            
        self.updateText('from')
        self.updateText('to')
        self.isChanged = True
 
                
    
class TextFrame(wx.Frame):
    
    def __init__(self, parent, title='Hitaext Text'):
        wx.Frame.__init__(self, parent, size=(800,600), title=title,
                          style=wx.MINIMIZE_BOX|wx.MAXIMIZE_BOX|wx.RESIZE_BORDER|wx.CAPTION) 
        self.title = title
        
        panel = wx.Panel(self)
        self.texts = {}
        self.sliders = {}

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        subSizers = {}
        
        for id in ("from", "to"):
            subSizers[id] = wx.BoxSizer(wx.VERTICAL)
            #self.texts[id] = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_READONLY)#|wx.TE_NOHIDESEL|wx.TE_RICH)
            self.texts[id] = wx.TextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH2)
            # this currently only works with develop version wxPython!
            self.texts[id].MacCheckSpelling(False)
            subSizers[id].Add(self.texts[id], 1, flag=wx.EXPAND)
            
            self.sliders[id] = wx.Slider(panel, -1, 0, 0, 1000,
                                         style=wx.SL_HORIZONTAL|wx.SL_AUTOTICKS|wx.SL_LABELS)
            subSizers[id].Add(self.sliders[id], 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 4)
            
            sizer.Add(subSizers[id], 1, wx.EXPAND) 
            
        panel.SetSizer(sizer)
        panel.Layout()
        
        self.Show()
        
        

class HitaextFrame(wx.Frame):
    
    alignWildcard = "Parallel text Corpus (*.ptc)|*.ptc|Alignment (*.xml)|*.xml"
    docWildcard = "XML Document (*.xml)|*.xml|All (*.*)|*.*"
    
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=-1, title="Hitaext",
                          size=(800,200))
        self.makeLogText()
        self.log("Hitaext (%s)" % __version__)
        
        self.makeMenuBar()
        self.CreateStatusBar()
        
        self.Bind(wx.EVT_CLOSE, self.onClose)  
        self.reset()
        
    def reset(self):
        # MSW requires explicit kill
        try:
            self.align.Destroy()
        except AttributeError:
            pass
        self.align = None
        self.alignTree = None
        self.docTrees = {'from': None, 'to': None}

    # ------------------------------------------------------------------------
    # widget construction methods
    # ------------------------------------------------------------------------
    
    def makeLogText(self):
        self.logText = wx.TextCtrl(self,
                                   style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH)
    
    def menuData(self): 
        # Using the "\tKeyName" syntax automatically creates a
        # wx.AcceleratorTable for this frame and binds the keys to
        # the menu items.  
        return (
                ("&File",
                   ("&New\tCtrl-N", "New alignment", self.onNew),
                   ("&Open\tCtrl-O", "Open alignment", self.onOpen),
                   #("&Reopen\tCtrl-R", "Reopen alignment", self.onReopen),
                   ("&Save\tCtrl-S", "Save alignment", self.onSave),
                   ("Save &As\tCtrl-A", "Save alignment as", self.onSaveAs),
                   #("&Quit\tCtrl-Q", "Quit", self.onClose)
                   ), 
                ("&Help",
                   ("&Hitaext Help\tCtrl-?", "Read online help", self.onHelp),
                   ("&About Hitaext", "Information about Hitaext", self.onAbout)
                   )
                )
    
    def makeMenuBar(self):                     
        menuBar = wx.MenuBar()     
        for eachMenuData in self.menuData(): 
            menuLabel = eachMenuData[0] 
            menuItems = eachMenuData[1:] 
            menuBar.Append(self.makeMenu(menuItems), menuLabel)
        
        self.SetMenuBar(menuBar) 
        
    def makeMenu(self, menuData):                                 
        menu = wx.Menu() 
        for eachLabel, eachStatus, eachHandler in menuData: 
            if not eachLabel: 
                menu.AppendSeparator() 
                continue 
            
            # a hack to bind the About menu from application menu in OS X
            if eachLabel.startswith("&About"):
                id = wx.ID_ABOUT
            else:
                id = -1
                
            menuItem = menu.Append(id, eachLabel, eachStatus) 
            self.Bind(wx.EVT_MENU, eachHandler, menuItem)
        return menu    
    
    def onClose(self, evt):
        self.saveChanges()
        
        if not self.isChanged():
            self.Destroy()
    
    # ------------------------------------------------------------------------
    # event methods
    # ------------------------------------------------------------------------
    
    def onNew(self, evt):
        self.saveChanges()
    
        if not self.isChanged():
            try:
                self.alignTree = HitaextDoc()
                
                for side in ('from','to'):
                    self.docTrees[side] = self.openDocument(side)            
                    self.alignTree.set_filename(side, self.docTrees[side].filename)
                    self.alignTree.init_elems(side, self.docTrees[side])
                    self.docTrees[side].update()      
           
                self.alignTree.inject_alignments(self.docTrees["from"], self.docTrees["to"])
                
                self.align = AlignFrame(self, self.docTrees, self.alignTree)
            except HitaextWarning, inst:
                # user canceled
                self.log(str(inst), level='WARNING')
            #except Exception, inst:
                # something else went wrong 
            #    self.log(str(inst), level='ERROR')
            #    self.reset()

    def onOpen(self, evt):
        self.saveChanges()
    
        if not self.isChanged():
            self.reset()
            
            try:
                self.alignTree = self.openAlignment()
                
                for side in ('from','to'):
                    docFilename = self.alignTree.get_filename(side)
                    self.docTrees[side] = self.smartReadDocument(side, docFilename)
                    # update is not included in __init__, 
                    # because when starting a new alignment 
                    # we have to init the <render> section first,
                    # which requires a document tree 
                    self.docTrees[side].update(self.alignTree.get_tags(side, "ignore"), 
                                               self.alignTree.get_tags(side, "newline"),
                                               self.alignTree.get_tags(side, "blankline"))  
           
                self.alignTree.inject_alignments(self.docTrees["from"], self.docTrees["to"])        
                    
                # constructing other align and text frames
                self.align = AlignFrame(self, self.docTrees, self.alignTree)
            except HitaextWarning, inst:
                # user canceled
                self.log(str(inst), level='WARNING')
            except Exception, inst:
                # something went wrong 
                self.log(str(inst), level='ERROR')
                self.reset()
                # uncomment while debugging
                ## raise
            
    
    def onReopen(self, evt):
        pass
                    
    def onSave(self, evt=None):
        if self.alignTree.filename:
            self.saveAlignment(self.alignTree.filename)
        else:
            self.onSaveAs()
    
    def onSaveAs(self, evt=None):
        filename = wx.FileSelector("Save alignment as...",
                                  default_extension=".xml",
                                   wildcard=self.alignWildcard, 
                                   flags=wx.SAVE|wx.OVERWRITE_PROMPT|wx.CHANGE_DIR)
        
        if filename:
            self.saveAlignment(filename)
        else:
            self.log('Save alignment canceled by user', level='WARNING')
            
    def onAbout(self, evt):
        info = wx.AboutDialogInfo()
        info.AddDeveloper("Erwin Marsi")
        info.SetName("Hitaext")
        info.SetDescription("Hierarchical text alignment tool")
        info.SetVersion("Version: " + __version__)
        info.SetCopyright("GNU Public License")
        info.SetWebSite("http://daeso.uvt.nl")
        wx.AboutBox(info)
    
    def onHelp(self, evt):
        HelpViewFrame(self, title="Hitaext help")
        
    # ------------------------------------------------------------------------
    # log methods
    # ------------------------------------------------------------------------
 
    def log(self, text, level='INFO', newline=True):
        text = level + ": " + text
        
        if newline:
            text += '\n'

        self.logText.AppendText(text)
    
    # ------------------------------------------------------------------------
    # file IO methods
    # ------------------------------------------------------------------------
    
    def openAlignment(self):
        '''
        select and read alignment file
        '''
        filename = wx.FileSelector("Open alignment...",
                                   wildcard=self.alignWildcard)
        if filename:
            return self.readAlignment(filename)
        else:
            raise HitaextWarning('Open alignment canceled by user')
            
    def readAlignment(self, filename):
        '''
        read alignment file
        '''
        # TODO: use current dir or a search path env var,
        # instead of the full path
        
        self.log("Reading alignment from %s" % filename)
        
        # errors are reported but are still raised 
        try:
            return HitaextDoc(file=filename)
        except IOError, inst:
            self.log('unable to open file, ' + str(inst), 
                     level='ERROR')
            raise
        except ExpatError, inst:
            self.log('cannot parse XML, ' + str(inst), 
                     level='ERROR')
            raise
        except AssertionError, inst:
            self.log('XML invalid, ' + str(inst), 
                     level='ERROR')
            raise
        except Exception, inst:
            self.log('unknown error, ' + str(inst), 
                     level='ERROR')
            raise
          
    def saveAlignment(self, filename):
        '''
        save alignment file
        '''
        self.log('Writing alignment to %s...' % filename)

        try:
            self.alignTree.extract_alignments(self.docTrees["from"],
                                              self.docTrees["to"])
            self.alignTree.write(filename)
        except Exception, inst:
            # catching all exception here to be on the safe side
            self.log('unable to save alignment, ' + str(inst),
                     level='ERROR')
            # uncomment whhen debuggging:
            raise
        else:
            # this function is also called from onSaveAs, so filename may have changed
            self.alignTree.filename= filename
            self.align.SetTitle(basename(filename))
            self.align.isChanged = False
            
    def openDocument(self, side):
        '''
        select and read source or target XML document
        '''
        if side == 'from':
            title = 'Open source document...'
        else:
            title = 'Open target document...'
            
        filename = wx.FileSelector(title,
                                   wildcard=self.docWildcard,
                                   flags=wx.OPEN|wx.CHANGE_DIR)
        if filename:
            return self.readDocument(side, filename)
        else:
            raise HitaextWarning("Open document canceled by user")
        
    def smartReadDocument(self, side, filename):
        if not isabs(filename):
            # Unless absolute, document file paths are interpreted relative to
            # the directory containing the alignment file (rather than the
            # current working dir)
            filename = joinpaths(
                dirname(self.alignTree.filename), 
                filename) 
        
        try:
            return self.readDocument(side, filename)
        except IOError:
            try:
                self.log('Searching for document in directory of alignment file')
                filename = joinpaths(dirname(self.alignTree.filename), 
                                     basename(filename))
                # Document file path is *not* updated in alignment file. This
                # is good when shipping files for annotation, with alignment
                # and document files in the same directory, because it
                # preserves the original document file paths.
                return self.readDocument(side, filename)
            except IOError:
                # Not sure if this is really smart, because it allows
                # selection of a totally different document
                self.log('Asking user to locate document')
                docTree = self.openDocument(side)
                filename = docTree.filename
                # In this case, the document file path does get updated
                self.log('Updating document filename to ' + filename)
                self.alignTree.set_filename(side, filename)
                # FIXME: self.align is not there yet
                # self.align.isChanged = True
                return docTree

    def readDocument(self, side, filename):
        '''
        read a source or target XML document
        '''
        
        if side == 'from':
            self.log("Reading source document from %s" % filename)
        else:
            self.log("Reading target document from %s" % filename)
        
        # errors are reported but are still raised 
        try:
            return IndexElemTree(filename)
        except IOError, inst:
            self.log('unable to open file, ' + str(inst),
                     level='ERROR')
            raise
        except ExpatError, inst:
            self.log('cannot parse XML, ' + str(inst),
                     level='ERROR')
            raise
        except Exception, inst:
            self.log('unknown error, ' + str(inst),
                     level='ERROR')
            raise
        
    def saveChanges(self):
        if self.isChanged():
            dlg = wx.MessageDialog(self,
                                   'The alignment has been modified. Save changes?',
                                   'Save',
                                   wx.YES_NO|wx.CANCEL)
            answer = dlg.ShowModal() 
            
            if answer == wx.ID_YES:
                self.onSave()
            elif answer == wx.ID_NO:
                # pretend nothing has changed
                self.align.isChanged = False
            # in case on wx.CANCEL, self.isChanged remains True    
            dlg.Destroy()

    ### ------------------------------------------------------------------------
    ### alignment update methods
    ### ------------------------------------------------------------------------
 
    ##def injectAlignment(self):
        ##'''
        ##Update the _alignments attributes in both document trees
        ##according to the links in the <alignments> section
        ##of the Hitaext XML document.
        ##'''
        ### Called when opening an Hitaext XML document.
        ### Assume "_alignments" attribute is initialized with empty list
        ### TODO: 
        ### - error handling
        ##for elem in self.alignTree.get_alignments():
            ##fromTag = elem.get('from_tag')
            ##fromN = int(elem.get('from_n'))
            ### fromN/toN counts from 1 -- tagCountTable counts from zero!!! 
            ##fromElem = self.docTrees["from"].tagCountTable[fromTag][fromN - 1]
            
            ##toTag = elem.get('to_tag')
            ##toN = int(elem.get('to_n'))
            ### fromN/toN counts from 1 -- tagCountTable counts from zero!!! 
            ##toElem = self.docTrees["to"].tagCountTable[toTag][toN - 1]
            
            ##fromElem.get("_alignments").append(toElem)
            ##toElem.get("_alignments").append(fromElem)    
          
    ##def extractAlignment(self):
        ##'''
        ##Replace the links in the <alignments> section
        ##of the Hitaext XML document according to 
        ##the _alignments attributes in both document trees.
        ##'''
        ###Called before saving an Hitaext XML document.
        ### TODO:
        ### - saving with id
        ##self.alignTree.clear_alignments()
        
        ##for fromElem in self.docTrees["from"].getiterator():
            ##for toElem in fromElem.get("_alignments", []):
                ##self.alignTree.add_n_alignment(fromElem.tag, fromElem.get("_n"), 
                                               ##toElem.tag, toElem.get("_n"))
    
    def isChanged(self):
        return ( self.align and self.align.isChanged )
    
    
    
 
class Hitaext(wx.App):
    
    def __init__(self, cl_args=None, redirect=False, filename=None):
        self.cl_args = cl_args
        wx.App.__init__(self, redirect=redirect, filename=filename)
    
    def OnInit(self):
        self.frame = HitaextFrame()        
        self.frame.Show() 
        self.SetTopWindow(self.frame)
        
        if self.cl_args:
            self.handleCommandLineOptions()
            
        return True
    
    def handleCommandLineOptions(self):
        if self.cl_args.corpus_file: 
            # This is a ugly hack. The current design should be rewritten to
            # seperate model actions (like reading a parallel text corpus)
            # from view actions (like open dialogues).
            try:
                frame = self.frame
                frame.alignTree = frame.readAlignment(self.cl_args.corpus_file)
                
                for side in ('from','to'):
                    docFilename = frame.alignTree.get_filename(side)
                    frame.docTrees[side] = frame.smartReadDocument(side, docFilename)
                    # update is not included in __init__, 
                    # because when starting a new alignment 
                    # we have to init the <render> section first,
                    # which requires a document tree 
                    frame.docTrees[side].update(frame.alignTree.get_tags(side, "ignore"), 
                                                frame.alignTree.get_tags(side, "newline"),
                                                frame.alignTree.get_tags(side, "blankline"))  
           
                frame.alignTree.inject_alignments(frame.docTrees["from"], 
                                                  frame.docTrees["to"])        
                    
                # constructing other align and text frames
                frame.align = AlignFrame(frame, frame.docTrees, frame.alignTree) 
            except HitaextWarning, inst:
                # user canceled
                frame.log(str(inst), level='WARNING')
            except Exception, inst:
                # something went wrong 
                frame.log(str(inst), level='ERROR')
                frame.reset()
                # uncomment while debugging
                ## raise
   
    
