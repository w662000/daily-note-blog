# daily-note-blog

由 WorkBuddy 自动发布的「每日工作日志」博客，使用 Jekyll + GitHub Pages 构建。

## 访问地址
https://w662000.github.io/daily-note-blog/

## 工作机制
- 每天 23:30，本机任务把当天的「每日工作总结」md 转换成 Jekyll 文章（`_posts/YYYY-MM-DD-daily-summary.md`，带 frontmatter）并 `git push`。
- 推送后 GitHub Pages 在云端自动把 Markdown 渲染成博客页面，无需任何桌面软件、无需手动「同步」。
- 该仓库作为**项目站点**挂在 `/daily-note-blog/` 子路径，与 Gridea 使用的 `w662000.github.io` 根域名**并存、互不影响**。

## 目录结构
- `_config.yml`：站点配置（baseurl、标题等）
- `_layouts/default.html`：页面布局与样式
- `index.md`：首页文章列表
- `_posts/`：每日日志文章（由脚本自动生成）

## 维护
- 如需改样式，编辑 `_layouts/default.html`。
- 新文章由同步脚本自动生成，无需手动添加。
