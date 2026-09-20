from pathlib import Path
from html import escape
import json
import shutil
from site_config import ROOT, DIST, DOCS, CONSOLE, REGISTRY, with_base_path
from unified import site_document, build_knowledge_pages, build_doc_redirects, load_posts, post_row

DIST.mkdir(parents=True, exist_ok=True)
if DIST != ROOT/'dist':
    shutil.copytree(ROOT/'dist/assets', DIST/'assets', dirs_exist_ok=True)
GITHUB='https://github.com/gachon-CCLab/FedOps'
# Resolve documentation links in shared navigation and authored page fragments.
DOC_LINKS={
    '/document/': DOCS,
    '/document/overview/': DOCS,
    '/document/task-owner/create-task/': DOCS+'v1.3/task-owner/create-task/',
    '/document/#resources': DOCS+'v1.3/resources/',
    **{f'/document/{slug}/': DOCS+f'v1.3/{slug}/' for slug in (
        'getting-started', 'task-owner', 'participant', 'agent-builder',
        'campaign', 'developer-guide',
    )},
}
NOTION='https://aspiring-space-882.notion.site/'
MAIN_DOC=NOTION+'3ce03357516780c78118e1ea39e0345c'
MANUALS=[
('00','Getting Started','Prepare Agent Studio, sign in, and get your local workspace ready.','00_Getting_Started-3da0335751678023850eef5f7937e734'),
('01','Create a New Task','Start as a Task Owner: prepare your model, create a release, and publish your Task.','01_Owner_Web_First_Task-3da0335751678009a92df657bb917cbd'),
('02','Import a Local Model','Bring an existing model into the Federated Task lifecycle.','02_Owner_Local_First_Task-3da0335751678045becbf0300d8c8c67'),
('03','Participant: Join & FL','Find a Task, request access, prepare local data, and start your FL Client.','03_Participant_Join_and_FederatedLearning-3da033575167804da2e6c3397c4446ca'),
('04','Agent Builder & Serving','Select model versions, validate your Agent, and use local chat or a Serving API.','04_Agent_Builder_and_Serving-3da03357516780779055c078fc38e50f'),
('05','Campaign & Server Management','Configure a Campaign, operate the FL Server, and follow training results.','05_Operator_Campaing_and_ServerManage-3da03357516780ea9c2dce76690dd869'),
]
def external(url,label,cls='text-link'):
    return f'<a class="{cls}" href="{escape(url,quote=True)}" target="_blank" rel="noopener noreferrer">{label}<span aria-hidden="true">↗</span><span class="sr-only"> (opens in a new tab)</span></a>'
def brand():
    return '<a class="brand" href="/version-2/"><span class="brandmark" aria-hidden="true"></span>FedOps</a>'
def page(path,title,description,body,section=''):
    # Docs stay in the separately maintained GitHub Pages documentation.
    content=site_document(title,description,body,section or 'home')
    for local_url, docs_url in DOC_LINKS.items():
        content=content.replace(f'href="{local_url}"', f'href="{docs_url}"')
    out=DIST/path
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(with_base_path(content),encoding='utf-8')

def head(kicker,title,description):
    return f'<section class="page-head"><div class="wrap"><p class="eyebrow">{kicker}</p><h1>{title}</h1><p>{description}</p></div></section>'

screens=json.loads((ROOT/'work/screens.json').read_text(encoding='utf-8'))
labels=[('Home','Choose your workflow'),('Prepare','Workspace & readiness'),('Register','Models & versions'),('Build','Agent composition'),('Serve','Local use & API'),('Improve','Training history')]
tabs=''.join(f'<button class="product-tab" id="product-tab-{i}" role="tab" aria-selected="{str(i==0).lower()}" aria-controls="productPanel" tabindex="{0 if i==0 else -1}" data-image="/assets/{s["image"]}" data-title="{escape(s["title"],quote=True)}" data-copy="{escape(s["description"],quote=True)}"><b>0{i+1} · {labels[i][0]}</b><span>{labels[i][1]}</span></button>' for i,s in enumerate(screens))
architecture=[
('01 / COORDINATE','FedOps Console','Publish Tasks, approve participants, configure Campaigns, and monitor training.',CONSOLE,'Open Console'),
('02 / WORK LOCALLY','Agent Studio','Prepare local data and models, join federated learning, and build your Agent.','/document/getting-started/','Get started'),
('03 / TRAIN TOGETHER','FL Server','Coordinate training rounds and aggregate model updates into Global Models.','/document/task-owner/create-task/','Read the guide'),
('04 / FIND & REUSE','Registry','Discover published Tasks and follow model versions back to their source.',REGISTRY,'Open Registry'),
]
def arch_link(url,label):
    if url.startswith(('https://', 'http://')): return external(url,label)
    return '<a class="text-link" href="'+url+'">'+label+' <span aria-hidden="true">→</span></a>'
arch=''.join(f'<article class="architecture-card"><span class="number">{n}</span><h3>{name}</h3><p>{desc}</p>{arch_link(url,label)}</article>' for n,name,desc,url,label in architecture)
steps=[('Create & Register','Prepare a local model and publish a Federated Task with an Initiative Model.'),('Load & Join','Request access to a Task and prepare your approved release locally.'),('Federated Learning','Train on local data and send model updates for aggregation.'),('Global Model','Track the results of each Campaign as a new model version.'),('Build & Serve','Pin model versions in an Agent Build, then use local chat or an API.'),('Improve','Retrain a selected model, validate it, and build a new Agent revision.')]
step_html=''.join(f'<article class="step"><b>0{i+1}</b><h3>{name}</h3><p>{desc}</p></article>' for i,(name,desc) in enumerate(steps))
news_row=''.join(post_row(post,'news') for post in load_posts(ROOT,'news')[:2]) or '<p>There are no published updates yet.</p>'
why_section='''
<section class="section why-section" id="whyfedops"><div class="wrap">
<p class="eyebrow">Federated learning operations</p><h2 class="section-title">Why FedOps?</h2>
<div class="why-grid">
<article class="why-item"><span class="number">01</span><h3>Start with your models &amp; data</h3><p>Prepare code, connect local data, and train a model in Agent Studio.</p></article>
<article class="why-item"><span class="number">02</span><h3>Coordinate learning together</h3><p>Use Console to manage Tasks, participation, Campaigns, and training progress.</p></article>
<article class="why-item"><span class="number">03</span><h3>Make models reusable</h3><p>Discover published Tasks and trace model versions back to their Releases and training runs in the Registry.</p></article>
<article class="why-item"><span class="number">04</span><h3>Bring models into an Agent</h3><p>Select the model versions for an Agent Build, validate it, and use local chat or a Serving API.</p></article>
<article class="why-item"><span class="number">05</span><h3>Keep improving deliberately</h3><p>Retrain a selected model, review the outcome, and create a new Agent revision when it is ready.</p></article>
</div>
<div class="design-partners" aria-labelledby="partner-title"><h2 id="partner-title" class="eyebrow">Design Partner</h2>
<div class="partner-logos"><img src="/assets/gachon.jpeg" alt="Gachon University" width="225" height="225" loading="lazy"><img src="/assets/flower.png" alt="Flower Framework" width="225" height="225" loading="lazy"><img src="/assets/cambridge.png" alt="University of Cambridge" width="225" height="225" loading="lazy"></div>
<p>A unified approach to federated learning, analytics, and evaluation. Federate any workload, any ML framework, and any programming language.</p></div>
</div></section>
'''
flower_profile=json.loads((ROOT/'work/flower-profile.json').read_text(encoding='utf-8'))
flower_stats=f'''<div class="gfedops-summary"><div class="gfedops-summary-title"><p class="eyebrow">GACHON CCL ON FLOWER HUB</p><h3>gfedops Apps</h3><p>Reusable apps for the Flower community.</p></div><dl class="gfedops-stats"><div><dt>Created Apps</dt><dd>{flower_profile["created_apps"]}</dd></div><div><dt>Total Stars</dt><dd>{flower_profile["total_stars"]}</dd></div></dl><div class="gfedops-summary-link">{external(flower_profile['url'],'Explore all apps')}<span>As of {flower_profile['checked_on']}</span></div></div>'''

ecosystem_section=f'''
<section class="section ecosystem" id="ecosystem"><div class="wrap ecosystem-layout"><div class="ecosystem-overview">
<div class="ecosystem-intro"><div><p class="eyebrow">Contributing to Flower</p><h2>Built with Flower.<br><span>Extended by Gachon CCL.</span></h2></div><div class="ecosystem-copy"><p>Gachon Cognitive Computing Lab turns FedOps research and real-world federated workflows into reusable Flower Apps, then validates federated fine-tuning methods through FlowerTune’s public benchmarks.</p><div class="actions">{external('https://flower.ai/profile/gfedops/apps','View @gfedops on Flower Hub','button ecosystem-primary')}{external('https://flower.ai/apps','Explore Flower Apps','button ecosystem-secondary')}</div></div></div>
{flower_stats}
</div><div class="ecosystem-evidence">
<div class="evidence-shell"><div class="evidence-tabs" role="tablist" aria-label="Gachon CCL contributions on Flower">
<button class="evidence-tab" id="evidence-tab-0" role="tab" aria-selected="true" aria-controls="evidencePanel" tabindex="0" data-image="/assets/hub-mnist.webp" data-title="FedOps MNIST XAI on Flower Hub" data-copy="A reusable FedOps client app for federated MNIST training with optional Grad-CAM explanations." data-link="https://flower.ai/apps/gfedops/fedops-mnist-xai"><b>01 · Flower Hub</b><span>MNIST + XAI</span></button>
<button class="evidence-tab" id="evidence-tab-1" role="tab" aria-selected="false" aria-controls="evidencePanel" tabindex="-1" data-image="/assets/hub-multimodal.webp" data-title="FedOps Multimodal on Flower Hub" data-copy="A Flower-native app for heterogeneous multimodal federated learning on Hateful Memes." data-link="https://flower.ai/apps/gfedops/fedops-multimodal"><b>02 · Flower Hub</b><span>Multimodal FL</span></button>
<button class="evidence-tab" id="evidence-tab-2" role="tab" aria-selected="false" aria-controls="evidencePanel" tabindex="-1" data-image="/assets/leaderboard-nlp.webp" data-title="General NLP · Rank 02" data-copy="Gachon Cognitive Computing Lab scores 69.19 average on the public FlowerTune General NLP leaderboard." data-link="https://flower.ai/benchmarks/llm-leaderboard/nlp"><b>03 · FlowerTune</b><span>General NLP · Rank 02</span></button>
<button class="evidence-tab" id="evidence-tab-3" role="tab" aria-selected="false" aria-controls="evidencePanel" tabindex="-1" data-image="/assets/leaderboard-medical.webp" data-title="Medical · Rank 04" data-copy="Gachon Cognitive Computing Lab scores 62.12 average on the public FlowerTune Medical leaderboard." data-link="https://flower.ai/benchmarks/llm-leaderboard/medical"><b>04 · FlowerTune</b><span>Medical · Rank 04</span></button>
</div><figure class="evidence-frame" id="evidencePanel" role="tabpanel" aria-labelledby="evidence-tab-0" tabindex="0"><div class="browser-bar" aria-hidden="true"><i></i><i></i><i></i><span>flower.ai · public evidence</span></div><div class="evidence-viewport"><img id="evidenceImage" class="evidence-image" src="/assets/hub-mnist.webp" alt="Flower Hub page for the @gfedops/fedops-mnist-xai app" width="1400" height="788" loading="eager"></div><figcaption class="evidence-caption"><div><b id="evidenceTitle">FedOps MNIST XAI on Flower Hub</b><p id="evidenceCopy">A reusable FedOps client app for federated MNIST training with optional Grad-CAM explanations.</p></div><a id="evidenceLink" href="https://flower.ai/apps/gfedops/fedops-mnist-xai" target="_blank" rel="noopener noreferrer">View source <span aria-hidden="true">↗</span><span class="sr-only"> (opens in a new tab)</span></a></figcaption></figure></div>
<p class="evidence-note">Flower public pages · captured September 2026. Open the source for current results.</p>
</div></div></section>
'''
home=f'''
<section class="hero"><div class="wrap"><div class="hero-grid"><div><p class="eyebrow light">Federated AI AgentOps Platform</p><h1>Build Agents.<br><span>Federate Intelligence.</span><br>Improve Continuously.</h1><p class="lead"><strong>FedOps 1.3</strong> connects local AI development, federated learning, versioned model assets, and Agent delivery in one governed lifecycle. Organizations learn together while raw data remains under each participant’s control.</p><div class="actions"><a class="button primary" href="/document/getting-started/">Get Started <span aria-hidden="true">→</span></a>{external(CONSOLE,'FedOps Console','button secondary')}</div></div><figure class="hero-architecture"><a href="/assets/main_v2png.png" target="_blank" rel="noopener noreferrer" aria-label="Open the FedOps architecture diagram at full size (opens in a new tab)"><img src="/assets/main_v2png.png" alt="FedOps Web manages Registry model assets and Server aggregation, connected to local Agent Studio training and Agent serving for your application." width="1536" height="1024" fetchpriority="high" decoding="async"><span class="hero-diagram-hint">View full diagram <span aria-hidden="true">↗</span></span></a></figure></div></div></section>
{why_section}
<section class="section product-showcase" id="product"><div class="wrap"><div class="intro"><div><p class="eyebrow">Inside Agent Studio</p><h2>One workspace.<br><span>From model to Agent.</span></h2></div><p>Follow the work from a local project to a reusable model and an Agent Build. Each step stays connected to the Task and model versions behind it.</p></div><div class="product-shell"><div class="product-tabs" role="tablist" aria-label="Agent Studio screens">{tabs}</div><div><figure class="product-frame" id="productPanel" role="tabpanel" aria-labelledby="product-tab-0" tabindex="0"><div class="browser-bar" aria-hidden="true"><i></i><i></i><i></i><span>FedOps Agent Studio</span></div><img id="productImage" class="product-image" src="/assets/{screens[0]['image']}" alt="FedOps Agent Studio home — development screen" width="1920" height="1080" loading="lazy"><figcaption class="product-caption"><b id="productTitle">{escape(screens[0]['title'])}</b><p id="productCopy">{escape(screens[0]['description'])}</p></figcaption></figure><p class="product-note">FedOps 1.3 development screens. Interfaces and workflows may change before release.</p></div></div></div></section>
<section class="section dark" id="architecture"><div class="wrap"><div class="intro"><div><p class="eyebrow light">How it connects</p><h2>Shared coordination.<br><span>Local execution.</span></h2></div><p>Four components connect the workflow. Your workspace handles local data and execution; shared services coordinate participation and model reuse.</p></div><div class="architecture-grid">{arch}</div></div></section>
<section class="section" id="lifecycle"><div class="wrap"><div class="intro"><div><p class="eyebrow">The lifecycle</p><h2>Train together.<br><span>Build on the result.</span></h2></div><p>Federated learning creates a model you can use again. Agent Builds keep the selected versions fixed while new models are trained and evaluated.</p></div><div class="steps">{step_html}</div><div class="model-note"><strong>A new model. A deliberate update.</strong><p>A new Global Model does not silently replace a running Agent. Select the new version, validate it, and build a new revision.</p></div></div></section>
{ecosystem_section}
<section class="section start-section" id="start"><div class="wrap"><p class="eyebrow">Choose your starting point</p><h2 class="section-title">Your next step with FedOps.</h2><div class="start-grid"><article class="start-card"><span class="number">FOR TASK OWNERS</span><h3>Bring a model.<br>Start a shared Task.</h3><p>Prepare your local project, create an Initiative Model, and publish a Task for others to join.</p><a class="text-link" href="/document/task-owner/">Create a Federated Task <span aria-hidden="true">→</span></a></article><article class="start-card"><span class="number">FOR PARTICIPANTS</span><h3>Find a Task.<br>Contribute locally.</h3><p>Request access to a published Task and train with your own data from Agent Studio.</p><a class="text-link" href="/document/participant/">Join federated learning <span aria-hidden="true">→</span></a></article></div></div></section>
<section class="section" id="news"><div class="wrap"><div class="news-header"><div><p class="eyebrow">News & updates</p><h2 class="section-title">What’s next for FedOps.</h2></div><a class="text-link" href="/news/">All news <span aria-hidden="true">→</span></a></div>{news_row}</div></section>
<section class="cta community" id="joincommunity"><div class="wrap"><h2>Join our Community!</h2><p>Join us on our journey to make federated approaches available to everyone.</p><div class="actions">{external("https://join.slack.com/t/fedopshq/shared_invite/zt-3h73abys7-ms07FlAVG7EP2108BzevcA", "Join our Slack", "button primary")}<a class="button secondary" href="/document/getting-started/">Read the Getting Started guide <span aria-hidden="true">→</span></a></div></div></section>
'''
page(Path('index.html'),'FedOps 1.3 — Federated AI AgentOps','Local model development, federated learning, and AI Agent delivery in one connected lifecycle.',home)

# Keep the existing fallback page; build the knowledge area from shared templates.
for entry in (ROOT/'pages').glob('*.json'):
    spec=json.loads(entry.read_text(encoding='utf-8'))
    if spec['section'] in ('document','blog','news'):
        continue
    body=(ROOT/'pages'/spec['body']).read_text(encoding='utf-8')
    page(Path(spec['path']),spec['title'],spec['description'],body,spec['section'])
# Preserve the selected homepage URL, with the same branding on every route.
homepage=(DIST/'index.html').read_text(encoding='utf-8')
preview=homepage
destination=DIST/'version-2'/'index.html'
destination.parent.mkdir(parents=True,exist_ok=True)
destination.write_text(preview,encoding='utf-8')
build_knowledge_pages(ROOT,page)
build_doc_redirects(ROOT,DOC_LINKS)
print('Built homepage and Git-authored Blog/News; Docs link to the existing manual.')
