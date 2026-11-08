"""Add the reviewed OINK table-reading classes to imported Markdown tables.

Only visible cells determine width. Code fences, raw HTML and .fields tables
retain their original bytes; existing table attributes are extended in place.
"""

import html
import re
import unicodedata

def cells(line):
    parts = re.split(r'(?<!\\)\|', line.strip())
    if parts and parts[0] == '':
        parts.pop(0)
    if parts and parts[-1] == '':
        parts.pop()
    return [p.strip() for p in parts]


def visible(cell):
    text = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', cell)
    text = re.sub(r'<[^>]*>', '', text)
    return html.unescape(text).replace('`', '').replace('**', '')


def width(text):
    return sum(2 if unicodedata.east_asian_width(c) in 'WF' else 1 for c in text)


def large_reason(rows, attr):
    n = len(rows[0])
    if re.search(r'(?<!\w)\.wide\b', attr) or re.search(r'class\s*=\s*[\"\'][^\"\']*\bwide\b', attr):
        return 'existing-wide'
    if n >= 5:
        return 'five-or-more-columns'
    if len(rows) - 1 >= 10:
        return 'ten-or-more-data-rows'
    if n >= 3:
        shown = [[visible(c) for c in row] for row in rows]
        if any(len(token) >= 24 for row in shown for c in row
               for token in re.findall(r'[A-Za-z0-9_./:@+\-]+', c)):
            return 'long-technical-token'
        maxima = [max(width(row[i]) for row in shown if len(row) > i) for i in range(n)]
        if sum(maxima) >= 100 or max(maxima) >= 70:
            return 'wide-cells'
    return ''


def tables(text):
    lines = text.splitlines(keepends=True)
    blocked = set()
    fm = lines[0].strip() if lines and lines[0].strip() in ('---', '+++') else None
    fence = None
    raw = None
    for i, line in enumerate(lines):
        if fm:
            blocked.add(i)
            if i and line.strip() == fm:
                fm = None
            continue
        match = re.match(r'^\s*(?:>\s*)*(`{3,}|~{3,})', line)
        if match:
            blocked.add(i)
            mark = match[1]
            if fence is None:
                fence = mark
            elif mark[0] == fence[0] and len(mark) >= len(fence):
                fence = None
            continue
        if fence:
            blocked.add(i)
            continue
        if raw:
            blocked.add(i)
            if raw in line:
                raw = None
            continue
        for start, end in [('<!--', '-->'), ('<pre', '</pre>'), ('<script', '</script>'), ('<style', '</style>'), ('<table', '</table>')]:
            if start in line:
                blocked.add(i)
                if end not in line:
                    raw = end
                break
    result = []
    i = 0
    while i + 1 < len(lines):
        if i in blocked or i+1 in blocked or '|' not in lines[i] or lines[i].startswith(('>', '    ', '\t')):
            i += 1
            continue
        header = cells(lines[i])
        sep = cells(lines[i+1])
        if len(header) < 2 or len(header) != len(sep) or not all(re.fullmatch(r':?-+:?', c) for c in sep):
            i += 1
            continue
        j = i+2
        rows = [header]
        while j < len(lines) and j not in blocked and '|' in lines[j] and not lines[j].lstrip().startswith(('{', '>')):
            rows.append(cells(lines[j]))
            j += 1
        attr = lines[j].strip() if j < len(lines) and re.fullmatch(r'\{[^\n]*\}\s*', lines[j]) else ''
        fields = bool(re.search(r'(?<!\w)\.fields\b', attr) or re.search(r'class\s*=\s*[\"\'][^\"\']*\bfields\b', attr))
        reason = large_reason(rows, attr)
        result.append({'line': i+1, 'end': j, 'columns': len(header), 'data_rows': len(rows)-1,
                       'attributes': attr, 'fields': fields, 'reason': reason, 'header': header,
                       'sample': rows[1:3]})
        i = max(j, i+2)
    return result


def add_table_reading(text):
    lines = text.splitlines(keepends=True)
    count = 0
    for t in reversed(tables(text)):
        if not t['reason'] or t['fields']:
            continue
        attr = t['attributes']
        missing = [c for c in ('wide','expand') if not re.search(r'(?<!\w)\.'+c+r'\b', attr)
                   and not re.search(r'class\s*=\s*[\"\'][^\"\']*\b'+c+r'\b',attr)]
        if not missing:
            continue
        j = t['end']
        ending = '\r\n' if any(l.endswith('\r\n') for l in lines[:3]) else '\n'
        if attr:
            original = lines[j]
            close = original.rfind('}')
            lines[j] = original[:close]+' '+ ' '.join('.'+c for c in missing)+original[close:]
        else:
            if not lines[j-1].endswith(('\n','\r')):
                lines[j-1] += ending
            lines.insert(j, '{'+ ' '.join('.'+c for c in missing)+'}'+ending)
        count += 1
    return ''.join(lines), count
