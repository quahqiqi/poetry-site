import json
import os

# 1. 指定 JSON 的路径（现在是在 poems 文件夹内）
json_path = 'poems/poems.json'

if not os.path.exists(json_path):
    print(f"错误：找不到文件 {json_path}，请检查路径！")
else:
    with open(json_path, 'r', encoding='utf-8') as f:
        poems = json.load(f)

    # HTML 模板
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
        body {{ font-family: "PingFang SC", "Microsoft YaHei", sans-serif; padding: 40px; max-width: 600px; margin: auto; line-height: 1.8; color: #333; }}
        .share-btn {{ margin-top: 30px; padding: 12px 24px; background: #222; color: #fff; border: none; cursor: pointer; border-radius: 30px; font-size: 16px; }}
        .share-btn:hover {{ background: #444; }}
    </style>
</head>
<body>
    <article>
        <h1>{title}</h1>
        <p style="white-space: pre-wrap;">{preview}</p>
    </article>
    
    <button class="share-btn" onclick="shareToSocial()">🔗 分享到 Instagram / 社交平台</button>

    <script>
    async function shareToSocial() {{
        const shareData = {{
            title: "{title}",
            text: "{preview}",
            url: window.location.href
        }};
        
        // 这里的路径 '../{img}' 表示从 poems 文件夹跳出来进入 images 文件夹
        const imageUrl = '../{img}'; 

        try {{
            const response = await fetch(imageUrl);
            const blob = await response.blob();
            // 创建图片文件对象
            const file = new File([blob], '{slug}.jpg', {{ type: 'image/jpeg' }});

            // 优先尝试调用原生分享面板（支持传图给 Instagram）
            if (navigator.canShare && navigator.canShare({{ files: [file] }})) {{
                await navigator.share({{
                    files: [file],
                    title: shareData.title,
                    text: shareData.text + " " + shareData.url
                }});
            }} else {{
                // 降级方案：只分享链接
                await navigator.share({{
                    title: shareData.title,
                    url: shareData.url
                }});
            }}
        }} catch (err) {{
            console.log('分享失败或被取消:', err);
        }}
    }}
    </script>
</body>
</html>
"""

    # 2. 批量生成 HTML
    for poem in poems:
        html_content = template.format(
            title=poem['title'],
            preview=poem['preview'],
            img=poem['img'],
            file=poem['file'],
            slug=poem['slug']
        )
        
        # 将 HTML 生成在 poems/ 文件夹下
        output_file = f"poems/{{poem['file']}}"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

    print(f"✅ 完成！已更新 {len(poems)} 首诗歌页面到 poems/ 目录。")
