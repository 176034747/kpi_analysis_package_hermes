#!/usr/bin/env python3
"""
extract_all_kpi_complete.py - 提取所有部门 KPI 数据
使用相对于本脚本的路径，需在 kpi_analysis_package/ 目录下运行
"""
import pandas as pd
import json
import os
import re

# 获取脚本所在目录的上级目录（即 kpi_analysis_package/）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def is_achieved(actual, target):
    """判断是否达成"""
    if not actual or not target or str(actual).strip() in ['', 'nan', 'None', '空', '/', '-']:
        return False
    
    actual_str = str(actual).strip()
    target_str = str(target).strip()
    
    try:
        actual_val = float(actual_str.replace('%', '').replace('：', ':').split(':')[-1])
        target_val = float(target_str.replace('%', '').replace('：', ':').split(':')[-1])
        return actual_val >= target_val
    except:
        pass
    
    complete_keywords = ['完成', '已上线', '已达成', '达成', '100%', '已']
    for kw in complete_keywords:
        if kw in actual_str and len(actual_str) > 2:
            return True
    
    return False

def parse_yunying_shuzihua(filepath):
    """运营数字化 - Y26部门KPI sheet"""
    kpis = []
    df = pd.read_excel(filepath, sheet_name='Y26部门KPI', header=None)
    
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
        month_target = str(row.iloc[14]).strip() if len(row) > 14 and pd.notna(row.iloc[14]) else ''
        if month_target in ['nan', 'None', '空']:
            month_target = ''
        
        month_actual = ''
        if i + 1 < len(df):
            actual_row = df.iloc[i + 1]
            first_col = str(actual_row.iloc[0]).strip() if len(actual_row) > 0 else ''
            if first_col in ['', 'nan', '空', '实际']:
                month_actual = str(actual_row.iloc[14]).strip() if len(actual_row) > 14 and pd.notna(actual_row.iloc[14]) else ''
                if month_actual in ['nan', 'None', '空']:
                    month_actual = ''
        
        kpis.append({'name': name, 'annual_target': annual, 'month_target': month_target, 'month_actual': month_actual})
    
    return kpis

def parse_it_service(filepath):
    """IT服务 - Sheet1"""
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

def parse_jichu_jiagou(filepath):
    """基础架构 - Sheet1"""
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
        if month_target in ['nan', 'None', '空']:
            month_target = ''
        
        month_actual = ''
        if i + 1 < len(df):
            actual_row = df.iloc[i + 1]
            first_col = str(actual_row.iloc[0]).strip() if len(actual_row) > 0 else ''
            if first_col in ['', 'nan', '空', '实际']:
                month_actual = str(actual_row.iloc[12]).strip() if len(actual_row) > 12 and pd.notna(actual_row.iloc[12]) else ''
                if month_actual in ['nan', 'None', '空']:
                    month_actual = ''
        
        kpis.append({'name': name, 'annual_target': annual, 'month_target': month_target, 'month_actual': month_actual})
    
    return kpis

def parse_shuzihua_qihua(filepath):
    """数字化企划部 - 3个sheet"""
    all_kpis = {}
    groups = {}
    
    # IPD组KPI
    df = pd.read_excel(filepath, sheet_name='IPD组KPI', header=None)
    kpis = []
    for i in range(2, len(df)):
        row = df.iloc[i]
        seq = str(row.iloc[1]).strip() if len(row) > 1 else ''
        if not seq or seq in ['nan', 'None', '空', '']:
            continue
        try:
            int(float(seq))
        except:
            continue
        
        name = str(row.iloc[3]).strip() if len(row) > 3 and pd.notna(row.iloc[3]) else ''
        if not name or name in ['nan', 'None', '空', '']:
            continue
        
        annual = str(row.iloc[7]).strip() if len(row) > 7 and pd.notna(row.iloc[7]) else ''
        month_target = str(row.iloc[14]).strip() if len(row) > 14 and pd.notna(row.iloc[14]) else ''
        if month_target in ['nan', 'None', '空']:
            month_target = ''
        
        month_actual = ''
        if i + 1 < len(df):
            actual_row = df.iloc[i + 1]
            first_col = str(actual_row.iloc[0]).strip() if len(actual_row) > 0 else ''
            if first_col in ['', 'nan', '空', '实际']:
                month_actual = str(actual_row.iloc[14]).strip() if len(actual_row) > 14 and pd.notna(actual_row.iloc[14]) else ''
                if month_actual in ['nan', 'None', '空']:
                    month_actual = ''
        
        kpis.append({'name': name, 'annual_target': annual, 'month_target': month_target, 'month_actual': month_actual})
    
    groups['IPD推进组'] = kpis
    all_kpis.update({'IPD推进组': kpis})
    
    # 流程组KPI
    df = pd.read_excel(filepath, sheet_name='流程组KPI', header=None)
    kpis = []
    for i in range(2, len(df)):
        row = df.iloc[i]
        seq = str(row.iloc[1]).strip() if len(row) > 1 else ''
        if not seq or seq in ['nan', 'None', '空', '']:
            continue
        try:
            int(float(seq))
        except:
            continue
        
        name = str(row.iloc[3]).strip() if len(row) > 3 and pd.notna(row.iloc[3]) else ''
        if not name or name in ['nan', 'None', '空', '']:
            continue
        
        annual = str(row.iloc[7]).strip() if len(row) > 7 and pd.notna(row.iloc[7]) else ''
        month_target = str(row.iloc[15]).strip() if len(row) > 15 and pd.notna(row.iloc[15]) else ''
        if month_target in ['nan', 'None', '空']:
            month_target = ''
        
        month_actual = ''
        if i + 1 < len(df):
            actual_row = df.iloc[i + 1]
            first_col = str(actual_row.iloc[0]).strip() if len(actual_row) > 0 else ''
            if first_col in ['', 'nan', '空', '实际']:
                month_actual = str(actual_row.iloc[15]).strip() if len(actual_row) > 15 and pd.notna(actual_row.iloc[15]) else ''
                if month_actual in ['nan', 'None', '空']:
                    month_actual = ''
        
        kpis.append({'name': name, 'annual_target': annual, 'month_target': month_target, 'month_actual': month_actual})
    
    groups['流程组'] = kpis
    all_kpis.update({'流程组': kpis})
    
    # 数据组KPI
    df = pd.read_excel(filepath, sheet_name='数据组KPI', header=None)
    kpis = []
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
        if month_target in ['nan', 'None', '空']:
            month_target = ''
        
        month_actual = ''
        if i + 1 < len(df):
            actual_row = df.iloc[i + 1]
            first_col = str(actual_row.iloc[0]).strip() if len(actual_row) > 0 else ''
            if first_col in ['', 'nan', '空', '实际']:
                month_actual = str(actual_row.iloc[12]).strip() if len(actual_row) > 12 and pd.notna(actual_row.iloc[12]) else ''
                if month_actual in ['nan', 'None', '空']:
                    month_actual = ''
        
        kpis.append({'name': name, 'annual_target': annual, 'month_target': month_target, 'month_actual': month_actual})
    
    groups['数据组'] = kpis
    all_kpis.update({'数据组': kpis})
    
    return all_kpis, groups

def parse_pingtai_shuzihua(filepath):
    """平台数字化 - 平台数字化KPI 26年 sheet"""
    kpis = []
    df = pd.read_excel(filepath, sheet_name='平台数字化KPI 26年', header=None)
    
    for i in range(1, len(df)):
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
        month_target = str(row.iloc[13]).strip() if len(row) > 13 and pd.notna(row.iloc[13]) else ''
        if month_target in ['nan', 'None', '空']:
            month_target = ''
        
        month_actual = ''
        if i + 1 < len(df):
            actual_row = df.iloc[i + 1]
            first_col = str(actual_row.iloc[0]).strip() if len(actual_row) > 0 else ''
            if first_col in ['', 'nan', '空', '实际']:
                month_actual = str(actual_row.iloc[13]).strip() if len(actual_row) > 13 and pd.notna(actual_row.iloc[13]) else ''
                if month_actual in ['nan', 'None', '空']:
                    month_actual = ''
        
        kpis.append({'name': name, 'annual_target': annual, 'month_target': month_target, 'month_actual': month_actual})
    
    return kpis

def parse_chanpin_shuzihua(filepath):
    """产品数字化 - 9255关键任务 sheet"""
    kpis = []
    df = pd.read_excel(filepath, sheet_name='9255关键任务', header=None)
    
    for i in range(1, len(df)):
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
        if month_target in ['nan', 'None', '空']:
            month_target = ''
        
        month_actual = ''
        if i + 1 < len(df):
            actual_row = df.iloc[i + 1]
            first_col = str(actual_row.iloc[0]).strip() if len(actual_row) > 0 else ''
            if '实际' in first_col or first_col in ['', 'nan', '空']:
                month_actual = str(actual_row.iloc[12]).strip() if len(actual_row) > 12 and pd.notna(actual_row.iloc[12]) else ''
                if month_actual in ['nan', 'None', '空']:
                    month_actual = ''
        
        kpis.append({'name': name, 'annual_target': annual, 'month_target': month_target, 'month_actual': month_actual})
    
    return kpis

# 主程序
results = {
    '运营数字化': parse_yunying_shuzihua(os.path.join(DATA_DIR, '运营数字化.xlsx')),
    'IT服务': parse_it_service(os.path.join(DATA_DIR, 'IT服务.xlsx')),
    '基础架构': parse_jichu_jiagou(os.path.join(DATA_DIR, '基础架构.xlsx')),
    '平台数字化': parse_pingtai_shuzihua(os.path.join(DATA_DIR, '平台数字化.xlsx')),
    '产品数字化': parse_chanpin_shuzihua(os.path.join(DATA_DIR, '产品数字化.xlsx')),
}

# 企划部需要分组处理
qihua_all, qihua_groups = parse_shuzihua_qihua(os.path.join(DATA_DIR, '数字化企划部.xlsx'))
results['数字化企划部'] = qihua_all

output = {}
for dept, kpis in results.items():
    if isinstance(kpis, dict):
        output[dept] = {'dept_name': dept, 'groups': kpis, 'kpis': [], 'total': sum(len(v) for v in kpis.values())}
    else:
        output[dept] = {'dept_name': dept, 'kpis': kpis, 'total': len(kpis)}
    print(f"\n{dept}: {output[dept]['total']} 项")

# 保存原始提取数据
output_path = os.path.join(DATA_DIR, 'kpi_data_complete.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

# 保存企划部分组数据（用于 judge_qihua_groups.py）
qihua_output = {'数字化企划部': {'groups': qihua_groups}}
qihua_path = os.path.join(DATA_DIR, 'qihua_by_group.json')
with open(qihua_path, 'w', encoding='utf-8') as f:
    json.dump(qihua_output, f, ensure_ascii=False, indent=2)

print(f"\n数据已保存到: {output_path}")
print(f"企划部分组数据: {qihua_path}")
