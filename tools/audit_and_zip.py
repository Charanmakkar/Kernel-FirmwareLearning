from pathlib import Path
import csv
import hashlib
import json
import re
import zipfile
import xml.etree.ElementTree as ET

WORKSPACE=Path(__file__).resolve().parents[1]
ROOT=WORKSPACE/'Embedded_Linux_Kernel_Firmware_Learning'
def read_csv(path):
    with (ROOT/path).open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))

checks=[]
def check(name,passed,detail):
    checks.append({'check':name,'passed':bool(passed),'detail':detail})

projects=read_csv('01_Learning_Roadmap/project_plan.csv')
check('project_count',len(projects)==15,len(projects))
distribution={level:sum(p['Level']==level for p in projects) for level in ['01_Basic','02_Intermediate','03_Advanced','04_Capstone']}
check('project_distribution',list(distribution.values())==[5,5,3,2],distribution)
check('unique_project_ids',len({p['ID'] for p in projects})==15,[p['ID'] for p in projects])
check('project_folders',all((ROOT/p['Folder']/'README.md').is_file() for p in projects),'All project README specifications exist')
roadmap=read_csv('01_Learning_Roadmap/roadmap_64_weeks.csv')
check('roadmap',len(roadmap)==64 and sum(int(r['Estimated hours']) for r in roadmap)==704,{'weeks':len(roadmap),'hours':sum(int(r['Estimated hours']) for r in roadmap)})
questions=json.loads((ROOT/'02_Interview_Questions_and_Answers/bank.json').read_text(encoding='utf-8'))
check('questions_count_and_ids',[q['ID'] for q in questions]==[f'Q{n:03d}' for n in range(1,201)],len(questions))
check('distinct_questions',len({q['Question'] for q in questions})==200,'Exact question-text uniqueness')
categories={kind:sum(q['Category']==kind for q in questions) for kind in ['coding','debugging/scenario','system design','code-output analysis','conceptual']}
check('category_minimums',categories['coding']>=25 and categories['debugging/scenario']>=25 and categories['system design']>=10,categories)
check('question_schema',all(all(str(v).strip() for v in q.values()) and len(q)==17 for q in questions),'Every item has 17 nonempty metadata/answer fields')
check('matrix_unassessed',all(r['Current evidence']=='not assessed' and r['Skill gap']=='not assessed' for r in read_csv('03_JD_JR_Skills_and_Learning_Content/reference_skills_matrix.csv')),'No learner scores inferred')
check('tracker_unassessed',all(r['Status']=='not assessed' for r in read_csv('10_Progress_Tracking/skills_tracker.csv')),'Learner progress is not fabricated')

# Bootstrap generated metadata destinations before checking the master index.
# The complete contents are written below, and no ZIP is produced on failure.
for rel,initial in [('10_Progress_Tracking/package_audit.json','{}\n'),('10_Progress_Tracking/file_inventory.csv','Relative path,Bytes,SHA256\n')]:
    target=ROOT/rel
    if not target.exists():target.write_text(initial,encoding='utf-8')

broken=[]
for p in ROOT.rglob('*.md'):
    text=p.read_text(encoding='utf-8')
    for dest in re.findall(r'\[[^\]]+\]\(([^)]+)\)',text):
        if dest.startswith(('https://','http://','mailto:','#')):continue
        target=(p.parent/dest.split('#')[0]).resolve()
        if not target.exists():broken.append({'file':str(p.relative_to(ROOT)),'target':dest})
check('local_markdown_links',not broken,broken)

P=ROOT/'07_Projects/01_Basic/B01_Embedded_C_Utility_Library'
for evidence in ['host.json','sanitize.json']:
    data=json.loads((P/'evidence'/evidence).read_text())
    hashes_match=all(hashlib.sha256((P/path).read_bytes()).hexdigest()==value for path,value in data['source_sha256'].items())
    check('B01_'+evidence,data['result']=='passed' and all(c['returncode']==0 for c in data['commands']) and hashes_match,
          {'result':data['result'],'source_hashes_match':hashes_match,'commands':len(data['commands'])})

documents=[]
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
for p in sorted((ROOT/'Word_Edition').glob('*.docx')):
    if p.name.startswith('~$'):continue
    with zipfile.ZipFile(p) as z:
        valid=z.testzip() is None
        root=ET.fromstring(z.read('word/document.xml'))
        texts=[''.join(par.itertext()) for par in root.findall('.//w:t',ns)]
        alltext=' '.join(texts)
        headings=[]
        for par in root.findall('.//w:p',ns):
            props=par.find('w:pPr',ns)
            if props is not None and props.find('w:pStyle',ns) is not None:
                style=props.find('w:pStyle',ns).get('{'+ns['w']+'}val')
                if style.startswith('Heading'):headings.append(''.join(t.text or '' for t in par.findall('.//w:t',ns)))
        unique_qs=set(re.findall(r'Q\d{3}',alltext))
        check('docx_'+p.name,valid and len(alltext)>1000,{'zip_integrity':valid,'text_chars':len(alltext),'headings':len(headings)})
        if p.name.startswith('Interview_Bank'):
            check('docx_200_answer_headings',sum(bool(re.match(r'Q\d{3} —',h)) for h in headings)==200,{'unique_question_ids':len(unique_qs)})
        documents.append({'file':p.name,'bytes':p.stat().st_size,'heading_count':len(headings),'text_characters':len(alltext)})
check('four_word_editions',len(documents)==4,documents)

render=ROOT/'10_Progress_Tracking/word_render_status.json'
if render.exists():
    rendered=json.loads(render.read_text(encoding='utf-8-sig'))
    if isinstance(rendered,dict):rendered=[rendered]
    check('word_rendering',len(rendered)==4 and all(r['pages']>0 for r in rendered),rendered)
else:checks.append({'check':'word_rendering','passed':None,'detail':'Not performed; XML integrity is not a visual rendering check'})

audit_path=ROOT/'10_Progress_Tracking/package_audit.json'
audit={'release':'1','date':'2026-10-27','full_master_prompt_complete':False,
       'complete_lessons':1,'complete_project_implementations':1,'planned_projects':15,
       'interview_questions':len(questions),'checks':checks,'all_required_structural_checks_passed':all(c['passed'] is not False for c in checks)}
audit_path.write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
if not audit['all_required_structural_checks_passed']:
    print(json.dumps([c for c in checks if c['passed'] is False],indent=2));raise SystemExit(1)

files=sorted(p for p in ROOT.rglob('*') if p.is_file() and 'build' not in p.relative_to(ROOT).parts and not p.name.startswith('~$') and p.name!='file_inventory.csv')
inventory=ROOT/'10_Progress_Tracking/file_inventory.csv'
with inventory.open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=['Relative path','Bytes','SHA256'])
    writer.writeheader()
    for p in files:writer.writerow({'Relative path':p.relative_to(ROOT).as_posix(),'Bytes':p.stat().st_size,'SHA256':hashlib.sha256(p.read_bytes()).hexdigest()})

zip_path=WORKSPACE/'Embedded_Linux_Kernel_Firmware_Learning_Release_1.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and 'build' not in p.relative_to(ROOT).parts and not p.name.startswith('~$'):z.write(p,p.relative_to(WORKSPACE).as_posix())
with zipfile.ZipFile(zip_path) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(files)+1
checksum=hashlib.sha256(zip_path.read_bytes()).hexdigest()
(WORKSPACE/'Embedded_Linux_Kernel_Firmware_Learning_Release_1.sha256').write_text(checksum+'  '+zip_path.name+'\n',encoding='ascii')
print(json.dumps({'audit':'passed','files_in_zip':len(files)+1,'zip_bytes':zip_path.stat().st_size,'zip_sha256':checksum,'path':str(zip_path)},indent=2))
