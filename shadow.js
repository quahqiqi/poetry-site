/*
  影子管家 —— 共用彩蛋逻辑
  原则：不创造内容，只负责发现内容。
  他只出现在阅读之外的缝隙：页面切换、加载完成、搜索无果、深夜、
  节日、404、很久没回来、很久没操作。
  绝不出现在诗歌正文里，绝不弹窗，绝不要求点击，绝不引导任务。
*/

/* ---------- 状态层：记住来访痕迹，给所有彩蛋提供统一的冷却能力 ---------- */
const ShadowState = (function () {
  const KEY_FIRST = 'shadow-first-visit';
  const KEY_LAST = 'shadow-last-visit';
  const KEY_COUNT = 'shadow-visit-count';
  const SESSION_GAP = 30 * 60 * 1000; // 隔超过30分钟，才算新的一次来访

  function now() { return Date.now(); }

  function init() {
    const firstRaw = localStorage.getItem(KEY_FIRST);
    const lastRaw = localStorage.getItem(KEY_LAST);
    let count = parseInt(localStorage.getItem(KEY_COUNT) || '0', 10);

    if (!firstRaw) localStorage.setItem(KEY_FIRST, String(now()));

    const isNewVisit = !lastRaw || (now() - parseInt(lastRaw, 10)) > SESSION_GAP;
    if (isNewVisit) {
      count += 1;
      localStorage.setItem(KEY_COUNT, String(count));
    }
    const lastVisitBefore = lastRaw ? parseInt(lastRaw, 10) : null;
    localStorage.setItem(KEY_LAST, String(now()));

    return {
      firstVisit: parseInt(localStorage.getItem(KEY_FIRST), 10),
      lastVisitBefore,
      visitCount: count,
      isNewVisit
    };
  }

  // 某句提示最近有没有说过，还在不在冷却里
  function canShow(hintKey, cooldownMs) {
    const last = localStorage.getItem('shadow-seen-' + hintKey);
    if (!last) return true;
    return (now() - parseInt(last, 10)) > cooldownMs;
  }

  function markShown(hintKey) {
    localStorage.setItem('shadow-seen-' + hintKey, String(now()));
  }

  return { init, canShow, markShown };
})();

const shadowVisit = ShadowState.init();

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

/* ---------- 说一句悄悄话，过一会儿自己消失 ---------- */
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

  /* ========== ⑪ 请假模式：手动开关，优先级最高，放在最前面 ========== */
  // 想让影子管家"消失"一天，就把日期加进下面这个数组，格式 'YYYY-MM-DD'
  // 生效期间：这个文件里所有其他彩蛋全部停止工作
  const SHADOW_LEAVE_DATES = ['2026-8-4'];
  const todayStr = new Date().toISOString().slice(0, 10);
  if (SHADOW_LEAVE_DATES.includes(todayStr)) {
    return; // 今天请假，后面什么都不做
  }


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
          shadowWhisper('已经到底啦！', 3000, 'center');
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

  /* ========== 好久不见：真的隔了一阵子才说 ========== */
  if (filename === '' || filename === 'index.html') {
    const GREETING_GAP = 36 * 60 * 60 * 1000; // 约1天没来，才算"好久不见"
    if (shadowVisit.lastVisitBefore && (Date.now() - shadowVisit.lastVisitBefore) > GREETING_GAP) {
      shadowWhisper('好久不见。');
    }
  }

  /* ========== 一分钟不动：他好像还惦记着你 ========== */
  (function () {
    const IDLE_MS = 60 * 1000;
    let idleTimer;

    function resetIdleTimer() {
      clearTimeout(idleTimer);
      idleTimer = setTimeout(() => {
        shadowWhisper('我帮你把风关小一点。');
        // 说完这句，什么都不会发生——他只是提了一下，不打扰你
      }, IDLE_MS);
    }

    ['mousemove', 'touchstart', 'touchmove', 'keydown', 'scroll', 'click']
      .forEach(evt => window.addEventListener(evt, resetIdleTimer, { passive: true }));

    resetIdleTimer();
  })();

  /* ========== 停留超过3分钟：还在这里吗 ========== */
  if (document.getElementById('poemContent')) {
    (function () {
      const READ_MS = 3 * 60 * 1000;
      let elapsed = 0;
      let lastTick = Date.now();
      let fired = false;

      const readTimer = setInterval(() => {
        if (fired) return;
        const now = Date.now();
        if (!document.hidden) elapsed += now - lastTick; // 切走标签页的时间不计入
        lastTick = now;

        if (elapsed >= READ_MS) {
          fired = true;
          shadowWhisper('还在这里吗？', 50000); // 停留10秒后自己消失
          clearInterval(readTimer);
        }
      }, 5000);
    })();
  }

  /* ========== ③ 凌晨专属：footer 多一句 ========== */
  const nowHour = new Date().getHours();
  if (nowHour >= 1 && nowHour < 6) {
    const footer = document.querySelector('footer');
    if (footer) {
      const lines = ['他已经睡了', '今晚由我值班'];
      const pick = lines[Math.floor(Math.random() * lines.length)];
      const span = document.createElement('span');
      span.textContent = ' · ' + pick;
      footer.appendChild(span);
    }
  }

  /* ========== ⑥ 连续随机10次：你是真的在随机 ========== */
  (function () {
    const RANDOM_KEY = 'shadow-random-count';

    // 如果这次落地是因为随机跳转而来，先检查次数够不够
    const count = parseInt(sessionStorage.getItem(RANDOM_KEY) || '0', 10);
    if (count > 0 && count % 10 === 0) {
      shadowWhisper('……你是真的在随机。');
    }

    const randomBtn = document.getElementById('randomBtn');
    if (randomBtn) {
      randomBtn.addEventListener('click', () => {
        const c = parseInt(sessionStorage.getItem(RANDOM_KEY) || '0', 10) + 1;
        sessionStorage.setItem(RANDOM_KEY, String(c));
      });
    }
  })();

  /* ========== ⑩ 一年以后：只说这一次 ========== */
  if (filename === '' || filename === 'index.html') {
    const ONE_YEAR = 365 * 24 * 60 * 60 * 1000;
    if (
      shadowVisit.firstVisit &&
      (Date.now() - shadowVisit.firstVisit) >= ONE_YEAR &&
      ShadowState.canShow('one-year', ONE_YEAR) // 说过就不会再说第二次
    ) {
      shadowWhisper('我们认识一年了。');
      ShadowState.markShown('one-year');
    }
  }

});
