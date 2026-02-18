import json
import os

# 1. 路径设置
json_path = 'poems/poems.json'

if not os.path.exists(json_path):
    print(f"找不到 {json_path}")
else:
    with open(json_path, 'r', encoding='utf-8') as f:
        poems = json.load(f)

    # --- 这里就是你原本的精美 HTML 模板 ---
    # 注意：CSS里的 { } 已经改成了 {{ }} 以兼容 Python
    template = """<!DOCTYPE html>
<html lang="zh-Hans">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | 一个青年的天马行空</title>
  
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{preview}">
  <meta property="og:image" content="https://quahqiqi.github.io/poetry-site/{img}">
  <meta property="og:url" content="https://quahqiqi.github.io/poetry-site/poems/{file}">
  <meta property="og:type" content="article">

  <style>
    body {{
      font-family: "STKaiti", "华文楷体", "KaiTi", serif;
      background-color: #f5f0e6;
      color: #333;
      padding: 1.5em;
      max-width: 700px;
      margin: auto;
    }}
    .poem-title {{
      font-size: 1.8em;
      margin-bottom: 0.5em;
    }}
    .poem-meta {{
      font-size: 0.9em;
      color: #777;
      margin-bottom: 1em;
    }}
    .poem-body {{
      white-space: pre-wrap;
      line-height: 1.8em;
      margin-bottom: 2em;
      font-size: 1.2em;
    }}
    .poem-image {{
      width: 100%;
      max-height: 400px;
      object-fit: cover;
      border-radius: 8px;
      margin: 1em 0;
      box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }}
    .actions {{
      display: flex;
      gap: 1em;
      margin-bottom: 2em;
    }}
    .actions button {{
      background-color: #e6dccb;
      color: #6b4e2e;
      border: 1px solid #cbb89d;
      padding: 0.6em 1.2em;
      border-radius: 6px;
      cursor: pointer;
      font-family: inherit;
    }}
    .nav-links {{
      display: flex;
      justify-content: space-between;
      margin: 2em 0;
    }}
    .nav-links a {{
      text-decoration: none;
      color: #6b4e2e;
      background-color: #e6dccb;
      padding: 0.5em 1em;
      border-radius: 6px;
    }}
  </style>
</head>
<body>
  <h1 class="poem-title">{title}</h1>
  <div class="poem-meta">创作日期：2026年 ｜ 标签：{tags}</div>

  <img src="../{img}" alt="{title}" class="poem-image" />

  <div class="poem-body">{full_text}</div>

  <div class="actions">
    <button onclick="alert('谢谢你的喜欢！')">👍 点赞</button>
    <button onclick="navigator.share ? navigator.share({{ title: '{title}', url: location.href }}) : alert('请手动复制链接')">🔗 分享</button>
  </div>

  <div class="nav-links">
    <a href="../index.html">← 返回首页</a>
    <a href="https://quahqiqi.github.io/poetry-site/toc.html">目录 →</a>
  </div>
</body>
</html>
"""

    # 2. 生成文件
    for poem in poems:
        # 这里的 full_text 会读取 JSON 里的 preview，如果你有 content 字段也会优先读取
        full_text = poem.get('content', poem['preview'])
        tags_str = " #".join(poem.get('tags', []))

        html_content = template.format(
            title=poem['title'],
            preview=poem['preview'][:30], # 截取前30字给社交媒体描述
            full_text=full_text,
            img=poem['img'],
            file=poem['file'],
            tags=tags_str
        )
        
        output_file = f"poems/{poem['file']}"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

    print(f"✅ 原创风格已完美还原！共更新 {len(poems)} 首诗。")
