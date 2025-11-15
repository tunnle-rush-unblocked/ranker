#!/bin/bash

# Netlify 自动部署脚本

echo "🚀 开始部署到 Netlify..."

# 检查是否安装了 Git
if ! command -v git &> /dev/null; then
    echo "❌ 错误：未安装 Git"
    echo "请先安装 Git: https://git-scm.com/"
    exit 1
fi

# 检查是否已初始化 Git 仓库
if [ ! -d .git ]; then
    echo "📦 初始化 Git 仓库..."
    git init
    git add .
    git commit -m "初始提交: 配置 Netlify 自动部署"
    echo "✅ Git 仓库初始化完成"
else
    echo "✅ Git 仓库已存在"
fi

echo ""
echo "📝 接下来的步骤："
echo ""
echo "1. 在 GitHub/GitLab/Bitbucket 创建一个新仓库"
echo ""
echo "2. 添加远程仓库并推送："
echo "   git remote add origin <你的仓库 URL>"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. 访问 Netlify: https://app.netlify.com/"
echo "   - 点击 'Add new site' → 'Import an existing project'"
echo "   - 选择你的 Git 提供商"
echo "   - 选择你刚创建的仓库"
echo "   - Netlify 会自动识别配置文件"
echo "   - 点击 'Deploy site'"
echo ""
echo "4. 完成！每次推送代码都会自动部署 🎉"
echo ""
echo "💡 提示：也可以使用 Netlify CLI 快速部署"
echo "   npm install -g netlify-cli"
echo "   netlify login"
echo "   netlify init"
echo "   netlify deploy --prod"

