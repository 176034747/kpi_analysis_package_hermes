#!/usr/bin/env python3
"""
judge_info_security.py - 人工审核信息安全管理部 KPI 达成情况
使用相对于本脚本的路径，需在 kpi_analysis_package/ 目录下运行

注意：运行此脚本前，需先：
1. 下载信息安全管理部 xlsx 文件到 data/ 目录
2. 在 parse_info_security() 中配置该部门的列位置
"""
import json
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def parse_info_security(filepath):
    """信息安全管理部 - Sheet1
    注意：根据 skill.md，该部门列位置：
    - Sheet: Sheet1
    - seq_col: 0, name_col: 1, annual_col: 5, month_col: 12
    """
    kpis = []
    df = pd.read_excel(filepath, sheet_name='Sheet1', header=None)
    
    for i in range(2, len(df)):
        row = df.iloc[i]
        seq = str(row.iloc[0]).strip() if len(row) > 0 else ''
        if not seq or seq in ['nan', 'None', '空', '']:
            continue
        try:
            int(float(seq))
        except:
            continue
        
        name = str(row.iloc[1]).strip() if len(row) > 1 and pd.notna(row.iloc[1]) else ''
        if not name or name in ['nan', 'None', '空', '']:
            continue
        
        annual = str(row.iloc[5]).strip() if len(row) > 5 and pd.notna(row.iloc[5]) else ''
        month_target = str(row.iloc[12]).strip() if len(row) > 12 and pd.notna(row.iloc[12]) else ''
        if month_target in ['nan', 'None', '空', '-']:
            month_target = ''
        
        month_actual = ''
        if i + 1 < len(df):
            actual_row = df.iloc[i + 1]
            first_col = str(actual_row.iloc[0]).strip() if len(actual_row) > 0 else ''
            if first_col in ['', 'nan', '空', '实际']:
                month_actual = str(actual_row.iloc[12]).strip() if len(actual_row) > 12 and pd.notna(actual_row.iloc[12]) else ''
                if month_actual in ['nan', 'None', '空', '-']:
                    month_actual = ''
        
        kpis.append({'name': name, 'annual_target': annual, 'month_target': month_target, 'month_actual': month_actual})
    
    return kpis

# ========== 手动逐条判断 ==========
# 注意：每月需要根据实际数据更新此处的判断
judgments = [
    (False, "目标要求完成软件管理文件编制并在DCC发布，实际仍在架构设计及代码开发中，未达成"),
    (True, "目标联调测试，实际完成平台与漏洞扫描系统对接、与SSO系统对接，联调测试达成"),
    (False, "目标攻击链分析智能体核心能力与接口开发，实际SOC智能安全中心进展，部分达成但核心目标未完全实现"),
    (True, "目标PoC测试，实际IPG、中兴通讯、海泰方圆、亿格云、华工安等测试环境已搭建，PoC测试达成"),
    (True, "目标0.99，实际1，达成"),
    (True, "目标组织全员AI安全基础通识培训及CAIE调研，实际已完成，达成"),
]

# 检查文件是否存在
info_file = os.path.join(DATA_DIR, '信息安全管理部.xlsx')
if not os.path.exists(info_file):
    print(f"警告：{info_file} 不存在，跳过信息安全管理部处理")
    print("如需处理，请先下载该文件到 data/ 目录")
else:
    kpis = parse_info_security(info_file)
    
    achieved = 0
    not_achieved = 0
    achieved_items = []
    not_achieved_items = []
    
    for i, kpi in enumerate(kpis):
        if i < len(judgments):
            is_ok, reason = judgments[i]
        else:
            is_ok = False
            reason = "需人工确认"
        
        kpi['is_achieved'] = is_ok
        kpi['judgment'] = reason
        
        if is_ok:
            achieved += 1
            achieved_items.append({
                'name': kpi['name'], 'annual_target': kpi['annual_target'],
                'month_target': kpi['month_target'], 'month_actual': kpi['month_actual'],
                'reason': reason
            })
        else:
            not_achieved += 1
            not_achieved_items.append({
                'name': kpi['name'], 'annual_target': kpi['annual_target'],
                'month_target': kpi['month_target'], 'month_actual': kpi['month_actual'],
                'reason': reason
            })
    
    rate = round(achieved / len(kpis) * 100, 1) if kpis else 0
    print(f"信息安全管理部: 达成 {achieved}/{len(kpis)} = {rate}%, 未达成 {not_achieved}")
    
    dept_data = {
        'name': '信息安全管理部',
        'total': len(kpis),
        'achieved': achieved,
        'not_achieved': not_achieved,
        'no_eval': 0,
        'achievement_rate': rate,
        'achieved_items': achieved_items,
        'not_achieved_items': not_achieved_items,
        'no_target_items': [],
        'kpis': kpis
    }
    
    # 追加到现有数据
    with open(os.path.join(DATA_DIR, 'kpi_data_judged.json'), 'r', encoding='utf-8') as f:
        all_data = json.load(f)
    
    all_data['信息安全管理部'] = dept_data
    
    with open(os.path.join(DATA_DIR, 'kpi_data_judged.json'), 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print("已更新到 kpi_data_judged.json")
