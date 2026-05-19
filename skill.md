# KPI Monthly Analysis Skill

## Metadata
- **Name**: KPI Monthly Analysis
- **Category**: Data Analysis / Reporting
- **Version**: 2.0
- **Author**: Digital Transformation Center
- **Trigger Phrases**: 
  - "分析本月KPI"
  - "生成KPI报表"
  - "KPI月度分析"
  - "部门KPI达成情况"
  - "运行KPI skill"

## Description
自动化分析数字化转型中心各部门月度KPI达成情况，从飞书文档读取原始数据，经人工审核判断后生成专业HTML报告并导出PNG长图。

## Prerequisites

### Dependencies
```bash
# Python packages
pip install pandas openpyxl playwright
python -m playwright install chromium

# Feishu CLI
npm install -g @larksuite/cli
lark-cli auth login
```

### Data Source
- **Location**: Feishu Drive "我的文件夹/KPI管理/部门级KPI"
- **Format**: xlsx files
- **Update Frequency**: Monthly

## Workflow

### Step 1: Download Data Files
Download 7 department xlsx files from Feishu to `data/` directory:
- 运营数字化.xlsx
- IT服务.xlsx
- 基础架构.xlsx
- 数字化企划部.xlsx (contains 3 sheets: IPD组, 流程组, 数据组)
- 平台数字化.xlsx
- 产品数字化.xlsx
- 信息安全管理部.xlsx

### Step 2: Extract KPI Data
```bash
python scripts/extract_all_kpi_complete.py
```
**Output**: `data/kpi_data_complete.json`

**Expected counts**:
- 运营数字化: 7 items
- IT服务: 7 items
- 基础架构: 7 items
- 数字化企划部: 15 items (IPD 6 + 流程 6 + 数据 3)
- 平台数字化: 7 items
- 产品数字化: 6 items
- 信息安全管理部: 6 items

### Step 3: Manual Review & Judgment
**CRITICAL**: Must manually review each KPI before running judgment scripts.

Edit these files with current month's judgments:
1. `scripts/manual_judge.py` - Update `manual_judgments` dict for 6 departments
2. `scripts/judge_qihua_groups.py` - Update `group_judgments` for 3 groups
3. `scripts/judge_info_security.py` - Update `judgments` list

**Judgment format**: `(is_achieved: bool, reason: str)`

Then run:
```bash
python scripts/manual_judge.py
python scripts/judge_qihua_groups.py
python scripts/judge_info_security.py
```

**Output**: `data/kpi_data_judged.json`

### Step 4: Generate HTML Report
```bash
python scripts/gen_report_final_v2.py
```
**Output**: `data/KPI_X月达成情况报告.html`

### Step 5: Export PNG
```bash
python scripts/html_to_png_pw3.py
```
**Output**: `data/KPI_X月达成情况报告.png`

## Key Technical Details

### Column Mapping (Critical)
Each department has different column positions for month data:

| Department | Sheet | seq_col | name_col | annual_col | month_col | Notes |
|------------|-------|---------|----------|------------|-----------|-------|
| 运营数字化 | Y26部门KPI | 0 | 1 | 5 | 14 | Standard |
| IT服务 | Sheet1 | 0 | 1 | 5 | 12 | Standard |
| 基础架构 | Sheet1 | 0 | 1 | 5 | 12 | Standard |
| 企划部-IPD | IPD组KPI | **1** | **3** | **7** | 14 | seq in Col 1 |
| 企划部-流程 | 流程组KPI | **1** | **3** | **7** | **15** | month in Col 15 |
| 企划部-数据 | 数据组KPI | 0 | 1 | 5 | 12 | Standard |
| 平台数字化 | 平台数字化KPI 26年 | 0 | 1 | 5 | **13** | Start from Row 1 |
| 产品数字化 | **9255关键任务** | 0 | 1 | 5 | 12 | Non-default sheet |
| 信息安全 | Sheet1 | 0 | 1 | 5 | 12 | Standard |

### Data Structure
All departments use "dual-row" structure:
- Row N: [seq] [KPI name] ... [month target]
- Row N+1: [empty/"actual"] ... [month actual]

### Qihua Department Special Handling
- Ranking: 数字化企划部 as ONE department (merged from 3 groups)
- Details: Show 3 sub-groups separately (IPD推进组, 流程组, 数据组)
- Data keys: "数字化企划部-IPD推进组", "数字化企划部-流程组", "数字化企划部-数据组"

### Text Newline Handling
All text fields must pass through `nl2br()` to convert `\n` to `<br>`:
- name, annual_target, month_target, month_actual, judgment, reason

## File Structure
```
kpi_analysis_package/
├── skill.md                    # This file
├── README.md                   # Usage guide
├── run_all.py                  # One-click execution
├── data/                       # Data directory (auto-created)
│   ├── *.xlsx                  # Source files (manual download)
│   ├── kpi_data_complete.json  # Extracted data
│   └── kpi_data_judged.json    # Final judged data
└── scripts/
    ├── extract_all_kpi_complete.py
    ├── manual_judge.py
    ├── judge_qihua_groups.py
    ├── judge_info_security.py
    ├── gen_report_final_v2.py
    ├── html_to_png_pw3.py
    └── fix_newlines.py
```

## Monthly Checklist
1. [ ] Download latest xlsx files from Feishu
2. [ ] Verify column positions match skill.md mapping
3. [ ] Run extract_all_kpi_complete.py
4. [ ] Verify item counts match expected
5. [ ] Update manual_judgments in 3 judgment files
6. [ ] Run all 3 judgment scripts
7. [ ] Run gen_report_final_v2.py
8. [ ] Run html_to_png_pw3.py
9. [ ] Verify HTML and PNG outputs

## Output Format
- **HTML Report**: Professional dashboard with rankings, highlights, and detail tables
- **PNG Export**: Full-page screenshot at 1400px width, suitable for email embedding

## Troubleshooting

### "Column not found" errors
Check month column position in Row 1 of xlsx files. Update month_col in extract script.

### Wrong item counts
Check for merged cells or empty rows in source data. Verify seq_col is correct.

### Newlines showing as `\n`
Run `python scripts/fix_newlines.py` or ensure nl2br() is applied in report generator.

### PNG incomplete
Increase wait_for_timeout in html_to_png_pw3.py (e.g., to 3000ms).

## Version History
- v2.0 (2026-05-18): Updated for Hermes Agent compatibility, added relative paths
- v1.0 (2026-05-13): Initial version
