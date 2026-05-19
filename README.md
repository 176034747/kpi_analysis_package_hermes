# KPI 月度分析 Skill (Hermes Agent 版本)

适用于 Hermes Agent 的 KPI 月度达成分析技能包。

## 安装方法

### 1. 解压文件
将 `kpi_analysis_package_hermes.zip` 解压到任意目录。

### 2. 安装依赖
```bash
pip install pandas openpyxl playwright
python -m playwright install chromium
npm install -g @larksuite/cli
lark-cli auth login
```

### 3. 导入 Hermes Agent
将 `skill.md` 复制到 Hermes Agent 的技能目录：
```bash
# 默认路径
~/.hermes/skills/data_analysis/kpi_monthly_analysis/skill.md
```

或者使用 Hermes Agent 的导入命令。

## 使用方法

### 触发词
- "分析本月KPI"
- "生成KPI报表"
- "KPI月度分析"
- "部门KPI达成情况"
- "运行KPI skill"

### 完整工作流

1. **下载数据文件**
   从飞书「我的文件夹/KPI管理/部门级KPI」下载7个xlsx文件到 `data/` 目录

2. **提取数据**
   ```bash
   python scripts/extract_all_kpi_complete.py
   ```

3. **人工审核（关键步骤）**
   编辑以下3个文件，更新本月的KPI达成判断：
   - `scripts/manual_judge.py` - 6个部门
   - `scripts/judge_qihua_groups.py` - 企划部3组
   - `scripts/judge_info_security.py` - 信息安全部

4. **运行判断脚本**
   ```bash
   python scripts/manual_judge.py
   python scripts/judge_qihua_groups.py
   python scripts/judge_info_security.py
   ```

5. **生成报表**
   ```bash
   python scripts/gen_report_final_v2.py
   ```

6. **导出PNG**
   ```bash
   python scripts/html_to_png_pw3.py
   ```

### 一键运行
```bash
python run_all.py
```

## 文件结构
```
kpi_analysis_package_hermes/
├── skill.md              # Hermes Agent 技能定义
├── README.md             # 本文件
├── run_all.py            # 一键运行脚本
├── data/                 # 数据目录
│   └── README.md
└── scripts/              # Python 脚本
    ├── extract_all_kpi_complete.py
    ├── manual_judge.py
    ├── judge_qihua_groups.py
    ├── judge_info_security.py
    ├── gen_report_final_v2.py
    ├── html_to_png_pw3.py
    └── fix_newlines.py
```

## 注意事项

1. **必须人工审核**：每月需要手动编辑3个判断文件，无法完全自动化
2. **列位置检查**：每月需确认xlsx中的月份列位置是否有变化
3. **Chromium路径**：如Playwright截图失败，需修改 `html_to_png_pw3.py` 中的CHROMIUM_PATH

## 详细文档

详见 `skill.md` 中的完整技术细节和故障排除章节。
