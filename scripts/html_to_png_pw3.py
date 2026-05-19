#!/usr/bin/env python3
"""
html_to_png_pw3.py - 使用 Playwright 导出 HTML 为 PNG 长图
使用相对于本脚本的路径，需在 kpi_analysis_package/ 目录下运行
"""
import asyncio
import os
from playwright.async_api import async_playwright

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

HTML_PATH = os.path.join(DATA_DIR, 'KPI_4月达成情况报告.html')
OUTPUT_PATH = os.path.join(DATA_DIR, 'KPI_4月达成情况报告.png')

# Chromium 路径 - 请根据实际安装位置修改
CHROMIUM_PATH = r"C:\Users\17603\AppData\Local\ms-playwright\chromium-1217\chrome-win64\chrome.exe"

async def main():
    async with async_playwright() as p:
        print("启动 Chromium 浏览器...")
        browser = await p.chromium.launch(
            executable_path=CHROMIUM_PATH,
            headless=True,
            args=["--hide-scrollbars", "--disable-gpu", "--no-sandbox"]
        )

        page = await browser.new_page(viewport={"width": 1400, "height": 900})

        file_url = "file:///" + HTML_PATH.replace("\\", "/")
        print(f"加载 HTML: {file_url}")
        await page.goto(file_url, wait_until="networkidle")
        await page.wait_for_timeout(2000)

        print("正在截图...")
        await page.screenshot(path=OUTPUT_PATH, full_page=True)

        print(f"截图已保存: {OUTPUT_PATH}")

        size_mb = os.path.getsize(OUTPUT_PATH) / (1024 * 1024)
        print(f"文件大小: {size_mb:.2f} MB")

        await browser.close()
        print("浏览器已关闭。")

if __name__ == '__main__':
    asyncio.run(main())
