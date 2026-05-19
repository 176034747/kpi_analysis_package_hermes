#!/usr/bin/env python3
"""
judge_qihua_groups.py - 人工审核数字化企划部 3 个组的 KPI 达成情况
使用相对于本脚本的路径，需在 kpi_analysis_package/ 目录下运行
"""
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# 读取企划部分组数据
with open(os.path.join(DATA_DIR, 'qihua_by_group.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)

groups = data['数字化企划部']['groups']

# ========== 手动逐条判断 ==========
# 注意：每月需要根据实际数据更新此处的判断
group_judgments = {
    'IPD推进组': [
        (True, "武汉区项目沟通完成，推行方案确定"),
        (True, "0.64 ≥ 0.6"),
        (True, "方案制定并共识完成"),
        (True, "完成现状梳理，建设目标明确"),
        (True, "4/15完成TCL华星IPD3.0能力提升咨询项目立项"),
        (True, "人员面试已完成"),
    ],
    '流程组': [
        (True, "高层已共识质量运营方案，详细子方案落地推进中"),
        (True, "已启动2次流程诊断，诊断报告已输出并在执委会汇报完成"),
        (True, "指标基线和目标已共识并宣导"),
        (True, "签核流模板治理中、低效流程治理正常开展、场景挖掘中、效率监控完成公告发布"),
        (True, "建设完成率20%，达成目标"),
        (True, "完成对外培训分享，线上课录制初版已完成"),
    ],
    '数据组': [
        (False, "端到端99.9%达标，但源头92.7%略低于目标93%"),
        (False, "未填写实际达成，无法确定X月达成情况"),
        (True, "自动入湖开发60%≥40%，MIS入湖源表注册6%≥5%"),
    ]
}

group_results = {}
all_kpis = []

for group_name, kpis in groups.items():
    judgments = group_judgments[group_name]
    
    achieved = 0
    not_achieved = 0
    no_eval = 0
    achieved_items = []
    not_achieved_items = []
    no_target_items = []
    
    for i, kpi in enumerate(kpis):
        is_ok, reason = judgments[i]
        kpi['is_achieved'] = is_ok
        kpi['judgment'] = reason
        kpi['group'] = group_name
        
        if '未填写实际达成' in reason or '未分解' in reason:
            no_eval += 1
            no_target_items.append({
                'name': kpi['name'],
                'annual_target': kpi['annual_target'],
                'reason': reason
            })
        elif is_ok:
            achieved += 1
            achieved_items.append({
                'name': kpi['name'],
                'annual_target': kpi['annual_target'],
                'month_target': kpi['month_target'],
                'month_actual': kpi['month_actual'],
                'reason': reason
            })
        else:
            not_achieved += 1
            not_achieved_items.append({
                'name': kpi['name'],
                'annual_target': kpi['annual_target'],
                'month_target': kpi['month_target'],
                'month_actual': kpi['month_actual'],
                'reason': reason
            })
    
    total = len(kpis)
    rate = round(achieved / total * 100, 1) if total > 0 else 0
    
    group_results[group_name] = {
        'name': f'数字化企划部-{group_name}',
        'total': total,
        'achieved': achieved,
        'not_achieved': not_achieved,
        'no_eval': no_eval,
        'achievement_rate': rate,
        'achieved_items': achieved_items,
        'not_achieved_items': not_achieved_items,
        'no_target_items': no_target_items,
        'kpis': kpis
    }
    
    all_kpis.extend(kpis)
    print(f"\n{group_name}: 达成 {achieved}/{total} = {rate}%, 未达成 {not_achieved}, 无法评估 {no_eval}")

total_achieved = sum(g['achieved'] for g in group_results.values())
total_all = len(all_kpis)
total_rate = round(total_achieved / total_all * 100, 1) if total_all > 0 else 0
print(f"\n数字化企划部总计: 达成 {total_achieved}/{total_all} = {total_rate}%")

# 读取现有判断数据并追加
with open(os.path.join(DATA_DIR, 'kpi_data_judged.json'), 'r', encoding='utf-8') as f:
    all_data = json.load(f)

for group_name, result in group_results.items():
    all_data[result['name']] = result

with open(os.path.join(DATA_DIR, 'kpi_data_judged.json'), 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

print("\n已更新到 kpi_data_judged.json")
