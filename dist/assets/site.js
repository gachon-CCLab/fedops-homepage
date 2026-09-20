const menuButton=document.querySelector('.menu-toggle');
const menu=document.querySelector('.nav-links');
if(menuButton&&menu){
  const close=()=>{menu.classList.remove('open');menuButton.setAttribute('aria-expanded','false');menuButton.textContent='Menu';};
  menuButton.addEventListener('click',()=>{const open=menuButton.getAttribute('aria-expanded')!=='true';menuButton.setAttribute('aria-expanded',String(open));menu.classList.toggle('open',open);menuButton.textContent=open?'Close':'Menu';});
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu.classList.contains('open')){close();menuButton.focus();}});
  menu.querySelectorAll('a').forEach(a=>a.addEventListener('click',close));
  window.matchMedia('(min-width:851px)').addEventListener('change',e=>{if(e.matches)close();});
}
const tabs=[...document.querySelectorAll('.product-tab')];
function activate(tab,focus=false){
  tabs.forEach(t=>{const chosen=t===tab;t.setAttribute('aria-selected',String(chosen));t.tabIndex=chosen?0:-1;});
  const image=document.getElementById('productImage');image.src=tab.dataset.image;image.alt=tab.dataset.title+' — FedOps 1.3 development screen';
  document.getElementById('productTitle').textContent=tab.dataset.title;
  document.getElementById('productCopy').textContent=tab.dataset.copy;
  document.getElementById('productPanel').setAttribute('aria-labelledby',tab.id);
  if(focus)tab.focus();
}
tabs.forEach((tab,index)=>{
  tab.addEventListener('click',()=>activate(tab));
  tab.addEventListener('keydown',e=>{let target=index;if(['ArrowRight','ArrowDown'].includes(e.key))target=(index+1)%tabs.length;else if(['ArrowLeft','ArrowUp'].includes(e.key))target=(index-1+tabs.length)%tabs.length;else if(e.key==='Home')target=0;else if(e.key==='End')target=tabs.length-1;else return;e.preventDefault();activate(tabs[target],true);});
});
const evidenceTabs=[...document.querySelectorAll('.evidence-tab')];
function activateEvidence(tab,focus=false){
  evidenceTabs.forEach(t=>{const chosen=t===tab;t.setAttribute('aria-selected',String(chosen));t.tabIndex=chosen?0:-1;});
  const image=document.getElementById('evidenceImage');
  image.src=tab.dataset.image;
  image.alt=tab.dataset.title+' — captured from Flower public pages';
  document.getElementById('evidenceTitle').textContent=tab.dataset.title;
  document.getElementById('evidenceCopy').textContent=tab.dataset.copy;
  document.getElementById('evidenceLink').href=tab.dataset.link;
  document.getElementById('evidencePanel').setAttribute('aria-labelledby',tab.id);
  if(focus)tab.focus();
}
evidenceTabs.forEach((tab,index)=>{
  tab.addEventListener('click',()=>activateEvidence(tab));
  tab.addEventListener('keydown',e=>{let target=index;if(['ArrowRight','ArrowDown'].includes(e.key))target=(index+1)%evidenceTabs.length;else if(['ArrowLeft','ArrowUp'].includes(e.key))target=(index-1+evidenceTabs.length)%evidenceTabs.length;else if(e.key==='Home')target=0;else if(e.key==='End')target=evidenceTabs.length-1;else return;e.preventDefault();activateEvidence(evidenceTabs[target],true);});
});
