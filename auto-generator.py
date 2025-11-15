#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化 SEO 网站生成器
功能：读取关键词 -> 搜索分析 -> 生成网页 -> 自动部署
"""

import os
import re
import json
import time
import subprocess
import urllib.parse
from datetime import datetime
from pathlib import Path

# 配置
MAX_KEYWORDS = 5  # 每次处理的关键词数量（可以改大）
SEARCH_DELAY = 2  # 搜索间隔（秒）
OUTPUT_DIR = "generated_sites"

class SiteGenerator:
    def __init__(self):
        self.keywords = []
        self.current_keyword = None
        self.site_dir = None
        
    def read_keywords(self, filename="kw.txt", max_count=MAX_KEYWORDS):
        """读取关键词文件"""
        print(f"📖 读取关键词文件: {filename}")
        keywords = []
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    if i == 0:  # 跳过标题行
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
        print(f"✅ 成功读取 {len(keywords)} 个关键词")
        return keywords
    
    def search_google(self, keyword):
        """搜索谷歌并获取前三名网页"""
        print(f"🔍 搜索关键词: {keyword}")
        
        # 模拟搜索结果（真实环境需要使用搜索 API）
        # 这里我们基于关键词生成内容
        search_results = {
            'keyword': keyword,
            'top_sites': [
                {
                    'title': f'{keyword.title()} - Calculator Tool',
                    'url': f'https://example1.com/{keyword.replace(" ", "-")}',
                    'description': f'Free online {keyword} tool'
                },
                {
                    'title': f'Best {keyword.title()} Online',
                    'url': f'https://example2.com/{keyword.replace(" ", "-")}',
                    'description': f'Calculate your {keyword} quickly'
                },
                {
                    'title': f'{keyword.title()} Guide',
                    'url': f'https://example3.com/{keyword.replace(" ", "-")}',
                    'description': f'Complete guide for {keyword}'
                }
            ]
        }
        
        time.sleep(SEARCH_DELAY)
        return search_results
    
    def analyze_content(self, search_results):
        """分析搜索结果内容"""
        keyword = search_results['keyword']
        
        # 基于关键词分析类型
        analysis = {
            'keyword': keyword,
            'type': 'calculator',
            'purpose': f'Calculate {keyword}',
            'features': [
                'Easy to use interface',
                'Instant results',
                'Mobile friendly',
                'Free to use'
            ]
        }
        
        return analysis
    
    def generate_calculator_page(self, keyword, analysis):
        """生成计算器页面"""
        print(f"🎨 生成计算器页面: {keyword}")
        
        # 创建干净的关键词（用于文件名和标题）
        clean_keyword = re.sub(r'[^a-z0-9\s-]', '', keyword.lower())
        slug = clean_keyword.replace(' ', '-')
        title = keyword.title()
        
        # HTML 内容
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Free online {keyword} tool. Easy to use, instant results, mobile friendly. Calculate your {keyword} quickly and accurately.">
    <meta name="keywords" content="{keyword}, calculator, online tool, free calculator">
    <meta name="author" content="{title} Calculator">
    <meta property="og:title" content="{title} - Free Online Calculator">
    <meta property="og:description" content="Calculate your {keyword} quickly and easily with our free online tool.">
    <meta property="og:type" content="website">
    <title>{title} - Free Online Calculator</title>
    <link rel="canonical" href="https://calculatorusa123.netlify.app/{slug}.html">
    <link rel="stylesheet" href="calculator-style.css">
</head>
<body>
    <header>
        <nav>
            <div class="nav-container">
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
    
    <main>
        <section class="hero">
            <h1>{title}</h1>
            <p>Free, fast, and accurate online calculator tool</p>
        </section>
        
        <section class="calculator-container">
            <div class="calculator-card">
                <h2>Calculate Your {title}</h2>
                
                <div class="input-group">
                    <label for="input1">Value 1:</label>
                    <input type="number" id="input1" placeholder="Enter value" step="any">
                </div>
                
                <div class="input-group">
                    <label for="input2">Value 2:</label>
                    <input type="number" id="input2" placeholder="Enter value" step="any">
                </div>
                
                <div class="input-group">
                    <label for="input3">Value 3 (Optional):</label>
                    <input type="number" id="input3" placeholder="Enter value" step="any">
                </div>
                
                <button class="calculate-btn" onclick="calculate()">Calculate</button>
                <button class="reset-btn" onclick="resetForm()">Reset</button>
                
                <div class="result-container" id="result">
                    <h3>Result:</h3>
                    <p class="result-value" id="resultValue">Enter values and click Calculate</p>
                </div>
            </div>
        </section>
        
        <section class="info-section">
            <div class="info-card">
                <h2>About This {title}</h2>
                <p>Our {keyword} is designed to help you quickly and accurately calculate results. Whether you're a student, professional, or just need quick calculations, our tool is here to help.</p>
            </div>
            
            <div class="info-card">
                <h2>✨ Key Features</h2>
                <ul>
                    <li>✅ Free to use - No registration required</li>
                    <li>⚡ Instant results - Get answers immediately</li>
                    <li>📱 Mobile friendly - Works on all devices</li>
                    <li>🎯 Accurate - Precise calculations every time</li>
                    <li>🔒 Privacy focused - No data collection</li>
                    <li>🌐 Always available - 24/7 access</li>
                </ul>
            </div>
            
            <div class="info-card">
                <h2>📖 How to Use</h2>
                <ol>
                    <li>Enter your values in the input fields</li>
                    <li>Click the "Calculate" button</li>
                    <li>View your instant results</li>
                    <li>Use the "Reset" button to start over</li>
                </ol>
            </div>
            
            <div class="info-card">
                <h2>❓ FAQ</h2>
                <details>
                    <summary>Is this calculator free?</summary>
                    <p>Yes! Our {keyword} is completely free to use with no hidden fees or registration required.</p>
                </details>
                <details>
                    <summary>Do I need to install anything?</summary>
                    <p>No installation needed. Just open your browser and start calculating.</p>
                </details>
                <details>
                    <summary>Is my data safe?</summary>
                    <p>Absolutely. All calculations are performed in your browser. We don't store or collect any of your data.</p>
                </details>
                <details>
                    <summary>Can I use this on mobile?</summary>
                    <p>Yes! Our calculator is fully responsive and works perfectly on smartphones and tablets.</p>
                </details>
            </div>
        </section>
        
        <section class="cta-section">
            <h2>Need More Calculators?</h2>
            <p>Explore our collection of free online calculators</p>
            <a href="index.html" class="cta-button">View All Calculators</a>
        </section>
    </main>
    
    <footer>
        <div class="footer-container">
            <div class="footer-col">
                <h3>Quick Links</h3>
                <ul>
                    <li><a href="index.html">Home</a></li>
                    <li><a href="about.html">About Us</a></li>
                    <li><a href="sitemap.html">Sitemap</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h3>Legal</h3>
                <ul>
                    <li><a href="privacy.html">Privacy Policy</a></li>
                    <li><a href="terms.html">Terms of Service</a></li>
                    <li><a href="contact.html">Contact Us</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h3>Connect</h3>
                <p>Have questions? <a href="contact.html">Get in touch</a></p>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; {datetime.now().year} Calculator Pro. All rights reserved.</p>
        </div>
    </footer>
    
    <script src="calculator.js"></script>
    <script>
        function calculate() {{
            const input1 = parseFloat(document.getElementById('input1').value) || 0;
            const input2 = parseFloat(document.getElementById('input2').value) || 0;
            const input3 = parseFloat(document.getElementById('input3').value) || 0;
            
            // 基础计算逻辑（可根据不同计算器类型定制）
            let result = input1 + input2 + input3;
            
            document.getElementById('resultValue').textContent = result.toFixed(2);
            document.getElementById('result').style.display = 'block';
        }}
        
        function resetForm() {{
            document.getElementById('input1').value = '';
            document.getElementById('input2').value = '';
            document.getElementById('input3').value = '';
            document.getElementById('resultValue').textContent = 'Enter values and click Calculate';
        }}
    </script>
</body>
</html>"""
        
        return html, slug
    
    def create_site_structure(self, keyword):
        """创建网站目录结构"""
        clean_keyword = re.sub(r'[^a-z0-9\s-]', '', keyword.lower())
        slug = clean_keyword.replace(' ', '-')[:50]  # 限制长度
        
        site_dir = Path(OUTPUT_DIR) / slug
        site_dir.mkdir(parents=True, exist_ok=True)
        
        self.site_dir = site_dir
        return site_dir
    
    def generate_seo_pages(self, site_dir, keyword):
        """生成 SEO 相关页面"""
        print(f"📄 生成 SEO 页面")
        
        # 生成 sitemap.xml
        sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://calculatorusa123.netlify.app/</loc>
        <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://calculatorusa123.netlify.app/about.html</loc>
        <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://calculatorusa123.netlify.app/privacy.html</loc>
        <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <priority>0.5</priority>
    </url>
    <url>
        <loc>https://calculatorusa123.netlify.app/terms.html</loc>
        <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <priority>0.5</priority>
    </url>
    <url>
        <loc>https://calculatorusa123.netlify.app/contact.html</loc>
        <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <priority>0.7</priority>
    </url>
</urlset>"""
        
        with open(site_dir / "sitemap.xml", 'w', encoding='utf-8') as f:
            f.write(sitemap)
        
        # robots.txt
        robots = """User-agent: *
Allow: /
Sitemap: https://calculatorusa123.netlify.app/sitemap.xml"""
        
        with open(site_dir / "robots.txt", 'w', encoding='utf-8') as f:
            f.write(robots)
        
        print(f"✅ SEO 页面已生成")
    
    def process_keyword(self, keyword):
        """处理单个关键词的完整流程"""
        print(f"\n{'='*60}")
        print(f"🚀 处理关键词: {keyword}")
        print(f"{'='*60}")
        
        try:
            # 1. 搜索
            search_results = self.search_google(keyword)
            
            # 2. 分析
            analysis = self.analyze_content(search_results)
            
            # 3. 创建目录
            site_dir = self.create_site_structure(keyword)
            
            # 4. 生成计算器页面
            html, slug = self.generate_calculator_page(keyword, analysis)
            with open(site_dir / f"{slug}.html", 'w', encoding='utf-8') as f:
                f.write(html)
            
            # 5. 生成 SEO 页面
            self.generate_seo_pages(site_dir, keyword)
            
            print(f"✅ 关键词 '{keyword}' 处理完成")
            return True
            
        except Exception as e:
            print(f"❌ 处理关键词 '{keyword}' 时出错: {e}")
            return False
    
    def run(self):
        """运行主程序"""
        print(f"\n{'#'*60}")
        print(f"# 🤖 自动化 SEO 网站生成器")
        print(f"{'#'*60}\n")
        
        # 读取关键词
        keywords = self.read_keywords()
        if not keywords:
            print("❌ 没有找到关键词")
            return
        
        # 处理每个关键词
        success_count = 0
        for i, keyword in enumerate(keywords, 1):
            print(f"\n进度: {i}/{len(keywords)}")
            if self.process_keyword(keyword):
                success_count += 1
        
        # 总结
        print(f"\n{'='*60}")
        print(f"✅ 完成！成功处理 {success_count}/{len(keywords)} 个关键词")
        print(f"📁 生成的网站位于: {OUTPUT_DIR}/")
        print(f"{'='*60}\n")

if __name__ == "__main__":
    generator = SiteGenerator()
    generator.run()

