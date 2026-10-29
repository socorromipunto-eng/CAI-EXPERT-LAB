"""Add Markdown structure to CAI documents written as plain text.

The converter proposes Markdown markup and line-break changes.
verify() checks word-sequence equivalence after removing selected markup.
That check does not establish semantic equivalence, correct rendering or
authorization to adopt a conversion. The CLI reports candidates read-only;
review the diff and rendered output under the document family's change rules.
"""
import re, sys, pathlib

KNOWN_HEADINGS = {'Purpose', 'Scope', 'End of Document', 'Status', 'Explicit Non-Claims', 'Non-Claims',
    'Relationship to CAI CORE', 'Relationship to CAI USA Baseline', 'Relationship to CAI ENGINE',
    'Relationship to Other CAI Documents', 'Scope and Non-Scope', 'Sector Scope', 'Sector Assumptions'}

META = re.compile(r'^(Version|Author|Creator|Copyright|All rights reserved|Use, distribution|Date|Status|Classification|Owner)\b', re.I)


def _short_title(s):
    if not s or len(s.split()) > 8 or not s[0].isupper():
        return False
    if s.endswith(('.', ',', ';', ':', '?', '!')) or META.match(s) or re.match(r'^[A-Z][\w /&()-]{0,40}: \S', s):
        return False
    if s.startswith(('-', '*', '#', '|', '>', '```')) or re.fullmatch(r'[A-Z0-9_ →\-–]+', s):
        return False
    return True

def _split_blocks(lines):
    """Insert blank lines (only) so that a title line glued to its text, and a
    list glued to its 'intro:' line, become separate blocks. Words unchanged."""
    out, n, i, fence = [], len(lines), 0, False
    while i < n:
        s = lines[i].strip()
        if s.startswith('```'):
            fence = not fence
            out.append(lines[i]); i += 1; continue
        if fence or not s:
            out.append(lines[i]); i += 1; continue
        k = i
        while k < n and lines[k].strip() and not lines[k].strip().startswith('```'):
            k += 1
        blk = lines[i:k]
        prev_blank = (i == 0) or not lines[i-1].strip()
        numh = lambda x: re.match(r'^\d+(\.\d+)*\.?\s+[A-Z]', x) and len(x.split()) <= 12 and not x.endswith(('.', ':', ';', ','))
        if sum(1 for b in blk if numh(b.strip())) >= 2 and all(numh(b.strip()) or len(b.split()) <= 8 for b in blk):
            for b in blk:                         # outline block: numbered titles with short entries under them
                if numh(b.strip()):
                    out.extend(['', b, ''])
                else:
                    out.append('- ' + b.strip())
            out.append('')
            i = k; continue
        if prev_blank and len(blk) >= 2 and _short_title(blk[0].strip()) and \
           (len(blk[1].split()) > 6 or blk[1].strip().endswith(':')):
            out.append(blk[0]); out.append(''); blk = blk[1:]
        j = 0
        while j < len(blk):
            b = blk[j].strip()
            items = blk[j+1:]
            if b.endswith(':') and items and all(len(x.split()) <= 16 and not x.strip().startswith(('-', '*', '|', '#')) for x in items):
                out.append(blk[j]); out.append('')
                out.extend(items); out.append('') if k < n and lines[k].strip() else None
                j = len(blk); break
            out.append(blk[j]); j += 1
        i = k
    return out

def _item(line):
    t = line.strip()
    if t[:1] in '•·▪◦–':                      # the source already shows a bullet character: keep it, break the line
        return t + '  '
    return '- ' + t

def is_heading(line, prev, nxt):
    s = line.strip()
    if not s or prev.strip() or nxt.strip():          # must stand alone between blank lines
        return False
    if s.endswith(('.', ',', ';', ':', '?', '!')) or s.endswith('.md'):
        return False
    if META.match(s) or s.startswith(('-', '*', '#', '|', '>', '```')):
        return False
    if re.match(r'^[A-Z][\w /&()-]{0,40}: \S', s):          # "Key: value" metadata
        return False
    words = s.split()
    if len(words) > 12 or not (s[0].isupper() or s[0].isdigit()):
        return False
    if re.fullmatch(r'[A-Z0-9_ →\-–]+', s) and len(words) > 1:   # state chains like MODEL → HARDEN
        return False
    return True

def heading_level(s):
    m = re.match(r'^(\d+(?:\.\d+)*)\.?\s', s)
    if m:
        return min(2 + m.group(1).count('.'), 4)
    return 2

def convert(text):
    lines = text.split('\n')
    if any(re.match(r'^#{1,6} ', l) for l in lines):
        return text                                  # already structured: untouched
    lines = _split_blocks(lines)
    out, n = [], len(lines)
    # title: first non-blank line that is not a file name
    first = next((i for i, l in enumerate(lines) if l.strip() and not l.strip().endswith('.md')), None)
    fname = next((i for i, l in enumerate(lines) if l.strip()), None)
    if first is not None and re.match(r'^\d+(\.\d+)*\.?\s+[A-Z]', lines[first].strip()):
        first = None                                  # document starts with a numbered section: no title line
    if first is not None and fname is not None and fname < first and META.match(lines[first].strip()):
        first = fname                                 # no title line: the file-name line is the title
    in_fence = False
    colon_run = False
    run_items = 0
    last_item_period = False
    i = 0
    while i < n:
        l = lines[i]; s = l.strip()
        if s and i > 0 and lines[i-1].strip() and not lines[i-1].strip().endswith(':'):
            colon_run = False                     # inside a multi-line paragraph
        starts_run = s.endswith(':') and not s.startswith('#')
        if s.startswith('```'):
            in_fence = not in_fence; out.append(l); i += 1; continue
        if in_fence:
            out.append(l); i += 1; continue
        prev = lines[i-1] if i > 0 else ''
        nxt = lines[i+1] if i + 1 < n else ''
        if i == first:
            out.append('# ' + s); i += 1; continue
        if s == 'NOTE' and not prev.strip():
            out.append('**NOTE**  '); i += 1
            while i < n and lines[i].strip():
                out.append(lines[i].rstrip() + '  '); i += 1
            continue
        if META.match(s) or (first is not None and i < first + 12 and s and not prev.strip() == '' and META.match(prev.strip())):
            out.append(l.rstrip() + '  '); i += 1; continue
        # blank-separated list: short single-line paragraphs after a line ending with ':'
        if re.match(r'^\d+(\.\d+)*\.?\s+[A-Z]', s) and len(s.split()) <= 12 and not s.endswith(('.', ':', ';', ',')) \
           and not nxt.strip() and prev.strip() and not prev.strip().endswith(':') and not colon_run:
            out.append('#' * heading_level(s) + ' ' + s); i += 1; continue
        if starts_run:
            colon_run = True; run_items = 0; last_item_period = False
            out.append(l); i += 1; continue
        if s and not prev.strip() and not nxt.strip() and colon_run:
            numbered = re.match(r'^\d+(\.\d+)*\.?\s', s)
            period_breaks = s.endswith('.') and run_items > 0 and not last_item_period
            q = i + 1
            while q < n and not lines[q].strip():
                q += 1
            nxt_nb = lines[q].strip() if q < n else ''
            if nxt_nb.endswith(':') or len(nxt_nb.split()) > 16:
                period_breaks = True                 # a title introducing new text, not a list item
            if not numbered and s not in KNOWN_HEADINGS and len(s.split()) <= 14 \
               and not (s.endswith('.') and len(s.split()) > 12) and not period_breaks:
                out.append(_item(s)); run_items += 1; last_item_period = s.endswith('.'); i += 1; continue
            colon_run = False
        if is_heading(l, prev, nxt):
            out.append('#' * heading_level(s) + ' ' + s); i += 1; continue
        # list block: consecutive non-blank lines after a line ending with ':' (or after blank following it)
        if s and not prev.strip():
            j = i - 2
            while j >= 0 and not lines[j].strip():
                j -= 1
            intro = lines[j].strip() if j >= 0 else ''
            k = i
            while k < n and lines[k].strip():
                k += 1
            block = lines[i:k]
            if intro.endswith(':') and (len(block) >= 2 or len(block[0].split()) <= 12) \
               and not any(b.strip().startswith(('-', '*', '|', '#', '```')) for b in block):
                tail = None
                lastb = block[-1].strip()
                if len(block) > 1 and re.match(r'^\d+(\.\d+)*\.?\s+[A-Z]', lastb) and len(lastb.split()) <= 12 \
                   and not lastb.endswith(('.', ':', ';', ',')):
                    tail = lastb; block = block[:-1]          # a numbered section title closes the list
                for b in block:
                    out.append(_item(b))
                run_items += len(block); last_item_period = block[-1].strip().endswith('.')
                if tail:
                    out.append(''); out.append('#' * heading_level(tail) + ' ' + tail); colon_run = False
                i = k; continue
        if s and not prev.strip() and nxt.strip():
            k = i
            while k < n and lines[k].strip():
                k += 1
            blk = [b.strip() for b in lines[i:k]]
            numh = lambda b: re.match(r'^\d+(\.\d+)*\.?\s+[A-Z]', b) and len(b.split()) <= 12 and not b.endswith(('.', ':', ';', ','))
            if numh(blk[0]) and not colon_run and not all(numh(b) for b in blk):
                out.append('#' * heading_level(blk[0]) + ' ' + blk[0]); i += 1; continue
            if all(numh(b) for b in blk):
                for idx, b in enumerate(blk):
                    if idx: out.append('')
                    out.append('#' * heading_level(b) + ' ' + b)
                i = k; continue
            k = i
            while k < n and lines[k].strip():
                k += 1
            block = lines[i:k]
            if not any(b.strip().startswith(('-', '*', '|', '#', '```', '>')) for b in block) and \
               all(b.rstrip().endswith(('.', ':', ';', '!', '?', ')')) or ((nb.strip()[:1].isupper() or nb.strip()[:1].isdigit()) and len(b.strip()) < 66)
                   for b, nb in zip(block, block[1:])):
                for b in block[:-1]:
                    out.append(b.rstrip() + '  ')
                out.append(block[-1])
                i = k; continue
        out.append(l); i += 1
    return '\n'.join(out)

def words(text):
    t = re.sub(r'^\s*#{1,6} ', '', text, flags=re.M)
    t = re.sub(r'^\s*- ', '', t, flags=re.M)
    t = t.replace('**NOTE**', 'NOTE')
    t = re.sub(r'^```[a-z]*\s*$', '', t, flags=re.M)
    return t.split()

def verify(src, dst):
    return words(src) == words(dst)

if __name__ == '__main__':
    for p in sys.argv[1:]:
        src = pathlib.Path(p).read_text(encoding='utf-8')
        dst = convert(src)
        ok = verify(src, dst)
        print(('OK   ' if ok else 'FAIL ') + p, sum(1 for l in dst.split('\n') if re.match(r'^#{1,6} ', l)), 'headings')
