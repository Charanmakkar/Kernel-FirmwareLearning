/* Fieldnotes: a dependency-free local reader. Course files are never written. */
(() => {
  'use strict';
  let library = JSON.parse(document.getElementById('library-data').textContent);
  let byPath = new Map(library.files.map(file => [file.path, file]));
  const $ = selector => document.querySelector(selector);
  const main = $('#main');
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const routeDoc = (path, heading = '') => `#doc/${encodeURIComponent(path)}${heading ? '?h=' + encodeURIComponent(heading) : ''}`;
  const routeSection = section => `#section/${encodeURIComponent(section)}`;
  const isLive = /^https?:$/.test(location.protocol);
  const symbols = {
    search:'<circle cx="10.8" cy="10.8" r="6.8"/><path d="m16 16 4 4"/>',
    home:'<path d="m3 10 9-7 9 7v10H3z"/><path d="M9 20v-7h6v7"/>',
    book:'<path d="M12 6c-3-2-6-2-9-1v15c3-1 6-1 9 1 3-2 6-2 9-1V5c-3-1-6-1-9 1v15"/>',
    compass:'<circle cx="12" cy="12" r="9"/><path d="m16 8-2 6-6 2 2-6z"/>',
    route:'<circle cx="5" cy="5" r="2"/><circle cx="19" cy="19" r="2"/><path d="M7 5h8a4 4 0 0 1 0 8H9a3 3 0 0 0 0 6h8"/>',
    chat:'<path d="M21 11a9 9 0 0 1-13 8l-5 2 1-5a9 9 0 1 1 17-5Z"/><path d="M8 9h8M8 13h5"/>',
    check:'<rect x="4" y="4" width="16" height="16" rx="3"/><path d="m8 12 3 3 6-7"/>',
    target:'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
    spark:'<path d="m12 3 2.5 6.5L21 12l-6.5 2.5L12 21l-2.5-6.5L3 12l6.5-2.5z"/>',
    code:'<path d="m8 6-6 6 6 6m8-12 6 6-6 6M14 3l-4 18"/>',
    case:'<rect x="3" y="7" width="18" height="14" rx="2"/><path d="M8 7V3h8v4M3 12c6 3 12 3 18 0"/>',
    link:'<path d="m9 15 6-6M8 17l-1 1a4 4 0 0 1-6-6l5-5a4 4 0 0 1 6 0m0 10a4 4 0 0 0 6 0l5-5a4 4 0 0 0-6-6l-1 1"/>',
    chart:'<path d="M4 3v17h17M8 16v-4m5 4V7m5 9v-7"/>',
    file:'<path d="M14 2H5v20h14V7zM14 2v5h5M8 12h8M8 16h8"/>',
    layers:'<path d="m3 7 9-4 9 4-9 4zM3 12l9 4 9-4M3 17l9 4 9-4"/>',
    arrow:'<path d="M4 12h16m-6-6 6 6-6 6"/>',
    chevron:'<path d="m9 5 7 7-7 7"/>',
    star:'<path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1.1 6.2-5.6-3-5.6 3 1.1-6.2L3 9.6l6.2-.9z"/>',
    sun:'<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1 1m12 12 1 1M5 19l1-1M18 6l1-1"/>',
    moon:'<path d="M20 14a8 8 0 0 1-10-10 9 9 0 1 0 10 10Z"/>',
    focus:'<path d="M8 3H3v5m13-5h5v5M3 16v5h5m13-5v5h-5"/>',
    menu:'<path d="M4 6h16M4 12h16M4 18h16"/>',
    download:'<path d="M12 3v12m-5-5 5 5 5-5M4 16v5h16v-5"/>',
    lock:'<rect x="5" y="10" width="14" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3M12 14v3"/>',
    print:'<path d="M7 8V3h10v5M7 17H3V8h18v9h-4M7 14h10v7H7z"/>',
  };
  const icon = name => `<svg viewBox="0 0 24 24" aria-hidden="true">${symbols[name] || symbols.file}</svg>`;
  let stored = {};
  try { stored = JSON.parse(localStorage.getItem('fieldnotes-reader-v1') || '{}') || {}; } catch (_) { /* Storage may be disabled for file URLs. */ }
  const prefs = {
    read: new Set(Array.isArray(stored.read) ? stored.read.filter(x => typeof x === 'string') : []),
    bookmarks: new Set(Array.isArray(stored.bookmarks) ? stored.bookmarks.filter(x => typeof x === 'string') : []),
    lastDoc: typeof stored.lastDoc === 'string' ? stored.lastDoc : '',
    theme: stored.theme === 'dark' ? 'dark' : 'light',
    font: Number.isFinite(stored.font) ? Math.min(22, Math.max(15, stored.font)) : 17,
  };
  let currentPath = '';
  let currentSection = '';
  let activeObserver = null;
  let toastTimer;
  const revealedAnswers = new Set();
  function notify(message) {
    $('#toast').textContent = message;
    $('#toast').classList.add('visible');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => $('#toast').classList.remove('visible'), 4200);
  }
  function save() {
    try {
      localStorage.setItem('fieldnotes-reader-v1', JSON.stringify({...prefs, read:[...prefs.read], bookmarks:[...prefs.bookmarks]}));
    } catch (_) { notify('Reading preferences work for this visit; this browser has disabled local saving.'); }
  }
  function applyPreferences() {
    document.documentElement.dataset.theme = prefs.theme;
    document.documentElement.style.setProperty('--reading-size', `${prefs.font}px`);
    $('#theme-toggle').innerHTML = icon(prefs.theme === 'dark' ? 'sun' : 'moon');
    $('#theme-toggle').setAttribute('aria-label', `Switch to ${prefs.theme === 'dark' ? 'light' : 'dark'} theme`);
    $('#font-minus').disabled = prefs.font <= 15;
    $('#font-plus').disabled = prefs.font >= 22;
  }
  const sectionInfo = section => library.sections.find(s => s.id === section) || {label:'Program overview',icon:'layers'};
  const sectionFiles = section => library.files.filter(f => f.section === section);
  function fileLabel(file) {
    if (file.answer) return 'Answer key';
    if (file.kind === 'word') return 'Word edition';
    if (file.path.startsWith('07_Projects') && file.path.endsWith('/README.md')) return file.path.includes('/B01_') ? 'Implementation' : 'Project plan';
    if (file.kind === 'csv') return 'Table';
    if (file.kind === 'json') return 'Data & evidence';
    if (file.kind === 'code') return 'Source code';
    if (file.path.includes('M01_C_')) return 'Lesson';
    return 'Document';
  }
  function originalURL(path) {
    return isLive ? `/materials/${path.split('/').map(encodeURIComponent).join('/')}` : `../${encodeURIComponent(library.sourceFolder)}/${path.split('/').map(encodeURIComponent).join('/')}`;
  }
  function navItem(href, label, symbol, active, count = '') {
    return `<a class="nav-item${active ? ' active' : ''}" href="${href}"${active ? ' aria-current="page"' : ''}>${icon(symbol)}<span>${esc(label)}</span>${count !== '' ? `<span class="nav-count">${count}</span>` : ''}</a>`;
  }
  function renderNavigation(view = '') {
    let html = navItem('#home','Library home','home',view === 'home');
    html += navItem('#view/all','Continuous reading','book',view === 'all');
    html += navItem('#view/bookmarks','Saved for later','star',view === 'bookmarks',prefs.bookmarks.size || '');
    html += '<div class="nav-label">YOUR LEARNING PATH</div>';
    library.sections.filter(s => !['_root','Word_Edition'].includes(s.id)).forEach(section => {
      const files = sectionFiles(section.id);
      if (!files.length) return;
      const special = section.id === '02_Interview_Questions_and_Answers' ? '#view/interviews' : section.id === '07_Projects' ? '#view/projects' : routeSection(section.id);
      html += navItem(special,section.label,section.icon,currentSection === section.id, files.length);
      if (currentPath && currentSection === section.id) {
        html += '<div class="nav-children">' + files.map(f => `<a class="nav-file${f.path === currentPath ? ' active' : ''}" href="${routeDoc(f.path)}"${f.path === currentPath ? ' aria-current="page"' : ''}>${esc(f.title)}</a>`).join('') + '</div>';
      }
    });
    html += '<div class="nav-label">LIBRARY</div>';
    html += navItem(routeSection('Word_Edition'),'Word editions','file',currentSection === 'Word_Edition');
    html += navItem(routeSection('_root'),'Program & delivery status','layers',currentSection === '_root');
    $('#navigation').innerHTML = html;
    $('#library-total').textContent = `${library.files.length} files`;
    $('#snapshot-label').textContent = `Content refreshed ${new Date(library.generatedAt).toLocaleDateString(undefined,{day:'numeric',month:'short',year:'numeric'})}`;
  }
  function breadcrumbs(section, tail = '') {
    return `<div class="breadcrumbs"><a href="#home">Library</a>${icon('chevron')}<a href="${routeSection(section)}">${esc(sectionInfo(section).label)}</a>${tail ? icon('chevron') + `<span>${esc(tail)}</span>` : ''}</div>`;
  }
  function fileCard(file) {
    return `<a class="file-card" href="${routeDoc(file.path)}">${icon(file.kind === 'code' ? 'code' : file.kind === 'csv' ? 'chart' : 'file')}<div><h3>${esc(file.title)}</h3><div class="card-tags"><span class="tag neutral">${esc(fileLabel(file))}</span><span class="result-label">${Math.max(1,Math.ceil(file.words / 220))} min read</span></div><p>${esc(file.path)}</p></div>${prefs.read.has(file.path) ? '<span class="read-check" aria-label="Marked read">✓</span>' : ''}</a>`;
  }
  function home() {
    const diagnostic = '04_Skill_Assessments/questions/D01_Initial_Diagnostic.md';
    const lesson = '03_JD_JR_Skills_and_Learning_Content/M01_C_Objects_Bytes_and_Contracts.md';
    const firstProject = library.projects.find(p => p.ID === 'B01');
    const resume = byPath.has(prefs.lastDoc) ? prefs.lastDoc : diagnostic;
    const count = [...prefs.read].filter(p => byPath.has(p)).length;
    main.innerHTML = `<div class="page home-page">
      <section class="hero"><div><p class="eyebrow">A place to learn, one concept at a time</p><h1>Your embedded<br>engineering <em>library.</em></h1><p class="hero-description">From C foundations to Linux, kernel development, and firmware.<br>All your learning material, connected in one quiet reading space.</p><div class="button-row"><a class="button primary" href="${routeDoc(resume)}">${prefs.lastDoc ? 'Continue reading' : 'Start with the diagnostic'} ${icon('arrow')}</a><a class="button" href="${routeDoc('01_Learning_Roadmap/roadmap_64_weeks.csv')}">${icon('route')} Explore the roadmap</a></div></div><aside class="release-card"><div class="release-small">The current collection</div><h2>A foundation to build on</h2><div class="release-line">${icon('check')} 1 complete learning module</div><div class="release-line">${icon('check')} 1 implemented & tested project</div><div class="release-line">${icon('route')} 14 more project specifications</div><a href="${routeDoc('PROGRESS.md')}">See what’s ready and what’s next →</a></aside></section>
      <div class="stat-strip"><div class="stat"><div class="stat-number">${library.stats.files}</div><div class="stat-label">files, one reading room</div></div><div class="stat"><div class="stat-number">${library.stats.weeks}</div><div class="stat-label">weeks in the full roadmap</div></div><div class="stat"><div class="stat-number">${library.stats.questions}</div><div class="stat-label">interview questions</div></div><div class="stat"><div class="stat-number">${library.stats.projects}</div><div class="stat-label">project specifications</div></div></div>
      <div class="section-title"><h2>A good place to begin</h2><span>UNDERSTAND → PRACTICE → BUILD</span></div>
      <div class="journey"><a class="journey-card" href="${routeDoc('00_Start_Here/PROFILE_AND_ASSUMPTIONS.md')}"><div class="journey-top"><span class="step-number">01 / GET ORIENTED</span>${icon('compass')}</div><h3>Find your starting point</h3><p>Understand the three tracks, your assumptions, and the initial skill diagnostic.</p><span class="text-link">Start here ${icon('arrow')}</span></a><a class="journey-card" href="${routeDoc(lesson)}"><div class="journey-top"><span class="step-number">02 / LEARN THE FOUNDATIONS</span>${icon('book')}</div><h3>Make the concepts click</h3><p>Read worked examples, follow a guided lab, and try an independent exercise.</p><span class="text-link">Open the first lesson ${icon('arrow')}</span></a><a class="journey-card" href="${routeDoc(firstProject ? firstProject.Folder + '/README.md' : '01_Learning_Roadmap/PROJECT_CATALOG.md')}"><div class="journey-top"><span class="step-number">03 / PUT IT INTO PRACTICE</span>${icon('code')}</div><h3>Build something you can explain</h3><p>Explore the C utility library, its source, tests, and actual validation evidence.</p><span class="text-link">Enter the workshop ${icon('arrow')}</span></a></div>
      <div class="home-lower"><section><div class="section-title"><h2>Your first chapter</h2><span>FOUNDATIONS / M01</span></div><div class="featured-lesson"><span class="tag">C PROGRAMMING</span><h3>Objects, bytes,<br>and bounded interfaces.</h3><p>Build a clear mental model of pointers, ownership, integer bounds, and the contracts that keep embedded code correct.</p><a class="button small" href="${routeDoc(lesson)}">Read the lesson ${icon('arrow')}</a></div></section><section><div class="section-title"><h2>Keep within reach</h2></div><div class="quick-links">${[
        ['#view/interviews','chat','Practice an interview','Answers revealed when you’re ready'],
        [routeDoc('00_Start_Here/ENVIRONMENT.md'),'code','Set up your environment','Start without purchasing a board'],
        [routeDoc('05_Interview_Strategy/revision_30_days.csv'),'route','Plan your next 30 days','A focused revision calendar'],
        [routeSection('09_References_and_Resources'),'link','Go to the primary sources','Official documentation and references'],
      ].map(([href,symbol,title,subtitle]) => `<a class="quick-link" href="${href}">${icon(symbol)}<span><strong>${title}</strong><small>${subtitle}</small></span>${icon('arrow')}</a>`).join('')}</div></section></div>
      <div class="reading-progress"><div><strong>${count ? `${count} ${count === 1 ? 'file' : 'files'} marked as read` : 'Make this space your own'}</strong><p>Save pages, adjust the text, and pick up where you left off. Reading marks are personal, not skill scores.</p></div><div class="progress-track" aria-label="Personal reading progress"><span style="width:${Math.min(100,count / Math.max(1,library.files.length) * 100)}%"></span></div></div>
      ${prefs.bookmarks.size ? `<div class="section-title"><h2>Saved for later</h2><a href="#view/bookmarks">See all →</a></div><div class="file-grid">${[...prefs.bookmarks].map(p => byPath.get(p)).filter(Boolean).slice(0,4).map(fileCard).join('')}</div>` : ''}
    </div>`;
    const releaseCounts = [
      ['check',`${library.stats.completeLessons} complete learning module${library.stats.completeLessons === 1 ? '' : 's'}`],
      ['check',`${library.stats.implementedProjects} implemented project${library.stats.implementedProjects === 1 ? '' : 's'}`],
      ['route',`${library.stats.projects-library.stats.implementedProjects} more project specifications`],
    ];
    main.querySelectorAll('.release-line').forEach((line,index) => {line.innerHTML = icon(releaseCounts[index][0]) + ' ' + esc(releaseCounts[index][1]);});
  }
  function sectionPage(section, bookmarks = false) {
    const info = bookmarks ? {label:'Saved for later'} : sectionInfo(section);
    const files = bookmarks ? [...prefs.bookmarks].map(p => byPath.get(p)).filter(Boolean) : sectionFiles(section);
    main.innerHTML = `<div class="page">${bookmarks ? '<div class="eyebrow">Your reading list</div>' : breadcrumbs(section)}<h1 class="page-title">${esc(info.label)}</h1><p class="page-intro">${bookmarks ? 'A place for the chapters, questions, and references you want to come back to.' : `${files.length} files from your learning program. Read them here, or move through this section as one continuous document.`}</p><div class="toolbar"><input class="inline-search" id="file-filter" type="search" placeholder="Filter by title or file name" aria-label="Filter files">${!bookmarks ? `<a class="button" href="#view/all?section=${encodeURIComponent(section)}">${icon('book')} Read this section</a>` : ''}</div><div class="file-grid" id="file-grid"></div></div>`;
    const draw = () => {
      const query = $('#file-filter').value.trim().toLowerCase();
      const filtered = files.filter(f => `${f.title} ${f.path}`.toLowerCase().includes(query));
      $('#file-grid').innerHTML = filtered.length ? filtered.map(fileCard).join('') : '<div class="empty-state">No matching files. Try a different title.</div>';
    };
    $('#file-filter').addEventListener('input',draw);draw();
  }
  function slug(value) {
    return value.toLowerCase().replace(/<[^>]*>/g,'').replace(/[^\p{L}\p{N}\-\s]/gu,'').trim().replace(/\s/g,'-');
  }
  function resolveLocal(href, source) {
    try {
      const url = new URL(href, `https://fieldnotes.invalid/${source}`);
      if (url.origin !== 'https://fieldnotes.invalid') return null;
      const path = decodeURIComponent(url.pathname).replace(/^\//,'');
      return byPath.has(path) ? {path,heading:decodeURIComponent(url.hash.slice(1))} : null;
    } catch (_) { return null; }
  }
  function enhanceLinks(container,file) {
    container.querySelectorAll('a[href]').forEach(anchor => {
      const href = anchor.getAttribute('href');
      if (/^https?:\/\//i.test(href)) { anchor.target = '_blank';anchor.rel = 'noopener noreferrer';return; }
      if (/^mailto:/i.test(href)) return;
      const local = resolveLocal(href,file.path);
      if (local) anchor.setAttribute('href',routeDoc(local.path,local.heading));
      else {
        anchor.removeAttribute('href');
        anchor.tabIndex = 0;
        anchor.setAttribute('role','button');
        anchor.title = 'This reference is not a delivered file in the current collection.';
        anchor.addEventListener('click',() => notify('This file or reference is not included in the current release.'));
        anchor.addEventListener('keydown',event => {if(event.key === 'Enter')anchor.click();});
      }
    });
  }
  function enhanceCode(container) {
    container.querySelectorAll('pre').forEach(pre => {
      if (pre.closest('.code-wrap')) return;
      const code = pre.querySelector('code');
      const label = code?.className.match(/language-([\w+-]+)/)?.[1] || 'TEXT';
      const wrapper = document.createElement('div');wrapper.className = 'code-wrap';
      const top = document.createElement('div');top.className = 'code-top';
      const name = document.createElement('span');name.textContent = label.toUpperCase();
      const copy = document.createElement('button');copy.className = 'code-copy';copy.textContent = 'Copy';copy.type = 'button';copy.setAttribute('aria-label','Copy code block');
      copy.addEventListener('click',() => copyText((code || pre).textContent,copy));
      top.append(name,copy);pre.before(wrapper);wrapper.append(top,pre);
    });
    container.querySelectorAll('table').forEach(table => {
      if(table.parentElement.classList.contains('table-wrap'))return;
      const wrap = document.createElement('div');wrap.className = 'table-wrap';wrap.tabIndex = 0;wrap.setAttribute('aria-label','Scrollable table');table.before(wrap);wrap.append(table);
    });
  }
  async function copyText(text,button) {
    try {
      if(navigator.clipboard?.writeText)await navigator.clipboard.writeText(text);
      else {
        const textarea = document.createElement('textarea');textarea.value = text;textarea.style.position = 'fixed';textarea.style.opacity = '0';document.body.append(textarea);textarea.select();
        const success = document.execCommand('copy');textarea.remove();if(!success)throw new Error('Clipboard unavailable');
      }
      const old = button.textContent;button.textContent = 'Copied';setTimeout(() => button.textContent = old,1600);
    } catch (_) { notify('Clipboard access is unavailable here. Select the code and copy it manually.'); }
  }
  function markdown(container,file,prefix = '',removeTitle = true) {
    const html = marked.parse(file.text,{gfm:true,breaks:false});
    container.innerHTML = DOMPurify.sanitize(html,{USE_PROFILES:{html:true},FORBID_TAGS:['img','iframe','object','embed','style','script','form','input','button'],FORBID_ATTR:['style']});
    const title = container.querySelector('h1');if(removeTitle && title)title.remove();
    const seen = new Map();
    container.querySelectorAll('h1,h2,h3,h4').forEach(heading => {
      const base = slug(heading.textContent) || 'section';
      const count = seen.get(base) || 0;seen.set(base,count+1);
      heading.id = prefix + base + (count ? '-' + count : '');
    });
    enhanceLinks(container,file);enhanceCode(container);
  }
  function makeTOC(container) {
    const toc = $('#document-toc');if(!toc)return;
    const headings = [...container.querySelectorAll('h2,h3')];
    headings.forEach((heading,index) => {if(!heading.id)heading.id = `reader-heading-${index}`;});
    toc.innerHTML = `<div class="toc-title">ON THIS PAGE</div>` + headings.map(h => `<a href="#" data-heading="${esc(h.id)}" class="${h.tagName === 'H3' ? 'toc-sub' : ''}">${esc(h.textContent)}</a>`).join('');
    toc.querySelectorAll('[data-heading]').forEach(a => a.addEventListener('click',event => {event.preventDefault();document.getElementById(a.dataset.heading)?.scrollIntoView({behavior:'smooth'});}));
    if(!headings.length){toc.hidden = true;return;}
    if('IntersectionObserver' in window){
      activeObserver = new IntersectionObserver(entries => {
        const visible = entries.find(e => e.isIntersecting);if(!visible)return;
        toc.querySelectorAll('a').forEach(a => a.classList.toggle('current',a.dataset.heading === visible.target.id));
      },{rootMargin:'-85px 0px -70% 0px'});
      headings.forEach(h => activeObserver.observe(h));
    }
  }
  function detail(title,html) {
    $('#detail-title').textContent = title;$('#detail-content').innerHTML = html;
    if(!$('#detail-dialog').open)$('#detail-dialog').showModal();
  }
  function tableView(container,file) {
    let allColumns = false;
    const columns = file.columns || [];
    const compact = file.path.endsWith('roadmap_64_weeks.csv') ? ['Week','Phase','Learning objectives','Project milestone','Objective exit test'] : file.path.endsWith('reference_skills_matrix.csv') ? ['Requirement ID','Requirement','Role track','Expected depth','Current evidence','Learning module'] : file.path.endsWith('project_plan.csv') ? ['ID','Level','Project','Hours','Implementation status'] : columns.slice(0,6);
    container.innerHTML = `<div class="toolbar"><input class="inline-search" type="search" placeholder="Filter table rows…" aria-label="Filter table rows"><button class="button small" data-columns>Show all columns</button></div><p class="table-hint">Select a row to read all its fields. Data is read-only.</p><div class="table-wrap data-wrap" tabindex="0" role="region" aria-label="Scrollable data table"><table class="data-table"></table></div><div class="table-status"><span data-count></span><a href="${originalURL(file.path)}" download>Download original CSV ↗</a></div>`;
    const input = container.querySelector('input');
    const draw = () => {
      const query = input.value.trim().toLowerCase();
      const rows = file.rows.map((row,index) => ({row,index})).filter(({row}) => row.join(' ').toLowerCase().includes(query));
      const chosen = (allColumns ? columns : compact).map(name => columns.indexOf(name)).filter(index => index >= 0);
      const table = container.querySelector('table');
      table.innerHTML = `<thead><tr>${chosen.map(i => `<th scope="col">${esc(columns[i])}</th>`).join('')}</tr></thead><tbody>${rows.map(({row,index}) => `<tr tabindex="0" role="button" aria-label="Read details for row ${index+1}" data-row="${index}">${chosen.map(i => `<td>${esc(row[i])}</td>`).join('')}</tr>`).join('')}</tbody>`;
      if(!rows.length)table.innerHTML += '<caption>No matching rows</caption>';
      table.querySelectorAll('[data-row]').forEach(tr => {
        const open = () => {
          const row = file.rows[Number(tr.dataset.row)];
          detail(`${file.title} · ${row[0] || 'row details'}`,columns.map((name,index) => {
            const value = row[index] || '—';
            const resolved = resolveLocal(value,file.path);
            return `<div class="detail-field"><strong>${esc(name)}</strong><p>${resolved ? `<a href="${routeDoc(resolved.path,resolved.heading)}" data-close-detail>${esc(value)}</a>` : esc(value)}</p></div>`;
          }).join(''));
        };
        tr.addEventListener('click',open);tr.addEventListener('keydown',event => {if(event.key === 'Enter' || event.key === ' '){event.preventDefault();open();}});
      });
      container.querySelector('[data-count]').textContent = `${rows.length} of ${file.rows.length} rows · ${chosen.length} of ${columns.length} columns`;
    };
    input.addEventListener('input',draw);
    container.querySelector('[data-columns]').addEventListener('click',event => {allColumns = !allColumns;event.currentTarget.textContent = allColumns ? 'Show reading view' : 'Show all columns';draw();});
    draw();
  }
  function jsonView(container,file) {
    const value = file.value;
    if(!value || typeof value !== 'object') {container.innerHTML = `<pre class="source-code">${esc(file.text)}</pre>`;return;}
    if(file.path.endsWith('/bank.json')) {
      container.innerHTML = `<div class="notice">This dataset contains the complete interview bank. Practice questions with answers hidden in the interview room.</div><a class="button primary" href="#view/interviews">Open interview practice ${icon('arrow')}</a><details class="json-summary"><summary>Read complete JSON dataset</summary><pre>${esc(JSON.stringify(value,null,2))}</pre></details>`;return;
    }
    const simple = Object.entries(value).filter(([,v]) => v === null || typeof v !== 'object');
    const structured = Object.entries(value).filter(([,v]) => v !== null && typeof v === 'object');
    container.innerHTML = `<div class="json-overview">${simple.slice(0,9).map(([key,v]) => `<div class="json-metric"><span>${esc(key.replace(/_/g,' '))}</span>${esc(v)}</div>`).join('')}</div>` + structured.map(([key,v]) => `<details class="json-summary"${['commands','checks'].includes(key) ? ' open' : ''}><summary>${esc(key.replace(/_/g,' '))} ${Array.isArray(v) ? `(${v.length})` : ''}</summary><pre>${esc(JSON.stringify(v,null,2))}</pre></details>`).join('') + `<details class="json-summary"><summary>Complete original JSON</summary><pre>${esc(file.text)}</pre></details>`;
  }
  function questionCard(q) {
    const fields = [['Spoken answer',q['Spoken answer']],['Deeper explanation & example',q['Deeper explanation/example']],['Assumptions & version',q['Assumptions/version']],['Common incorrect answer',q['Common incorrect answer']],['Follow-up',q['Follow-up']],['Full-credit discriminator',q['Full-credit discriminator']]];
    return `<article class="question-card" id="${esc(q.ID.toLowerCase())}"><div class="question-top"><span class="question-id">${esc(q.ID)}</span><span class="tag">${esc(q.Category)}</span><span class="tag neutral">${esc(q.Difficulty)}</span><span class="tag neutral">${esc(q.Track)}</span></div><h2>${esc(q.Question)}</h2><p class="question-context">${esc(q.Round)} · Assesses: ${esc(q['Assessed skill'])}</p><details><summary>Reveal answer & discussion</summary><div class="question-answer">${fields.map(([label,value],index) => `<h3>${label}</h3><p class="${index === 0 ? 'spoken-answer' : ''}">${esc(value)}</p>`).join('')}<h3>Learning connection</h3><p><a href="${routeDoc('03_JD_JR_Skills_and_Learning_Content/MODULE_CATALOG.md',q['Learning module'].split('/')[0].toLowerCase())}">${esc(q['Learning module'])}</a> · ${esc(q.References)}</p><h3>Scoring</h3><p>0 unsafe/incorrect · 1 terminology only · 2 core answer · 3 deeper explanation · 4 full discriminator, follow-up, and a meaningful boundary/failure test.</p></div></details></article>`;
  }
  function questionTopic(file) {
    const range = file.path.split('/').pop().match(/^(\d{3})_(\d{3})_/);
    return range ? library.questions.filter(q => Number(q.ID.slice(1)) >= Number(range[1]) && Number(q.ID.slice(1)) <= Number(range[2])) : null;
  }
  function fileContent(container,file,prefix = '',ignoreGate = false) {
    if(file.answer && !ignoreGate && !revealedAnswers.has(file.path)) {
      container.innerHTML = `<div class="answer-gate">${icon('lock')}<h2>Try the exercise first.</h2><p>This file contains assessment answers or reference solutions. Reveal it when you’re ready to review your attempt.</p><button class="button" data-reveal-answer>Reveal this answer key</button></div>`;
      container.querySelector('button').addEventListener('click',() => {revealedAnswers.add(file.path);fileContent(container,file,prefix,true);makeTOC(container);});return;
    }
    if(file.error)container.innerHTML = `<div class="notice">${esc(file.error)}</div><a class="button" href="${originalURL(file.path)}" download>Download the original file</a>`;
    else if(file.kind === 'csv')tableView(container,file);
    else if(file.kind === 'json')jsonView(container,file);
    else if(file.kind === 'markdown') {
      const questions = questionTopic(file);
      if(questions)container.innerHTML = `<div class="notice">Try each question before revealing its answer. Use the interview practice view to filter across the full bank.</div><div class="question-list">${questions.map(questionCard).join('')}</div>`;
      else {container.classList.add('prose');markdown(container,file,prefix);}
    } else if(file.kind === 'word') {
      container.innerHTML = `<div class="notice">Text extracted from the Word edition is shown below. The Markdown chapters provide the best web formatting; the original document remains available to download.</div><a class="button small" href="${originalURL(file.path)}" download>${icon('download')} Download Word edition</a><div class="word-text prose" style="white-space:pre-wrap"></div>`;
      container.querySelector('.word-text').textContent = file.text;
    } else if(file.kind === 'code') {
      container.innerHTML = `<pre><code class="language-${esc(file.path.split('.').pop().toLowerCase())}">${esc(file.text)}</code></pre>`;enhanceCode(container);
    } else container.innerHTML = `<div class="notice">This attachment can be opened in its original application.</div><a class="button" href="${originalURL(file.path)}" download>Download attachment</a>`;
  }
  function documentPage(path,heading = '') {
    const file = byPath.get(path);
    if(!file){main.innerHTML = '<div class="page"><h1 class="page-title">This file isn’t in the current collection.</h1><p class="page-intro">It may be a planned item or a file added after this snapshot. Refresh the library to include new material.</p><a class="button" href="#home">Return to the library</a></div>';return;}
    prefs.lastDoc = path;save();
    const sectionList = sectionFiles(file.section);const index = sectionList.findIndex(f => f.path === path);
    const prev = sectionList[index-1];const next = sectionList[index+1];
    main.innerHTML = `<div class="page reader-page">${breadcrumbs(file.section,fileLabel(file))}<div class="reader-heading"><h1 class="page-title">${esc(file.title)}</h1><div class="reader-actions"><button class="button small" id="bookmark-doc" aria-pressed="${prefs.bookmarks.has(path)}">${icon('star')} ${prefs.bookmarks.has(path) ? 'Saved' : 'Save'}</button><button class="button small" id="read-doc" aria-pressed="${prefs.read.has(path)}">${icon('check')} ${prefs.read.has(path) ? 'Read' : 'Mark read'}</button><button class="icon-button" id="print-doc" aria-label="Print current document">${icon('print')}</button></div></div><div class="document-meta"><span class="tag ${fileLabel(file) === 'Project plan' ? 'amber' : 'neutral'}">${esc(fileLabel(file))}</span><span>${Math.max(1,Math.ceil(file.words / 220))} min read</span><span>·</span><a href="${originalURL(path)}" download>Download original ↗</a></div><div class="reader-layout"><div><article class="document" id="document-content"></article><div class="document-bottom">${prev ? `<a href="${routeDoc(prev.path)}">← ${esc(prev.title)}</a>` : '<span></span>'}${next ? `<a href="${routeDoc(next.path)}">${esc(next.title)} →</a>` : ''}</div></div><aside class="toc" id="document-toc" aria-label="On this page"></aside></div></div>`;
    const article = $('#document-content');fileContent(article,file);makeTOC(article);
    $('#bookmark-doc').addEventListener('click',event => {
      if(prefs.bookmarks.has(path))prefs.bookmarks.delete(path);else prefs.bookmarks.add(path);save();
      event.currentTarget.innerHTML = icon('star') + (prefs.bookmarks.has(path) ? ' Saved' : ' Save');event.currentTarget.setAttribute('aria-pressed',prefs.bookmarks.has(path));renderNavigation('doc');
    });
    $('#read-doc').addEventListener('click',event => {
      if(prefs.read.has(path))prefs.read.delete(path);else prefs.read.add(path);save();
      event.currentTarget.innerHTML = icon('check') + (prefs.read.has(path) ? ' Read' : ' Mark read');event.currentTarget.setAttribute('aria-pressed',prefs.read.has(path));notify(prefs.read.has(path) ? 'Marked as read. This is a reading preference, not a skill assessment.' : 'Reading mark removed.');
    });
    $('#print-doc').addEventListener('click',() => window.print());
    if(heading)requestAnimationFrame(() => {
      const target = document.getElementById(heading);if(target)target.scrollIntoView();else notify('That heading was not found; the referenced document is open.');
    });
  }
  function interviewPage() {
    main.innerHTML = `<div class="page"><div class="eyebrow">Interview practice</div><h1 class="page-title">Think it through. Then reveal.</h1><p class="page-intro">${library.questions.length} questions across Linux, kernel development, and firmware. Explain your reasoning first; use the answer to review the gaps.</p><div class="toolbar"><input class="inline-search" id="question-search" type="search" placeholder="Search question text or ID…" aria-label="Search interview questions"><select id="question-topic" class="filter-select" aria-label="Filter by topic"><option value="">All topics</option>${[...new Set(library.questions.map(q => q.Topic))].map(topic => `<option>${esc(topic)}</option>`).join('')}</select><select id="question-type" class="filter-select" aria-label="Filter by question type"><option value="">All question types</option>${[...new Set(library.questions.map(q => q.Category))].map(type => `<option>${esc(type)}</option>`).join('')}</select><select id="question-track" class="filter-select" aria-label="Filter by role track"><option value="">All tracks</option><option value="EL">Embedded Linux</option><option value="KD">Kernel / drivers</option><option value="FW">Firmware / RTOS</option></select></div><div class="table-status"><span id="question-count"></span><a href="${routeSection('02_Interview_Questions_and_Answers')}">Browse source documents ↗</a></div><div class="question-list" id="questions" style="margin-top:18px"></div><div class="pagination"><button class="button small" id="questions-prev">← Previous</button><span id="question-page"></span><button class="button small" id="questions-next">Next →</button></div></div>`;
    let page = 0;const size = 10;let selected = library.questions;
    function draw(reset = false) {
      if(reset)page = 0;
      const query = $('#question-search').value.trim().toLowerCase();const topic = $('#question-topic').value;const type = $('#question-type').value;const track = $('#question-track').value;
      selected = library.questions.filter(q => (!query || `${q.ID} ${q.Question}`.toLowerCase().includes(query)) && (!topic || q.Topic === topic) && (!type || q.Category === type) && (!track || q.Track === 'All' || q.Track.split('/').includes(track)));
      page = Math.min(page,Math.max(0,Math.ceil(selected.length / size)-1));
      $('#questions').innerHTML = selected.length ? selected.slice(page*size,(page+1)*size).map(questionCard).join('') : '<div class="empty-state">No questions match these filters.</div>';
      $('#question-count').textContent = `${selected.length} questions · answers start hidden`;
      $('#question-page').textContent = `Page ${page+1} of ${Math.max(1,Math.ceil(selected.length / size))}`;
      $('#questions-prev').disabled = page === 0;$('#questions-next').disabled = (page+1)*size >= selected.length;
    }
    $('#question-search').addEventListener('input',() => draw(true));['#question-topic','#question-type','#question-track'].forEach(id => $(id).addEventListener('change',() => draw(true)));
    $('#questions-prev').addEventListener('click',() => {page--;draw();window.scrollTo({top:0,behavior:'smooth'});});$('#questions-next').addEventListener('click',() => {page++;draw();window.scrollTo({top:0,behavior:'smooth'});});draw();
  }
  function projectsPage() {
    main.innerHTML = `<div class="page"><div class="eyebrow">Project workshop</div><h1 class="page-title">From a small library to a complete system.</h1><p class="page-intro">Five basic, five intermediate, three advanced, and two capstone projects. B01 includes the reference implementation and executed tests; the remaining projects are specifications for future work.</p><div class="toolbar"><select class="filter-select" id="project-level" aria-label="Filter project level"><option value="">All project levels</option><option value="01_Basic">Basic</option><option value="02_Intermediate">Intermediate</option><option value="03_Advanced">Advanced</option><option value="04_Capstone">Capstone</option></select><a class="button" href="${routeDoc('01_Learning_Roadmap/project_plan.csv')}">${icon('chart')} View the project matrix</a><a class="button" href="${routeSection('07_Projects')}">All project files →</a></div><div class="project-grid" id="projects"></div></div>`;
    function draw(){const level = $('#project-level').value;$('#projects').innerHTML = library.projects.filter(p => !level || p.Level === level).map(project => `<article class="project-card"><div class="question-top"><span class="project-id">${esc(project.ID)}</span><span class="tag neutral">${esc(project.Level.split('_').slice(1).join(' '))}</span><span class="tag ${project.ID === 'B01' ? '' : 'amber'}">${project.ID === 'B01' ? 'Implementation & tests' : 'Specification · code pending'}</span></div><h2>${esc(project.Project)}</h2><p>${esc(project.Acceptance)}</p><div class="project-info"><span>${esc(project.Hours)} estimated project hours</span><a href="${routeDoc(project.Folder+'/README.md')}">Open project →</a></div></article>`).join('');}
    $('#project-level').addEventListener('change',draw);draw();
  }
  function allPage(section = '') {
    const files = library.files.filter(f => (!section || f.section === section));
    main.innerHTML = `<div class="page reader-page"><div class="eyebrow">Continuous reading</div><h1 class="page-title">${section ? esc(sectionInfo(section).label) : 'The whole library, in one place.'}</h1><p class="page-intro">Move through your material without opening separate files. Tables, code, datasets, and compiled Word copies expand when you need them. Assessment answer keys require a deliberate reveal.</p><div class="toolbar"><select id="reading-section" class="filter-select" aria-label="Choose continuous reading section"><option value="">All sections</option>${library.sections.map(s => `<option value="${s.id}"${s.id === section ? ' selected' : ''}>${esc(s.label)}</option>`).join('')}</select><span class="result-label">${files.length} files in this reading view</span></div><div id="all-content"></div></div>`;
    const target = $('#all-content');
    files.forEach((file,index) => {
      const wrap = document.createElement('section');wrap.className = 'document read-all-section';
      const header = document.createElement('div');header.className = 'read-all-header';header.innerHTML = `<h2>${esc(file.title)}</h2><a href="${routeDoc(file.path)}">Open chapter ↗</a>`;
      const path = document.createElement('p');path.className = 'source-path';path.textContent = file.path;
      wrap.append(header,path);
      if(file.kind !== 'markdown' || file.answer || file.path.endsWith('questions_only.md')){
        const details = document.createElement('details');const summary = document.createElement('summary');summary.textContent = file.answer ? 'Open assessment answer key' : `Read ${fileLabel(file).toLowerCase()}`;
        details.append(summary);let loaded = false;
        details.addEventListener('toggle',() => {if(details.open && !loaded){const body = document.createElement('div');details.append(body);fileContent(body,file,`all-${index}-`);loaded = true;}});wrap.append(details);
      }else{const body = document.createElement('div');fileContent(body,file,`all-${index}-`);wrap.append(body);}
      target.append(wrap);
    });
    $('#reading-section').addEventListener('change',event => location.hash = '#view/all' + (event.target.value ? '?section='+encodeURIComponent(event.target.value) : ''));
  }
  function route(){
    activeObserver?.disconnect();activeObserver = null;currentPath = '';currentSection = '';
    document.body.classList.remove('nav-open');$('#mobile-menu').setAttribute('aria-expanded','false');
    if($('#detail-dialog').open)$('#detail-dialog').close();
    let hash = location.hash.slice(1) || 'home';const questionIndex = hash.indexOf('?');const params = new URLSearchParams(questionIndex >= 0 ? hash.slice(questionIndex+1) : '');hash = questionIndex >= 0 ? hash.slice(0,questionIndex) : hash;
    let view = 'home';
    try{
      if(hash.startsWith('doc/')){view = 'doc';currentPath = decodeURIComponent(hash.slice(4));currentSection = byPath.get(currentPath)?.section || '';documentPage(currentPath,params.get('h') || '');}
      else if(hash.startsWith('section/')){view = 'section';currentSection = decodeURIComponent(hash.slice(8));sectionPage(currentSection);}
      else if(hash === 'view/interviews'){view = 'interviews';currentSection = '02_Interview_Questions_and_Answers';interviewPage();}
      else if(hash === 'view/projects'){view = 'projects';currentSection = '07_Projects';projectsPage();}
      else if(hash === 'view/bookmarks'){view = 'bookmarks';sectionPage('',true);}
      else if(hash === 'view/all'){view = 'all';currentSection = params.get('section') || '';allPage(currentSection);}
      else home();
    }catch(error){console.error(error);main.innerHTML = '<div class="page"><h1 class="page-title">This page could not be displayed.</h1><p class="page-intro">Refresh the library and try again. Your original learning files are unchanged.</p><a class="button" href="#home">Return home</a></div>';}
    renderNavigation(view);$('#topbar-label').textContent = currentSection ? sectionInfo(currentSection).label.toUpperCase() : 'THE LEARNING ROOM';
    document.title = (currentPath ? byPath.get(currentPath)?.title + ' — ' : '') + 'Fieldnotes · Embedded Systems';
    if(!params.get('h'))window.scrollTo({top:0,behavior:'instant'});
  }
  function excerpt(text,query){
    const index = text.toLowerCase().indexOf(query);const start = Math.max(0,index-65);return (start ? '…' : '') + text.slice(start,start+190).replace(/\s+/g,' ') + '…';
  }
  function highlight(text,query){
    if(!query)return esc(text);let result = '';let cursor = 0;let index;const lower = text.toLowerCase();
    while((index = lower.indexOf(query,cursor)) >= 0){result += esc(text.slice(cursor,index)) + '<mark>' + esc(text.slice(index,index+query.length)) + '</mark>';cursor = index + query.length;}
    return result + esc(text.slice(cursor));
  }
  function search(){
    const query = $('#global-search').value.trim().toLowerCase();const target = $('#search-results');
    if(query.length < 2){target.innerHTML = '<div class="empty-state">Type at least two characters. Try “ownership”, “DMA”, or “Q153”.</div>';return;}
    const results = [];
    library.questions.forEach(q => {if(`${q.ID} ${q.Question}`.toLowerCase().includes(query))results.push({title:`${q.ID} · ${q.Question}`,text:q.Topic,href:'#view/interviews',question:q.ID});});
    library.files.filter(f => !f.answer && !questionTopic(f) && f.kind !== 'word' && !f.path.endsWith('bank.json')).forEach(file => {
      if(`${file.title} ${file.path} ${file.text}`.toLowerCase().includes(query))results.push({title:file.title,text:excerpt(file.text,query),href:routeDoc(file.path),path:file.path});
    });
    results.sort((a,b) => Number(b.title.toLowerCase().includes(query))-Number(a.title.toLowerCase().includes(query)));
    target.innerHTML = `<div class="search-hint">${results.length} results${results.length > 45 ? ' · showing the first 45' : ''}</div>` + results.slice(0,45).map((result,index) => `<button class="search-result" data-result="${index}"><strong>${highlight(result.title,query)}</strong><small>${esc(result.path || 'Interview question')}</small><p>${highlight(result.text,query)}</p></button>`).join('');
    if(!results.length)target.innerHTML += '<div class="empty-state">No matches. Try a different term or refresh newly added content.</div>';
    target.querySelectorAll('[data-result]').forEach(button => button.addEventListener('click',() => {
      const result = results[Number(button.dataset.result)];$('#search-dialog').close();
      if(result.question){location.hash = '#view/interviews';if(location.hash === '#view/interviews' && !$('#question-search'))route();setTimeout(() => {$('#question-search').value = result.question;$('#question-search').dispatchEvent(new Event('input'));},0);}
      else location.hash = result.href;
    }));
  }
  function openSearch(){if(!$('#search-dialog').open)$('#search-dialog').showModal();search();$('#global-search').focus();}
  $('#open-search').addEventListener('click',openSearch);$('#close-search').addEventListener('click',() => $('#search-dialog').close());
  let searchTimer;$('#global-search').addEventListener('input',() => {clearTimeout(searchTimer);searchTimer = setTimeout(search,120);});
  $('#search-dialog').addEventListener('click',event => {if(event.target === $('#search-dialog'))$('#search-dialog').close();});
  $('#close-detail').addEventListener('click',() => $('#detail-dialog').close());
  document.addEventListener('click',event => {if(event.target.closest('[data-close-detail]'))$('#detail-dialog').close();});
  document.addEventListener('keydown',event => {
    if((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k'){event.preventDefault();openSearch();}
    if(event.key === 'Escape'){document.body.classList.remove('nav-open');$('#mobile-menu').setAttribute('aria-expanded','false');}
  });
  $('#theme-toggle').addEventListener('click',() => {prefs.theme = prefs.theme === 'dark' ? 'light' : 'dark';applyPreferences();save();});
  $('#font-minus').addEventListener('click',() => {prefs.font = Math.max(15,prefs.font-1);applyPreferences();save();});
  $('#font-plus').addEventListener('click',() => {prefs.font = Math.min(22,prefs.font+1);applyPreferences();save();});
  $('#focus-mode').innerHTML = icon('focus');$('#focus-mode').addEventListener('click',event => {const active = document.body.classList.toggle('focus');event.currentTarget.setAttribute('aria-pressed',active);});
  $('#mobile-menu').innerHTML = icon('menu');$('#mobile-menu').addEventListener('click',() => {const open = document.body.classList.toggle('nav-open');$('#mobile-menu').setAttribute('aria-expanded',open);});
  $('#mobile-shade').addEventListener('click',() => {document.body.classList.remove('nav-open');$('#mobile-menu').setAttribute('aria-expanded','false');});
  $('#about-reader').addEventListener('click',() => {
    const notices = JSON.parse($('#third-party-notices').textContent);
    detail('About this reading room',`<div class="prose"><p>All learning content comes from your existing <code>${esc(library.sourceFolder)}</code> folder. The reader keeps those files unchanged.</p><p>Open <code>index.html</code> for offline reading. Run <code>refresh.cmd</code> after editing course files, or <code>start_live.cmd</code> for refresh directly in the application. Reading marks and bookmarks are browser preferences, not skill scores.</p><p>Markdown rendering uses Marked 16.4.2 and DOMPurify 3.3.0, bundled locally. Their license notices are included below.</p></div>` + Object.entries(notices).map(([name,text]) => `<details class="json-summary"><summary>${esc(name)} · license notice</summary><pre>${esc(text)}</pre></details>`).join(''));
  });
  $('#refresh-library').addEventListener('click',async event => {
    if(!isLive){detail('Refresh your reading room','<div class="prose"><p>This HTML file contains an offline snapshot of your learning folder.</p><p>After editing or adding learning material, double-click <code>Learning_Reader/refresh.cmd</code>, or run:</p><pre><code>python Learning_Reader/build_reader.py</code></pre><p>For a reader that can reload the source folder directly, run <code>Learning_Reader/start_live.cmd</code> and open <code>http://127.0.0.1:8765</code>.</p><p>These commands read the original files; they only update this separate reader.</p></div>');return;}
    const button = event.currentTarget;button.disabled = true;
    try{const response = await fetch('/api/library',{cache:'no-store'});if(!response.ok)throw new Error('Live reader endpoint unavailable');const refreshed = await response.json();if(!Array.isArray(refreshed.files))throw new Error('Invalid library');library = refreshed;byPath = new Map(library.files.map(file => [file.path,file]));revealedAnswers.clear();route();notify('Library refreshed from your original learning folder.');}
    catch(_){notify('Run the included serve.py for live refresh, or refresh.cmd to rebuild the offline reader.');}finally{button.disabled = false;}
  });
  $('.search-icon').innerHTML = icon('search');$('#search-symbol').innerHTML = icon('search');
  window.addEventListener('hashchange',route);
  applyPreferences();route();
})();
