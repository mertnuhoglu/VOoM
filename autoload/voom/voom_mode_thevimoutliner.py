# voom_mode_thevimoutliner.py
# Last Modified: 2013-10-31
# VOoM -- Vim two-pane outliner, plugin for Python-enabled Vim 7.x
# Website: http://www.vim.org/scripts/script.php?script_id=2657
# Author: Vlad Irnov (vlad DOT irnov AT gmail DOT com)
# License: CC0, see http://creativecommons.org/publicdomain/zero/1.0/

"""
VOoM markup mode for The Vim Outliner format.
See |voom-mode-thevimoutliner|,  ../../doc/voom.txt#*voom-mode-thevimoutliner*

Headlines and body lines are indented with Tabs. Number of tabs indicates
level. 0 Tabs means level 1.

Headlines are lines with >=0 Tabs followed by any character except '|'.

Blank lines are not headlines.
"""

# Body lines start with these chars
BODY_CHARS = {'|':0,}

# ------ the rest is identical to voom_mode_vimoutliner.py -------------------
def hook_makeOutline(VO, blines):
    """Return (tlines, bnodes, levels) for Body lines blines.
    blines is either Vim buffer object (Body) or list of buffer lines.
    """
    Z = len(blines)
    tlines, bnodes, levels = [], [], []
    tlines_add, bnodes_add, levels_add = tlines.append, bnodes.append, levels.append
    for i in range(Z):
        bline = blines[i].rstrip()
        if not bline:
            continue
        head = bline.lstrip('\t')
        if head[0] in BODY_CHARS:
            continue
        lev = len(bline) - len(head) + 1

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
    bodyLines = ['%s%s' %('\t'*(level-1), tree_head),]
    return (tree_head, bodyLines)


#def hook_changeLevBodyHead(VO, h, levDelta):
    #"""Increase of decrease level number of Body headline by levDelta."""
    #if levDelta==0: return h

def hook_doBodyAfterOop(VO, oop, levDelta, blnum1, tlnum1, blnum2, tlnum2, blnumCut, tlnumCut):
    # this is instead of hook_changeLevBodyHead()
    if not levDelta: return

    indent = abs(levDelta) * '\t'

    Body = VO.Body
    Z = len(Body)

    # ---- identical to voom_mode_python.py code ----------------------------
    if blnum1:
        assert blnum1 == VO.bnodes[tlnum1-1]
        if tlnum2 < len(VO.bnodes):
            assert blnum2 == VO.bnodes[tlnum2]-1
        else:
            assert blnum2 == Z

    # dedent (if possible) or indent every non-blank line in Body region blnum1,blnum2
    blines = []
    for i in range(blnum1-1,blnum2):
        line = Body[i]
        if not line.strip():
            blines.append(line)
            continue
        if levDelta > 0:
            line = '%s%s' %(indent,line)
        elif levDelta < 0 and line.startswith(indent):
            line = line[len(indent):]
        blines.append(line)

    # replace Body region
    Body[blnum1-1:blnum2] = blines
    assert len(Body)==Z
