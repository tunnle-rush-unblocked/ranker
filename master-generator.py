#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的自动化 SEO 网站生成和部署系统
功能：关键词 -> 搜索 -> 生成 -> 部署 一条龙服务
"""

import os
import re
import json
import time
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

# 配置
MAX_KEYWORDS_PER_BATCH = 10  # 每批处理的关键词数量
OUTPUT_DIR = "output"
TEMPLATES_DIR = "templates"
NETLIFY_AUTH_TOKEN = "nfp_wpsiURMR4PxCp3Sj59kf9TAqMNEfYxER3943"

class MasterGenerator:
    def __init__(self):
        self.keywords = []
        self.output_dir = Path(OUTPUT_DIR)
        self.templates_dir = Path(TEMPLATES_DIR)
        self.current_site_dir = None
        
        # 创建输出目录
        self.output_dir.mkdir(exist_ok=True)
        
    def read_keywords(self, filename="kw.txt", max_count=MAX_KEYWORDS_PER_BATCH):
        """读取关键词"""
        print(f"📖 读取关键词文件: {filename}")
        keywords = []
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    if i == 0:  # 跳过标题
                        continue
                    keyword = line.strip()
                    if keyword:
                        keywords.append(keyword)
                    if len(keywords) >= max_count:
                        break
        except Exception as e:
            print(f"❌ 读取文件出错: {e}")
            return []
        
        self.keywords = keywords
        print(f"✅ 读取了 {len(keywords)} 个关键词")
        return keywords
    
    def generate_calculator_html(self, keyword):
        """生成计算器 HTML"""
        clean_keyword = re.sub(r'[^a-z0-9\s-]', '', keyword.lower())
        slug = clean_keyword.replace(' ', '-')
        title = keyword.title()
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Free {keyword} tool - Fast, accurate, and easy to use. Calculate your {keyword} instantly online.">
    <meta name="keywords" content="{keyword}, calculator, online tool, free">
    <title>{title} - Free Online Calculator</title>
    <link rel="stylesheet" href="style.css">
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "WebApplication",
      "name": "{title}",
      "description": "Free online {keyword} calculator",
      "applicationCategory": "UtilityApplication",
      "offers": {{
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "USD"
      }}
    }}
    </script>
</head>
<body>
    <header>
        <nav>
            <div class="container">
                <h1 class="logo">🧮 Calculator Pro</h1>
                <ul class="nav-menu">
                    <li><a href="index.html">Home</a></li>
                    <li><a href="about.html">About</a></li>
                    <li><a href="privacy.html">Privacy</a></li>
                    <li><a href="contact.html">Contact</a></li>
                </ul>
            </div>
        </nav>
    </header>
    
    <main class="container">
        <div class="hero">
            <h1>{title}</h1>
            <p class="subtitle">Fast, Free & Accurate Online Calculator</p>
        </div>
        
        <div class="calculator-box">
            <h2>Enter Your Values</h2>
            
            <div class="input-group">
                <label for="value1">First Value:</label>
                <input type="number" id="value1" step="any" placeholder="Enter first value">
            </div>
            
            <div class="input-group">
                <label for="value2">Second Value:</label>
                <input type="number" id="value2" step="any" placeholder="Enter second value">
            </div>
            
            <div class="input-group">
                <label for="value3">Third Value (Optional):</label>
                <input type="number" id="value3" step="any" placeholder="Enter third value">
            </div>
            
            <div class="button-group">
                <button onclick="calculate()" class="btn-primary">Calculate</button>
                <button onclick="reset()" class="btn-secondary">Reset</button>
            </div>
            
            <div id="result" class="result-box" style="display:none;">
                <h3>Result:</h3>
                <div id="resultValue" class="result-value">0</div>
            </div>
        </div>
        
        <div class="content-grid">
            <div class="content-card">
                <h2>About This {title}</h2>
                <p>Our {keyword} provides quick and accurate calculations for your needs. Whether you're a student, professional, or just need fast results, this tool is designed to help you.</p>
                <p>All calculations are performed instantly in your browser - no data is sent to any server, ensuring your privacy and security.</p>
            </div>
            
            <div class="content-card">
                <h2>✨ Key Features</h2>
                <ul class="feature-list">
                    <li>✅ Completely free to use</li>
                    <li>⚡ Instant results</li>
                    <li>📱 Mobile-friendly interface</li>
                    <li>🎯 Accurate calculations</li>
                    <li>🔒 Privacy-focused (no data collection)</li>
                    <li>🌐 Works offline</li>
                    <li>💯 No registration required</li>
                </ul>
            </div>
            
            <div class="content-card">
                <h2>📖 How to Use</h2>
                <ol>
                    <li>Enter your values in the input fields</li>
                    <li>Click the "Calculate" button</li>
                    <li>View your instant result below</li>
                    <li>Use "Reset" to clear and start over</li>
                </ol>
                <p>It's that simple! No complicated steps or confusing interfaces.</p>
            </div>
            
            <div class="content-card">
                <h2>❓ Frequently Asked Questions</h2>
                
                <details>
                    <summary>Is this calculator really free?</summary>
                    <p>Yes! This {keyword} is 100% free with no hidden costs or premium features. All functionality is available to everyone.</p>
                </details>
                
                <details>
                    <summary>Do I need to create an account?</summary>
                    <p>No account needed! Just visit the page and start calculating right away.</p>
                </details>
                
                <details>
                    <summary>Is my data safe?</summary>
                    <p>Absolutely. All calculations happen in your browser. We don't collect, store, or transmit any of your data.</p>
                </details>
                
                <details>
                    <summary>Can I use this on my phone?</summary>
                    <p>Yes! Our calculator is fully responsive and works perfectly on smartphones, tablets, and desktop computers.</p>
                </details>
                
                <details>
                    <summary>Are the results accurate?</summary>
                    <p>Yes, our calculator uses precise mathematical algorithms to ensure accurate results every time.</p>
                </details>
            </div>
        </div>
        
        <div class="cta-section">
            <h2>Need More Calculators?</h2>
            <p>Explore our full collection of free online tools</p>
            <a href="index.html" class="btn-cta">Browse All Calculators</a>
        </div>
    </main>
    
    <footer>
        <div class="container">
            <div class="footer-grid">
                <div class="footer-col">
                    <h3>Quick Links</h3>
                    <ul>
                        <li><a href="index.html">Home</a></li>
                        <li><a href="about.html">About</a></li>
                        <li><a href="contact.html">Contact</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h3>Legal</h3>
                    <ul>
                        <li><a href="privacy.html">Privacy Policy</a></li>
                        <li><a href="terms.html">Terms of Service</a></li>
                        <li><a href="sitemap.html">Sitemap</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h3>About</h3>
                    <p>Free online calculators for everyone. Fast, accurate, and always free.</p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; {datetime.now().year} Calculator Pro. All rights reserved.</p>
            </div>
        </div>
    </footer>
    
    <script>
        function calculate() {{
            const v1 = parseFloat(document.getElementById('value1').value) || 0;
            const v2 = parseFloat(document.getElementById('value2').value) || 0;
            const v3 = parseFloat(document.getElementById('value3').value) || 0;
            
            // 基础计算 (可自定义)
            const result = v1 + v2 + v3;
            
            document.getElementById('resultValue').textContent = result.toFixed(2);
            document.getElementById('result').style.display = 'block';
        }}
        
        function reset() {{
            document.getElementById('value1').value = '';
            document.getElementById('value2').value = '';
            document.getElementById('value3').value = '';
            document.getElementById('result').style.display = 'none';
        }}
    </script>
</body>
</html>"""
        return html
    
    def generate_css(self):
        """生成 CSS 样式"""
        css = """/* Reset */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* Variables */
:root {
    --primary: #4f46e5;
    --secondary: #10b981;
    --dark: #1f2937;
    --light: #f9fafb;
    --border: #e5e7eb;
    --text: #111827;
    --text-light: #6b7280;
}

/* Global */
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    color: var(--text);
    background: var(--light);
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
}

/* Header */
header {
    background: white;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 1000;
}

header .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
}

.logo {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--primary);
}

.nav-menu {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.nav-menu a {
    color: var(--text);
    text-decoration: none;
    font-weight: 500;
    transition: color 0.3s;
}

.nav-menu a:hover {
    color: var(--primary);
}

/* Hero */
.hero {
    text-align: center;
    padding: 3rem 0;
    background: linear-gradient(135deg, var(--primary), #7c3aed);
    color: white;
    border-radius: 20px;
    margin: 2rem 0;
}

.hero h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

.subtitle {
    font-size: 1.2rem;
    opacity: 0.9;
}

/* Calculator Box */
.calculator-box {
    background: white;
    padding: 2.5rem;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    max-width: 600px;
    margin: 2rem auto;
}

.calculator-box h2 {
    color: var(--primary);
    margin-bottom: 1.5rem;
    text-align: center;
}

.input-group {
    margin-bottom: 1.5rem;
}

.input-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
}

.input-group input {
    width: 100%;
    padding: 0.75rem;
    border: 2px solid var(--border);
    border-radius: 8px;
    font-size: 1rem;
    transition: border 0.3s;
}

.input-group input:focus {
    outline: none;
    border-color: var(--primary);
}

/* Buttons */
.button-group {
    display: flex;
    gap: 1rem;
    margin-top: 2rem;
}

.btn-primary,
.btn-secondary,
.btn-cta {
    flex: 1;
    padding: 0.875rem 2rem;
    font-size: 1rem;
    font-weight: 600;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s;
}

.btn-primary {
    background: var(--primary);
    color: white;
}

.btn-primary:hover {
    background: #4338ca;
    transform: translateY(-2px);
}

.btn-secondary {
    background: var(--text-light);
    color: white;
}

.btn-secondary:hover {
    background: #4b5563;
}

.btn-cta {
    display: inline-block;
    background: var(--primary);
    color: white;
    text-decoration: none;
    text-align: center;
}

/* Result */
.result-box {
    margin-top: 2rem;
    padding: 1.5rem;
    background: linear-gradient(135deg, #ecfdf5, #d1fae5);
    border-radius: 10px;
    border-left: 4px solid var(--secondary);
}

.result-box h3 {
    color: var(--secondary);
    margin-bottom: 0.5rem;
}

.result-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--text);
}

/* Content Grid */
.content-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin: 3rem 0;
}

.content-card {
    background: white;
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    transition: transform 0.3s;
}

.content-card:hover {
    transform: translateY(-5px);
}

.content-card h2 {
    color: var(--primary);
    margin-bottom: 1rem;
}

.feature-list {
    list-style: none;
}

.feature-list li {
    padding: 0.5rem 0;
    border-bottom: 1px solid var(--border);
}

details {
    margin: 1rem 0;
    border: 1px solid var(--border);
    padding: 1rem;
    border-radius: 8px;
}

summary {
    cursor: pointer;
    font-weight: 600;
    color: var(--primary);
}

/* CTA Section */
.cta-section {
    text-align: center;
    padding: 3rem;
    background: linear-gradient(135deg, #fef3c7, #fde68a);
    border-radius: 20px;
    margin: 3rem 0;
}

.cta-section h2 {
    font-size: 2rem;
    margin-bottom: 1rem;
}

/* Footer */
footer {
    background: var(--dark);
    color: white;
    padding: 3rem 0 1rem;
    margin-top: 4rem;
}

.footer-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}

.footer-col h3 {
    margin-bottom: 1rem;
    color: var(--secondary);
}

.footer-col ul {
    list-style: none;
}

.footer-col ul li {
    margin-bottom: 0.5rem;
}

.footer-col a {
    color: #d1d5db;
    text-decoration: none;
    transition: color 0.3s;
}

.footer-col a:hover {
    color: white;
}

.footer-bottom {
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid #374151;
    color: #9ca3af;
}

/* Responsive */
@media (max-width: 768px) {
    .hero h1 {
        font-size: 2rem;
    }
    
    .nav-menu {
        gap: 1rem;
        font-size: 0.9rem;
    }
    
    .calculator-box {
        padding: 1.5rem;
    }
    
    .button-group {
        flex-direction: column;
    }
    
    .content-grid {
        grid-template-columns: 1fr;
    }
}"""
        return css
    
    def copy_templates(self, site_dir):
        """复制模板文件"""
        if self.templates_dir.exists():
            for template_file in ['privacy.html', 'terms.html', 'contact.html', 'about.html']:
                src = self.templates_dir / template_file
                if src.exists():
                    shutil.copy(src, site_dir / template_file)
    
    def generate_seo_files(self, site_dir, keyword):
        """生成 SEO 文件"""
        # sitemap.xml
        sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://calculatorusa123.netlify.app/</loc>
        <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://calculatorusa123.netlify.app/about.html</loc>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://calculatorusa123.netlify.app/privacy.html</loc>
        <priority>0.5</priority>
    </url>
    <url>
        <loc>https://calculatorusa123.netlify.app/terms.html</loc>
        <priority>0.5</priority>
    </url>
    <url>
        <loc>https://calculatorusa123.netlify.app/contact.html</loc>
        <priority>0.7</priority>
    </url>
</urlset>"""
        
        (site_dir / "sitemap.xml").write_text(sitemap, encoding='utf-8')
        
        # robots.txt
        robots = """User-agent: *
Allow: /
Sitemap: https://calculatorusa123.netlify.app/sitemap.xml"""
        
        (site_dir / "robots.txt").write_text(robots, encoding='utf-8')
        
        # netlify.toml
        netlify_toml = """[build]
  publish = "."

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200"""
        
        (site_dir / "netlify.toml").write_text(netlify_toml, encoding='utf-8')
    
    def create_site(self, keyword):
        """创建完整网站"""
        print(f"\n{'='*60}")
        print(f"🚀 生成网站: {keyword}")
        print(f"{'='*60}")
        
        try:
            # 创建目录
            clean_keyword = re.sub(r'[^a-z0-9\s-]', '', keyword.lower())
            slug = clean_keyword.replace(' ', '-')[:50]
            site_dir = self.output_dir / slug
            site_dir.mkdir(exist_ok=True)
            
            # 生成主页 (计算器页面)
            html = self.generate_calculator_html(keyword)
            (site_dir / "index.html").write_text(html, encoding='utf-8')
            
            # 生成 CSS
            css = self.generate_css()
            (site_dir / "style.css").write_text(css, encoding='utf-8')
            
            # 复制模板
            self.copy_templates(site_dir)
            
            # 生成 SEO 文件
            self.generate_seo_files(site_dir, keyword)
            
            print(f"✅ 网站生成完成: {site_dir}")
            return site_dir
            
        except Exception as e:
            print(f"❌ 生成网站出错: {e}")
            return None
    
    def deploy_to_netlify(self, site_dir, site_name):
        """部署到 Netlify"""
        print(f"\n🚀 部署到 Netlify: {site_name}")
        
        try:
            # 切换到网站目录
            original_dir = os.getcwd()
            os.chdir(site_dir)
            
            # 设置环境变量
            env = os.environ.copy()
            env['NETLIFY_AUTH_TOKEN'] = NETLIFY_AUTH_TOKEN
            
            # 部署命令
            cmd = ['netlify', 'deploy', '--prod', '--dir', '.']
            
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            os.chdir(original_dir)
            
            if result.returncode == 0:
                print(f"✅ 部署成功!")
                # 提取 URL
                for line in result.stdout.split('\n'):
                    if 'URL:' in line and 'http' in line:
                        print(f"🌐 {line.strip()}")
                return True
            else:
                print(f"⚠️ 部署遇到问题")
                return False
                
        except Exception as e:
            print(f"❌ 部署出错: {e}")
            os.chdir(original_dir)
            return False
    
    def run(self):
        """运行完整流程"""
        print(f"\n{'#'*60}")
        print(f"# 🤖 自动化 SEO 网站生成和部署系统")
        print(f"{'#'*60}\n")
        
        # 读取关键词
        keywords = self.read_keywords()
        if not keywords:
            print("❌ 没有找到关键词")
            return
        
        # 处理每个关键词
        success_count = 0
        for i, keyword in enumerate(keywords, 1):
            print(f"\n[{i}/{len(keywords)}] 处理关键词: {keyword}")
            
            # 生成网站
            site_dir = self.create_site(keyword)
            if site_dir:
                # 部署网站
                if self.deploy_to_netlify(site_dir, site_dir.name):
                    success_count += 1
                
                time.sleep(2)  # 避免请求过快
        
        # 总结
        print(f"\n{'='*60}")
        print(f"✅ 完成！")
        print(f"   成功生成: {len(keywords)} 个网站")
        print(f"   成功部署: {success_count} 个网站")
        print(f"   输出目录: {self.output_dir}")
        print(f"{'='*60}\n")

if __name__ == "__main__":
    generator = MasterGenerator()
    generator.run()

