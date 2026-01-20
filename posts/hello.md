# 欢迎来到 Nie.net


这是我的第一篇博客文章，运行在 **纯静态** 环境下。

## 为什么选择这个架构？

* **轻量**：不需要数据库，不占 VPS 内存。
* **快速**：Markdown 实时渲染。
* **Higan 风格**：极简、专注内容。

## 代码高亮测试

```python
def hello_world():
    print("Hello, NieKaiXiang!")
"技术是为了更好的生活，而不是为了折腾而折腾。"

---

### 4. 部署教程

由于你有 VPS 和 GitHub，推荐两种最适合你的方式：

#### 方案 A：部署在 VPS (Nginx) - **推荐**
因为你已经有 `as6.org` 或 `nkx.moe` 解析到服务器了。

1.  **上传文件**：
    使用 SFTP (如 FinalShell) 将 `index.html` 和 `posts` 文件夹上传到服务器目录，例如 `/var/www/myblog`。

2.  **配置 Nginx**：
    在你的 Nginx 配置文件中（通常在 `/etc/nginx/sites-available/default` 或 `vhost` 配置里），添加或修改：

    ```nginx
    server {
        listen 80;
        server_name blog.nkx.moe;  # 换成你的域名

        root /var/www/myblog;      # 刚才上传的目录
        index index.html;

        location / {
            try_files $uri $uri/ =404;
        }
    }
    ```
3.  **重启 Nginx**：`systemctl reload nginx`。

#### 方案 B：部署在 GitHub Pages (最省心)
如果你想把 VPS 留着跑 Docker 和 Python 脚本，不想放网页。

1.  **新建仓库**：在 GitHub 建一个仓库，例如 `blog`。
2.  **上传代码**：把 `index.html` 和 `posts` 文件夹 push 上去。
3.  **开启 Pages**：
    * 进入仓库 Settings -> Pages。
    * Build from branch 选择 `main` -> `/ root`。
    * 保存。
4.  **自定义域名** (可选)：在 Custom domain 填入 `nkx.moe`，然后在 Cloudflare/域名商那里 CNAME 解析到 `你的ID.github.io`。

### 5. 如何写新文章？

1.  在本地用 Markdown 编辑器（Typora/VSCode）写好 `xxx.md`。
2.  把文件丢进服务器的 `posts/` 文件夹。
3.  **关键一步**：打开 `index.html`，找到 `config` 部分，加一行：
    ```javascript
    { title: "新文章标题", file: "xxx.md", date: "2026-01-21" },
    ```
4.  保存，刷新网页，文章就出来了。
