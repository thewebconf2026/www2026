#!/usr/bin/env python3
"""
Generate program/overview.html and program/full-schedule.html
from the Excel Program sheet.
"""
import openpyxl
from datetime import datetime
import html as html_lib
import re

# ─────────────────────────────────────────────
# 1. Parse Excel
# ─────────────────────────────────────────────

wb = openpyxl.load_workbook(
    'program/Detailed WebConf 2026 Program.xlsx', data_only=True
)
ws = wb['Program']

all_rows = [list(row) for row in ws.iter_rows(values_only=True)]

# Find last non-empty row
last_row = 0
for i, row in enumerate(all_rows):
    if any(v is not None for v in row):
        last_row = i

def is_special_event(slot_code):
    """Return True if col B value looks like a single special event."""
    specials = ['break', 'keynote', 'conference opening', 'town hall',
                'plenary', 'posters and demos']
    if slot_code is None:
        return False
    return any(slot_code.lower().startswith(s) for s in specials)

def track_label(code):
    """Convert a track code to a human-readable label."""
    if code is None:
        return ''
    c = str(code).strip()
    mappings = {
        'tut': 'Tutorial', 'wk': 'Workshop',
        'Econ': 'Economics', 'Graph': 'Graph Neural Networks',
        'Search': 'Search & Retrieval', 'Semantics': 'Semantic Web',
        'Social': 'Social Web', 'Systems': 'Web Systems',
        'Security': 'Security & Privacy', 'Mining': 'Data Mining',
        'RecSys': 'Recommender Systems', 'Industry': 'Industry Track',
        'History': 'History of the Web', 'Web4Good': 'Web4Good',
        'RespWeb': 'Responsible Web', 'PhD Symposium': 'PhD Symposium',
        'Web4All': 'Web4All',
        'Demos': 'Demos', 'ShortPapers': 'Short Papers',
        'EconPoster': 'Economics Posters', 'GraphPoster': 'Graph Posters',
        'SearchPoster': 'Search Posters', 'SemanticsPoster': 'Semantics Posters',
        'SecurityPoster': 'Security Posters', 'SocialPoster': 'Social Posters',
        'SystemsPoster': 'Systems Posters', 'RecSysPoster': 'RecSys Posters',
        'MiningPoster': 'Mining Posters', 'IndustryPoster': 'Industry Posters',
        'Web4GoodPoster': 'Web4Good Posters', 'RespWebPoster': 'RespWeb Posters',
        'BestPaper': 'Best Paper Candidates',
    }
    for prefix, label in mappings.items():
        if c.startswith(prefix):
            return label
    return c

def track_color_class(code):
    """Map track code to a CSS class for styling."""
    if code is None:
        return 'track-other'
    c = str(code).strip()
    if c.startswith('tut'):      return 'track-tutorial'
    if c.startswith('wk'):       return 'track-workshop'
    if c.startswith('Econ'):     return 'track-econ'
    if c.startswith('Graph'):    return 'track-graph'
    if c.startswith('Search'):   return 'track-search'
    if c.startswith('Semantic'): return 'track-semantics'
    if c.startswith('Social'):   return 'track-social'
    if c.startswith('System'):   return 'track-systems'
    if c.startswith('Security'): return 'track-security'
    if c.startswith('Mining'):   return 'track-mining'
    if c.startswith('RecSys'):   return 'track-recsys'
    if c.startswith('Industry'): return 'track-industry'
    if c.startswith('History'):  return 'track-history'
    if c.startswith('Web4Good'): return 'track-web4good'
    if c.startswith('RespWeb'):  return 'track-respweb'
    if c.startswith('PhD'):      return 'track-phd'
    if c.startswith('Web4All'):  return 'track-web4all'
    if c.startswith('Demos'):    return 'track-demos'
    if c.startswith('ShortP'):   return 'track-short'
    if c.startswith('BestP'):    return 'track-best'
    return 'track-other'


# Build program structure
program = []  # list of day dicts
current_day = None
i = 0

while i <= last_row:
    row = all_rows[i]
    col_a = row[0]
    col_b = row[1] if len(row) > 1 else None

    # Skip header rows
    if i < 2:
        i += 1
        continue

    # Day row
    if isinstance(col_a, datetime):
        current_day = {'date': col_a, 'slots': []}
        program.append(current_day)
        i += 1
        continue

    # Time slot row
    if col_a and isinstance(col_a, str) and current_day is not None:
        time_str = col_a.strip()
        
        # Gather session codes (cols B..N)
        codes = []
        for j in range(1, 27):
            val = row[j] if j < len(row) else None
            if val is not None:
                codes.append({'col_idx': j, 'code': str(val).strip()})

        # Is this a special single event?
        only_b = (len(codes) == 1 and codes[0]['col_idx'] == 1)
        special = is_special_event(col_b) if only_b else False

        slot = {
            'time': time_str,
            'special': special,
            'event': col_b if special else None,
            'sessions': [] if not special else None,
            'detail_rows': []
        }

        if not special:
            for c in codes:
                slot['sessions'].append({
                    'col_idx': c['col_idx'],
                    'code': c['code'],
                    'name': None,
                    'papers': [],
                    'url': None,
                })

        current_day['slots'].append(slot)

        # Collect detail rows
        i += 1
        detail_rows = []
        while i <= last_row:
            nr = all_rows[i]
            if nr[0] is not None:
                break
            dr = {}
            for j in range(1, 27):
                v = nr[j] if j < len(nr) else None
                if v is not None:
                    dr[j] = str(v)
            if dr:
                detail_rows.append(dr)
            i += 1

        slot['detail_rows'] = detail_rows

        # ── Interpret detail rows ──────────────────────
        if not special and slot['sessions']:
            sessions_by_col = {s['col_idx']: s for s in slot['sessions']}
            n_detail = len(detail_rows)

            if n_detail == 0:
                pass  # nothing extra

            elif n_detail == 1:
                # Tutorial / Workshop / Poster subcategory with just title line
                dr0 = detail_rows[0]
                for j, text in dr0.items():
                    if j in sessions_by_col:
                        lines = text.split('\n')
                        # First line is the title, rest are authors/url
                        sessions_by_col[j]['name'] = lines[0].strip()
                        rest = '\n'.join(lines[1:]).strip()
                        # Detect URL
                        urls = re.findall(r'https?://\S+', rest)
                        if urls:
                            sessions_by_col[j]['url'] = urls[0]
                        # Authors line
                        non_url = re.sub(r'https?://\S+', '', rest).strip()
                        if non_url:
                            sessions_by_col[j]['papers'].append({
                                'title': lines[0].strip(),
                                'authors': non_url,
                                'acm_url': None
                            })
                        else:
                            sessions_by_col[j]['papers'].append({
                                'title': lines[0].strip(),
                                'authors': '',
                                'acm_url': None
                            })

            elif n_detail >= 2:
                # First detail row: session names (no \n expected)
                dr0 = detail_rows[0]
                for j, text in dr0.items():
                    if j in sessions_by_col:
                        sessions_by_col[j]['name'] = text.strip()

                # Second detail row: papers (title\nauthor blocks separated by \n\n)
                dr1 = detail_rows[1]
                for j, text in dr1.items():
                    if j in sessions_by_col:
                        blocks = re.split(r'\n\s*\n', text.strip())
                        for block in blocks:
                            block = block.strip()
                            if not block:
                                continue
                            blines = block.split('\n')
                            title = blines[0].strip()
                            authors = ' '.join(l.strip() for l in blines[1:] if l.strip())
                            sessions_by_col[j]['papers'].append({
                                'title': title,
                                'authors': authors,
                                'acm_url': None
                            })
        continue

    i += 1


# ─────────────────────────────────────────────
# 2. HTML generation helpers
# ─────────────────────────────────────────────

def esc(s):
    return html_lib.escape(str(s)) if s else ''

DAY_LABELS = {
    'Monday': 'Mon', 'Tuesday': 'Tue', 'Wednesday': 'Wed',
    'Thursday': 'Thu', 'Friday': 'Fri', 'Saturday': 'Sat', 'Sunday': 'Sun'
}

def day_id(day):
    return day['date'].strftime('day-%Y-%m-%d')

def format_day_tab(day):
    d = day['date']
    weekday = d.strftime('%A')
    return f"{weekday}<br><span>{d.strftime('%-d %b')}</span>"

def format_day_heading(day):
    d = day['date']
    return d.strftime('%A, %B %-d, %Y')

SPECIAL_EVENT_CLASS = {
    'break': 'slot-break',
    'keynote': 'slot-keynote',
    'conference opening': 'slot-opening',
    'town hall': 'slot-closing',
    'plenary': 'slot-plenary',
    'posters and demos': 'slot-posters',
}

def special_class(event):
    if event is None:
        return 'slot-special'
    el = event.lower()
    for k, v in SPECIAL_EVENT_CLASS.items():
        if el.startswith(k):
            return v
    return 'slot-special'


def render_session_card_overview(sess):
    code = sess['code']
    name = sess['name'] or track_label(code)
    color_cls = track_color_class(code)
    tlabel = track_label(code)
    url = sess.get('url')

    title_html = esc(name)
    if url:
        title_html = f'<a href="{esc(url)}" target="_blank" class="session-ext-link">{esc(name)} <i class="fas fa-external-link-alt"></i></a>'

    return f'''<div class="session-card {color_cls}">
  <div class="session-track-badge">{esc(tlabel)}</div>
  <div class="session-name">{title_html}</div>
</div>'''


def render_session_card_full(sess, slot_idx, sess_idx):
    code = sess['code']
    name = sess['name'] or track_label(code)
    color_cls = track_color_class(code)
    tlabel = track_label(code)
    papers = sess['papers']
    url = sess.get('url')
    collapse_id = f"collapse-{slot_idx}-{sess_idx}"

    title_html = esc(name)
    if url:
        title_html = f'<a href="{esc(url)}" target="_blank" class="session-ext-link">{esc(name)} <i class="fas fa-external-link-alt"></i></a>'

    papers_html = ''
    if papers:
        items = []
        for p in papers:
            ptitle = esc(p['title'])
            pauth = esc(p['authors'])
            # Wrap title in <a> with placeholder href for future ACM DL link
            # The data-acm attribute makes it easy to add links later
            title_link = f'<a href="#" class="paper-title acm-link-placeholder" data-acm="">{ptitle}</a>'
            if pauth:
                items.append(f'<li class="paper-item"><span class="paper-title-wrap">{title_link}</span><span class="paper-authors">{pauth}</span></li>')
            else:
                items.append(f'<li class="paper-item"><span class="paper-title-wrap">{title_link}</span></li>')
        papers_html = f'<ul class="paper-list">' + ''.join(items) + '</ul>'

    toggle = ''
    papers_section = ''
    if papers:
        toggle = f' data-bs-toggle="collapse" data-bs-target="#{collapse_id}" aria-expanded="false" aria-controls="{collapse_id}"'
        count = len(papers)
        paper_label = f'{count} paper{"s" if count > 1 else ""}'
        papers_section = f'''<div class="collapse" id="{collapse_id}">
  <div class="papers-container">{papers_html}</div>
</div>'''
        header_extra = f'<button class="papers-toggle" {toggle}><span class="papers-count">{paper_label}</span><i class="fas fa-chevron-down toggle-icon"></i></button>'
    else:
        header_extra = ''

    return f'''<div class="session-card {color_cls}">
  <div class="session-card-header">
    <div class="session-track-badge">{esc(tlabel)}</div>
    <div class="session-name">{title_html}</div>
    {header_extra}
  </div>
  {papers_section}
</div>'''


COMMON_HEAD_LINKS = '''
    <link rel="stylesheet" href="../css/styles.css">
    <link rel="stylesheet" href="../css/tab-menu.css">
    <link rel="stylesheet" href="../css/dropdown-menu.css">
    <link rel="stylesheet" href="../css/header-layout.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
'''

PROGRAM_CSS = '''
<style>
/* ── Program layout ────────────────────────── */
.program-page { padding: 30px 0 60px; }

/* Day navigation tabs */
.day-tabs {
  display: flex; flex-wrap: wrap; gap: 6px;
  margin-bottom: 30px; border-bottom: 2px solid #e0e0e0; padding-bottom: 0;
}
.day-tab-btn {
  background: #f4f4f4; border: none; border-radius: 6px 6px 0 0;
  padding: 10px 18px; cursor: pointer; font-size: 0.9rem; font-weight: 600;
  color: #555; transition: all .2s; text-align: center; line-height: 1.3;
  border-bottom: 3px solid transparent; margin-bottom: -2px;
}
.day-tab-btn:hover { background: #ede5ff; color: #6a00ff; }
.day-tab-btn.active { background: white; color: #6a00ff;
  border-bottom: 3px solid #6a00ff; }
.day-tab-btn span { font-size: 0.8rem; font-weight: 400; display: block; }

/* Day panels */
.day-panel { display: none; }
.day-panel.active { display: block; }

/* Time slot blocks */
.time-slot { margin-bottom: 20px; }
.time-label {
  display: inline-flex; align-items: center; gap: 6px;
  color: #555; font-size: 0.82rem; font-weight: 700;
  letter-spacing: .4px; margin-bottom: 10px;
  padding: 4px 0;
}
.time-label i { opacity: .5; font-size: 0.78rem; }
.time-note { font-size: 0.75rem; color: #888; margin-left: 8px; font-style: italic; }

/* Special events — unified structure, colour accent only differs */
.slot-special-block {
  border-radius: 6px; padding: 13px 18px; margin-bottom: 4px;
  font-size: 0.95rem; font-weight: 600; line-height: 1.4; color: #1a1a1a;
  background: #fff; border: 1px solid #e8e8e8;
  border-left: 4px solid #bbb;
  box-shadow: 0 1px 4px rgba(0,0,0,.05);
}
.slot-keynote  { border-left-color: #6a00ff; }
.slot-break    { border-left-color: #bbb; font-weight: 400; font-size: 0.85rem; }
.slot-opening  { border-left-color: #00a855; }
.slot-closing  { border-left-color: #00a855; }
.slot-plenary  { border-left-color: #e08000; }
.slot-posters  { border-left-color: #0078d4; }

/* Session grid */
.session-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 10px;
}
@media (max-width: 768px) {
  .session-grid { grid-template-columns: 1fr 1fr; }
  .day-tab-btn { padding: 8px 12px; font-size: 0.82rem; }
  .slot-special-block { font-size: 0.88rem; padding: 11px 14px; }
  .day-heading { font-size: 1.1rem; }
}
@media (max-width: 480px) {
  .session-grid { grid-template-columns: 1fr; }
  .day-tabs { gap: 4px; }
  .day-tab-btn { padding: 7px 9px; font-size: 0.78rem; }
  .time-label { font-size: 0.78rem; }
  .program-page { padding: 16px 0 40px; }
}

/* Session cards */
.session-card {
  border-radius: 8px; padding: 12px 14px;
  background: white; border: 1px solid #e0e0e0;
  box-shadow: 0 1px 4px rgba(0,0,0,.06);
  transition: box-shadow .2s, transform .1s;
  display: flex; flex-direction: column; gap: 6px;
}
.session-card:hover { box-shadow: 0 4px 14px rgba(0,0,0,.13); transform: translateY(-1px); }

.session-card-header { display: flex; flex-direction: column; gap: 6px; }
.session-track-badge {
  font-size: 0.68rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: .7px; padding: 2px 8px; border-radius: 20px;
  display: inline-block; align-self: flex-start;
}
.session-name {
  font-size: 0.88rem; font-weight: 600; color: #1a1a1a; line-height: 1.4;
}
.session-ext-link { color: inherit; text-decoration: none; }
.session-ext-link:hover { text-decoration: underline; }
.session-ext-link .fas { font-size: 0.7rem; opacity: 0.7; }

/* Track colors */
.track-tutorial .session-track-badge  { background:#f3e8ff; color:#6a00ff; }
.track-workshop .session-track-badge  { background:#e8eaff; color:#2d3ad0; }
.track-econ     .session-track-badge  { background:#fff3e0; color:#b06000; }
.track-graph    .session-track-badge  { background:#e3f2fd; color:#0d47a1; }
.track-search   .session-track-badge  { background:#e0f7fa; color:#006064; }
.track-semantics .session-track-badge { background:#e8f5e9; color:#1b5e20; }
.track-social   .session-track-badge  { background:#fce4ec; color:#880e4f; }
.track-systems  .session-track-badge  { background:#ede7f6; color:#311b92; }
.track-security .session-track-badge  { background:#ffebee; color:#b71c1c; }
.track-mining   .session-track-badge  { background:#e8f5e9; color:#33691e; }
.track-recsys   .session-track-badge  { background:#e8eaf6; color:#1a237e; }
.track-industry .session-track-badge  { background:#fafafa; color:#424242; border:1px solid #bdbdbd; }
.track-history  .session-track-badge  { background:#fff8e1; color:#6d4c41; }
.track-web4good .session-track-badge  { background:#e0f2f1; color:#004d40; }
.track-respweb  .session-track-badge  { background:#fbe9e7; color:#bf360c; }
.track-phd      .session-track-badge  { background:#f9fbe7; color:#558b2f; }
.track-web4all  .session-track-badge  { background:#e1f5fe; color:#01579b; }
.track-demos    .session-track-badge  { background:#e8eaf6; color:#283593; }
.track-short    .session-track-badge  { background:#f3e5f5; color:#6a1b9a; }
.track-best     .session-track-badge  { background:#fff9c4; color:#827717; }
.track-other    .session-track-badge  { background:#f5f5f5; color:#616161; }

/* Left border colors per track */
.track-tutorial  { border-left:3px solid #6a00ff; }
.track-workshop  { border-left:3px solid #2d3ad0; }
.track-econ      { border-left:3px solid #f0a000; }
.track-graph     { border-left:3px solid #1565c0; }
.track-search    { border-left:3px solid #00838f; }
.track-semantics { border-left:3px solid #2e7d32; }
.track-social    { border-left:3px solid #c2185b; }
.track-systems   { border-left:3px solid #512da8; }
.track-security  { border-left:3px solid #c62828; }
.track-mining    { border-left:3px solid #558b2f; }
.track-recsys    { border-left:3px solid #283593; }
.track-industry  { border-left:3px solid #616161; }
.track-history   { border-left:3px solid #8d6e63; }
.track-web4good  { border-left:3px solid #00796b; }
.track-respweb   { border-left:3px solid #e64a19; }
.track-phd       { border-left:3px solid #689f38; }
.track-web4all   { border-left:3px solid #0277bd; }
.track-demos     { border-left:3px solid #3949ab; }
.track-short     { border-left:3px solid #8e24aa; }
.track-best      { border-left:3px solid #f9a825; }
.track-other     { border-left:3px solid #9e9e9e; }

/* Papers toggle button */
.papers-toggle {
  display: flex; align-items: center; gap: 6px;
  background: none; border: 1px solid #e0e0e0; border-radius: 4px;
  padding: 4px 10px; cursor: pointer; font-size: 0.78rem; color: #555;
  transition: all .2s; align-self: flex-start; margin-top: 4px;
}
.papers-toggle:hover { background: #f5f0ff; color: #6a00ff; border-color: #6a00ff; }
.papers-toggle[aria-expanded="true"] .toggle-icon { transform: rotate(180deg); }
.papers-count { font-weight: 600; }
.toggle-icon { transition: transform .2s; font-size: 0.7rem; }

/* Papers list */
.papers-container {
  margin-top: 8px; border-top: 1px solid #f0e8ff; padding-top: 8px;
}
.paper-list { list-style: none; margin: 0; padding: 0; }
.paper-item {
  padding: 7px 0; border-bottom: 1px solid #f5f5f5;
  display: flex; flex-direction: column; gap: 2px;
}
.paper-item:last-child { border-bottom: none; }
.paper-title-wrap { }
.paper-title {
  font-size: 0.82rem; font-weight: 600; color: #1a1a1a;
  text-decoration: none; line-height: 1.35;
}
.paper-title:hover { color: #6a00ff; text-decoration: underline; }
.acm-link-placeholder { color: #1a1a1a; pointer-events: none; cursor: default; }
.acm-link-placeholder[href]:not([href="#"]) {
  color: #1565c0; pointer-events: auto; cursor: pointer;
}
.paper-authors {
  font-size: 0.76rem; color: #666; line-height: 1.3;
}

/* Timezone note */
.timezone-note {
  background: #f5f5f5; border: 1px solid #e0e0e0; border-radius: 6px;
  padding: 10px 16px; margin-bottom: 24px; font-size: 0.88rem; color: #555;
  display: flex; align-items: center; gap: 8px;
}

/* Day header */
.day-heading {
  font-size: 1.3rem; font-weight: 700; color: #1a1a1a;
  padding: 14px 0 10px; border-bottom: 2px solid #6a00ff;
  margin-bottom: 20px;
}
</style>
'''

COMMON_SCRIPTS = '''
    <script src="../js/header-loader.js"></script>
    <script src="../js/footer-loader.js"></script>
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        // Day tab switching
        document.querySelectorAll('.day-tab-btn').forEach(function(btn) {
            btn.addEventListener('click', function() {
                var target = this.dataset.target;
                document.querySelectorAll('.day-tab-btn').forEach(b => b.classList.remove('active'));
                document.querySelectorAll('.day-panel').forEach(p => p.classList.remove('active'));
                this.classList.add('active');
                document.getElementById(target).classList.add('active');
            });
        });
        // Activate first tab
        var firstBtn = document.querySelector('.day-tab-btn');
        if (firstBtn) firstBtn.click();
    });
    </script>
'''

COLLAPSE_SCRIPT = '''
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        // Collapse toggle (no Bootstrap dependency)
        document.querySelectorAll('[data-bs-toggle="collapse"]').forEach(function(btn) {
            btn.addEventListener('click', function() {
                var targetId = this.dataset.bsTarget.replace('#','');
                var panel = document.getElementById(targetId);
                if (!panel) return;
                var expanded = this.getAttribute('aria-expanded') === 'true';
                if (expanded) {
                    panel.classList.remove('show');
                    this.setAttribute('aria-expanded','false');
                } else {
                    panel.classList.add('show');
                    this.setAttribute('aria-expanded','true');
                }
            });
        });
    });
    </script>
'''

COLLAPSE_CSS = '''
    <style>
    .collapse { display: none; }
    .collapse.show { display: block; }
    </style>
'''

# ─────────────────────────────────────────────
# 3. Build overview.html
# ─────────────────────────────────────────────

def build_overview():
    tabs_html = ''
    panels_html = ''

    for di, day in enumerate(program):
        did = day_id(day)
        heading = format_day_heading(day)
        tab_label = format_day_tab(day)
        tabs_html += f'<button class="day-tab-btn" data-target="{did}">{tab_label}</button>\n'

        slots_html = ''
        for slot in day['slots']:
            time_html = f'<div class="time-label"><i class="fas fa-clock" style="opacity:.7;margin-right:5px;"></i>{esc(slot["time"])}</div>'

            if slot['special']:
                sc = special_class(slot['event'])
                slots_html += f'''<div class="time-slot">
  {time_html}
  <div class="slot-special-block {sc}">{esc(slot["event"])}</div>
</div>\n'''
            else:
                cards = ''
                if slot['sessions']:
                    for sess in slot['sessions']:
                        cards += render_session_card_overview(sess) + '\n'
                slots_html += f'''<div class="time-slot">
  {time_html}
  <div class="session-grid">{cards}</div>
</div>\n'''

        panels_html += f'''<div class="day-panel" id="{did}">
  <h2 class="day-heading">{esc(heading)}</h2>
  {slots_html}
</div>\n'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Program Overview - The Web Conference 2026</title>
    {COMMON_HEAD_LINKS}
    {PROGRAM_CSS}
</head>
<body>
    <div id="header-placeholder">Header loading...</div>

    <section class="page-header">
        <div class="container">
            <h1>Program Overview</h1>
        </div>
    </section>

    <section class="page-content program-page">
        <div class="container">
            <div class="timezone-note">
                <i class="fas fa-info-circle"></i>
                All times are in <strong>UAE time (GST, UTC+4)</strong>.
            </div>

            <div class="day-tabs">
                {tabs_html}
            </div>

            {panels_html}
        </div>
    </section>

    <div id="footer-placeholder"></div>
    {COMMON_SCRIPTS}
</body>
</html>
'''


# ─────────────────────────────────────────────
# 4. Build full-schedule.html
# ─────────────────────────────────────────────

def build_full_schedule():
    tabs_html = ''
    panels_html = ''
    global_slot_idx = 0

    for di, day in enumerate(program):
        did = day_id(day)
        heading = format_day_heading(day)
        tab_label = format_day_tab(day)
        tabs_html += f'<button class="day-tab-btn" data-target="{did}">{tab_label}</button>\n'

        slots_html = ''
        for slot in day['slots']:
            time_html = f'<div class="time-label"><i class="fas fa-clock" style="opacity:.7;margin-right:5px;"></i>{esc(slot["time"])}</div>'

            if slot['special']:
                sc = special_class(slot['event'])
                slots_html += f'''<div class="time-slot">
  {time_html}
  <div class="slot-special-block {sc}">{esc(slot["event"])}</div>
</div>\n'''
            else:
                cards = ''
                if slot['sessions']:
                    for si, sess in enumerate(slot['sessions']):
                        cards += render_session_card_full(sess, global_slot_idx, si) + '\n'
                slots_html += f'''<div class="time-slot">
  {time_html}
  <div class="session-grid">{cards}</div>
</div>\n'''
            global_slot_idx += 1

        panels_html += f'''<div class="day-panel" id="{did}">
  <h2 class="day-heading">{esc(heading)}</h2>
  {slots_html}
</div>\n'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Full Schedule - The Web Conference 2026</title>
    {COMMON_HEAD_LINKS}
    {PROGRAM_CSS}
    {COLLAPSE_CSS}
</head>
<body>
    <div id="header-placeholder">Header loading...</div>

    <section class="page-header">
        <div class="container">
            <h1>Full Schedule</h1>
        </div>
    </section>

    <section class="page-content program-page">
        <div class="container">
            <div class="timezone-note">
                <i class="fas fa-info-circle"></i>
                All times are in <strong>UAE time (GST, UTC+4)</strong>.
                Click <strong>"N papers"</strong> on any session card to expand the paper list.
            </div>

            <div class="day-tabs">
                {tabs_html}
            </div>

            {panels_html}
        </div>
    </section>

    <div id="footer-placeholder"></div>
    {COMMON_SCRIPTS}
    {COLLAPSE_SCRIPT}
</body>
</html>
'''


# ─────────────────────────────────────────────
# 5. Write files
# ─────────────────────────────────────────────

overview_html = build_overview()
full_html = build_full_schedule()

with open('program/overview.html', 'w', encoding='utf-8') as f:
    f.write(overview_html)
print('Written: program/overview.html')

with open('program/full-schedule.html', 'w', encoding='utf-8') as f:
    f.write(full_html)
print('Written: program/full-schedule.html')

# Stats
total_papers = 0
for day in program:
    for slot in day['slots']:
        if not slot['special'] and slot['sessions']:
            for sess in slot['sessions']:
                total_papers += len(sess['papers'])

print(f'\nProgram stats:')
print(f'  Days: {len(program)}')
for day in program:
    slots = len(day["slots"])
    print(f'  {day["date"].strftime("%A %b %d")}: {slots} slots')
print(f'  Total papers/posters/tutorials: {total_papers}')
