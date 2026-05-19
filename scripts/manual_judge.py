#!/usr/bin/env python3
"""
manual_judge.py - 人工审核 6 个部门 KPI 达成情况
使用相对于本脚本的路径，需在 kpi_analysis_package/ 目录下运行
"""
import json
import os

# 获取脚本所在目录的上级目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# ========== 手动逐条判断数据 ==========
# 格式: (是否达成, 判断理由)
# 注意：每月需要根据实际数据更新此处的判断
manual_judgments = {
    "运营数字化": [
        (False, "详设完成92%，目标涉及多个模块(t11/t9/t3/t5)，整体仍在进行中"),
        (False, "第1项梳理导入计划未提及进展，第3项关键属性100%达标；整体部分达成"),
        (False, "未分解月度目标，无法确定X月达成情况"),
        (False, "投入回收比例79.4%，未达到100%回收目标"),
        (True, "领航级场景材料修改完成"),
        (False, "未分解月度目标，无法确定X月达成情况"),
        (False, "未分解月度目标，无法确定X月达成情况"),
    ],
    "IT服务": [
        (True, "0.9776 ≥ 0.952"),
        (False, "未分解月度目标，无法确定X月达成情况"),
        (True, "0.5 = 0.5，按计划达成"),
        (False, "未分解月度目标，无法确定X月达成情况"),
        (True, "4月目标为0（无建设计划），实际完成4间MLED改造，超额达成"),
        (True, "4月目标为0（无建设计划），实际有进展，超额达成"),
        (True, "核心人才保留率达标"),
    ],
    "基础架构": [
        (True, "0.9776 ≥ 0.952"),
        (True, "566.29万远超125万目标"),
        (False, "新增0核0个项目，未达成月度目标"),
        (False, "完成1个Agent（20%），目标5个"),
        (False, "满意度数据未填写，工单减少情况无法确认是否达标"),
        (False, "华兆已交割，但其他项目仍在推进中，未完全达成"),
        (False, "核心人才保留率100%达标，但年度证书仅获得1个（目标6个），部分达成"),
    ],
    "平台数字化": [
        (True, "4号16:00出具管报，比目标24:00提前8小时"),
        (True, "标准成本4/1完成立项"),
        (True, "0.7 = 0.7"),
        (True, "源头准确率100% ≥ 99%"),
        (False, "流程AI预审已在开发，但飞书创新应用5个未明确达成，活跃度70%未达80%目标"),
        (False, "投入回收比例91%，未达到100%"),
        (True, "累计完成4场培训分享 ≥ 目标3场"),
    ],
    "产品数字化": [
        (False, "未分解月度目标，无法确定X月达成情况"),
        (False, "KPI功能上线100%达成，但详细方案设计仅完成10%（目标30%），仿真平台合同仍在推进中"),
        (True, "实际达成100%，客户FCST模块开发已完成，销售FCST-DP模块调研完成且设计评审完成"),
        (True, "源头99%≥99%，BOM99.48%≥99%，客户78%≥78%，全部达标"),
        (True, "完成实验管理优化上线和生命周期优化上线，目标达成"),
        (True, "FASTGPT应用培训完成3场，周分享会组织，月度培训已安排"),
    ],
}

# 读取原始数据
with open(os.path.join(DATA_DIR, 'kpi_data_complete.json'), 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

# 应用手动判断
output = {}
for dept_name, dept_info in raw_data.items():
    # 跳过企划部（由 judge_qihua_groups.py 处理）
    if dept_name == '数字化企划部':
        continue
    
    kpis = dept_info['kpis']
    judgments = manual_judgments.get(dept_name, [])
    
    achieved = 0
    not_achieved = 0
    no_eval = 0
    achieved_items = []
    not_achieved_items = []
    no_target_items = []
    
    for i, kpi in enumerate(kpis):
        if i < len(judgments):
            is_ok, reason = judgments[i]
        else:
            is_ok = False
            reason = "需人工确认"
        
        kpi['judgment'] = reason
        kpi['is_achieved'] = is_ok
        
        if '未分解月度目标' in reason or '未填写实际达成' in reason:
            no_eval += 1
            no_target_items.append({
                'name': kpi['name'],
                'annual_target': kpi.get('annual_target', ''),
                'reason': reason
            })
        elif is_ok:
            achieved += 1
            achieved_items.append({
                'name': kpi['name'],
                'annual_target': kpi.get('annual_target', ''),
                'month_target': kpi.get('month_target', ''),
                'month_actual': kpi.get('month_actual', ''),
                'reason': reason
            })
        else:
            not_achieved += 1
            not_achieved_items.append({
                'name': kpi['name'],
                'annual_target': kpi.get('annual_target', ''),
                'month_target': kpi.get('month_target', ''),
                'month_actual': kpi.get('month_actual', ''),
                'reason': reason
            })
    
    total = len(kpis)
    rate = round(achieved / total * 100, 1) if total > 0 else 0
    
    output[dept_name] = {
        'dept_name': dept_name,
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
    
    print(f"\n{dept_name}: 达成 {achieved}/{total} = {rate:.1f}%, 未达成 {not_achieved}, 无法评估 {no_eval}")

# 保存（首次保存，后续由 judge_qihua_groups.py 等追加）
with open(os.path.join(DATA_DIR, 'kpi_data_judged.json'), 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\n已保存到 kpi_data_judged.json（6个部门）")
print("注意：数字化企划部需单独运行 judge_qihua_groups.py")
