#!/usr/bin/env python3
"""
fix_newlines.py - 修复 KPI 名称及其他字段中的换行符
将数据中的 \\n 替换为 <br>，确保 HTML 正确显示换行
使用相对于本脚本的路径，需在 kpi_analysis_package/ 目录下运行
"""
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def fix_text_with_newlines(obj, fields):
    """递归修复指定字段中的换行符"""
    if isinstance(obj, dict):
        for field in fields:
            if field in obj and isinstance(obj[field], str):
                if '\n' in obj[field]:
                    obj[field] = obj[field].replace('\n', '<br>')
        for v in obj.values():
            fix_text_with_newlines(v, fields)
    elif isinstance(obj, list):
        for item in obj:
            fix_text_with_newlines(item, fields)

if __name__ == '__main__':
    json_path = os.path.join(DATA_DIR, 'kpi_data_judged.json')
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 需要处理换行的字段
    fields_to_fix = ['name', 'annual_target', 'month_target', 'month_actual', 'judgment', 'reason']
    
    fix_text_with_newlines(data, fields_to_fix)
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"已修复 {json_path} 中的换行符")
