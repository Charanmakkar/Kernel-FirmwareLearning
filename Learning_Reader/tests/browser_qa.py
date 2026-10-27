"""Headless acceptance checks with a disposable browser profile.

Only for developer QA; the reader needs neither Playwright nor a browser install.
"""
from pathlib import Path
import json
import sys
import time
import urllib.error
import urllib.request

APP=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(APP/'.qa/python'))
from playwright.sync_api import sync_playwright, expect

BASE='http://127.0.0.1:8765'
EVIDENCE=APP/'evidence'
EVIDENCE.mkdir(exist_ok=True)
checks=[]
errors=[]
def passed(name):
    checks.append({'test':name,'result':'passed'})
    print('PASS',name,flush=True)

with sync_playwright() as playwright:
    browser=playwright.chromium.launch(executable_path='C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless=True,args=['--disable-gpu'])
    context=browser.new_context(viewport={'width':1440,'height':1050},device_scale_factor=1)
    page=context.new_page()
    page.on('pageerror',lambda error:errors.append(str(error)))
    response=page.goto(BASE,wait_until='networkidle')
    assert response.status==200
    expect(page.get_by_role('heading',name='Your embedded engineering library.')).to_be_visible()
    assert page.locator('.stat-number').all_text_contents()==['88','64','200','15']
    page.screenshot(path=str(EVIDENCE/'home_desktop.png'),full_page=True)
    passed('desktop home and complete library counts')

    page.get_by_role('link',name='Read the lesson').click()
    expect(page.locator('#document-content h2').first).to_be_visible()
    expect(page.locator('#document-toc a')).not_to_have_count(0)
    assert page.locator('#document-content .code-wrap').count()>0
    page.screenshot(path=str(EVIDENCE/'lesson_desktop.png'),full_page=True)
    passed('Markdown lesson, code blocks and table of contents')

    before=page.locator('html').evaluate("element => getComputedStyle(element).getPropertyValue('--reading-size')")
    page.get_by_role('button',name='Increase reading text size').click()
    after=page.locator('html').evaluate("element => getComputedStyle(element).getPropertyValue('--reading-size')")
    assert before!=after
    page.get_by_role('button',name='Toggle focus mode').click()
    assert 'focus' in (page.locator('body').get_attribute('class') or '')
    page.get_by_role('button',name='Toggle focus mode').click()
    passed('text sizing and focused reading layout')

    page.get_by_role('button',name='Save',exact=True).click()
    page.get_by_role('button',name='Mark read',exact=True).click()
    page.reload(wait_until='networkidle')
    expect(page.get_by_role('button',name='Saved',exact=True)).to_have_attribute('aria-pressed','true')
    expect(page.get_by_role('button',name='Read',exact=True)).to_have_attribute('aria-pressed','true')
    passed('bookmark and reading state survive reload')

    page.get_by_role('button',name='Search the library Ctrl K').click()
    page.get_by_role('searchbox',name='Search all learning content').fill('ownership')
    expect(page.locator('.search-result').first).to_be_visible()
    assert not page.locator('.search-result').filter(has_text='D01 key and remediation').count()
    page.get_by_role('button',name='Close search').click()
    passed('full-content search and answer-key exclusion')

    page.goto(BASE+'/#view/interviews')
    expect(page.locator('.question-card')).to_have_count(10)
    assert page.locator('.question-card details[open]').count()==0
    page.locator('.question-card summary').first.click()
    expect(page.locator('.spoken-answer').first).to_be_visible()
    page.get_by_label('Filter by question type').select_option('coding')
    expect(page.locator('#question-count')).to_contain_text('44 questions')
    page.get_by_label('Filter by role track').select_option('FW')
    assert page.locator('.question-card').count()>0
    page.screenshot(path=str(EVIDENCE/'interviews_desktop.png'),full_page=True)
    passed('interview reveal, category and role filters')

    page.goto(BASE+'/#doc/02_Interview_Questions_and_Answers%2F001_010_C_objects_and_ownership.md')
    page.locator('#document-toc a').first.click()
    assert page.locator('#reader-heading-0').count()==1
    passed('interview topic table of contents targets actual headings')

    page.goto(BASE+'/#doc/01_Learning_Roadmap%2Froadmap_64_weeks.csv')
    expect(page.locator('.data-table tbody tr')).to_have_count(64)
    page.get_by_role('searchbox',name='Filter table rows').fill('Objects, arrays')
    expect(page.locator('.data-table tbody tr')).to_have_count(1)
    page.locator('.data-table tbody tr').click()
    expect(page.locator('#detail-dialog')).to_be_visible()
    expect(page.locator('#detail-content')).to_contain_text('Objective exit test')
    page.get_by_role('button',name='Close details').click()
    page.get_by_role('button',name='Show all columns').click()
    expect(page.locator('.data-table th')).to_have_count(13)
    passed('CSV filter, full row details and all columns')

    page.goto(BASE+'/#doc/04_Skill_Assessments%2Fanswer_keys%2FD01_Key.md')
    expect(page.get_by_role('button',name='Reveal this answer key')).to_be_visible()
    assert page.locator('#document-content').get_by_text('C25:',exact=False).count()==0
    page.get_by_role('button',name='Reveal this answer key').click()
    expect(page.locator('#document-content')).to_contain_text('C25:')
    passed('assessment answer key requires deliberate reveal')

    page.goto(BASE+'/#view/projects')
    expect(page.locator('.project-card')).to_have_count(15)
    page.get_by_label('Filter project level').select_option('03_Advanced')
    expect(page.locator('.project-card')).to_have_count(3)
    passed('all 15 project specifications and level filter')

    page.goto(BASE+'/#doc/07_Projects%2F01_Basic%2FB01_Embedded_C_Utility_Library%2Finclude%2Fembedded_util.h')
    expect(page.locator('pre')).to_contain_text('eu_packet_decode')
    page.goto(BASE+'/#doc/07_Projects%2F01_Basic%2FB01_Embedded_C_Utility_Library%2Fevidence%2Fhost.json')
    expect(page.locator('#document-content')).to_contain_text('passed')
    page.goto(BASE+'/#doc/Word_Edition%2FAssessment_Questions_Release_1.docx')
    expect(page.locator('.word-text')).to_contain_text('Q200')
    passed('source, executed evidence and extracted Word content')

    page.goto(BASE+'/#view/all?section=00_Start_Here')
    expect(page.locator('.read-all-section')).to_have_count(2)
    expect(page.locator('#all-content')).to_contain_text('Environment and target policy')
    passed('continuous section reading')

    page.goto(BASE+'/#view/all')
    expect(page.locator('.read-all-section')).to_have_count(88)
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    passed('continuous reading includes every distributable file')

    page.goto(BASE)
    page.get_by_role('button',name='Refresh content').click()
    expect(page.locator('#toast')).to_contain_text('Library refreshed')
    page.get_by_role('button',name='Switch to dark theme').click()
    expect(page.locator('html')).to_have_attribute('data-theme','dark')
    page.screenshot(path=str(EVIDENCE/'home_dark.png'),full_page=True)
    passed('live refresh and dark theme')

    page.set_viewport_size({'width':390,'height':844})
    page.get_by_role('button',name='Open navigation').click()
    expect(page.locator('#sidebar')).to_be_in_viewport()
    page.get_by_role('link',name='Lessons & skills').click()
    expect(page.locator('body')).not_to_have_class('nav-open')
    page.goto(BASE)
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    page.screenshot(path=str(EVIDENCE/'home_mobile.png'),full_page=True)
    passed('mobile navigation and no horizontal page overflow')

    offline=context.new_page()
    offline.on('pageerror',lambda error:errors.append(str(error)))
    offline.goto((APP/'index.html').as_uri(),wait_until='load')
    expect(offline.get_by_role('heading',name='Your embedded engineering library.')).to_be_visible()
    offline.get_by_role('link',name='Read the lesson').click()
    expect(offline.locator('#document-content')).to_contain_text('C11')
    offline.get_by_role('button',name='Refresh content').click()
    expect(offline.locator('#detail-dialog')).to_contain_text('refresh.cmd')
    passed('direct file opening works offline without a server')

    offline.get_by_role('button',name='Close details').click()
    offline.get_by_role('button',name='About this reader').click()
    expect(offline.locator('#detail-content')).to_contain_text('DOMPurify 3.3.0')
    passed('offline help and embedded third-party license notices')

    for attack in ['/materials/%2e%2e/README.md','/materials/%2e%2e/%2e%2e/LICENSE']:
        try:
            urllib.request.urlopen(BASE+attack)
            raise AssertionError('Traversal was not rejected')
        except urllib.error.HTTPError as error:
            assert error.code==404
    passed('live server rejects paths outside the learning folder')
    assert not errors,errors
    passed('no browser JavaScript errors')
    browser.close()

(EVIDENCE/'browser_qa.json').write_text(json.dumps({'browser':'Microsoft Edge, headless, disposable profile','checks':checks,'javascriptErrors':errors},indent=2)+'\n',encoding='utf-8')
print('All browser checks passed.',flush=True)
