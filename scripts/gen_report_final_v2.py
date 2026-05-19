#!/usr/bin/env python3
"""
gen_report_final_v2.py - 生成 HTML 报表
使用相对于本脚本的路径，需在 kpi_analysis_package/ 目录下运行
"""
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def nl2br(s):
    """将字符串中的 \\n 替换为 <br>"""
    if not s:
        return s
    return s.replace('\n', '<br>')

def generate_html_report(data, output_path):
    """生成HTML报告"""
    
    # 分离企划部子组和普通部门
    qihua_groups = {}
    normal_depts = {}
    
    for dept_name, dept_info in data.items():
        dept_info['name'] = dept_name
        if '数字化企划部-' in dept_name:
            group_short = dept_name.replace('数字化企划部-', '')
            qihua_groups[group_short] = dept_info
        else:
            normal_depts[dept_name] = dept_info
    
    # 合并数字化企划部为一个整体部门
    qihua_total = {
        'name': '数字化企划部',
        'total': sum(g['total'] for g in qihua_groups.values()),
        'achieved': sum(g['achieved'] for g in qihua_groups.values()),
        'not_achieved': sum(g['not_achieved'] for g in qihua_groups.values()),
        'no_eval': sum(g['no_eval'] for g in qihua_groups.values()),
        'achievement_rate': round(sum(g['achieved'] for g in qihua_groups.values()) / sum(g['total'] for g in qihua_groups.values()) * 100, 1),
        'achieved_items': [],
        'not_achieved_items': [],
        'no_target_items': [],
        'kpis': [],
        'groups': qihua_groups,
        'has_groups': True
    }
    for g in qihua_groups.values():
        qihua_total['achieved_items'].extend(g['achieved_items'])
        qihua_total['not_achieved_items'].extend(g['not_achieved_items'])
        qihua_total['no_target_items'].extend(g['no_target_items'])
        qihua_total['kpis'].extend(g['kpis'])
    
    departments_data = list(normal_depts.values()) + [qihua_total]
    
    total_kpis = sum(d['total'] for d in departments_data)
    total_achieved = sum(d['achieved'] for d in departments_data)
    total_not_achieved = sum(d['not_achieved'] for d in departments_data)
    
    sorted_depts = sorted(departments_data, key=lambda x: x['achievement_rate'], reverse=True)
    
    all_achieved = []
    all_not_achieved = []
    for dept in departments_data:
        for item in dept['achieved_items']:
            all_achieved.append({**item, 'dept': dept['name']})
        for item in dept['not_achieved_items']:
            all_not_achieved.append({**item, 'dept': dept['name']})
        for item in dept['no_target_items']:
            all_not_achieved.append({**item, 'dept': dept['name']})
    
    dept_cards = ''
    colors = ['#4CAF50', '#8BC34A', '#FFC107', '#FF9800', '#FF5722', '#F44336']
    for i, dept in enumerate(sorted_depts):
        color = colors[min(i, len(colors)-1)]
        dept_cards += f'''
        <div class="dept-card" style="border-left-color: {color}">
            <div class="dept-name">{dept['name']}</div>
            <div class="dept-rate">{dept['achievement_rate']}%</div>
            <div class="dept-detail">达成: {dept['achieved']}/{dept['total']}</div>
            <div class="dept-unfilled">未填写/无法评估: {dept['no_eval']}</div>
        </div>
        '''
    
    achieved_section = ''
    if all_achieved:
        for item in all_achieved[:20]:
            reason = item.get('reason', '')
            achieved_section += f'''
            <div class="highlight-item good">
                <strong>{item['dept']}</strong> - {item['name']}
                <div class="reason">{reason}</div>
            </div>
            '''
    else:
        achieved_section = '<div class="no-data">暂无达成优秀项</div>'
    
    not_achieved_section = ''
    if all_not_achieved:
        for item in all_not_achieved[:25]:
            reason = item.get('reason', '')
            not_achieved_section += f'''
            <div class="highlight-item warning">
                <strong>{item['dept']}</strong> - {item['name']}
                <div class="reason">{reason}</div>
            </div>
            '''
    else:
        not_achieved_section = '<div class="no-data">暂无需要关注的项</div>'
    
    detail_tables = ''
    for dept in sorted_depts:
        if dept.get('has_groups') and dept.get('groups'):
            detail_tables += f'''
            <div class="dept-section">
                <h3>{dept['name']} <span class="dept-summary">(达成率: {dept['achievement_rate']}%, {dept['achieved']}/{dept['total']})</span></h3>
            '''
            
            for group_name, group_data in dept['groups'].items():
                detail_tables += f'''
                <div class="sub-group">
                    <h4 class="group-title">{group_name} <span class="dept-summary">(达成率: {group_data['achievement_rate']}%, {group_data['achieved']}/{group_data['total']})</span></h4>
                    <table class="kpi-table">
                        <thead>
                            <tr>
                                <th>KPI名称</th>
                                <th>年度目标</th>
                                <th>4月目标</th>
                                <th>4月达成</th>
                                <th>状态</th>
                                <th>判断依据</th>
                            </tr>
                        </thead>
                        <tbody>
                '''
                
                for kpi in group_data['kpis']:
                    name = nl2br(kpi['name'])
                    annual = nl2br(kpi.get('annual_target', ''))
                    month_target = nl2br(kpi.get('month_target', ''))
                    month_actual = nl2br(kpi.get('month_actual', ''))
                    judgment = nl2br(kpi.get('judgment', ''))
                    is_achieved = kpi.get('is_achieved', False)
                    
                    if len(annual) > 80: annual = annual[:80] + '...'
                    if len(month_target) > 50: month_target = month_target[:50] + '...'
                    if len(month_actual) > 50: month_actual = month_actual[:50] + '...'
                    if len(judgment) > 40: judgment = judgment[:40] + '...'
                    
                    month_target = '-' if not month_target or month_target == '' else month_target
                    month_actual = '-' if not month_actual or month_actual == '' else month_actual
                    
                    if '未分解月度目标' in kpi.get('judgment', '') or '未填写实际达成' in kpi.get('judgment', ''):
                        status = '未分解目标' if '未分解' in kpi.get('judgment', '') else '未填写'
                        status_class = 'status-no-target'
                    elif is_achieved:
                        status = '已达成'
                        status_class = 'status-achieved'
                    else:
                        status = '未达成'
                        status_class = 'status-not-achieved'
                    
                    detail_tables += f'''
                    <tr>
                        <td>{name}</td>
                        <td>{annual}</td>
                        <td>{month_target}</td>
                        <td>{month_actual}</td>
                        <td class="{status_class}">{status}</td>
                        <td class="judgment">{judgment}</td>
                    </tr>
                    '''
                
                detail_tables += '''
                        </tbody>
                    </table>
                </div>
                '''
            
            detail_tables += '</div>'
        else:
            rows = ''
            for kpi in dept['kpis']:
                name = nl2br(kpi['name'])
                annual = nl2br(kpi.get('annual_target', ''))
                month_target = nl2br(kpi.get('month_target', ''))
                month_actual = nl2br(kpi.get('month_actual', ''))
                judgment = nl2br(kpi.get('judgment', ''))
                is_achieved = kpi.get('is_achieved', False)
                
                if len(annual) > 80: annual = annual[:80] + '...'
                if len(month_target) > 50: month_target = month_target[:50] + '...'
                if len(month_actual) > 50: month_actual = month_actual[:50] + '...'
                if len(judgment) > 40: judgment = judgment[:40] + '...'
                
                month_target = '-' if not month_target or month_target == '' else month_target
                month_actual = '-' if not month_actual or month_actual == '' else month_actual
                
                if '未分解月度目标' in kpi.get('judgment', '') or '未填写实际达成' in kpi.get('judgment', ''):
                    status = '未分解目标' if '未分解' in kpi.get('judgment', '') else '未填写'
                    status_class = 'status-no-target'
                elif is_achieved:
                    status = '已达成'
                    status_class = 'status-achieved'
                else:
                    status = '未达成'
                    status_class = 'status-not-achieved'
                
                rows += f'''
                <tr>
                    <td>{name}</td>
                    <td>{annual}</td>
                    <td>{month_target}</td>
                    <td>{month_actual}</td>
                    <td class="{status_class}">{status}</td>
                    <td class="judgment">{judgment}</td>
                </tr>
                '''
            
            detail_tables += f'''
            <div class="dept-section">
                <h3>{dept['name']} <span class="dept-summary">(达成率: {dept['achievement_rate']}%, {dept['achieved']}/{dept['total']})</span></h3>
                <table class="kpi-table">
                    <thead>
                        <tr>
                            <th>KPI名称</th>
                            <th>年度目标</th>
                            <th>4月目标</th>
                            <th>4月达成</th>
                            <th>状态</th>
                            <th>判断依据</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
            </div>
            '''
    
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>数字化转型中心 4月KPI达成情况报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .header h1 {{ font-size: 32px; margin-bottom: 10px; }}
        .header .subtitle {{ font-size: 16px; opacity: 0.9; }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            padding: 30px 40px;
            background: #f8f9fa;
        }}
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .summary-card .number {{ font-size: 36px; font-weight: bold; color: #667eea; }}
        .summary-card .label {{ color: #666; margin-top: 5px; }}
        .section {{ padding: 30px 40px; }}
        .section-title {{
            font-size: 24px;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        .ranking {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }}
        .dept-card {{
            background: white;
            border-radius: 12px;
            padding: 20px;
            border-left: 5px solid;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }}
        .dept-card:hover {{ transform: translateY(-2px); }}
        .dept-name {{ font-size: 16px; font-weight: bold; color: #333; margin-bottom: 8px; }}
        .dept-rate {{ font-size: 28px; font-weight: bold; color: #667eea; }}
        .dept-detail {{ color: #666; font-size: 14px; margin-top: 5px; }}
        .dept-unfilled {{ color: #999; font-size: 12px; margin-top: 3px; }}
        .highlights {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }}
        .highlight-box {{
            background: #f8f9fa;
            border-radius: 12px;
            padding: 20px;
        }}
        .highlight-box h3 {{
            color: #333;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .highlight-box.good h3::before {{
            content: "\\2713";
            color: #4CAF50;
            font-weight: bold;
        }}
        .highlight-box.warning h3::before {{
            content: "\\26A0";
            color: #FF9800;
        }}
        .highlight-item {{
            background: white;
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 8px;
            border-left: 4px solid;
        }}
        .highlight-item.good {{ border-left-color: #4CAF50; }}
        .highlight-item.warning {{ border-left-color: #FF9800; }}
        .highlight-item .reason {{ color: #666; font-size: 12px; margin-top: 5px; }}
        .dept-section {{ margin-bottom: 30px; }}
        .dept-section h3 {{ color: #667eea; margin-bottom: 15px; font-size: 20px; }}
        .dept-section .dept-summary {{ color: #666; font-size: 14px; font-weight: normal; }}
        .sub-group {{
            margin-bottom: 20px;
            margin-left: 10px;
            padding-left: 15px;
            border-left: 3px solid #e0e0e0;
        }}
        .group-title {{
            color: #555;
            margin-bottom: 10px;
            font-size: 16px;
        }}
        .group-title .dept-summary {{ color: #888; font-size: 13px; font-weight: normal; }}
        .kpi-table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            font-size: 13px;
        }}
        .kpi-table th {{
            background: #667eea;
            color: white;
            padding: 10px 8px;
            text-align: left;
            font-weight: 600;
        }}
        .kpi-table td {{ padding: 10px 8px; border-bottom: 1px solid #eee; vertical-align: top; }}
        .kpi-table tr:hover {{ background: #f8f9fa; }}
        .kpi-table td:nth-child(2) {{ max-width: 150px; }}
        .kpi-table td:nth-child(3) {{ max-width: 120px; }}
        .kpi-table td:nth-child(4) {{ max-width: 120px; }}
        .kpi-table .judgment {{ color: #888; font-size: 11px; max-width: 180px; }}
        .status-achieved {{ color: #4CAF50; font-weight: bold; }}
        .status-not-achieved {{ color: #F44336; }}
        .status-no-target {{ color: #999; }}
        .status-no-data {{ color: #FF9800; }}
        .no-data {{ color: #999; text-align: center; padding: 20px; }}
        @media (max-width: 768px) {{
            .summary {{ grid-template-columns: repeat(2, 1fr); }}
            .highlights {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>数字化转型中心 4月KPI达成情况报告</h1>
            <div class="subtitle">报告日期：2026年5月</div>
        </div>
        
        <div class="summary">
            <div class="summary-card">
                <div class="number">{len(departments_data)}</div>
                <div class="label">部门总数</div>
            </div>
            <div class="summary-card">
                <div class="number">{total_kpis}</div>
                <div class="label">KPI总项数</div>
            </div>
            <div class="summary-card">
                <div class="number">{total_achieved}</div>
                <div class="label">已达成项数</div>
            </div>
            <div class="summary-card">
                <div class="number">{total_not_achieved}</div>
                <div class="label">未达成项数</div>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">部门达成情况排名</h2>
            <div class="ranking">
                {dept_cards}
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">重点关注项</h2>
            <div class="highlights">
                <div class="highlight-box good">
                    <h3>达成优秀项</h3>
                    {achieved_section}
                </div>
                <div class="highlight-box warning">
                    <h3>需关注项</h3>
                    {not_achieved_section}
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">各部门KPI明细</h2>
            {detail_tables}
        </div>
    </div>
</body>
</html>'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == '__main__':
    with open(os.path.join(DATA_DIR, 'kpi_data_judged.json'), 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    output_path = os.path.join(DATA_DIR, 'KPI_4月达成情况报告.html')
    generate_html_report(data, output_path)
    print(f"报告已生成: {output_path}")
