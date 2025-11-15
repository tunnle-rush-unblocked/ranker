#!/bin/bash

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "═══════════════════════════════════════════════════════════"
echo "        Netlify 全自动部署 - 一键配置脚本"
echo "═══════════════════════════════════════════════════════════"
echo ""

# 检查 Git 是否安装
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ 错误：未检测到 Git${NC}"
    echo "请先安装 Git: https://git-scm.com/"
    exit 1
fi

echo -e "${GREEN}✅ Git 已安装${NC}"
echo ""

# 检查是否已有 Git 仓库
if [ -d .git ]; then
    echo -e "${BLUE}ℹ️  检测到现有 Git 仓库${NC}"
    echo ""
else
    echo "📦 初始化 Git 仓库..."
    git init
    git add .
    git commit -m "初始提交：配置全自动部署"
    echo -e "${GREEN}✅ Git 仓库初始化完成${NC}"
    echo ""
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 接下来需要您完成以下步骤："
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "步骤 1：创建 GitHub 仓库"
echo "────────────────────────────────────────"
echo "   1. 访问：https://github.com/new"
echo "   2. 创建一个新仓库"
echo "   3. 复制仓库 URL"
echo ""
read -p "请粘贴您的 GitHub 仓库 URL: " REPO_URL
echo ""

if [ -n "$REPO_URL" ]; then
    echo "🔗 添加远程仓库..."
    git remote remove origin 2>/dev/null
    git remote add origin "$REPO_URL"
    git branch -M main
    
    echo "📤 推送代码到 GitHub..."
    if git push -u origin main; then
        echo -e "${GREEN}✅ 代码已推送到 GitHub${NC}"
    else
        echo -e "${YELLOW}⚠️  推送失败，请手动执行：${NC}"
        echo "   git push -u origin main"
    fi
    echo ""
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "步骤 2：配置 Netlify"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "请在浏览器中完成以下操作："
echo ""
echo "🌐 A. 创建 Netlify 站点"
echo "   ────────────────────────────────────────"
echo "   1. 访问：https://app.netlify.com/"
echo "   2. 点击 \"Add new site\" → \"Import an existing project\""
echo "   3. 选择 GitHub 并授权"
echo "   4. 选择您刚创建的仓库"
echo "   5. 点击 \"Deploy site\""
echo ""
read -p "按回车键继续..."
echo ""

echo "🔑 B. 获取 Netlify 凭证"
echo "   ────────────────────────────────────────"
echo "   获取 Auth Token:"
echo "   1. 访问：https://app.netlify.com/user/applications#personal-access-tokens"
echo "   2. 点击 \"New access token\""
echo "   3. 描述：GitHub Actions 自动部署"
echo "   4. 复制生成的 token"
echo ""
read -p "请粘贴 NETLIFY_AUTH_TOKEN: " NETLIFY_TOKEN
echo ""

echo "   获取 Site ID:"
echo "   1. 进入您的站点设置"
echo "   2. 在 \"Site details\" 找到 \"Site ID\""
echo "   3. 复制 Site ID"
echo ""
read -p "请粘贴 NETLIFY_SITE_ID: " NETLIFY_SITE_ID
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "步骤 3：配置 GitHub Secrets"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "请在 GitHub 完成以下操作："
echo ""
echo "1. 进入您的仓库"
echo "2. Settings → Secrets and variables → Actions"
echo "3. 点击 \"New repository secret\""
echo ""
echo "添加第一个密钥："
echo "   Name:  NETLIFY_AUTH_TOKEN"
echo "   Value: $NETLIFY_TOKEN"
echo ""
echo "添加第二个密钥："
echo "   Name:  NETLIFY_SITE_ID"
echo "   Value: $NETLIFY_SITE_ID"
echo ""
read -p "按回车键继续..."
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "步骤 4：启用 GitHub Actions"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. 在 GitHub 仓库点击 \"Actions\" 标签"
echo "2. 如果需要，点击 \"I understand my workflows\""
echo "3. 查看自动部署工作流"
echo ""
read -p "按回车键继续..."
echo ""

echo "═══════════════════════════════════════════════════════════"
echo -e "${GREEN}✅ 配置完成！${NC}"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "🎉 全自动部署已启用！"
echo ""
echo "日常使用："
echo "   1. 修改代码"
echo "   2. git add ."
echo "   3. git commit -m \"更新描述\""
echo "   4. git push"
echo "   5. 自动部署！✨"
echo ""
echo "📋 查看部署状态："
echo "   GitHub Actions: ${REPO_URL}/actions"
echo "   Netlify: https://app.netlify.com/"
echo ""
echo "📚 详细文档：请查看 \"自动部署配置指南.md\""
echo ""
echo "═══════════════════════════════════════════════════════════"

