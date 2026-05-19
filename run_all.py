#!/usr/bin/env python3
"""
KPI 月度分析 - 一键运行脚本
需在 kpi_analysis_package/ 目录下运行
"""
import subprocess
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, 'data')

def run(script_name):
    path = os.path.join(SCRIPT_DIR, 'scripts', script_name)
    print(f"\n{'='*60}")
    print(f"运行: {script_name}")
    print(f"{'='*60}")
    result = subprocess.run(['python', path], cwd=SCRIPT_DIR)
    if result.returncode != 0:
        print(f"[ERROR] {script_name} 执行失败，退出码: {result.returncode}")
        return False
    return True

def main():
    print("=" * 60)
    print("KPI 月度达成分析 - 一键运行")
    print("=" * 60)

    # Step 1: 检查数据文件
    required_files = [
        '运营数字化.xlsx', 'IT服务.xlsx', '基础架构.xlsx',
        '数字化企划部.xlsx', '平台数字化.xlsx', '产品数字化.xlsx'
    ]
    missing = [f for f in required_files if not os.path.exists(os.path.join(DATA_DIR, f))]
    if missing:
        print("\n警告：以下文件缺失：")
        for f in missing:
            print(f"  - {f}")
        print("\n请先将 xlsx 文件放入 data/ 目录。")

    # Step 2: 提取数据
    if not run('extract_all_kpi_complete.py'):
        return

    # Step 3: 人工审核判断提示
    print("\n" + "=" * 60)
    print("请先在 scripts/manual_judge.py、scripts/judge_qihua_groups.py、")
    print("scripts/judge_info_security.py 中更新本月的判断数据，")
    print("然后再继续执行后续步骤。")
    print("=" * 60)
    proceed = input("是否继续执行人工审核脚本? (y/n): ").strip().lower()
    if proceed != 'y':
        print("已取消。")
        return

    if not run('manual_judge.py'):
        return
    if not run('judge_qihua_groups.py'):
        return
    if not run('judge_info_security.py'):
        return

    # Step 4: 生成报表
    if not run('gen_report_final_v2.py'):
        return

    # Step 5: 导出 PNG
    if not run('html_to_png_pw3.py'):
        return

    print("\n" + "=" * 60)
    print("完成！")
    print("=" * 60)
    print("输出文件:")
    print(f"  - {os.path.join(DATA_DIR, 'KPI_4月达成情况报告.html')}")
    print(f"  - {os.path.join(DATA_DIR, 'KPI_4月达成情况报告.png')}")

if __name__ == '__main__':
    main()
