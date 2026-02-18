import json
import os

# 1. 路径设置
json_path = 'poems/poems.json'

# 检查 JSON 是否存在
if not os.path.exists(json_path):
    print(f"错误：找不到 {json_path}")
else:
    with open(json_path, 'r', encoding='utf-8') as f:
        poems = json.load(f)

    # HTML 模板 - 修复了 OG 标签和分享逻辑
    template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{preview}">
    <meta property="og:image" content="https://quahqiqi.github.io/poetry-site/{img}">
    <meta property="og:url" content="https://quahqiqi.github.io/poetry-site/poems/{file}">
    <meta property="og:type" content="article">

    <style>
        body {{ font-family: "PingFang SC", sans-serif; padding: 40px; max-width: 600px; margin: auto; line-height: 1.8; color: #333; }}
        img {{ width: 100%; border-radius: 8px; margin-bottom: 20px; }}
        .share-btn {{ margin-top: 30px; padding: 12px 24px; background: #222; color: #fff; border: none; cursor: pointer; border-radius: 30px; font-size: 16px; width: 100%; }}
    </style>
</head>
<body>
    <article>
        <img src="../{img}" alt="{title}">
        <h1>{title}</h1>
        <p style="white-space: pre-wrap;">{preview}</p>
    </article>
    
    <button class="share-btn" onclick="shareToSocial()">🔗 分享到 Instagram / Facebook</button>

    <script>
    async function shareToSocial() {{
        const shareData = {{
            title: "{title}",
            text: "{preview}",
            url: window.location.href
        }};
        const imageUrl = '../{img}'; 
        try {{
            const response = await fetch(imageUrl);
            const blob = await response.blob();
            const file = new File([blob], '{slug}.jpg', {{ type: 'image/jpeg' }});
            if (navigator.canShare && navigator.canShare({{ files: [file] }})) {{
                await navigator.share({{
                    files: [file],
                    title: shareData.title,
                    text: shareData.text + " " + shareData.url
                }});
            }} else {{
                await navigator.share({{ title: shareData.title, url: shareData.url }});
            }}
        }} catch (err) {{
            console.log('分享失败:', err);
        }}
    }}
    </script>
</body>
</html>
"""

    # 2. 批量生成 HTML
    for poem in poems:
        # 修正这里的 format 逻辑
        html_content = template.format(
            title=poem['title'],
            preview=poem['preview'],
            img=poem['img'],
            file=poem['file'],
            slug=poem['slug']
        )
        
        # --- 重点修复：这里的 output_file 不能有双大括号 ---
        output_file = f"poems/{poem['file']}"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

    print(f"✅ 大功告成！已重新生成 {len(poems)} 个正确的网页文件。")
