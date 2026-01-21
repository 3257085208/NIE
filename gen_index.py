name: Auto Build

on:
  push:
    branches: [ "main" ]
  workflow_dispatch:

permissions:
  contents: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Generate JSON with Metadata
        run: |
          python3 -c "
          import os, json, re

          posts = []
          POSTS_DIR = 'posts'

          if os.path.exists(POSTS_DIR):
              for f in os.listdir(POSTS_DIR):
                  if f.endswith('.md'):
                      filepath = os.path.join(POSTS_DIR, f)
                      
                      # 默认值 (如果文章没写头信息，就用这些兜底)
                      metadata = {
                          'title': f.replace('.md', ''),
                          'date': 'Unknown',
                          'category': '日常',  # 默认分类
                          'tags': [],
                          'file': f
                      }

                      # 尝试从文件名获取日期 (YYYY-MM-DD-标题.md)
                      filename_match = re.match(r'(\d{4}-\d{2}-\d{2})-(.+)\.md', f)
                      if filename_match:
                          metadata['date'] = filename_match.group(1)
                          metadata['title'] = filename_match.group(2)

                      # 读取文件内容解析 Front Matter
                      with open(filepath, 'r', encoding='utf-8') as file:
                          content = file.read()
                          
                          # 正则匹配 --- 之间的内容
                          front_matter = re.search(r'^---\s+(.*?)\s+---', content, re.DOTALL)
                          
                          if front_matter:
                              yaml_text = front_matter.group(1)
                              for line in yaml_text.split('\n'):
                                  if ':' in line:
                                      key, value = line.split(':', 1)
                                      key = key.strip()
                                      value = value.strip()
                                      
                                      # 处理数组格式 [Tag1, Tag2]
                                      if key == 'tags' and value.startswith('[') and value.endswith(']'):
                                          value = [t.strip() for t in value[1:-1].split(',')]
                                      elif key == 'tags': # 处理 tags: tag1 (单个)
                                          value = [value]
                                      
                                      metadata[key] = value

                      posts.append(metadata)

          # 按日期倒序
          posts.sort(key=lambda x: x['date'], reverse=True)

          with open('posts.json', 'w', encoding='utf-8') as out:
              json.dump(posts, out, ensure_ascii=False)
          print('JSON Generated')
          "

      - name: Commit and Push
        run: |
          git config --global user.name 'github-actions[bot]'
          git config --global user.email '41898282+github-actions[bot]@users.noreply.github.com'
          git add posts.json
          git commit -m "Auto update metadata" || echo "No changes to commit"
          git push
