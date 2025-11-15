#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动部署脚本 - 将生成的网站部署到 Netlify
"""

import os
import subprocess
import time
import json
from pathlib import Path

# 配置
NETLIFY_AUTH_TOKEN = "nfp_wpsiURMR4PxCp3Sj59kf9TAqMNEfYxER3943"
SITE_DIR = "generated_sites"

class NetlifyDeployer:
    def __init__(self, auth_token):
        self.auth_token = auth_token
        
    def check_netlify_cli(self):
        """检查 Netlify CLI 是否已安装"""
        try:
            result = subprocess.run(['netlify', '--version'], 
                                  capture_output=True, text=True)
            print(f"✅ Netlify CLI 已安装: {result.stdout.strip()}")
            return True
        except FileNotFoundError:
            print("❌ Netlify CLI 未安装")
            print("正在安装...")
            subprocess.run(['npm', 'install', '-g', 'netlify-cli'], check=True)
            return True
    
    def deploy_site(self, site_path, site_name):
        """部署单个网站"""
        print(f"\n{'='*60}")
        print(f"🚀 部署网站: {site_name}")
        print(f"📁 路径: {site_path}")
        print(f"{'='*60}")
        
        try:
            # 切换到网站目录
            os.chdir(site_path)
            
            # 设置环境变量
            env = os.environ.copy()
            env['NETLIFY_AUTH_TOKEN'] = self.auth_token
            
            # 部署到 Netlify
            cmd = [
                'netlify', 'deploy',
                '--prod',
                '--dir', '.',
                '--message', f'Auto-deploy: {site_name}'
            ]
            
            print("⏳ 正在部署...")
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode == 0:
                # 从输出中提取 URL
                output = result.stdout
                if 'Website URL:' in output or 'Live URL:' in output:
                    for line in output.split('\n'):
                        if 'URL:' in line:
                            url = line.split('URL:')[1].strip()
                            print(f"✅ 部署成功!")
                            print(f"🌐 网站地址: {url}")
                            return url
                print(f"✅ 部署成功!")
                return True
            else:
                print(f"❌ 部署失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 部署出错: {e}")
            return False
    
    def deploy_all_sites(self):
        """部署所有生成的网站"""
        site_dir = Path(SITE_DIR)
        
        if not site_dir.exists():
            print(f"❌ 网站目录不存在: {SITE_DIR}")
            return
        
        # 获取所有子目录
        sites = [d for d in site_dir.iterdir() if d.is_dir()]
        
        if not sites:
            print("❌ 没有找到要部署的网站")
            return
        
        print(f"\n📦 找到 {len(sites)} 个网站待部署")
        
        success_count = 0
        deployed_urls = []
        
        for site in sites:
            site_name = site.name
            if self.deploy_site(site, site_name):
                success_count += 1
            time.sleep(2)  # 避免请求过快
        
        # 总结
        print(f"\n{'='*60}")
        print(f"✅ 完成！成功部署 {success_count}/{len(sites)} 个网站")
        print(f"{'='*60}\n")

def main():
    print(f"\n{'#'*60}")
    print(f"# 🚀 Netlify 自动部署工具")
    print(f"{'#'*60}\n")
    
    deployer = NetlifyDeployer(NETLIFY_AUTH_TOKEN)
    
    # 检查 CLI
    if not deployer.check_netlify_cli():
        return
    
    # 部署所有网站
    deployer.deploy_all_sites()

if __name__ == "__main__":
    main()

