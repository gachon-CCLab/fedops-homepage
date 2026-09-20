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
document.querySelectorAll('.contribution-card').forEach(card=>{
  const contributionTabs=[...card.querySelectorAll('.contribution-tabs [role="tab"]')];
  const panel=card.querySelector('.contribution-preview');
  if(!panel||!contributionTabs.length)return;
  function activateContribution(tab,focus=false){
    contributionTabs.forEach(t=>{const chosen=t===tab;t.setAttribute('aria-selected',String(chosen));t.tabIndex=chosen?0:-1;});
    const image=panel.querySelector('.contribution-image');
    image.src=tab.dataset.image;
    image.alt=tab.dataset.title+' — captured from Flower public pages';
    panel.querySelector('.contribution-title').textContent=tab.dataset.title;
    panel.querySelector('.contribution-source').href=tab.dataset.link;
    panel.setAttribute('aria-labelledby',tab.id);
    if(focus)tab.focus();
  }
  contributionTabs.forEach((tab,index)=>{
    tab.addEventListener('click',()=>activateContribution(tab));
    tab.addEventListener('keydown',e=>{let target=index;if(['ArrowRight','ArrowDown'].includes(e.key))target=(index+1)%contributionTabs.length;else if(['ArrowLeft','ArrowUp'].includes(e.key))target=(index-1+contributionTabs.length)%contributionTabs.length;else if(e.key==='Home')target=0;else if(e.key==='End')target=contributionTabs.length-1;else return;e.preventDefault();activateContribution(contributionTabs[target],true);});
  });
});
const contributionSwitcher=document.querySelector('.contribution-switcher');
if(contributionSwitcher){
  const buttons=[...contributionSwitcher.querySelectorAll('button')];
  const mobile=window.matchMedia('(max-width:700px)');
  let active=buttons[0].getAttribute('aria-controls');
  function showContributions(){
    buttons.forEach(button=>{
      const chosen=button.getAttribute('aria-controls')===active;
      button.setAttribute('aria-pressed',String(chosen));
      document.getElementById(button.getAttribute('aria-controls')).hidden=mobile.matches&&!chosen;
    });
  }
  buttons.forEach(button=>button.addEventListener('click',()=>{active=button.getAttribute('aria-controls');showContributions();}));
  mobile.addEventListener('change',showContributions);
  showContributions();
}
