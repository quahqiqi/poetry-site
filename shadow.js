/*
  影子管家 —— 共用彩蛋逻辑
  原则：不创造内容，只负责发现内容。
  他只出现在阅读之外的缝隙：页面切换、加载完成、搜索无果、深夜、
  节日、404、很久没回来、很久没操作。
  绝不出现在诗歌正文里，绝不弹窗，绝不要求点击，绝不引导任务。
*/

/* ---------- 视觉样式：只加一次 ---------- */
(function injectShadowStyle() {
  const style = document.createElement('style');
  style.textContent = `
    .shadow-whisper{
      position:fixed;
      right:24px;
      bottom:24px;
      font-size:.78rem;
      color:var(--text-muted, #8b7e74);
      opacity:0;
      transition:opacity 1.2s ease;
      pointer-events:none;
      z-index:9999;
      letter-spacing:.05em;
      max-width:220px;
      text-align:right;
    }
    .shadow-whisper.show{ opacity:.75; }

    .shadow-whisper-center{
      right:auto; bottom:auto;
      left:50%; top:50%;
      transform:translate(-50%,-50%);
      text-align:center;
      max-width:280px;
      font-size:.9rem;
      letter-spacing:.3em;
    }
  `;
  document.head.appendChild(style);
})();

/* ---------- 说一句悄悄话，过一会儿自己消失 ----------
   约定：所有弹幕默认走右下角（corner），跟夜间模式那条一致。
   除非有特殊理由，调用时不要传 'center'。
------------------------------------------------------- */
function shadowWhisper(text, duration = 3000, position = 'corner') {
  let el = document.getElementById('shadowWhisper');
  if (!el) {
    el = document.createElement('div');
    el.id = 'shadowWhisper';
    document.body.appendChild(el);
  }
  el.className = 'shadow-whisper' + (position === 'center' ? ' shadow-whisper-center' : '');
  el.textContent = text;
  requestAnimationFrame(() => el.classList.add('show'));
  clearTimeout(el._timer);
  el._timer = setTimeout(() => el.classList.remove('show'), duration);
}

document.addEventListener('DOMContentLoaded', () => {

  /* ========== ⑦ 夜间模式：每次切到夜间都说话 ========== */
  const darkBtn = document.getElementById('darkBtn');
  if (darkBtn) {
    // 注册得比页面原本的 onclick 晚，所以会在切换动作完成之后才触发
    darkBtn.addEventListener('click', () => {
      const isDark = document.body.classList.contains('dark');
      if (isDark) {
        shadowWhisper('灯已经关好了。');
      }
    });
  }

  /* ========== ⑤ 搜索"影子"：查无此人 ========== */
  const searchInput = document.getElementById('searchInput');
  if (searchInput) {
    searchInput.addEventListener('input', () => {
      const q = searchInput.value.trim();
      if (q !== '影子') return;

      // 兼容两种页面结构：toc.html 的下拉列表 / index.html 的主网格
      const resultsDiv = document.getElementById('searchResults');
      const poemsGrid = document.getElementById('poemsGrid');
      const heroPoem = document.getElementById('heroPoem');
      const pagination = document.getElementById('pagination');
      const mainTitle = document.getElementById('mainTitle');
      const latestBadge = document.getElementById('latestBadge');

      // 立刻覆盖掉原本可能渲染出的真实结果（同一帧内完成，不会闪一下）
      if (resultsDiv) resultsDiv.innerHTML = '';
      if (poemsGrid) {
        if (heroPoem) heroPoem.style.display = 'none';
        if (pagination) pagination.innerHTML = '';
        if (mainTitle) mainTitle.innerText = '寻: 影子';
        if (latestBadge) latestBadge.innerText = '共 0 篇';
        poemsGrid.innerHTML = '';
      }

      // 停顿两秒，如果输入没变，才悄悄出现这句话
      setTimeout(() => {
        if (searchInput.value.trim() !== '影子') return;
        const msg = '我不在这里。';
        if (resultsDiv) {
          resultsDiv.innerHTML = `<div style="text-align:center; padding:15px; color:var(--text-muted); font-size:0.9rem; letter-spacing:1px; opacity:.7;">${msg}</div>`;
        }
        if (poemsGrid) {
          poemsGrid.innerHTML = `<p style="grid-column:1/-1;text-align:center;color:var(--text-muted);letter-spacing:2px;margin-top:20px;opacity:.7;">${msg}</p>`;
        }
      }, 2000);
    });
  }

  /* ========== 到底之后：不是滑多远，是"再推几次" ========== */
  const SCROLL_PAGES = ['', 'index.html', 'about.html', 'toc.html'];
  const filename = (location.pathname.split('/').pop() || 'index.html').toLowerCase();

  if (SCROLL_PAGES.includes(filename)) {
    const PUSHES_NEEDED = 5;
    let atBottom = false;
    let pushCount = 0;
    let bottomMessageShown = false;
    let redirected = false;

    function isAtBottom() {
      return (window.scrollY + window.innerHeight) >= (document.documentElement.scrollHeight - 4);
    }

    function checkBottom() {
      const nowAtBottom = isAtBottom();
      if (nowAtBottom && !atBottom) {
        atBottom = true;
        pushCount = 0;
        if (!bottomMessageShown) {
          bottomMessageShown = true;
          shadowWhisper('已经到底啦！');
        }
      } else if (!nowAtBottom && atBottom) {
        // 离开了底部，重新计数，下次到底会再提示一次
        atBottom = false;
        pushCount = 0;
        bottomMessageShown = false;
      }
    }
    window.addEventListener('scroll', checkBottom, { passive: true });

    function registerPush() {
      if (!atBottom || redirected) return;
      pushCount++;
      if (pushCount >= PUSHES_NEEDED) {
        redirected = true;
        setTimeout(() => { window.location.href = 'knot.html'; }, 300);
      }
    }

    // 桌面：已经到底后，鼠标滚轮还在继续往下滚
    window.addEventListener('wheel', (e) => {
      if (atBottom && e.deltaY > 0) registerPush();
    }, { passive: true });

    // 移动端：已经到底后，手指还在继续往上划
    let touchStartY = null;
    window.addEventListener('touchstart', (e) => {
      touchStartY = e.touches[0].clientY;
    }, { passive: true });
    window.addEventListener('touchend', (e) => {
      if (touchStartY === null) return;
      const endY = e.changedTouches[0].clientY;
      if (touchStartY - endY > 25) registerPush();
      touchStartY = null;
    }, { passive: true });
  }

});
