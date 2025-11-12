
// 主交互逻辑：菜单、搜索、遮罩、暗色模式、随机诗
(function(){
  const menuBtn = document.getElementById('menuBtn');
  const sidebar = document.getElementById('sidebar');
  const backdrop = document.getElementById('backdrop');
  const searchBtn = document.getElementById('searchBtn');
  const searchPanel = document.getElementById('searchPanel');
  const searchInput = document.getElementById('searchInput');
  const toggleDarkMode = document.getElementById('toggleDarkMode');
  const randomPoemBtn = document.getElementById('randomPoemBtn');
  const poemLinks = Array.from(document.querySelectorAll('.poem-list a'));

  function openSidebar(){
    sidebar.classList.add('open');
    sidebar.setAttribute('aria-hidden','false');
    menuBtn.setAttribute('aria-expanded','true');
    backdrop.classList.add('visible');
    backdrop.setAttribute('aria-hidden','false');
    const first = sidebar.querySelector('a,button'); if(first) first.focus();
  }
  function closeSidebar(){
    sidebar.classList.remove('open');
    sidebar.setAttribute('aria-hidden','true');
    menuBtn.setAttribute('aria-expanded','false');
    backdrop.classList.remove('visible');
    backdrop.setAttribute('aria-hidden','true');
    menuBtn.focus();
  }

  function openSearch(){
    searchPanel.setAttribute('aria-hidden','false');
    searchPanel.classList.add('open');
    searchBtn.setAttribute('aria-expanded','true');
    if(searchInput) searchInput.focus();
  }
  function closeSearch(){
    searchPanel.setAttribute('aria-hidden','true');
    searchPanel.classList.remove('open');
    searchBtn.setAttribute('aria-expanded','false');
    searchBtn.focus();
  }

  menuBtn && menuBtn.addEventListener('click', ()=>{
    sidebar.classList.contains('open') ? closeSidebar() : openSidebar();
  });

  backdrop && backdrop.addEventListener('click', ()=>{ closeSidebar(); closeSearch(); });

  searchBtn && searchBtn.addEventListener('click', ()=>{
    searchPanel && (searchPanel.classList.contains('open') ? closeSearch() : openSearch());
  });

  document.addEventListener('keydown', (e)=>{
    if(e.key === 'Escape'){
      closeSidebar(); closeSearch();
    }
  });

  searchInput && searchInput.addEventListener('keydown', (e)=>{
    if(e.key === 'Enter'){
      const q = searchInput.value.trim().toLowerCase();
      if(!q) return;
      const match = poemLinks.find(a=>a.textContent.toLowerCase().includes(q) || (a.dataset.excerpt && a.dataset.excerpt.toLowerCase().includes(q)));
      if(match) window.location = match.href;
      else {
        searchInput.setAttribute('aria-invalid','true');
        setTimeout(()=>searchInput.removeAttribute('aria-invalid'), 1000);
      }
    }
    if(e.key === 'Escape') closeSearch();
  });

  // 暗色主题持久化
  function applyTheme(t){
    if(t === 'dark') document.documentElement.setAttribute('data-theme','dark');
    else document.documentElement.removeAttribute('data-theme');
    toggleDarkMode && toggleDarkMode.setAttribute('aria-pressed', t === 'dark');
  }
  const saved = localStorage.getItem('site-theme'); if(saved) applyTheme(saved);
  toggleDarkMode && toggleDarkMode.addEventListener('click', ()=>{
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const next = isDark ? 'light' : 'dark';
    localStorage.setItem('site-theme', next);
    applyTheme(next);
  });

  // 随机跳转
  randomPoemBtn && randomPoemBtn.addEventListener('click', ()=>{
    if(poemLinks.length === 0) return;
    const idx = Math.floor(Math.random()*poemLinks.length);
    window.location = poemLinks[idx].href;
  });

  // 侧边栏 focus trap
  sidebar && sidebar.addEventListener('keydown', (e)=>{
    if(e.key === 'Tab'){
      const focusables = Array.from(sidebar.querySelectorAll('a,button')).filter(el=>!el.disabled);
      if(focusables.length === 0) return;
      const first = focusables[0];
      const last = focusables[focusables.length-1];
      if(e.shiftKey && document.activeElement === first){ e.preventDefault(); last.focus(); }
      else if(!e.shiftKey && document.activeElement === last){ e.preventDefault(); first.focus(); }
    }
  });
})();
