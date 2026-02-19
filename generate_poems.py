import json
import os

# 确保存放诗歌 HTML 的目录存在
output_dir = "poems"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 1. 加载 JSON 数据
with open('poems/poems.json', 'r', encoding='utf-8') as f:
    poems = json.load(f)

# 2. HTML 模板
html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | 一个青年的天马行空</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #fdf6e3; --text: #222; --accent: #b89c7a; --muted: #6d5850; --border: #d7cdbd;
      --bg-dark: #121212; --text-dark: #d4d4d4; --card-dark: #1e1e1e;
    }}
    * {{ box-sizing: border-box; }}
    body {{ 
      margin: 0; background: var(--bg); color: var(--text); 
      font-family: 'Noto Serif SC', serif; transition: 0.3s;
      line-height: 1.8;
    }}
    body.dark {{ background: var(--bg-dark); color: var(--text-dark); }}

    /* --- Header (与首页保持一致) --- */
    header {{
      position: sticky; top: 0; z-index: 1000;
      display: flex; align-items: center; justify-content: space-between;
      padding: 10px 16px; background: rgba(253,246,227,0.9);
      border-bottom: 1px solid var(--border); backdrop-filter: blur(10px); height: 64px;
    }}
    body.dark header {{ background: rgba(18,18,18,0.9); border-color: #333; }}
    .back-btn {{ text-decoration: none; color: var(--muted); display: flex; align-items: center; gap: 4px; font-weight: bold; }}
    .logo-title {{ position: absolute; left: 50%; transform: translateX(-50%); display: flex; align-items: center; gap: 8px; text-decoration: none; color: inherit; }}
    .logo-title img {{ height: 32px; width: 32px; border-radius: 6px; }}
    .logo-title h1 {{ margin: 0; font-size: 1rem; }}

    /* --- ✨ 统一图片容器：物理裁剪的关键 ✨ --- */
    .poem-img-box {{
      width: 100%;
      max-width: 700px;
      margin: 40px auto;
      /* 🎯 关键：强制 4:3 比例，你可以改成 3:2 如果你喜欢更扁一点 */
      aspect-ratio: 4 / 3; 
      overflow: hidden;
      border-radius: 12px;
      box-shadow: 0 15px 45px rgba(0,0,0,0.1);
      background: #eee;
    }}
    .poem-img-box img {{
      width: 100%;
      height: 100%;
      /* 🎯 关键：裁剪图片并居中，不再受原图长宽比影响 */
      object-fit: cover; 
      object-position: center;
      display: block;
      transition: transform 0.5s;
    }}
    .poem-img-box:hover img {{ transform: scale(1.05); }}

    /* --- 诗歌正文 --- */
    main {{ max-width: 700px; margin: 0 auto; padding: 0 25px 80px; }}
    .poem-header {{ text-align: center; margin-bottom: 40px; }}
    .poem-title {{ font-size: 2.2rem; color: var(--accent); margin-bottom: 10px; letter-spacing: 2px; }}
    .poem-meta {{ font-size: 0.9rem; color: var(--muted); display: flex; justify-content: center; gap: 10px; opacity: 0.7; }}

    .poem-content {{ 
      font-size: 1.25rem; white-space: pre-wrap; word-break: break-word; 
      color: #333; text-align: center; /* 居中排版更有诗意 */
    }}
    body.dark .poem-content {{ color: #ccc; }}

    /* --- 字体控制按钮 --- */
    .font-controls {{
      display: flex; justify-content: center; gap: 15px; margin: 40px 0; opacity: 0.5; transition: 0.3s;
    }}
    .font-controls:hover {{ opacity: 1; }}
    .f-btn {{ 
      background: rgba(184,156,122,0.1); border: 1px solid var(--accent); 
      color: var(--accent); padding: 5px 12px; border-radius: 20px; cursor: pointer; 
    }}

    footer {{ text-align: center; padding: 40px; font-size: 0.8rem; color: var(--muted); border-top: 1px solid var(--border); margin-top: 60px; }}
  </style>
</head>
<body class="">
  <header>
    <a href="../index.html" class="back-btn">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"></polyline></svg>
      返回
    </a>
    <a href="../index.html" class="logo-title">
        <img src="../images/logo.png" alt="logo" onerror="this.src='../images/logo.png'">
        <h1>天马行空</h1>
    </a>
    <button class="f-btn" onclick="document.body.classList.toggle('dark')">🌓</button>
  </header>

  <div class="poem-img-box">
    <img src="../{img_path}" alt="{title}" onerror="this.style.display='none'">
  </div>

  <main>
    <div class="poem-header">
      <h1 class="poem-title">{title}</h1>
      <div class="poem-meta">
        {tags_html}
      </div>
    </div>

    <div class="font-controls">
      <button class="f-btn" onclick="changeFont(-1)">A -</button>
      <button class="f-btn" onclick="changeFont(1)">A +</button>
    </div>

    <div class="poem-content" id="poemContent">{content}</div>
  </main>

  <footer>© 一个写诗青年的天马行空</footer>

  <script>
    function changeFont(delta) {{
      const el = document.getElementById('poemContent');
      const style = window.getComputedStyle(el, null).getPropertyValue('font-size');
      const currentSize = parseFloat(style);
      el.style.fontSize = (currentSize + delta) + 'px';
    }}
    // 初始化暗色模式
    if(localStorage.getItem('site-dark')==='1') document.body.classList.add('dark');
  </script>
</body>
</html>
"""

# 3. 循环生成 HTML
for poem in poems:
    # 转换标签为 HTML 格式
    tags_html = "".join([f"<span>#{tag}</span>" for tag in poem.get('tags', [])])
    
    # 填充模板
    html_content = html_template.format(
        title=poem['title'],
        img_path=poem['img'],  # 这里会自动使用你 JSON 里的 images/poemXX.jpg
        tags_html=tags_html,
        content=poem['content']
    )
    
    # 写入文件
    file_path = os.path.join(output_dir, poem['file'])
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

print(f"✅ 成功生成 {len(poems)} 首诗歌页面！请查看 /poems 目录。")
