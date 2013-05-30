#!/usr/bin/env pythonw
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

__version__ = "$Id: hitaext.py 1295 2010-04-15 03:38:31Z emarsi $"
__author__ = "Erwin Marsi"

from htxt.gui import Hitaext
from daeso.utils.cli import DaesoArgParser


description = """
Hitaext: hierarchical text aligment tool
"""

parser = DaesoArgParser(description=description.strip(), version=__version__)

parser.add_argument(
    "corpus_file",
    metavar="FILE",
    nargs="?", 
    help="parallel text corpus file")

parser.add_argument(
    "-r", "--redirect",
    action='store_true',
    help="redirect output written to stdout and stderr streams "
    "to a pop-up window")

args = parser.parse_args()

app = Hitaext(cl_args=args, redirect=args.redirect)
app.MainLoop() 

