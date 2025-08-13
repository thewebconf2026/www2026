# WWW2026 网站自动部署配置

## 概述

本仓库已配置了GitHub Actions自动部署功能，当您向`main`分支推送代码时，网站将自动更新。

## 如何启用自动部署

### 1. 启用GitHub Pages

1. 进入您的GitHub仓库页面：`https://github.com/thewebconf2026/www2026`
2. 点击 **Settings** 标签页
3. 在左侧菜单中找到 **Pages** 选项
4. 在 **Source** 部分，选择 **GitHub Actions**
5. 点击 **Save** 保存设置

### 2. 验证部署

启用GitHub Pages后，您的网站将在以下地址可访问：
- `https://thewebconf2026.github.io/www2026/`

## 自动部署工作流程

1. **触发条件**：当您向`main`分支推送代码时
2. **构建过程**：GitHub Actions会自动构建网站
3. **部署过程**：构建完成后自动部署到GitHub Pages

## 如何更新网站

1. **直接在GitHub网页编辑**：
   - 在GitHub仓库中找到要编辑的文件
   - 点击文件名打开文件
   - 点击编辑按钮（铅笔图标）
   - 进行修改后，在页面底部填写提交信息
   - 点击 **Commit changes** 提交

2. **本地编辑后推送**：
   ```bash
   # 克隆仓库（如果还没有）
   git clone https://github.com/thewebconf2026/www2026.git
   cd www2026
   
   # 进行修改...
   
   # 提交并推送
   git add .
   git commit -m "更新网站内容"
   git push origin main
   ```

3. **自动部署**：
   - 推送后，GitHub Actions会自动运行
   - 您可以在仓库的 **Actions** 标签页查看部署进度
   - 部署完成后，网站会自动更新

## 常见问题

### Q: 如何查看部署状态？
A: 在GitHub仓库页面，点击 **Actions** 标签页，您可以看到所有的部署运行记录。

### Q: 部署失败怎么办？
A: 在 **Actions** 页面点击失败的运行记录，查看错误日志。常见问题包括：
- HTML语法错误
- 文件路径错误
- 图片文件过大

### Q: 网站更新需要多长时间？
A: 通常在推送代码后2-5分钟内完成部署。

## 文件结构说明

```
www2026/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions部署配置
├── css/                        # 样式文件
├── js/                         # JavaScript文件
├── images/                     # 图片资源
├── data/                       # 数据文件
├── index.html                  # 首页
├── about.html                  # 关于页面
├── calls.html                  # 征稿页面
├── program.html                # 程序页面
├── attending.html              # 参会页面
└── README-DEPLOYMENT.md        # 本文档
```

## 技术支持

如果您在使用过程中遇到问题，请：
1. 检查GitHub Actions的运行日志
2. 确认文件路径和语法正确
3. 联系技术支持团队

