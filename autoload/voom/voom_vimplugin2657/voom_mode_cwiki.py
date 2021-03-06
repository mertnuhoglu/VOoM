# File: voom_mode_cwiki.py
# Last Modified: 2017-01-07
# Description: VOoM -- two-pane outliner plugin for Python-enabled Vim
# Website: http://www.vim.org/scripts/script.php?script_id=2657
# Author: Vlad Irnov (vlad DOT irnov AT gmail DOT com)
# License: CC0, see http://creativecommons.org/publicdomain/zero/1.0/

"""
VOoM markup mode for cwiki Vim plugin. Contributed by Craig B. Allen.
http://www.vim.org/scripts/script.php?script_id=2176
See |voom-mode-various|,  ../../../doc/voom.txt#*voom-mode-various*

+++ headline level 1
some text
++++ headline level 2
more text
+++++ headline level 3
++++++ headline level 4
etc.

First + must be at start of line. Whitespace after the last + is optional.
"""

import sys
if sys.version_info[0] > 2:
    xrange = range

import re
headline_match = re.compile(r'^\+\+(\++)').match


def hook_makeOutline(VO, blines):
    """Return (tlines, bnodes, levels) for Body lines blines.
    blines is either Vim buffer object (Body) or list of buffer lines.
    """
    Z = len(blines)
    tlines, bnodes, levels = [], [], []
    tlines_add, bnodes_add, levels_add = tlines.append, bnodes.append, levels.append
    for i in xrange(Z):
        if not blines[i].startswith('+'):
            continue
        bline = blines[i]
        m = headline_match(bline)
        if not m:
            continue
        lev = len(m.group(1))
        head = bline[2+lev:].strip()
        tline = '  %s|%s' %('. '*(lev-1), head)
        tlines_add(tline)
        bnodes_add(i+1)
        levels_add(lev)
    return (tlines, bnodes, levels)


def hook_newHeadline(VO, level, blnum, tlnum):
    """Return (tree_head, bodyLines).
    tree_head is new headline string in Tree buffer (text after |).
    bodyLines is list of lines to insert in Body buffer.
    """
    tree_head = 'NewHeadline'
    bodyLines = ['++%s %s' %('+'*level, tree_head), '']
    return (tree_head, bodyLines)


def hook_changeLevBodyHead(VO, h, levDelta):
    """Increase of decrease level number of Body headline by levDelta."""
    if levDelta==0: return h
    m = headline_match(h)
    level = len(m.group(1))
    return '++%s%s' %('+'*(level+levDelta), h[m.end(1):])


