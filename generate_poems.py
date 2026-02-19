import json
import os

# 1. 路径设置
json_path = 'poems/poems.json'

if not os.path.exists(json_path):
    print(f"错误：找不到 {json_path}")
    exit()

with open(json_path, 'r', encoding='utf-8') as f:
    poems_data = json.load(f)

# 转换JS数组字符串（用于随机功能）
all_poem_files = [p['file'] for p in poems_data]
poems_list_js = json.dumps(all_poem_files)

# === 2. 1:1 完美复刻首页的模板 ===
template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | 一个青年的天马行空</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&display=swap" rel="stylesheet">
  
  <style>
    /* === 1. 全局与变量 === */
    :root {{
      --bg: #fdf6e3; --card: #fff; --muted: #6d5850; --accent: #b89c7a; --border: #d7cdbd;
      --bg-dark: #121212; --card-dark: #1e1e1e; --muted-dark: #d4d4d4; --border-dark: #333;
      --sidebar-w: 280px;
      --p-font: 1.15rem;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: 'Noto Serif SC', serif; background: var(--bg); color: #222; transition: 0.3s; }}
    body.dark {{ background: var(--bg-dark); color: var(--muted-dark); }}

    /* === 2. 顶部 Header (绝对居中与对称布局) === */
    header {{
      position: sticky; top: 0; z-index: 1200; display: flex; align-items: center; justify-content: space-between;
      padding: 10px 16px; background: rgba(253, 246, 227, 0.9); border-bottom: 1px solid var(--border); backdrop-filter: blur(10px); height: 64px;
    }}
    body.dark header {{ background: rgba(18, 18, 18, 0.9); border-color: #333; }}

    .icon-btn {{ background: transparent; border: none; padding: 8px; cursor: pointer; color: var(--muted); display: flex; align-items: center; transition: 0.2s; text-decoration: none; }}
    body.dark .icon-btn {{ color: var(--muted-dark); }}
    .icon-btn svg {{ width: 24px; height: 24px; stroke-width: 2.2; stroke: currentColor; }}

    .logo-title {{ position: absolute; left: 50%; transform: translateX(-50%); display: flex; align-items: center; gap: 8px; text-decoration: none; color: inherit; width: max-content; }}
    .logo-title img {{ height: 38px; width: 38px; border-radius: 6px; }}
    .logo-title h1 {{ margin: 0; font-size: 1.05rem; font-weight: 700; white-space: nowrap; }}

    /* === 3. 完美侧边栏 Sidebar === */
    .sidebar {{ position: fixed; left: calc(-1 * var(--sidebar-w)); top: 0; height: 100%; width: var(--sidebar-w); background: var(--bg); border-right: 1px solid var(--border); transition: 0.3s; z-index: 1250; padding: 20px 14px; overflow-y: auto; }}
    body.dark .sidebar {{ background: #1a1a1a; border-color: #333; }}
    .sidebar.active {{ left: 0; }}
    
    .nav-item {{
      display: flex; align-items: center; gap: 12px; width: 100%; padding: 12px 16px; margin-bottom: 6px;
      border-radius: 10px; background: transparent; color: var(--muted); text-decoration: none; border: none; cursor: pointer; font-size: 1rem; font-family: inherit; transition: 0.2s;
    }}
    body.dark .nav-item {{ color: #aaa; }}
    .nav-item:hover, .nav-item.active {{ background: #efe7da; color: var(--accent); font-weight: 700; }}
    body.dark .nav-item:hover {{ background: #2a2a2a; }}
    .nav-item svg {{ width: 20px; height: 20px; stroke-width: 2; fill: none; stroke: currentColor; }}

    /* 标签折叠功能 */
    .chevron {{ margin-left: auto; width: 14px !important; transition: 0.3s; }}
    .nav-item.open .chevron {{ transform: rotate(180deg); }}
    .tag-box {{ max-height: 0; overflow: hidden; transition: 0.3s; display: flex; flex-wrap: wrap; gap: 8px; padding-left: 16px; }}
    .tag-box.show {{ max-height: 200px; margin: 10px 0 20px; }}
    .tag-pill {{ padding: 6px 14px; background: #f3eee3; border-radius: 20px; font-size: 0.9rem; color: #8c7e74; cursor: pointer; transition: 0.2s; text-decoration: none; display: inline-block; }}
    body.dark .tag-pill {{ background: #2a2a2a; color: #999; }}
    .tag-pill:hover {{ background: #efe7da; color: var(--accent); }}

    .backdrop {{ position: fixed; inset: 0; background: rgba(0,0,0,0.3); display: none; z-index: 1240; backdrop-filter: blur(2px); }}
    .backdrop.show {{ display: block; }}

    /* === 4. 正文与字号调节 === */
    main {{ max-width: 750px; margin: 30px auto; padding: 0 20px; animation: fadeIn 0.6s ease; }}
    @keyframes fadeIn {{ from{{opacity:0; transform:translateY(10px);}} to{{opacity:1; transform:translateY(0);}} }}

    .poem-title {{ font-size: 2rem; color: var(--accent); text-align: center; margin-bottom: 10px; text-wrap: balance; line-height: 1.3; }}
    .poem-meta {{ text-align: center; font-size: 0.9rem; color: var(--muted); margin-bottom: 25px; }}

    .reader-tools {{ display: flex; justify-content: space-between; align-items: center; background: rgba(184, 156, 122, 0.08); padding: 10px 20px; border-radius: 12px; margin-bottom: 20px; }}
    .font-setter {{ display: flex; align-items: center; gap: 15px; }}
    .font-btn {{ background: var(--card); border: 1px solid var(--border); width: 34px; height: 34px; border-radius: 50%; cursor: pointer; color: var(--accent); font-weight: bold; font-family: serif; display:flex; align-items:center; justify-content:center; transition: 0.2s; }}
    body.dark .font-btn {{ background: var(--card-dark); border-color: var(--border-dark); }}
    .font-btn:hover {{ background: var(--accent); color: #fff; }}
    
    .poem-image {{ width: 100%; border-radius: 12px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }}

    .poem-body {{ font-family: "STKaiti", "华文楷体", "KaiTi", serif; font-size: var(--p-font); line-height: 2.2; white-space: pre-wrap; transition: font-size 0.2s; }}

    .actions {{ display: flex; justify-content: center; gap: 20px; margin: 50px 0; }}
    .btn-action {{ padding: 10px 24px; border-radius: 30px; border: 1px solid var(--accent); background: transparent; color: var(--accent); cursor: pointer; display: flex; align-items: center; gap: 8px; font-size: 1rem; transition: 0.3s; }}
    .btn-action:hover {{ background: var(--accent); color: white; }}
    .btn-action.active {{ background: #e74c3c; border-color: #e74c3c; color: white; }}

    .post-nav {{ display: flex; justify-content: space-between; border-top: 1px solid var(--border); padding-top: 30px; gap: 10px; margin-bottom: 40px; }}
    body.dark .post-nav {{ border-color: var(--border-dark); }}
    .nav-card {{ flex: 1; padding: 15px; border-radius: 10px; background: rgba(0,0,0,0.02); text-decoration: none; color: inherit; display: flex; flex-direction: column; gap: 5px; transition: 0.2s; }}
    body.dark .nav-card {{ background: rgba(255,255,255,0.03); }}
    .nav-card .label {{ font-size: 0.8rem; color: var(--muted); }}
    .nav-card .p-title {{ font-weight: bold; font-size: 0.95rem; }}
    .nav-card:hover {{ background: rgba(184, 156, 122, 0.1); }}
  </style>
</head>
<body>

  <header>
    <button class="icon-btn" id="menuBtn">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
    </button>
    <a href="../index.html" class="logo-title">
        <img src="../assets/img/logo.png" alt="logo">
        <h1>一个青年的天马行空</h1>
    </a>
    <a href="../index.html" class="icon-btn" id="searchBtn">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="11" cy="11" r="7"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
    </a>
  </header>

  <aside class="sidebar" id="sidebar">
    <a href="../index.html" class="nav-item">
        <svg viewBox="0 0 24 24"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path></svg>首页
    </a>
    <a href="../toc.html" class="nav-item">
        <svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="16" rx="2"></rect><path d="M7 8h10M7 12h10M7 16h6"></path></svg>目录
    </a>
    <a href="../about.html" class="nav-item">
        <svg viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>作者简介
    </a>
    
    <div style="height:1px; background:var(--border); margin:10px 0; opacity:0.4;"></div>

    <button class="nav-item" id="tagToggleBtn">
        <svg viewBox="0 0 24 24"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path></svg>
        分类浏览
        <svg class="chevron" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
    </button>
    <div class="tag-box" id="tagBox">
        <a href="../index.html?q=见人" class="tag-pill">#见人</a>
        <a href="../index.html?q=见物" class="tag-pill">#见物</a>
        <a href="../index.html?q=见我" class="tag-pill">#见我</a>
    </div>

    <div style="height:1px; background:var(--border); margin:10px 0; opacity:0.4;"></div>

    <button id="randomBtn" class="nav-item"><svg viewBox="0 0 24 24"><polyline points="16 3 21 3 21 8"></polyline><line x1="4" y1="20" x2="21" y2="3"></line><polyline points="21 16 21 21 16 21"></polyline></svg>随机读一首</button>
    <button id="darkBtn" class="nav-item"><svg viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"></path></svg>深色模式</button>
  </aside>

  <div class="backdrop" id="backdrop"></div>

  <main>
    <h1 class="poem-title">{title}</h1>
    <p class="poem-meta"># {tags_str}</p>

    <div class="reader-tools">
        <div class="font-setter">
            <span style="font-size: 0.85rem; color: var(--muted);">字号调节</span>
            <button class="font-btn" onclick="changeFont(-0.1)">A-</button>
            <button class="font-btn" onclick="changeFont(0.1)">A+</button>
        </div>
        <div style="font-size: 0.8rem; color: var(--accent); font-weight: bold;">阅读模式</div>
    </div>

    <img src="../{img}" class="poem-image" alt="封面图">

    <div class="poem-body" id="poemContent">{full_text}</div>

    <div class="actions">
        <button class="btn-action" id="likeBtn" onclick="toggleLike()">
            <svg id="heartIcon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>
            <span id="likeText">喜欢</span>
        </button>
        <button class="btn-action" onclick="sharePage()">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"></circle><circle cx="6" cy="12" r="3"></circle><circle cx="18" cy="19" r="3"></circle><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line></svg>
            分享
        </button>
    </div>

    <nav class="post-nav">
        {prev_html}
        {next_html}
    </nav>
  </main>

  <script>
    const sidebar = document.getElementById('sidebar');
    const backdrop = document.getElementById('backdrop');
    const tagBox = document.getElementById('tagBox');
    const tagToggleBtn = document.getElementById('tagToggleBtn');
    const allPoems = {poems_list_js};

    document.getElementById('menuBtn').onclick = () => {{ sidebar.classList.add('active'); backdrop.classList.add('show'); }};
    backdrop.onclick = () => {{ sidebar.classList.remove('active'); backdrop.classList.remove('show'); }};
    tagToggleBtn.onclick = () => {{ tagToggleBtn.classList.toggle('open'); tagBox.classList.toggle('show'); }};

    document.getElementById('darkBtn').onclick = () => {{
        const isDark = document.body.classList.toggle('dark');
        localStorage.setItem('site-dark', isDark ? '1' : '0');
    }};
    if(localStorage.getItem('site-dark')==='1') document.body.classList.add('dark');

    document.getElementById('randomBtn').onclick = () => {{
        const otherPoems = allPoems.filter(p => p !== '{file}');
        if(otherPoems.length) window.location.href = otherPoems[Math.floor(Math.random()*otherPoems.length)];
    }};

    let currentSize = parseFloat(localStorage.getItem('p-font')) || 1.15;
    document.documentElement.style.setProperty('--p-font', currentSize + 'rem');
    function changeFont(delta) {{
        currentSize = Math.max(0.9, Math.min(1.8, currentSize + delta));
        document.documentElement.style.setProperty('--p-font', currentSize + 'rem');
        localStorage.setItem('p-font', currentSize);
    }}

    const poemId = '{file}';
    const likeBtn = document.getElementById('likeBtn');
    const heartIcon = document.getElementById('heartIcon');
    if(localStorage.getItem('liked_' + poemId)) {{
        likeBtn.classList.add('active');
        heartIcon.setAttribute('fill', 'currentColor');
        document.getElementById('likeText').innerText = '已喜欢';
    }}
    function toggleLike() {{
        const isLiked = likeBtn.classList.toggle('active');
        if(isLiked) {{
            localStorage.setItem('liked_' + poemId, '1');
            heartIcon.setAttribute('fill', 'currentColor');
            document.getElementById('likeText').innerText = '已喜欢';
        }} else {{
            localStorage.removeItem('liked_' + poemId);
            heartIcon.setAttribute('fill', 'none');
            document.getElementById('likeText').innerText = '喜欢';
        }}
    }}

    function sharePage() {{
        if (navigator.share) navigator.share({{ title: '{title}', url: window.location.href }});
        else alert('请复制链接分享给好友');
    }}
  </script>
</body>
</html>
"""

# === 3. 开始生成所有诗歌文件 ===
for i, poem in enumerate(poems_data):
    full_text = poem.get('content', poem.get('preview', ''))
    tags = poem.get('tags', [])
    tags_str = " / ".join(tags) if tags else "暂无分类"

    # 处理上一篇和下一篇的跳转逻辑
    prev_p = poems_data[i-1] if i > 0 else None
    next_p = poems_data[i+1] if i < len(poems_data)-1 else None

    prev_html = f'<a href="{prev_p["file"]}" class="nav-card"><span class="label">上一篇</span><span class="p-title">{prev_p["title"]}</span></a>' if prev_p else '<div class="nav-card" style="opacity:0.3"><span class="label">已经是</span><span class="p-title">第一篇</span></div>'
    next_html = f'<a href="{next_p["file"]}" class="nav-card" style="text-align:right"><span class="label">下一篇</span><span class="p-title">{next_p["title"]}</span></a>' if next_p else '<div class="nav-card" style="opacity:0.3; text-align:right"><span class="label">已经是</span><span class="p-title">最后一篇</span></div>'

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
    
    with open(f"poems/{poem['file']}", 'w', encoding='utf-8') as f:
        f.write(html_content)

print("✅ 诗歌详情页全站适配完成！")
