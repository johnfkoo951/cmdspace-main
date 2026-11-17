#!/usr/bin/env python3
"""Render the audience-based program catalog from the vault master.

One source (vault `programs-by-audience.md`) feeds five public surfaces:
  1. data/programs.json                  public fields only (offline rebuild source)
  2. index.html                          block between <!-- COURSES:BEGIN --> and <!-- COURSES:END -->
  3. docs/cmdspace-course-proposal.md    block between <!-- PROGRAMS:BEGIN --> and <!-- PROGRAMS:END -->
  4. llms.txt                            the "## 대상별 교육·코칭·컨설팅 과정" section
  5. docs/cmdspace-brochure.md,
     docs/yohan-ax-portfolio.md          at-a-glance table between <!-- AUDIENCE-OVERVIEW:BEGIN --> and END

  python3 scripts/sync-programs.py            parse the vault master, validate, write all four
  python3 scripts/sync-programs.py --check    validate only, write nothing
  python3 scripts/sync-programs.py --data     rebuild surfaces 2-5 from the checked-in data/programs.json

`- 내부근거:` lines in the master are never read into any output.
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MASTER = (Path.home() / 'Local Obsidian_MBP/CMDSPACE_Local_MBP/70. Outputs/74. Projects'
                  / 'cmdspace-landing/programs-by-audience.md')
DATA_JSON = ROOT / 'data/programs.json'
INDEX_HTML = ROOT / 'index.html'
PROPOSAL_MD = ROOT / 'docs/cmdspace-course-proposal.md'
LLMS_TXT = ROOT / 'llms.txt'
OVERVIEW_DOCS = [ROOT / 'docs/cmdspace-brochure.md', ROOT / 'docs/yohan-ax-portfolio.md']

DEPTHS = {'범용': 'general', '핵심': 'core', '특화': 'special'}
DEPTH_ORDER = ['범용', '핵심', '특화']
LLMS_HEADING = '## 대상별 교육·코칭·컨설팅 과정'
FIELD_KEYS = {'깊이': 'depth', '유형': 'kind', '형식': 'format', '다루는 것': 'covers',
              '산출물': 'outputs', '근거': 'evidence', '링크': 'link'}
LIST_FIELDS = {'covers', 'outputs'}
REQUIRED = ['title', 'summary', 'depth', 'kind', 'format', 'covers', 'outputs', 'evidence']


def fail(msg):
    sys.exit('❌ ' + msg)


def strip_frontmatter(text):
    lines = text.split('\n')
    if lines and lines[0].strip() == '---':
        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                return lines[i + 1:]
    return lines


def parse_master(text):
    audiences, programs = [], []
    mode, cur, body = None, None, []

    def flush():
        nonlocal cur, body
        if cur is None:
            return
        paragraph = []
        for ln in body:
            s = ln.strip()
            m = re.match(r'^-\s+([^:]+?):\s*(.*)$', s)
            if m:
                label, value = m.group(1).strip(), m.group(2).strip()
                if mode == 'audiences' and label == '순서':
                    cur['order'] = [p.strip() for p in value.split(',') if p.strip()]
                elif mode == 'audiences' and label == '질문':
                    cur['question'] = value
                elif mode == 'programs' and label in FIELD_KEYS:
                    key = FIELD_KEYS[label]
                    cur[key] = [v.strip() for v in value.split('|') if v.strip()] if key in LIST_FIELDS else value
                # anything else (내부근거 included) is dropped on purpose
            elif s and not s.startswith('>'):
                paragraph.append(s)
        text_ = ' '.join(paragraph).strip()
        if mode == 'audiences':
            cur['desc'] = text_
            audiences.append(cur)
        else:
            cur['summary'] = text_
            programs.append(cur)
        cur, body = None, []

    for raw in strip_frontmatter(text):
        s = raw.strip()
        if s.startswith('## '):
            flush()
            head = s[3:].lower()
            mode = 'audiences' if 'audiences' in head else 'programs' if 'programs' in head else None
            continue
        if mode is None:
            continue
        if re.match(r'^(-{3,}|\*{3,}|_{3,})$', s):
            continue
        if mode == 'audiences':
            m = re.match(r'^###\s+([a-z]+)\s*·\s*(.+)$', s)
            if m:
                flush()
                cur = {'key': m.group(1), 'label': m.group(2).strip(), 'question': '', 'desc': '', 'order': []}
                continue
        else:
            m = re.match(r'^###\s+(P\d+)\s*·\s*(.+)$', s)
            if m:
                flush()
                full = m.group(2).strip()
                title, _, sub = full.partition(':')
                cur = {'id': m.group(1), 'title': title.strip(), 'subtitle': sub.strip()}
                continue
        if cur is not None:
            body.append(raw)
    flush()
    return {'audiences': audiences, 'programs': programs}


def validate(data):
    auds, progs = data['audiences'], data['programs']
    if not auds or not progs:
        fail('No audiences or programs parsed — check the two level-2 headings in the master')
    ids = [p['id'] for p in progs]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        fail('Duplicate program IDs: ' + ', '.join(sorted(dup)))
    keys = [a['key'] for a in auds]
    if len(set(keys)) != len(keys) or 'all' in keys:
        fail('Audience keys must be unique and must not be "all"')
    for p in progs:
        missing = [k for k in REQUIRED if not p.get(k)]
        if missing:
            fail(f"{p['id']} is missing: {', '.join(missing)}")
        if p['depth'] not in DEPTHS:
            fail(f"{p['id']} depth must be one of {', '.join(DEPTHS)} (got {p['depth']!r})")
        if p.get('link') and not re.fullmatch(r'https://[A-Za-z0-9./_?=&%-]+', p['link']):
            fail(f"{p['id']} link must be a plain https URL")
    placed = set()
    for a in auds:
        if not a['desc'] or not a['order'] or not a.get('question'):
            fail(f"Audience {a['key']} needs a description, a 질문 line and a 순서 line")
        if len(set(a['order'])) != len(a['order']):
            fail(f"Audience {a['key']} lists a program twice")
        unknown = [i for i in a['order'] if i not in ids]
        if unknown:
            fail(f"Audience {a['key']} lists unknown programs: {', '.join(unknown)}")
        placed.update(a['order'])
    orphans = [i for i in ids if i not in placed]
    if orphans:
        fail('Programs not shown under any audience: ' + ', '.join(orphans))


def audiences_of(data, pid):
    return [a for a in data['audiences'] if pid in a['order']]


esc = html.escape


def link_label(url):
    return re.sub(r'^https://', '', url).rstrip('/')


def render_html(data):
    auds, progs = data['audiences'], data['programs']
    first = auds[0]
    t = '\t\t'
    out = [t + '<!-- COURSES:BEGIN — generated by scripts/sync-programs.py from the vault master; do not edit by hand -->',
           t + '<div class="course-filter reveal">',
           t + '\t<div class="course-tabs" id="course-tabs" role="group" aria-label="교육 대상">']
    for i, a in enumerate(auds):
        active = ' active' if i == 0 else ''
        out.append(f'{t}\t\t<button class="course-tab{active}" type="button" data-for="{a["key"]}" '
                   f'aria-pressed="{"true" if i == 0 else "false"}">{esc(a["label"])}<span class="n">{len(a["order"])}</span></button>')
    out.append(f'{t}\t\t<button class="course-tab" type="button" data-for="all" aria-pressed="false">전체<span class="n">{len(progs)}</span></button>')
    out += [t + '\t</div>',
            t + '\t<div class="course-depths" id="course-depths" role="group" aria-label="주제 깊이">',
            t + '\t\t<span class="course-depths-label">주제 깊이</span>',
            t + '\t\t<button class="chip course-depth active" type="button" data-depth="all" aria-pressed="true">전체</button>']
    for label in DEPTH_ORDER:
        out.append(f'{t}\t\t<button class="chip course-depth" type="button" data-depth="{DEPTHS[label]}" aria-pressed="false">{label}</button>')
    out += [t + '\t</div>',
            t + '</div>',
            f'{t}<p class="course-desc reveal" aria-live="polite"><strong class="course-q" id="course-q">{esc(first["question"])}</strong>'
            f'<span id="course-desc">{esc(first["desc"])}</span></p>',
            # no .reveal on the grid: with every card shown it is taller than 12 viewports on a phone,
            # so the page's reveal observer (threshold 8% of the element) could never fire and the grid would stay invisible
            t + '<div class="course-grid" id="course-grid">']
    for p in progs:
        mine = audiences_of(data, p['id'])
        sub = f'<span class="course-sub">{esc(p["subtitle"])}</span>' if p.get('subtitle') else ''
        covers = ''.join(f'<li>{esc(c)}</li>' for c in p['covers'])
        link = (f'<a class="course-link" href="{esc(p["link"])}" target="_blank" rel="noopener">{esc(link_label(p["link"]))}</a>'
                if p.get('link') else '')
        out += [
            f'{t}\t<article class="course-card reveal" id="course-{p["id"].lower()}" data-id="{p["id"]}" data-depth="{DEPTHS[p["depth"]]}">',
            f'{t}\t\t<div class="course-meta"><span class="course-badge" data-depth="{DEPTHS[p["depth"]]}">{p["depth"]}</span>'
            f'<span class="course-kind">{esc(p["kind"])}</span><span class="course-format">{esc(p["format"])}</span></div>',
            f'{t}\t\t<h3>{esc(p["title"])}{sub}</h3>',
            f'{t}\t\t<p class="course-summary">{esc(p["summary"])}</p>',
            f'{t}\t\t<ul class="course-covers">{covers}</ul>',
            f'{t}\t\t<dl class="course-facts"><div><dt>산출물</dt><dd>{esc(", ".join(p["outputs"]))}</dd></div>'
            f'<div><dt>근거</dt><dd>{esc(p["evidence"])}</dd></div></dl>',
            f'{t}\t\t<div class="course-foot"><span class="course-for">대상: {esc(", ".join(a["label"] for a in mine))}</span>{link}</div>',
            f'{t}\t</article>']
    payload = {'audiences': [{'key': a['key'], 'label': a['label'], 'question': a['question'], 'desc': a['desc'],
                              'order': a['order']} for a in auds]}
    out += [t + '</div>',
            t + '<p class="course-empty" id="course-empty" hidden>이 조합에 해당하는 과정이 없습니다. 주제 깊이를 전체로 바꿔 보세요.</p>',
            t + '<script type="application/json" id="course-data">'
            + json.dumps(payload, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + '</script>',
            t + '<!-- COURSES:END -->']
    return '\n'.join(out)


def cell(s):
    return s.replace('|', '/').strip()


def overview_rows(data):
    by_id = {p['id']: p for p in data['programs']}
    rows = ['| 대상 | 이 질문에서 시작합니다 | 대표 과정 |', '|------|------------------------|-----------|']
    for a in data['audiences']:
        top = ', '.join(by_id[pid]['title'] for pid in a['order'][:3])
        rows.append(f'| {cell(a["label"])} | {cell(a["question"])} | {cell(top)} |')
    return rows


def render_overview(data):
    return '\n'.join(['<!-- AUDIENCE-OVERVIEW:BEGIN — generated by scripts/sync-programs.py; do not edit by hand -->', '']
                     + overview_rows(data) + ['', '<!-- AUDIENCE-OVERVIEW:END -->'])


def render_proposal(data):
    # Layout rule for md-to-pdf (report theme): a table never splits from the heading right above it,
    # but a paragraph between them lets the heading strand at the bottom of a page — so tables come first,
    # notes after. Audience sections are H3 so the PDF table of contents (H2 only) stays on one page.
    by_id = {p['id']: p for p in data['programs']}
    out = ['<!-- PROGRAMS:BEGIN — generated by scripts/sync-programs.py from the vault master; do not edit by hand -->', '',
           '## 대상별 과정 한눈에 보기', '']
    out += overview_rows(data)
    out += ['', f'교육을 받는 주체를 {len(data["audiences"])}가지로 나누고 과정 {len(data["programs"])}개를 배치했습니다. '
            '한 과정이 여러 대상에 걸칠 수 있습니다.', '',
            '## 주제 깊이로 보기', '',
            '| 깊이 | 과정 |', '|------|------|']
    for d in reversed(DEPTH_ORDER):
        out.append(f'| {d} | {cell(", ".join(p["title"] for p in data["programs"] if p["depth"] == d))} |')
    out += ['', '범용은 누구나 들을 수 있는 주제, 핵심은 주력 과정, 특화는 구축과 자문을 포함한 뾰족한 주제입니다.', '',
            '## 대상별 과정', '']
    for a in data['audiences']:
        # md-to-pdf escapes inline HTML, so cells stay plain Markdown (no <br>)
        out += [f'### {a["label"]}: {a["question"]}', '',
                '| 과정 | 구분과 형식 | 다루는 것 | 산출물 |', '|------|-------------|-----------|--------|']
        for pid in a['order']:
            p = by_id[pid]
            name = f'**{p["title"]}**' + (f': {p["subtitle"]}' if p.get('subtitle') else '')
            kind = f'{p["depth"]}, {p["kind"]}. {p["format"]}'
            out.append(f'| {cell(name)} | {cell(kind)} | {cell(", ".join(p["covers"]))} | {cell(", ".join(p["outputs"]))} |')
        out += ['', a['desc'], '']
    out += ['## 과정별 수행 근거', '',
            '| 과정 | 깊이 | 수행 근거 |', '|------|------|-----------|']
    for p in data['programs']:
        out.append(f'| {cell(p["title"])} | {p["depth"]} | {cell(p["evidence"])} |')
    out += ['', '근거는 직접 수행했거나 직접 운영하는 범위만 적었습니다. 기업 경영진과 임원 과정은 고객명을 쓰지 않고 규모와 업종만 적습니다.',
            '', '<!-- PROGRAMS:END -->']
    return '\n'.join(out)


def render_llms(data):
    by_id = {p['id']: p for p in data['programs']}
    out = [LLMS_HEADING, '',
           f'교육을 받는 주체별로 들을 수 있는 과정을 정리했습니다(과정 {len(data["programs"])}개). '
           '사이트에서는 https://cmdspace.work/?for=<대상 키>#courses 로 해당 탭을 바로 엽니다. 가격은 범위 확인 뒤 견적합니다.', '']
    for a in data['audiences']:
        out.append(f'### {a["label"]} (`for={a["key"]}`)')
        out.append('')
        out.append(f'{a["question"]}? {a["desc"]}')
        out.append('')
        for pid in a['order']:
            p = by_id[pid]
            title = p['title'] + (f': {p["subtitle"]}' if p.get('subtitle') else '')
            out.append(f'- {title} [{p["depth"]}, {p["kind"]}, {p["format"]}]: {p["summary"]}')
        out.append('')
    return '\n'.join(out)


def replace_between(text, begin_re, end_re, block, what):
    m = re.search(begin_re + r'.*?' + end_re, text, re.S)
    if not m:
        fail(f'Markers for {what} not found')
    return text[:m.start()] + block + text[m.end():]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--master', type=Path, default=DEFAULT_MASTER)
    ap.add_argument('--data', action='store_true', help='rebuild from data/programs.json instead of the vault master')
    ap.add_argument('--check', action='store_true', help='validate only')
    args = ap.parse_args()

    if args.data:
        data = json.loads(DATA_JSON.read_text(encoding='utf-8'))
    else:
        if not args.master.exists():
            fail(f'Vault master not found: {args.master}')
        data = parse_master(args.master.read_text(encoding='utf-8'))
    validate(data)
    counts = {d: sum(p['depth'] == d for p in data['programs']) for d in DEPTH_ORDER}
    print(f'📊 {len(data["audiences"])} audiences, {len(data["programs"])} programs '
          f'({", ".join(f"{k} {v}" for k, v in counts.items())})')
    for a in data['audiences']:
        print(f'   {a["key"]:<9}{len(a["order"])}  {a["label"]}')
    if args.check:
        print('✅ Check passed. Nothing written.')
        return

    if not args.data:
        DATA_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'📥 {DATA_JSON.relative_to(ROOT)}')

    page = INDEX_HTML.read_text(encoding='utf-8')
    page = replace_between(page, r'[ \t]*<!-- COURSES:BEGIN', r'<!-- COURSES:END -->', render_html(data), 'index.html')
    INDEX_HTML.write_text(page, encoding='utf-8')
    print('✅ index.html (#courses)')

    if PROPOSAL_MD.exists():
        doc = PROPOSAL_MD.read_text(encoding='utf-8')
        doc = replace_between(doc, r'<!-- PROGRAMS:BEGIN', r'<!-- PROGRAMS:END -->', render_proposal(data), 'the course proposal')
        PROPOSAL_MD.write_text(doc, encoding='utf-8')
        print(f'✅ {PROPOSAL_MD.relative_to(ROOT)}')
    else:
        print(f'ℹ️  {PROPOSAL_MD.relative_to(ROOT)} not found — skipped')

    for doc_path in OVERVIEW_DOCS:
        if doc_path.exists() and 'AUDIENCE-OVERVIEW:BEGIN' in doc_path.read_text(encoding='utf-8'):
            doc = replace_between(doc_path.read_text(encoding='utf-8'), r'<!-- AUDIENCE-OVERVIEW:BEGIN',
                                  r'<!-- AUDIENCE-OVERVIEW:END -->', render_overview(data), doc_path.name)
            doc_path.write_text(doc, encoding='utf-8')
            print(f'✅ {doc_path.relative_to(ROOT)}')

    llms = LLMS_TXT.read_text(encoding='utf-8')
    block = render_llms(data)
    pattern = re.escape(LLMS_HEADING) + r'\n.*?(?=\n## )'
    if re.search(pattern, llms, re.S):
        llms = re.sub(pattern, lambda _: block.rstrip('\n') + '\n', llms, count=1, flags=re.S)
    else:
        anchor = '\n## 주요 페이지'
        if anchor not in llms:
            fail('llms.txt: neither the program section nor the "## 주요 페이지" anchor was found')
        llms = llms.replace(anchor, '\n' + block.rstrip('\n') + '\n' + anchor, 1)
    LLMS_TXT.write_text(llms, encoding='utf-8')
    print('✅ llms.txt')
    print('\nNext: ./scripts/build-pdf.sh (proposal PDF) → ./deploy.sh')


if __name__ == '__main__':
    main()
