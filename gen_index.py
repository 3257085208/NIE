import os
import json
import re

# 配置
POSTS_DIR = 'posts'
OUTPUT_FILE = 'posts.json'

def generate_json():
    posts = []
    
    # 扫描 posts 文件夹
    if not os.path.exists(POSTS_DIR):
        print(f"Directory {POSTS_DIR} not found.")
        return

    for filename in os.listdir(POSTS_DIR):
        if filename.endswith('.md'):
            # 解析文件名: 2026-01-20-标题.md
            # 如果文件名不规范，就用修改时间和文件名
            match = re.match(r'(\d{4}-\d{2}-\d{2})-(.+)\.md', filename)
            
            if match:
                date = match.group(1)
                title = match.group(2)
            else:
                date = "Unknown"
                title = filename.replace('.md', '')

            posts.append({
                "title": title,
                "date": date,
                "file": filename
            })

    # 按日期倒序排序
    posts.sort(key=lambda x: x['date'], reverse=True)

    # 写入 json
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    
    print(f"Generated {len(posts)} posts into {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_json()
