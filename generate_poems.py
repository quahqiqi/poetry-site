import json
import os

json_path = 'poems/poems.json'

if not os.path.exists(json_path):
    print(f"错误：找不到 {json_path}")
    exit()

with open(json_path, 'r', encoding='utf-8') as f:
    poems_data = json.load(f)

# 提取所有文件名用于随机功能
all_poem_files = [p['file'] for p in poems_data]
poems_list_js = json.dumps(all_poem_files)

template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | 一个青年的天马行空</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&display=swap" rel="stylesheet">
  
  <style>
    :root {{
      --bg: #fdf6e3; --card: #fff; --muted: #6d5850; --accent: #b89c7a; --border: #d7cdbd;
      --bg-dark: #121212; --card-dark: #1e1e1e; --muted-dark: #d4d4d4; --border-dark: #333;
      --max-w: 700px; --sidebar-width: 280px;
      --poem-font-size: 1.2rem; 
    }}
    * {{ box-sizing:border-box; margin:0; padding:0; }}
    html,body {{ font-family: 'Noto Serif SC', serif; background:var(--bg); color:#222; transition: background .25s, color .25s; overflow-x: hidden; }}
    body.dark {{ background:var(--bg-dark); color:var(--muted-dark); }}

    /* === 顶部 Header 修复居中 === */
    header {{
      position:sticky; top:0; z-index:1200; display:flex; align-items:center; justify-content:space-between;
      padding:12px 20px; background: rgba(253,246,227,0.9); border-bottom:1px solid var(--border); backdrop-filter: blur(8px);
    }}
    body.dark header {{ background: rgba(18,18,18,0.9); border-color:var(--border-dark); }}
    .icon-btn {{ background:transparent; border:none; padding:8px; cursor:pointer; color:inherit; display:flex; align-items:center; }}
    
    /* 绝对居中 Logo 和标题 */
    .logo-title {{ position: absolute; left: 50%; transform: translateX(-50%); display:flex; align-items:center; gap:10px; text-decoration:none; }}
    .logo-title img {{ height:36px; width:36px; object-fit:cover; border-radius:6px; }}
    .logo-title h1 {{ font-size:1.1rem; color:var(--muted); font-weight: 700; white-space:nowrap; }}
    body.dark .logo-title h1 {{ color: var(--muted-dark); }}

    /* === 侧边栏完美复刻 === */
    .sidebar {{
      position:fixed; left:calc(-1 * var(--sidebar-width)); top:0; height:100%; width:var(--sidebar-width); padding:20px;
      background:var(--bg); border-right:1px solid var(--border); transition:left .3s cubic-bezier(0.4, 0, 0.2, 1); z-index:1250; overflow-y: auto;
    }}
    body.dark .sidebar {{ background:var(--bg-dark); border-color:var(--border-dark); }}
    .sidebar.active {{ left:0; }}
    .nav-item {{ 
      display:flex; align-items:center; gap:12px; width:100%; padding:14px 12px; margin:4px 0; 
      border-radius:8px; color:inherit; text-decoration:none; border:none; background:transparent; 
      cursor:pointer; font-size:1.05rem; text-align: left; transition: background 0.2s;
    }}
    .nav-item:hover, .nav-item.active {{ background: rgba(184,156,122,0.15); color: var(--accent); font-weight: bold; }}
    body.dark .nav-item:hover {{ background: rgba(255,255,255,0.08); }}
    .nav-item svg {{ width:20px; height:20px; stroke-width: 2px; stroke: currentColor; fill: none; }}
    .sidebar-divider {{ border:0; border-top:1px solid var(--border); margin:15px 0; }}
    body.dark .sidebar-divider {{ border-color: var(--border-dark); }}

    /* 标签手风琴菜单 */
    .tags-container {{ display: flex; flex-wrap: wrap; gap: 8px; padding: 10px 12px 10px 45px; display: none; }}
    .tags-container.show {{ display: flex; }}
    .sidebar-tag {{
        font-size: 0.9rem; padding: 6px 14px; background: rgba(0,0,0,0.05); 
        border-radius: 20px; color: var(--muted); text-decoration: none; transition: all 0.2s;
    }}
    body.dark .sidebar-tag {{ background: rgba(255,255,255,0.1); color: var(--muted-dark); }}
    .sidebar-tag:hover {{ background: var(--accent); color: #fff; }}

    .backdrop {{ position:fixed; inset:0; background:rgba(0,0,0,0.4); display:none; z-index:1240; backdrop-filter: blur(2px); }}
    .backdrop.show {{ display:block; }}

    /* === 正文与排版 === */
    main {{ max-width: var(--max-w); margin: 30px auto; padding: 0 20px; }}
    
    /* 标题防断行折叠 */
    .poem-title {{ 
        font-size: 2.2rem; margin-bottom: 20px; color: var(--accent); text-align: center; 
        text-wrap: balance; word-break: keep-all; line-height: 1.3;
    }}
    
    /* Meta区域和字号调节合并 */
    .meta-bar {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px dashed var(--border); padding-bottom: 15px; margin-bottom: 25px; }}
    body.dark .meta-bar {{ border-color: var(--border-dark); }}
    .poem-meta {{ color:var(--muted); font-size: 0.95rem; opacity: 0.9; }}
    
    /* 醒目的字号调节器 */
    .font-controls {{ display: flex; gap: 8px; background: rgba(184,156,122,0.1); padding: 4px; border-radius: 20px; }}
    .font-btn {{ 
        background: transparent; border: none; width: 32px; height: 32px; border-radius: 50%; 
        color: var(--accent); cursor: pointer; font-size: 1rem; font-weight: bold; display: flex; align-items: center; justify-content: center; transition: background 0.2s;
    }}
    .font-btn:hover {{ background: var(--accent); color: #fff; }}

    .poem-image {{ width:100%; border-radius:12px; margin-bottom: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
    body.dark .poem-image {{ opacity: 0.9; }}

    .poem-body {{ 
        white-space: pre-wrap; line-height: 2.2; font-size: var(--poem-font-size); 
        color: #333; transition: font-size 0.3s ease; font-family: "STKaiti", "华文楷体", "KaiTi", serif;
    }}
    body.dark .poem-body {{ color: #ccc; }}

    /* 喜欢和分享按钮 */
    .actions {{ display: flex; justify-content: center; gap: 20px; margin: 40px 0; }}
    .action-btn {{ 
        background: transparent; border: 1px solid var(--accent); color: var(--accent); 
        padding: 10px 25px; border-radius: 30px; cursor: pointer; font-size: 1rem;
        display: flex; align-items: center; gap: 8px; transition: all 0.2s;
    }}
    .action-btn:hover {{ background: var(--accent); color: #fff; }}
    .action-btn.liked {{ background: #e74c3c; border-color: #e74c3c; color: white; }}

    /* === 上下页导航 === */
    .poem-nav {{ 
        display: flex; justify-content: space-between; gap: 10px; margin-top: 50px; padding-top: 20px; border-top: 1px solid var(--border); 
    }}
    body.dark .poem-nav {{ border-color: var(--border-dark); }}
    .nav-link {{ 
        flex: 1; padding: 15px; border-radius: 8px; background: rgba(0,0,0,0.03); 
        text-decoration: none; color: var(--muted); font-size: 0.95rem; display: flex; flex-direction: column; transition: background 0.2s;
    }}
    body.dark .nav-link {{ background: rgba(255,255,255,0.05); color: var(--muted-dark); }}
    .nav-link:hover {{ background: rgba(184,156,122,0.1); color: var(--accent); }}
    .nav-label {{ font-size: 0.8rem; opacity: 0.7; margin-bottom: 4px; }}
    .nav-link.next {{ text-align: right; }}

  </style>
</head>
<body>

  <header>
    <button class="icon-btn" id="menuBtn">
        <svg width="24" height="24" viewBox="0 0 24 24"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
    </button>
    <a href="../index.html" class="logo-title">
        <img src="../assets/img/logo.png" alt="logo">
        <h1>一个青年的天马行空</h1>
    </a>
    <a href="../index.html?search=open" class="icon-btn">
        <svg width="22" height="22" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
    </a>
  </header>

  <aside class="sidebar" id="sidebar">
    <a href="../index.html" class="nav-item">
      <svg viewBox="0 0 24 24"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
      首页
    </a>
    <a href="../toc.html" class="nav-item">
      <svg viewBox="0 0 24 24"><line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line><line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line><line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line></svg>
      目录
    </a>
    <a href="../about.html" class="nav-item">
      <svg viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
      作者简介
    </a>
    
    <button class="nav-item" id="tagMenuBtn">
      <svg viewBox="0 0 24 24"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path><line x1="7" y1="7" x2="7.01" y2="7"></line></svg>
      标签分类
      <svg id="tagChevron" style="margin-left:auto; width:16px; height:16px; transition:transform 0.3s;" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
    </button>
    <div class="tags-container" id="tagsContainer">
        <a href="../index.html?q=见人" class="sidebar-tag">#见人</a>
        <a href="../index.html?q=见物" class="sidebar-tag">#见物</a>
        <a href="../index.html?q=见我" class="sidebar-tag">#见我</a>
    </div>

    <hr class="sidebar-divider">

    <button id="toggleDarkMode" class="nav-item">
      <svg viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
      <span id="darkModeText">夜间模式</span>
    </button>
    <button id="randomPoemBtn" class="nav-item">
      <svg viewBox="0 0 24 24"><polyline points="16 3 21 3 21 8"></polyline><line x1="4" y1="20" x2="21" y2="3"></line><polyline points="21 16 21 21 16 21"></polyline><line x1="15" y1="15" x2="21" y2="21"></line><line x1="4" y1="4" x2="9" y2="9"></line></svg>
      随机一首
    </button>
  </aside>
  <div class="backdrop" id="backdrop"></div>

  <main>
    <article>
        <h1 class="poem-title">{title}</h1>
        
        <div class="meta-bar">
            <div class="poem-meta">分类：{tags_str}</div>
            <div class="font-controls">
                <button class="font-btn" id="fontDecrease" title="缩小字号">A-</button>
                <button class="font-btn" id="fontIncrease" title="放大字号">A+</button>
            </div>
        </div>
        
        <img src="../{img}" class="poem-image" alt="{title}">
        <div class="poem-body" id="poemBody">{full_text}</div>

        <div class="actions">
          <button class="action-btn" id="likeBtn" onclick="handleLike()">
            <svg viewBox="0 0 24 24" width="20" height="20"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>
            <span id="likeText">喜欢</span>
          </button>
          <button class="action-btn" onclick="sharePage()">
            <svg viewBox="0 0 24 24" width="20" height="20"><circle cx="18" cy="5" r="3"></circle><circle cx="6" cy="12" r="3"></circle><circle cx="18" cy="19" r="3"></circle><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line></svg>
            分享
          </button>
        </div>

        <div class="poem-nav">
            {prev_html}
            {next_html}
        </div>
    </article>
  </main>

  <script>
    // 侧边栏逻辑
    const menuBtn = document.getElementById('menuBtn');
    const sidebar = document.getElementById('sidebar');
    const backdrop = document.getElementById('backdrop');
    menuBtn.onclick = () => {{ sidebar.classList.add('active'); backdrop.classList.add('show'); }};
    backdrop.onclick = () => {{ sidebar.classList.remove('active'); backdrop.classList.remove('show'); }};

    // 标签菜单折叠
    const tagMenuBtn = document.getElementById('tagMenuBtn');
    const tagsContainer = document.getElementById('tagsContainer');
    const tagChevron = document.getElementById('tagChevron');
    tagMenuBtn.onclick = () => {{
        tagsContainer.classList.toggle('show');
        tagChevron.style.transform = tagsContainer.classList.contains('show') ? 'rotate(180deg)' : 'rotate(0deg)';
    }};

    // 夜间模式
    const toggleDarkModeBtn = document.getElementById('toggleDarkMode');
    const darkModeText = document.getElementById('darkModeText');
    function updateDarkMode(isDark) {{
        document.body.classList.toggle('dark', isDark);
        darkModeText.innerText = isDark ? "日间模式" : "夜间模式";
    }}
    toggleDarkModeBtn.onclick = () => {{
        const isDark = document.body.classList.toggle('dark');
        localStorage.setItem('site-dark', isDark ? '1' : '0');
        updateDarkMode(isDark);
    }};
    if(localStorage.getItem('site-dark')==='1') updateDarkMode(true);

    // 字号调节 (带本地记忆)
    const root = document.documentElement;
    let currentSize = parseFloat(localStorage.getItem('poemFontSize')) || 1.2;
    root.style.setProperty('--poem-font-size', currentSize + 'rem');
    
    document.getElementById('fontIncrease').onclick = () => {{
        if(currentSize < 1.8) {{ currentSize += 0.1; root.style.setProperty('--poem-font-size', currentSize.toFixed(1) + 'rem'); localStorage.setItem('poemFontSize', currentSize.toFixed(1)); }}
    }};
    document.getElementById('fontDecrease').onclick = () => {{
        if(currentSize > 0.9) {{ currentSize -= 0.1; root.style.setProperty('--poem-font-size', currentSize.toFixed(1) + 'rem'); localStorage.setItem('poemFontSize', currentSize.toFixed(1)); }}
    }};

    // 随机一首
    const allPoems = {poems_list_js}; 
    document.getElementById('randomPoemBtn').onclick = () => {{
        const otherPoems = allPoems.filter(p => p !== '{file}');
        if (otherPoems.length > 0) window.location.href = otherPoems[Math.floor(Math.random() * otherPoems.length)];
    }};

    // 分享与点赞 (纯本地视觉反馈)
    function sharePage() {{
      if (navigator.share) navigator.share({{ title: '{title}', url: window.location.href }});
      else alert('请复制浏览器链接分享');
    }}

    const likeBtn = document.getElementById('likeBtn');
    const likeText = document.getElementById('likeText');
    const poemId = 'like_{file}';
    if(localStorage.getItem(poemId)) {{ likeBtn.classList.add('liked'); likeText.innerText = '已喜欢'; }}
    
    function handleLike() {{
        if(!localStorage.getItem(poemId)) {{
            localStorage.setItem(poemId, 'true');
            likeBtn.classList.add('liked');
            likeText.innerText = '已喜欢';
            // 添加一个小小的跳动动画效果
            likeBtn.style.transform = 'scale(1.1)';
            setTimeout(() => likeBtn.style.transform = 'scale(1)', 200);
        }} else {{
            // 允许取消点赞
            localStorage.removeItem(poemId);
            likeBtn.classList.remove('liked');
            likeText.innerText = '喜欢';
        }}
    }}
  </script>
</body>
</html>
"""

print(f"开始生成 {len(poems_data)} 首诗歌页面...")
for i, poem in enumerate(poems_data):
    full_text = poem.get('content', poem['preview'])
    tags = poem.get('tags', [])
    tags_str = " / ".join(tags) if tags else "暂无分类"
    
    # === 计算上一篇和下一篇 ===
    prev_poem = poems_data[i-1] if i > 0 else None
    next_poem = poems_data[i+1] if i < len(poems_data) - 1 else None

    if prev_poem:
        prev_html = f'<a href="{prev_poem["file"]}" class="nav-link"><span class="nav-label">上一篇</span><span>{prev_poem["title"]}</span></a>'
    else:
        prev_html = f'<div class="nav-link" style="opacity:0.5;"><span class="nav-label">已经是</span><span>第一篇了</span></div>'

    if next_poem:
        next_html = f'<a href="{next_poem["file"]}" class="nav-link next"><span class="nav-label">下一篇</span><span>{next_poem["title"]}</span></a>'
    else:
        next_html = f'<div class="nav-link next" style="opacity:0.5;"><span class="nav-label">已经是</span><span>最后一篇了</span></div>'


    html_content = template.format(
        title=poem['title'],
        full_text=full_text,
        img=poem['img'],
        file=poem['file'],
        tags_str=tags_str,
        poems_list_js=poems_list_js,
        prev_html=prev_html,
        next_html=next_html
    )
    
    output_file = f"poems/{poem['file']}"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

print(f"✅ 大功告成！全功能升级完毕。")
