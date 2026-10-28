// All reading content and the two HT34 cases are usable without JavaScript.
const live = Object.fromEntries([...document.querySelectorAll('[data-question]')].map(row => [row.dataset.id, {state: 'archived'}]));
function filters() {
  const kind = document.querySelector('#kind')?.value;
  const effort = document.querySelector('#effort')?.value;
  const state = document.querySelector('#availability')?.value;
  let count = 0;
  document.querySelectorAll('[data-question]').forEach(row => {
    const show = (!kind || row.dataset.kind === kind) && (!effort || row.dataset.effort === effort) && (!state || live[row.dataset.id]?.state === state);
    row.hidden = !show; if (show) count++;
  });
  const empty = document.querySelector('#filter-empty'); if (empty) empty.hidden = count !== 0;
}
document.querySelectorAll('.filters select').forEach(select => select.addEventListener('change', filters));

// Archival availability is an editorial disposition, not a live claim state.
// We do not poll and overwrite it with a database slot's former availability.
document.querySelectorAll('[data-copy]').forEach(button => button.addEventListener('click', async () => {
  const field = document.getElementById(button.dataset.copy);
  const scope = button.closest('details') || button.closest('section');
  const status = scope.querySelector('.copy-status');
  const historical = button.dataset.copy === 'prompt';
  try {
    await navigator.clipboard.writeText(field.value);
    status.textContent = button.dataset.copyMessage || (historical ? 'Historical prompt copied. Current corrections and the new research gate still apply.' : 'Current brief copied. No experiment has been started or task reserved.');
  } catch {
    const disclosure = field.closest('details'); if (disclosure) disclosure.open = true;
    field.focus(); field.select();
    status.textContent = 'The text is selected. Copy it manually. No experiment has been started or task reserved.';
  }
}));

const search = document.querySelector('#file-search');
if (search) search.addEventListener('input', () => {
  const query = search.value.trim().toLowerCase(); let count = 0;
  document.querySelectorAll('[data-file]').forEach(row => {
    row.hidden = !row.dataset.file.includes(query); if (!row.hidden) count++;
  });
  document.querySelector('#file-count').textContent = `${count} ${count === 1 ? 'file matches' : 'files match'}${query ? ' your search' : ' this index'}.`;
});

const controls = document.querySelector('[data-demo-controls]');
if (controls) {
  const interpretation = document.getElementById('interpretation');
  const stories = {neutral: ['Part A', 'Part B'], paid: ['Paid', 'Unpaid'], allocated: ['Allocated', 'Unallocated'], issued: ['Issued', 'Retained']};
  function updateExample() {
    const reading = controls.querySelector('input[name=reading]:checked').value;
    const labels = stories[interpretation.value] || stories.neutral;
    document.querySelectorAll('[data-case]').forEach(item => item.hidden = reading !== 'both' && item.dataset.case !== reading);
    document.querySelector('.equation-grid').classList.toggle('is-single', reading !== 'both');
    document.querySelectorAll('[data-label-a]').forEach(label => label.textContent = labels[0]);
    document.querySelectorAll('[data-label-b]').forEach(label => label.textContent = labels[1]);
    const consequence = reading === '37' ? '70 + 37 = 107. This rejects the exact complement under the stated assumptions; it does not select a meaning.' : reading === '30' ? '70 + 30 = 100. The complement fits under the stated assumptions; its meaning remains open.' : 'The 30 branch gives 100; the 37 branch gives 107. The reading changes the arithmetic, while meaning still needs independent evidence.';
    const story = interpretation.value === 'neutral' ? 'The labels are neutral quantities.' : `“${labels[0]} / ${labels[1]}” is an illustrative hypothesis, not a translation. Changing the labels adds no evidence.`;
    document.getElementById('demo-feedback').textContent = `${consequence} ${story}`;
  }
  controls.addEventListener('change', updateExample);
  controls.hidden = false;
  updateExample();
}

const mobileMenu = document.querySelector('.mobile-nav');
if (mobileMenu) {
  document.addEventListener('keydown', event => {if (event.key === 'Escape' && mobileMenu.open) {mobileMenu.open = false; mobileMenu.querySelector('summary').focus();}});
  document.addEventListener('click', event => {if (mobileMenu.open && !mobileMenu.contains(event.target)) mobileMenu.open = false;});
  mobileMenu.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {mobileMenu.open = false;}));
}

// The research record is static. Controls provide direct feedback without scroll or entrance animation.

// A portable contribution is useful before a visitor decides where to submit it.
const draftForm = document.getElementById('contribution-draft');
if (draftForm) {
  const storageKey = 'linear-a-contribution-draft-v1';
  const keys = ['mission','title','target','body','sources','method','uncertainty','exposure','credit','license','relatedId'];
  const status = document.getElementById('draft-status');
  const guidance = {
    source: 'A citation, access route and the page or figure that matters. A missing-source lead can be enough.',
    correction: 'The exact claim, your correction and supporting evidence. Identify what changes and what still holds.',
    reproduction: 'Input version, commands, actual output and any mismatch. Reproducing an exposed result is different from unused validation.',
    review: 'The work you reviewed, checks you performed and remaining uncertainty. Your review is public evidence for others to assess.',
    idea: 'Serious alternatives, a separating observation and a finite checking route. Explain what would stop the investigation.',
  };
  function values() { return Object.fromEntries(keys.map(key => [key, draftForm.elements.namedItem(key).value])); }
  function setRequirements() {
    const type = draftForm.elements.namedItem('mission').value;
    document.getElementById('draft-guidance').textContent = guidance[type] || guidance.source;
    draftForm.elements.namedItem('target').required = ['correction','reproduction','review'].includes(type);
    draftForm.elements.namedItem('method').required = ['reproduction','review'].includes(type);
  }
  function saveDraft() {
    try { localStorage.setItem(storageKey, JSON.stringify(values())); status.textContent = 'Draft saved on this browser. It has not been submitted.'; }
    catch { status.textContent = 'This browser cannot save the draft. Download a copy before leaving.'; }
  }
  try {
    const saved = JSON.parse(localStorage.getItem(storageKey) || 'null');
    if (saved && typeof saved === 'object') {
      for (const key of keys) {
        const control = draftForm.elements.namedItem(key);
        if (typeof saved[key] === 'string') {
          if (control.tagName === 'SELECT' && ![...control.options].some(option => option.value === saved[key])) continue;
          control.value = saved[key].slice(0, control.maxLength > 0 ? control.maxLength : 40000);
        }
      }
      status.textContent = 'Your draft was restored on this browser. Nothing has been submitted.';
    }
  } catch { status.textContent = 'Local draft storage is unavailable. You can still write and download a copy.'; }
  const routeParams = new URLSearchParams(location.search);
  if (routeParams.has('type')) draftForm.elements.namedItem('mission').value = draftForm.dataset.draftType;
  if (draftForm.dataset.draftRelated) {
    draftForm.elements.namedItem('relatedId').value = draftForm.dataset.draftRelated;
    draftForm.elements.namedItem('target').value = location.origin + '/contributions/' + draftForm.dataset.draftRelated;
    status.textContent = 'Independent review linked to the selected contribution. Any saved draft text is retained for you to check.';
  }
  setRequirements();
  draftForm.addEventListener('input', () => {setRequirements(); saveDraft();});
  draftForm.addEventListener('change', () => {setRequirements(); saveDraft();});
  draftForm.addEventListener('submit', saveDraft);
  document.querySelectorAll('a[href*="/signin-with-chatgpt"],a[href^="/profile"]').forEach(link => link.addEventListener('click', saveDraft));
  document.querySelectorAll('[data-contribution-type]').forEach(link => link.addEventListener('click', event => {
    event.preventDefault();
    draftForm.elements.namedItem('mission').value = link.dataset.contributionType;
    setRequirements(); saveDraft();
    history.replaceState(null, '', link.getAttribute('href'));
    document.getElementById('draft').scrollIntoView({block:'start'});
    document.getElementById('draft-title').focus({preventScroll:true});
  }));
  function markdownDraft(data) {
    const labels = {target:'Evidence or claim',body:'Contribution',sources:'Sources and provenance',method:'Checks and reproduction',uncertainty:'Alternatives and limits',exposure:'Prior exposure',credit:'Credit and assistance'};
    return '# ' + (data.title || 'Untitled contribution') + '\n\n' +
      'Contribution type: ' + data.mission + '\nBaseline: C044 / D2026-10-26\nStatus: Draft — not submitted or reviewed\n\n' +
      Object.entries(labels).map(([key,label]) => '## ' + label + '\n\n' + (data[key] || 'Not declared.') + '\n').join('\n') +
      '\n## Related contribution\n\n' + (data.relatedId ? 'https://linear-a-open-research.madebyhenry.chatgpt.site/contributions/' + data.relatedId : 'None specified.') +
      '\n\n## Reuse permission\n\n' + data.license + ' for my original text. Referenced material retains its own rights.\n\n' +
      'Prepared from https://linear-a-open-research.madebyhenry.chatgpt.site/contribute. This draft does not create a claim, start an experiment or change the reviewed research record.\n';
  }
  document.querySelectorAll('[data-draft-download]').forEach(button => button.addEventListener('click', () => {
    const data = values(), format = button.dataset.draftDownload;
    const text = format === 'json' ? JSON.stringify({format:'linear-a-contribution-draft',schemaVersion:1,status:'draft',baseline:'C044 / D2026-10-26',...data}, null, 2) : markdownDraft(data);
    const url = URL.createObjectURL(new Blob([text], {type:format === 'json' ? 'application/json' : 'text/markdown;charset=utf-8'}));
    const link = document.createElement('a'); link.href = url; link.download = 'linear-a-' + data.mission + '-draft.' + format;
    document.body.appendChild(link); link.click(); link.remove(); setTimeout(() => URL.revokeObjectURL(url), 1000);
    status.textContent = 'Draft downloaded. It has not been submitted. Keep the sources, credit and reuse terms with your copy.';
  }));
  const github = document.querySelector('[data-github-draft]');
  github.addEventListener('click', event => {
    const data = values();
    const params = new URLSearchParams({template:'research.yml',title:'[Research] '+(data.title||'New contribution')});
    const types = {source:'Source',correction:'Correction',reproduction:'Reproduction',review:'Independent review',idea:'Candidate evidence'};
    const licenses = {'CC-BY-4.0':'CC-BY-4.0 — Creative Commons Attribution 4.0','CC0-1.0':'CC0-1.0 — CC0 1.0 dedication','UNSPECIFIED':'UNSPECIFIED — No additional reuse license'};
    params.set('type',types[data.mission]); params.set('license',licenses[data.license]);
    for (const key of ['target','sources','method','uncertainty','exposure','credit']) if (data[key]) params.set(key,data[key]);
    if (data.body) params.set('evidence',data.body);
    if (data.relatedId) params.set('related','https://linear-a-open-research.madebyhenry.chatgpt.site/contributions/'+data.relatedId);
    const url = 'https://github.com/HenryBranchAdams/linear-a-open-research/issues/new?' + params.toString();
    if (url.length > 7000) {
      event.preventDefault();
      status.textContent = 'This draft is too long for a GitHub prefill link. Download Markdown, then use the empty GitHub form below and paste or attach your draft.';
      let fallback = document.getElementById('github-empty-form');
      if (!fallback) { fallback = document.createElement('a'); fallback.id='github-empty-form'; fallback.href='https://github.com/HenryBranchAdams/linear-a-open-research/issues/new?template=research.yml'; fallback.textContent='Open an empty GitHub contribution form'; fallback.className='text-link'; status.after(fallback); }
      return;
    }
    saveDraft(); github.href = url;
  });
  document.getElementById('clear-draft').addEventListener('click', () => {
    try { localStorage.removeItem(storageKey); } catch {}
    draftForm.reset(); setRequirements();
    status.textContent = 'Saved draft cleared on this browser. Downloaded files and submitted records are unchanged.';
  });
}

if(document.modelContext?.registerTool){const lifecycle=new AbortController();window.addEventListener('pagehide',()=>lifecycle.abort(),{once:true});for(const tool of [{name:'get_research_prompt',description:'Read the unchanged historical prompt on an archived research-task page. It predates the current baseline and does not authorize new work or create a claim.',inputSchema:{type:'object',properties:{},additionalProperties:false},annotations:{readOnlyHint:true,untrustedContentHint:false},execute(input){if(!input||typeof input!=='object'||Object.keys(input).length)throw new Error('No arguments accepted.');let prompt=document.querySelector('#prompt');if(!prompt)throw new Error('Open a research-question page first.');return {prompt:prompt.value,archived:true,currentBrief:'/contribute',claimed:false};}},{name:'filter_research_questions',description:'Filter the historical research-task archive by type, original effort, and archival status.',inputSchema:{type:'object',properties:{kind:{type:'string'},effort:{type:'string'},availability:{type:'string'}},additionalProperties:false},annotations:{readOnlyHint:true,untrustedContentHint:false},execute(input){if(!input||Object.keys(input).some(x=>!['kind','effort','availability'].includes(x)))throw new Error('Invalid filters.');for(const [key,value]of Object.entries(input)){const el=document.querySelector('#'+key);if(!el||![...el.options].some(o=>o.value===value))throw new Error('Unknown filter value.');}for(const [key,value]of Object.entries(input))document.querySelector('#'+key).value=value;filters();return {visible:[...document.querySelectorAll('[data-question]')].filter(el=>!el.hidden).map(el=>el.dataset.id)};}}])try{Promise.resolve(document.modelContext.registerTool(tool,{signal:lifecycle.signal})).catch(()=>{});}catch{}}
