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
    status.textContent = historical ? 'Historical prompt copied. Current corrections and the new research gate still apply.' : 'Current brief copied. No experiment has been started or task reserved.';
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

// Motion enhances an already readable page. No content waits for this code.
// Entrances start only when observed, and never run again on re-entry.
const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
if (!motionPreference.matches && 'IntersectionObserver' in window) {
  const hero = document.querySelector('.hero');
  if (hero) hero.classList.add('has-entrance');
  const arrivals = [...document.querySelectorAll('[data-arrive]')];
  const observer = new IntersectionObserver(entries => {
    let order = 0;
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      const item = entry.target;
      observer.unobserve(item);
      if (motionPreference.matches) continue;
      item.classList.add('arrived', `arrival-delay-${order++ % 4}`);
      item.addEventListener('animationend', () => item.classList.add('arrival-complete'), {once: true});
    }
  }, {threshold: 0.12, rootMargin: '0px 0px -28px 0px'});
  arrivals.forEach(item => observer.observe(item));

  const photograph = document.querySelector('.masthead-photo');
  let photographVisible = false;
  const updateDrift = () => photograph?.classList.toggle('photo-running', photographVisible && document.visibilityState === 'visible' && !motionPreference.matches);
  const photographObserver = new IntersectionObserver(entries => {
    photographVisible = entries.some(entry => entry.isIntersecting);
    updateDrift();
  }, {threshold: 0.05});
  if (photograph) {
    photograph.classList.add('photo-drift');
    photographObserver.observe(photograph);
    document.addEventListener('visibilitychange', updateDrift);
  }
  motionPreference.addEventListener('change', event => {
    if (!event.matches) return;
    hero?.classList.remove('has-entrance');
    arrivals.forEach(item => item.classList.add('arrival-complete'));
    observer.disconnect();
    photographObserver.disconnect();
    photograph?.classList.remove('photo-drift', 'photo-running');
    document.removeEventListener('visibilitychange', updateDrift);
  });
}

if(document.modelContext?.registerTool){const lifecycle=new AbortController();window.addEventListener('pagehide',()=>lifecycle.abort(),{once:true});for(const tool of [{name:'get_research_prompt',description:'Read the unchanged historical prompt on an archived research-task page. It predates the current baseline and does not authorize new work or create a claim.',inputSchema:{type:'object',properties:{},additionalProperties:false},annotations:{readOnlyHint:true,untrustedContentHint:false},execute(input){if(!input||typeof input!=='object'||Object.keys(input).length)throw new Error('No arguments accepted.');let prompt=document.querySelector('#prompt');if(!prompt)throw new Error('Open a research-question page first.');return {prompt:prompt.value,archived:true,currentBrief:'/contribute',claimed:false};}},{name:'filter_research_questions',description:'Filter the historical research-task archive by type, original effort, and archival status.',inputSchema:{type:'object',properties:{kind:{type:'string'},effort:{type:'string'},availability:{type:'string'}},additionalProperties:false},annotations:{readOnlyHint:true,untrustedContentHint:false},execute(input){if(!input||Object.keys(input).some(x=>!['kind','effort','availability'].includes(x)))throw new Error('Invalid filters.');for(const [key,value]of Object.entries(input)){const el=document.querySelector('#'+key);if(!el||![...el.options].some(o=>o.value===value))throw new Error('Unknown filter value.');}for(const [key,value]of Object.entries(input))document.querySelector('#'+key).value=value;filters();return {visible:[...document.querySelectorAll('[data-question]')].filter(el=>!el.hidden).map(el=>el.dataset.id)};}}])try{Promise.resolve(document.modelContext.registerTool(tool,{signal:lifecycle.signal})).catch(()=>{});}catch{}}
