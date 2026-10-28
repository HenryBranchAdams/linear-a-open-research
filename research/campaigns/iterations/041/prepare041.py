from pathlib import Path
import json, hashlib, shutil, zipfile

BASE = Path(__file__).resolve().parent
OLD = BASE / 'Linear_A_Campaign_040'
NEW = BASE / 'Linear_A_Campaign_041'
WORK = BASE / 'iteration041'

def read(path):
    return json.loads(path.read_text())

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

sources = [
    {
        'id':'C041-S01', 'title':'Nikolakopoulou2019, Akrotiri, Thera. Middle Bronze Age Pottery and Stratigraphy, volumeI (including Hilditch, PhasesB-C)',
        'url':'https://www.archetai.gr/images/pdfs/bae/BAE_318.pdf',
        'access':'Official full PDF acquired; selected target/mark/fabric passages, sample concordance and recorded macroscopic tables inspected; not a claim to have read every page',
        'sha256':'0ccd138b1b2fd2885f22516573e08ab373cf338c5bdc28d7256ffe64ccc50b52',
        'size_bytes':73120857, 'pdf_pages':561,
        'decisive_locators':['printed203','printed220','Hilditch377–470, especially378/402 and Table3.23 at458–461'],
        'access_history':'040 UvA metadata-only access is superseded for availability by041 official publisher full PDF, found via actual publisher catalogue hyperlink',
        'limits':'Same exposed carriers; no target specimen-register join or new assay. Integer sample IDs are not AKR/ACV aliases.',
        'authored_record':'iterations/041/agents/SOURCE_ROUTE.md'
    },
    {
        'id':'C041-S02', 'title':'Nikolakopoulou2019, Akrotiri, Thera. Middle Bronze Age Pottery and Stratigraphy, volumeII catalogue and plates',
        'url':'https://www.archetai.gr/images/pdfs/bae/BAE_319.pdf',
        'access':'Official full PDF acquired; exact entries/plate121/plateLVII/concordance inspected as actual pixels',
        'sha256':'3a9a22ab23de0e939a6e3153907300948c45effcee20942af973a3981b34ee73',
        'size_bytes':36676561, 'pdf_pages':633,
        'decisive_locators':['printed258–259, entries1121/1122','printed543, plateLVII','printed609, inventory/context concordance'],
        'limits':'Inventory identification and source measurements; no target residue result or second measured volume',
        'authored_record':'iterations/041/evidence/CATALOGUE_OVERLAY.json'
    },
    {
        'id':'C041-S03', 'aliases':['C041-OBJ-S02'],
        'title':'Roumpou et al.2013, An interdisciplinary approach to the study of cooking vessels from Bronze Age Akrotiri, Thera',
        'url':'https://www.academia.edu/4944783/An_interdisciplinary_approach_to_the_study_of_cooking_vessels_from_Bronze_Age_Akrotiri_Thera',
        'access':'Substantive author-hosted searchable body and Table1 transcription inspected; actual table pixels not inspected; local HTML download returned403',
        'decisive_locators':['methods35–36','Table1 at39–40','interpretation41–44'],
        'finding':'Positive-result subset provides17 ACV-to-AKR code pairings; no target inventory join recovered in inspected records',
        'limits':'Selected positives, not full38-sherd inventory or marked-vessel census. No transfer to9384/9730. Plain Hilditch sample integers belong to a separate namespace.',
        'authored_record':'iterations/041/agents/OBJECT_EVIDENCE.md'
    },
    {
        'id':'C041-S04', 'title':'Roumpou, Kylikoglou and Kalogeropoulos2021, Organic residues in pottery and cooking areas at Akrotiri',
        'url':'https://www.santorini.net/wp-content/uploads/akrotiri-40years-contents-1.pdf',
        'access':'Contents/bibliographic navigation only; bounded exact-title/author/institution/author-profile routes did not acquire article; zero article pages inspected',
        'locator_status':'Contents starts375; Nestor bibliography reports374–381 versus target375–382. Original pagination not adjudicated.',
        'limits':'Not global unavailability, not rejection of unseen scientific argument',
        'authored_record':'iterations/041/agents/OBJECT_EVIDENCE.md'
    }
]

claims = [{
    'id':'LA-041-001', 'iteration':41, 'updated_date':'2026-10-23',
    'claim':'The original2019 Akrotiri catalogue securely maps1121 to9384 and1122 to9730, refines source-specific rim measurements and qualifies mark/use history. The inspected sample concordance does not furnish a direct exact-target analytical join; the pair still does not provide a crossed independent manufacture/content comparison.',
    'disposition':'catalogue_source_qualification_retained_exact_analytical_binding_unrecovered',
    'evidence_kind':'original_catalogue_entries_actual_plates_and_bounded_sample_concordance_check',
    'witnesses':['Akrotiri9384/catalogue1121','Akrotiri9730/catalogue1122'],
    'evidence_path':'iterations/041/evidence/CATALOGUE_OVERLAY.json',
    'additional_evidence_paths':['iterations/041/agents/SOURCE_ROUTE.md','iterations/041/agents/challenger/REVIEW.md','iterations/041/analysis/JOIN_DECISION.md'],
    'dependencies':['C041-S01','C041-S02','C041-S03','LA-040-001'],
    'basis_and_limits':'2019 outer/inner rim values and later approximate rim accounts remain separate; older tentativeAB9/27 comparison does not refute laterAB81 attribution. No target use diagnosis from fabric label or neighboring soot. No exact join in inspected Table3.23; blank cells, numbering gaps and separate sample namespaces prohibit a never-sampled inference.',
    'strongest_rival':'Contents/use and production-related marking remain unresolved; technical contrast grounds production rival but identifies no workshop. Recipient remains timing-compatible without independent order evidence.',
    'evidence_needed_to_reopen_or_advance':'Exact inventory/catalogue-to-specimen register or documented refit/photo join, diagnostic use data at the relevant temporal/resolution scope, and comparison separating manufacture from content/use; consequential surface evidence can separately refine reading.',
    'evidence_access_level':'Official full2019 PDFs acquired, selected target/plate/concordance actual pixels inspected independently;2013 author-hosted table transcription, no table pixels;2021 residue article zero pages.',
    'action_meaning':None, 'participant_role':None, 'new_semantic_relationship':False,
    'new_testable_linguistic_prediction':False, 'new_to_scholarship':False,
    'novelty':'New project source access and controlled catalogue/sample-link evaluation; no new ancient carrier or semantic identification.',
    'campaign_archive':'iterations/041/Linear_A_Campaign_041.zip'
}]

experiments = [
    {
        'id':'C041-CATALOGUE-SAMPLE-LINK', 'iteration':41, 'status':'completed',
        'kind':'bounded primary-source and exact specimen-link feasibility inquiry',
        'title':'Akrotiri9384/9730 catalogue and manufacturing concordance',
        'input':['C041-S01','C041-S02','LA-040-001'],
        'method':'Original inventory/catalogue mapping, separate measurement/reading histories, actual image-only concordance check and independent challenge; recorded remaining macrotable inspection.',
        'outputs':['iterations/041/evidence/CATALOGUE_OVERLAY.json','iterations/041/agents/SOURCE_ROUTE.md','iterations/041/agents/challenger/REVIEW.md'],
        'finding':'Original catalogue access obtained; precise object controls retained. No exact target analytical join recovered in inspected records.',
        'limitations':'Published-table scope, blank cells and sample-number gaps; no never-sampled inference, autopsy, new assay or independent ancient witness.',
        'semantic_experiment_admitted':False,'new_semantic_relationship':False,'new_testable_linguistic_prediction':False,
        'archive':'iterations/041/Linear_A_Campaign_041.zip'
    },
    {
        'id':'C041-RESIDUE-ACCESS-AND-CROSSWALK', 'iteration':41, 'status':'completed',
        'kind':'bounded acquisition and analytical-code crosswalk feasibility',
        'title':'Exact Akrotiri contents/use route',
        'input':['C041-S03','C041-S04'],
        'method':'Exact title/author institutional and author-hosted route checks; transcribe positive-result ACV↔AKR table; require inventory link independent of mark.',
        'outputs':['iterations/041/agents/OBJECT_EVIDENCE.md','iterations/041/agents/RESIDUE_SAMPLE_CROSSWALK.json','iterations/041/analysis/JOIN_DECISION.md'],
        'finding':'17 positive-result code pairs retained, no exact targets joined.2021 full chapter not acquired in checked routes; zero article pages.',
        'limitations':'Text-transcription access to2013, no actual table pixels; positive subset not full sample census; broad lipids/coatings do not identify specific contents.',
        'semantic_experiment_admitted':False,'new_semantic_relationship':False,'new_testable_linguistic_prediction':False,
        'archive':'iterations/041/Linear_A_Campaign_041.zip'
    }
]

for name, additions, total in [('claims.json',claims,85),('experiments.json',experiments,36),('sources.json',sources,113)]:
    data=read(OLD/'registry'/name)
    if isinstance(data,dict):
        prior=data['claims']; data['claims']=prior+additions; data['updated_date']='2026-10-23'; count=len(data['claims'])
    else:
        data=data+additions; count=len(data)
    assert count==total,(name,count)
    write(NEW/'registry'/name,data)
    write(WORK/'registry_additions'/name,additions)

write(WORK/'evidence/SOURCE_RECORDS.json',sources)
write(WORK/'SOURCE_CAPTURE_MANIFEST.json',{
    'campaign':'LA-C041-2026-10-23',
    'sources':[{'id':s['id'], **{k:s[k] for k in ['url','sha256','size_bytes','pdf_pages','access'] if k in s}} for s in sources],
    'redistribution':'Full third-party publications and temporary source page renders excluded; authored records and factual source locators retained',
    'pdf_page_mapping':'For target2019 pages, printed page+1=one-basedPDF page. Page labels in UI or zero-based scripts must be distinguished.'
})

write(WORK/'STATE_DELTA.json',{
    'campaign_id':'LA-C041-2026-10-23',
    'authority_before':'B2026-10-18 plusC038/C039/C040',
    'authority_after':'B2026-10-18 plusC038/C039/C040/C041',
    'status':'completed_stopped',
    'claim_changes':[{'id':'LA-041-001','before':'Original2019 exact catalogue/analytical concordance not adjudicated','after':claims[0]['disposition']}],
    'evidence_levels':{'access':'Official complete2019 volumes acquired;2021 residue article not acquired','reading_object_control':'Exact catalogue aliases, measurement convention and historical mark qualifications','physical_constraint':'No new assay/volume measurement','semantic_discrimination':None,'linguistic_replication':None,'mission_construction':None},
    'active_candidates':0,'deep_inquiries_completed':1,'semantic_experiments_admitted':0,'new_ancient_objects':0,
    'registry_additions':{'claims':1,'access_feasibility_records':2,'sources':4},
    'expected_totals':{'claims':85,'access_feasibility_records':36,'sources':113},
    'stop':'Exact target analytical/use binding unrecovered in finite inspected packet; no crossed comparison executable',
    'independence':'New modern sources and reviewers, same exposed carriers; no unused linguistic prediction',
    'external_actions':[]
})

# Only authored records enter the portable checkpoint. Raw source bytes remain outside it.
dest=NEW/'iterations/041'
for f in WORK.rglob('*'):
    rel=f.relative_to(WORK)
    if f.is_file() and f.suffix in {'.md','.json'} and not any(x in rel.parts for x in ['raw','lead_views','object_raw']):
        out=dest/rel; out.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(f,out)
shutil.copy2(BASE/'prepare041.py',dest/'prepare041.py')
print(json.dumps({'registry_totals':[85,36,113],'authored_records_staged':len(list(dest.rglob('*'))),'pending':'Final review, current navigation, manifest and archive checks'}))
