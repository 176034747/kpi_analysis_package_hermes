# data 目录说明

本目录用于存放运行时数据文件：

## 运行时需放置的文件（从飞书下载）

- `运营数字化.xlsx`
- `IT服务.xlsx`
- `基础架构.xlsx`
- `数字化企划部.xlsx`
- `平台数字化.xlsx`
- `产品数字化.xlsx`
- `信息安全管理部.xlsx`

## 运行时自动生成的文件

- `kpi_data_complete.json` - 原始提取数据（extract_all_kpi_complete.py 生成）
- `qihua_by_group.json` - 企划部分组数据（extract_all_kpi_complete.py 生成）
- `info_security_kpi.json` - 信息安全数据（extract_all_kpi_complete.py 生成）
- `kpi_data_judged.json` - 最终判断数据（manual_judge.py 等生成）

## 报表输出

- `KPI_4月达成情况报告.html` - HTML 报表（gen_report_final_v2.py 生成）
- `KPI_4月达成情况报告.png` - PNG 长图（html_to_png_pw3.py 生成）
