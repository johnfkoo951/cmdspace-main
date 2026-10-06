#!/usr/bin/env python3
"""Render the reviewed public hub from the vault master (or --data for offline rebuilds)."""
import argparse
import html
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MASTER = Path.home() / 'Local Obsidian_MBP/CMDSPACE_Local_MBP/70. Outputs/74. Projects/cmdspace-landing/hub-links.md'
EXCLUDED = {'lg', 'lge', 'ax', 'test', 'labs', 'akm-study', 'files', 'course'}
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--master', type=Path, default=DEFAULT_MASTER)
parser.add_argument('--data', action='store_true', help='Rebuild from the checked-in public JSON')
args = parser.parse_args()
if args.data:
    data = json.loads((ROOT / 'data/hub-links.json').read_text())
else:
    match = re.search(r'```json\s*\n(.*?)\n```', args.master.read_text(), re.S)
    if not match:
        raise SystemExit('No JSON block in the vault master')
    data = json.loads(match.group(1))

seen = set()
for group in data['groups']:
    if not re.fullmatch(r'[a-z-]+', group['id']):
        raise SystemExit('Invalid group ID')
    for link in group['links']:
        host = link['host']
        if not re.fullmatch(r'[a-z0-9-]+\.cmdspace\.work', host) or host.split('.')[0] in EXCLUDED or host in seen:
            raise SystemExit('Excluded, duplicate, or invalid public host: ' + host)
        seen.add(host)
esc = html.escape
lines = ['<!-- HUB -->', '<section id="hub" style="border-bottom: none;">', '\t<div class="wrap">',
         '\t\t<div class="section-head reveal">', '\t\t\t<div class="kicker">Ecosystem</div>',
         '\t\t\t<h2><span class="cmd accent-word">cmdspace.work</span> 서비스 허브</h2>',
         '\t\t\t<p>처음이라면 Brain에서 시작하고, 도구는 Apps에서 찾아보세요. 공개 자료를 용도별로 정리했습니다.</p>',
         '\t\t\t<p>공개 링크 ' + str(len(seen)) + '개 · 확인 ' + esc(data['checkedAt']) + ' · 고객 전용·내부 자료 제외</p>',
         '\t\t</div>', '\t\t<nav class="hub-nav" aria-label="서비스 허브 분류">']
for group in data['groups']:
    lines.append('\t\t\t<a class="chip" href="#hub-' + group['id'] + '">' + esc(group['title'].split(' · ')[-1]) + '</a>')
lines.append('\t\t</nav>')
for group in data['groups']:
    lines += ['\t\t<div class="hub-group reveal" id="hub-' + group['id'] + '">', '\t\t\t<h3>' + esc(group['title']) + '</h3>', '\t\t\t<div class="hub-grid">']
    for link in group['links']:
        lines += ['\t\t\t\t<a class="hub-card" href="https://' + esc(link['host']) + '" target="_blank" rel="noopener">',
                  '\t\t\t\t\t<div class="domain">' + esc(link['host']) + '</div>',
                  '\t\t\t\t\t<h4>' + esc(link['title']) + '</h4>',
                  '\t\t\t\t\t<p class="hub-desc">' + esc(link['description']) + '</p>', '\t\t\t\t\t<div class="hub-tags">']
        lines += ['\t\t\t\t\t\t<span class="hub-tag">' + esc(tag) + '</span>' for tag in link['tags']]
        lines += ['\t\t\t\t\t</div>', '\t\t\t\t</a>']
    lines += ['\t\t\t</div>', '\t\t</div>']
lines += ['\t</div>', '</section>']
page = ROOT / 'index.html'
source = page.read_text()
start = source.index('<!-- HUB -->')
end = source.index('</section>', start) + len('</section>')
page.write_text(source[:start] + '\n'.join(lines) + source[end:])
(ROOT / 'data/hub-links.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
search_file = ROOT / 'llms.txt'
search = search_file.read_text()
start = search.index('## 주요 페이지')
end = search.index('## 표기', start)
section = '## 주요 페이지\n\n- [CMDSPACE 랜딩](https://cmdspace.work): 서비스·활동 이력·공개 서비스 허브\n\n'
section += '\n\n'.join('### ' + group['title'] + '\n\n' + '\n'.join(
    '- [' + link['title'] + '](https://' + link['host'] + '): ' + link['description']
    for link in group['links']) for group in data['groups'])
search_file.write_text(search[:start] + section + '\n\n' + search[end:])
print(f'Rendered {len(seen)} reviewed links in {len(data["groups"])} groups')
