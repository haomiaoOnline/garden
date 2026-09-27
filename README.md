# 🌱 程龙的数字花园

基于 [Quartz](https://github.com/jackyzha0/quartz) 构建的个人数字花园：梳理项目、沉淀知识、记录学习心得。先自我成长，顺带 build in public。

在线访问：https://haomiaoOnline.github.io/garden/

## 内容结构

```
content/
├── index.md          # 花园首页
├── 项目库/            # 每个项目一页：目标、进展、学到的东西
├── 知识库/            # 技术学习笔记
└── 成长记录/          # 学习心得与复盘
```

笔记成熟度：🌱 种子 → 🌿 生长中 → 🌳 长青

## 本地写作流程

1. 在 Obsidian 里写笔记（`content/` 可以直接作为 Obsidian 仓库打开）
2. 想公开的笔记放进 `content/`，私密笔记留在本地其他目录（`private/`、`templates/`、`.obsidian/` 会被自动忽略）
3. 本地预览：`npx quartz build --serve`，打开 http://localhost:8080
4. `git push` 到 `main` 分支，GitHub Actions 自动构建并发布到 GitHub Pages
