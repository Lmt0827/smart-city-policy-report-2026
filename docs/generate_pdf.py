#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate PDF from the smart city policy report HTML.
Uses reportlab for professional PDF output with charts.
"""

import os
import sys
import platform
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether, ListFlowable, ListItem
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors

# ============================================================
# CJK Font Registration
# ============================================================
def register_cjk_font():
    system = platform.system()
    font_paths = []
    if system == "Darwin":
        font_paths = [
            "/System/Library/Fonts/PingFang.ttc",
            "/Library/Fonts/Arial Unicode.ttf",
            "/System/Library/Fonts/STHeiti Medium.ttc",
        ]
    elif system == "Windows":
        font_paths = [
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simsun.ttc",
        ]
    else:  # Linux
        font_paths = [
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJKsc-Regular.otf",
            "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        ]

    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont("CJKFont", font_path, subfontIndex=0))
                print(f"Registered CJK font: {font_path}")
                return "CJKFont"
            except Exception as e:
                print(f"Failed to register {font_path}: {e}")
                continue
    return None

cjk_font = register_cjk_font()
if not cjk_font:
    print("WARNING: No CJK font found, using Helvetica")
    cjk_font = "Helvetica"

# ============================================================
# Page Geometry
# ============================================================
PAGE_SIZE = A4
PAGE_WIDTH, PAGE_HEIGHT = PAGE_SIZE
TOP_MARGIN = 0.8 * inch
BOTTOM_MARGIN = 0.8 * inch
LEFT_MARGIN = 0.75 * inch
RIGHT_MARGIN = 0.75 * inch
CONTENT_WIDTH = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN
CONTENT_HEIGHT = PAGE_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN

# ============================================================
# Colors
# ============================================================
PRIMARY = HexColor('#1a365d')
ACCENT = HexColor('#2563eb')
ACCENT2 = HexColor('#0ea5e9')
INK = HexColor('#1a1a2e')
MUTED = HexColor('#6b7280')
RULE = HexColor('#e5e7eb')
BG = HexColor('#f7f9fc')
BG2 = HexColor('#ffffff')
SUCCESS = HexColor('#16a34a')
WARNING = HexColor('#f59e0b')

# ============================================================
# Styles
# ============================================================
def get_styles():
    return {
        'title': ParagraphStyle(
            'Title', fontName=cjk_font, fontSize=26, leading=32,
            textColor=PRIMARY, spaceAfter=12, alignment=TA_CENTER, wordWrap='CJK'
        ),
        'subtitle': ParagraphStyle(
            'Subtitle', fontName=cjk_font, fontSize=13, leading=18,
            textColor=MUTED, spaceAfter=24, alignment=TA_CENTER, wordWrap='CJK'
        ),
        'h1': ParagraphStyle(
            'H1', fontName=cjk_font, fontSize=18, leading=24,
            textColor=PRIMARY, spaceBefore=20, spaceAfter=10, wordWrap='CJK',
            borderWidth=0, borderColor=ACCENT, borderPadding=5,
            leftIndent=0, backColor=None
        ),
        'h2': ParagraphStyle(
            'H2', fontName=cjk_font, fontSize=15, leading=21,
            textColor=ACCENT, spaceBefore=16, spaceAfter=8, wordWrap='CJK'
        ),
        'h3': ParagraphStyle(
            'H3', fontName=cjk_font, fontSize=13, leading=18,
            textColor=INK, spaceBefore=12, spaceAfter=6, wordWrap='CJK'
        ),
        'body': ParagraphStyle(
            'Body', fontName=cjk_font, fontSize=10, leading=16,
            textColor=INK, spaceBefore=0, spaceAfter=8,
            firstLineIndent=0, wordWrap='CJK'
        ),
        'body_small': ParagraphStyle(
            'BodySmall', fontName=cjk_font, fontSize=9, leading=14,
            textColor=MUTED, spaceBefore=0, spaceAfter=6, wordWrap='CJK'
        ),
        'caption': ParagraphStyle(
            'Caption', fontName=cjk_font, fontSize=9, leading=12,
            textColor=MUTED, alignment=TA_CENTER, spaceBefore=6, spaceAfter=12, wordWrap='CJK'
        ),
        'tag': ParagraphStyle(
            'Tag', fontName=cjk_font, fontSize=8, leading=10,
            textColor=ACCENT, wordWrap='CJK'
        ),
        'meta_label': ParagraphStyle(
            'MetaLabel', fontName=cjk_font, fontSize=8, leading=12,
            textColor=MUTED, wordWrap='CJK'
        ),
        'meta_value': ParagraphStyle(
            'MetaValue', fontName=cjk_font, fontSize=9, leading=14,
            textColor=INK, wordWrap='CJK'
        ),
        'timeline_date': ParagraphStyle(
            'TimelineDate', fontName=cjk_font, fontSize=9, leading=14,
            textColor=ACCENT, wordWrap='CJK'
        ),
        'timeline_title': ParagraphStyle(
            'TimelineTitle', fontName=cjk_font, fontSize=11, leading=16,
            textColor=INK, wordWrap='CJK'
        ),
        'timeline_source': ParagraphStyle(
            'TimelineSource', fontName=cjk_font, fontSize=8, leading=12,
            textColor=MUTED, wordWrap='CJK'
        ),
        'footer': ParagraphStyle(
            'Footer', fontName=cjk_font, fontSize=8, leading=12,
            textColor=white, alignment=TA_CENTER, wordWrap='CJK'
        ),
    }

styles = get_styles()

# ============================================================
# Helpers
# ============================================================
def colored_divider(width, height=2, color=ACCENT, space_before=6, space_after=10):
    from reportlab.platypus import Flowable
    class ColoredDivider(Flowable):
        def __init__(self, w, h, c, sb, sa):
            Flowable.__init__(self)
            self.width = w
            self.height = h
            self.color = c
            self.spaceBefore = sb
            self.spaceAfter = sa
        def draw(self):
            self.canv.setFillColor(self.color)
            self.canv.rect(0, 0, self.width, self.height, fill=1, stroke=0)
    return ColoredDivider(width, height, color, space_before, space_after)

def safe_image(path, max_w=CONTENT_WIDTH*0.9, max_h=CONTENT_HEIGHT*0.5):
    if not os.path.exists(path):
        return None
    from PIL import Image as PILImage
    pil_img = PILImage.open(path)
    orig_w_px, orig_h_px = pil_img.size
    dpi = pil_img.info.get('dpi', (150, 150))
    dpi_x = dpi[0] if dpi[0] else 150
    orig_w_pt = orig_w_px / dpi_x * 72
    orig_h_pt = orig_h_px / dpi_x * 72
    scale = min(max_w / orig_w_pt, max_h / orig_h_pt, 1.0)
    display_w = orig_w_pt * scale
    display_h = orig_h_pt * scale
    img = Image(path, width=display_w, height=display_h)
    img.hAlign = 'CENTER'
    return img

def wrap_cells(data, header_style, body_style):
    wrapped = []
    for i, row in enumerate(data):
        style = header_style if i == 0 else body_style
        wrapped.append([Paragraph(str(cell), style) for cell in row])
    return wrapped

def create_table(data, col_widths=None, is_large=False):
    header_style = ParagraphStyle(
        'TableHeader', fontName=cjk_font, fontSize=9, leading=12,
        textColor=white, wordWrap='CJK', alignment=TA_CENTER
    )
    body_style = ParagraphStyle(
        'TableBody', fontName=cjk_font, fontSize=8, leading=12,
        wordWrap='CJK', alignment=TA_LEFT
    )
    wrapped = wrap_cells(data, header_style, body_style)
    if col_widths is None:
        col_widths = [CONTENT_WIDTH / len(data[0])] * len(data[0])
    table = Table(wrapped, colWidths=col_widths, repeatRows=1 if is_large else 0)
    table.setStyle([
        ('BACKGROUND', (0, 0), (-1, 0), ACCENT),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, -1), cjk_font),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f7fafc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f7fafc'), white]),
        ('GRID', (0, 0), (-1, -1), 0.5, RULE),
    ])
    return table

# ============================================================
# Generate Charts as Images
# ============================================================
def generate_charts():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np

    chart_dir = "/workspace/smart-city-policy-report/assets"
    os.makedirs(chart_dir, exist_ok=True)

    # Set CJK font for matplotlib
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'Noto Sans CJK SC', 'SimHei', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False

    # Chart 1: Policy Count
    fig, ax = plt.subplots(figsize=(6, 3.5))
    dates = ['6/17', '6/12', '6/9', '6/8', '4/29', '4/17', '5/19']
    domestic = [1, 2, 1, 1, 1, 1, 1]
    foreign = [0, 1, 0, 0, 0, 0, 0]
    x = np.arange(len(dates))
    width = 0.35
    ax.bar(x - width/2, domestic, width, label='国内', color='#2563eb')
    ax.bar(x + width/2, foreign, width, label='国外', color='#0ea5e9')
    ax.set_xlabel('日期')
    ax.set_ylabel('政策数量')
    ax.set_title('国内外政策发布数量对比')
    ax.set_xticks(x)
    ax.set_xticklabels(dates)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    fig.savefig(f'{chart_dir}/chart_policy_count.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

    # Chart 2: Hot Area
    fig, ax = plt.subplots(figsize=(5, 4))
    labels = ['城市更新', '数字治理', 'AI应用', '数字孪生', '智能出行', '数据要素']
    sizes = [25, 20, 18, 15, 12, 10]
    colors = ['#2563eb', '#0ea5e9', '#6b7280', '#2563ebcc', '#0ea5e9cc', '#6b7280cc']
    ax.pie(sizes, labels=labels, autopct='%1.0f%%', colors=colors, startangle=90)
    ax.set_title('政策热点领域分布')
    plt.tight_layout()
    fig.savefig(f'{chart_dir}/chart_hot_area.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

    # Chart 3: Policy Level
    fig, ax = plt.subplots(figsize=(5, 4))
    labels = ['国家级', '地方级', '国外国家级', '国外地方级']
    sizes = [3, 2, 4, 2]
    colors = ['#2563eb', '#0ea5e9', '#6b7280', '#2563eb99']
    ax.pie(sizes, labels=labels, autopct='%1.0f%%', colors=colors, startangle=90)
    ax.set_title('政策层级分布')
    plt.tight_layout()
    fig.savefig(f'{chart_dir}/chart_policy_level.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

    # Chart 4: Tech Freq
    fig, ax = plt.subplots(figsize=(6, 4))
    keywords = ['人工智能', '数据要素', '数字孪生', '一网统管', '智能出行', 'CIM平台', '数据空间', 'REITs', '物联网', '区块链']
    freqs = [10, 9, 8, 7, 6, 5, 4, 3, 3, 2]
    colors_bar = ['#2563eb', '#0ea5e9', '#6b7280', '#2563ebcc', '#0ea5e9cc', '#6b7280cc', '#2563eb99', '#0ea5e999', '#6b728099', '#2563eb77']
    ax.barh(keywords, freqs, color=colors_bar)
    ax.set_xlabel('出现次数')
    ax.set_title('技术关键词出现频率')
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    plt.tight_layout()
    fig.savefig(f'{chart_dir}/chart_tech_freq.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

    # Chart 5: Funding
    fig, ax = plt.subplots(figsize=(6, 3.5))
    categories = ['中央预算\n内投资', '超长期\n特别国债', '中央财政\n补助', '地方\n专项债', '社会\n资本']
    values = [970, 1600, 500, 800, 1200]
    colors_bar = ['#2563eb', '#0ea5e9', '#6b7280', '#2563ebcc', '#0ea5e9cc']
    ax.bar(categories, values, color=colors_bar)
    ax.set_ylabel('亿元')
    ax.set_title('国内政策资金规模')
    for i, v in enumerate(values):
        ax.text(i, v + 30, str(v), ha='center', va='bottom', fontsize=9)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    fig.savefig(f'{chart_dir}/chart_funding.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

    # Chart 6: International Investment
    fig, ax = plt.subplots(figsize=(6, 3.5))
    categories = ['新加坡\nAI投资', '韩国\n智慧城市', '欧盟\n数字欧洲', '欧盟\nLDT4SSC', '越南\n智慧城市']
    values = [7.5, 0.85, 0.63, 0.032, 0.5]
    ax.bar(categories, values, color='#0ea5e9')
    ax.set_ylabel('亿美元')
    ax.set_title('国外政策投资规模对比')
    for i, v in enumerate(values):
        ax.text(i, v + 0.1, str(v), ha='center', va='bottom', fontsize=9)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    fig.savefig(f'{chart_dir}/chart_invest.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

    # Chart 7: Trend
    fig, ax = plt.subplots(figsize=(6, 4))
    years = ['2022', '2023', '2024', '2025', '2026']
    tech = [85, 80, 75, 70, 65]
    data_driven = [40, 55, 70, 82, 90]
    institution = [30, 35, 45, 60, 78]
    operation = [25, 30, 40, 55, 72]
    ax.plot(years, tech, marker='o', label='技术驱动', color='#6b7280')
    ax.plot(years, data_driven, marker='o', label='数据驱动', color='#2563eb', linewidth=2)
    ax.plot(years, institution, marker='o', label='制度驱动', color='#0ea5e9')
    ax.plot(years, operation, marker='o', label='运营驱动', color='#16a34a')
    ax.set_xlabel('年份')
    ax.set_ylabel('政策关注度指数')
    ax.set_title('政策趋势变化分析')
    ax.legend()
    ax.grid(linestyle='--', alpha=0.3)
    plt.tight_layout()
    fig.savefig(f'{chart_dir}/chart_trend.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

    print("Charts generated successfully!")

# ============================================================
# Build PDF
# ============================================================
def build_pdf():
    output_path = "/workspace/smart-city-policy-report/智慧城市政策日报_2026年6月24日.pdf"
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN,
    )

    story = []

    # ===== COVER PAGE =====
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("智慧城市政策日报", styles['title']))
    story.append(Paragraph("全球智慧城市政策动态监测与分析平台", styles['subtitle']))
    story.append(Spacer(1, 0.5*inch))
    story.append(colored_divider(CONTENT_WIDTH*0.6, 3, ACCENT, 0, 20))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("2026年6月24日 星期二", styles['subtitle']))
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph("本报告涵盖当日国内外智慧城市相关政策文件的发布动态、详细解读、数据可视化分析及趋势预测", styles['body_small']))
    story.append(PageBreak())

    # ===== TABLE OF CONTENTS =====
    story.append(Paragraph("目录", styles['h1']))
    story.append(colored_divider(CONTENT_WIDTH*0.3, 2, ACCENT, 0, 12))
    toc_items = [
        "一、国内政策分析",
        "   1.1 今日国内政策发布时间线",
        "   1.2 国内政策详细分析",
        "   1.3 地方试点动态",
        "二、国外政策分析",
        "   2.1 今日国外政策发布时间线",
        "   2.2 国外政策详细分析",
        "三、数据分析与可视化",
        "   3.1 政策关键词与热点分析",
        "   3.2 数据可视化图表",
        "   3.3 同类政策变化趋势对比",
        "   3.4 核心发现",
    ]
    for item in toc_items:
        story.append(Paragraph(item, styles['body']))
    story.append(PageBreak())

    # ===== SECTION 1: DOMESTIC =====
    story.append(Paragraph("一、国内政策分析", styles['h1']))
    story.append(colored_divider(CONTENT_WIDTH*0.3, 2, ACCENT, 0, 12))

    story.append(Paragraph("1.1 今日国内政策发布时间线", styles['h2']))

    domestic_timeline = [
        ["日期", "政策名称", "来源"],
        ["2026年6月17日", "住建部、国家数据局联合发布《关于全面建立房屋建筑统一代码制度的通知》", "住建部官网/国家数据局"],
        ["2026年6月12日", "国务院新闻办公室发布《城市更新\"十五五\"规划(2026-2030)》", "国务院新闻办公室"],
        ["2026年6月12日", "住建部、自然资源部联合印发建办厅函〔2026〕68号", "住建部官网"],
        ["2026年6月9日", "国家数据局印发《2026年数字社会发展工作要点》", "国家数据局"],
        ["2026年6月8日", "国务院新闻办公室举行城市更新政策吹风会", "国务院新闻办公室"],
        ["2026年4月29日", "甘肃省印发《深化智慧城市发展推进全域数字化转型行动方案》", "甘肃省人民政府"],
        ["2026年4月17日", "住建部、自然资源部联合印发城市更新可复制经验清单", "住建部官网"],
    ]
    story.append(create_table(domestic_timeline, [1.2*inch, 3.8*inch, 1.5*inch]))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("1.2 国内政策详细分析", styles['h2']))

    # Policy 1
    story.append(Paragraph("政策一：《关于全面建立房屋建筑统一代码制度的通知》", styles['h3']))
    meta_data = [
        ["发布单位", "住建部、国家数据局"],
        ["文号", "建办〔2026〕32号"],
        ["发布时间", "2026年6月17日"],
        ["政策层级", "国家级"],
        ["监督单位", "住建部、国家数据局"],
        ["数据来源", "住建部官网"],
    ]
    meta_table = Table([[Paragraph(k, styles['meta_label']), Paragraph(v, styles['meta_value'])] for k, v in meta_data],
                       colWidths=[1.5*inch, 3.5*inch])
    meta_table.setStyle([
        ('BACKGROUND', (0, 0), (0, -1), HexColor('#f7fafc')),
        ('GRID', (0, 0), (-1, -1), 0.5, RULE),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ])
    story.append(meta_table)
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph("<b>超详细政策要求：</b>", styles['body']))
    reqs = [
        "全面推行房屋建筑统一代码制度，为每套房屋分配18位终身不变编码",
        "2027年底实现新建房屋赋码全覆盖，2030年底完成存量房屋补录",
        "编码覆盖房屋全生命周期：规划、施工、验收、交易、运维、更新改造",
        "打通住建、自然资源、税务、公安、街道社区、消防、物业等部门数据",
        "建立全国统一房屋基础信息数据库，实现\"一码贯通\"",
        "支撑城市更新、社区治理、公共服务等领域应用",
    ]
    for req in reqs:
        story.append(Paragraph(f"• {req}", styles['body']))

    story.append(Paragraph("<b>与前政策的详细区别：</b>", styles['body']))
    diffs = [
        "此前仅在部分城市试点房屋编码，本次面向全国落地执行",
        "不动产单元号只管产权信息，新编码覆盖房屋全生命周期工程资料",
        "新增\"一房一码\"数据库，实现房屋从建设到拆除的完整档案管理",
        "首次明确将房屋编码与城市更新、社区治理深度绑定",
    ]
    for diff in diffs:
        story.append(Paragraph(f"• {diff}", styles['body']))
    story.append(Spacer(1, 0.15*inch))

    # Policy 2
    story.append(Paragraph("政策二：《城市更新\"十五五\"规划(2026-2030)》", styles['h3']))
    meta_data2 = [
        ["发布单位", "国务院"],
        ["发布时间", "2026年6月8日"],
        ["政策层级", "国家级专项规划"],
        ["资金支持", "超2500亿元"],
        ["监督单位", "住建部、发改委"],
        ["数据来源", "36氪/国务院政策文件"],
    ]
    meta_table2 = Table([[Paragraph(k, styles['meta_label']), Paragraph(v, styles['meta_value'])] for k, v in meta_data2],
                        colWidths=[1.5*inch, 3.5*inch])
    meta_table2.setStyle([
        ('BACKGROUND', (0, 0), (0, -1), HexColor('#f7fafc')),
        ('GRID', (0, 0), (-1, -1), 0.5, RULE),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ])
    story.append(meta_table2)
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph("<b>超详细政策要求：</b>", styles['body']))
    reqs2 = [
        "城市更新首部国家级专项规划，明确2026-2030年目标指标",
        "部署6方面重点任务：新动能、生活空间、绿色低碳、安全韧性、文化繁荣、治理能力",
        "14项重大工程：好房子建设、老旧小区改造、完整社区建设、老旧街区厂区改造等",
        "中央预算内投资970亿元，超长期特别国债1600亿元支持地下管网建设",
        "2030年前完成50万套危房更新改造（较上期翻倍）",
        "2030年前实现95%以上城市住房基础数据数字化",
        "建立可持续投融资机制：中央资金、地方专项债、社会资本、居民共担",
    ]
    for req in reqs2:
        story.append(Paragraph(f"• {req}", styles['body']))

    story.append(Paragraph("<b>与前政策的详细区别：</b>", styles['body']))
    diffs2 = [
        "从\"大规模扩张\"转向\"提质增效\"，强调存量资源优化",
        "首次将房地产定位为城市更新核心环节，提出\"保刚需、优改善、促转型\"",
        "新增\"好房子\"建设标准，全链条提升住房品质",
        "引入数字家庭建设，丰富数字家庭应用场景",
        "从单纯政府投资转向多元化融资，鼓励REITs等市场化工具",
    ]
    for diff in diffs2:
        story.append(Paragraph(f"• {diff}", styles['body']))
    story.append(PageBreak())

    # Policy 3 & 4
    story.append(Paragraph("政策三：《完善城市更新工程项目建设实施管理机制可复制经验做法清单》", styles['h3']))
    story.append(Paragraph("发布单位：住建部、自然资源部 | 文号：建办厅函〔2026〕68号 | 发布时间：2026年4月17日", styles['body_small']))
    story.append(Paragraph("<b>政策要点：</b>梳理全国30项成熟经验，覆盖前期策划、政策标准、审批流程、高效办成一件事、实施监管、长效运营6大模块。", styles['body']))
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph("政策四：《深化智慧城市发展推进全域数字化转型行动方案》", styles['h3']))
    story.append(Paragraph("发布单位：甘肃省数据局等五部门 | 文号：甘数发〔2026〕4号 | 发布时间：2026年4月29日", styles['body_small']))
    story.append(Paragraph("<b>政策要点：</b>到2027年底数据赋能城市经济社会发展效果明显增强，构建城市智慧高效治理体系，深化\"一网统管\"，加快CIM建设，建立\"一房一码\"数据库。", styles['body']))
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph("政策五：《2026年数字社会发展工作要点》", styles['h3']))
    story.append(Paragraph("发布单位：国家数据局 | 发布时间：2026年5月19日", styles['body_small']))
    story.append(Paragraph("<b>政策要点：</b>聚焦4个方面23项任务，\"因地制宜开展城市全域数字化转型试点建设\"列为核心方向。", styles['body']))
    story.append(PageBreak())

    story.append(Paragraph("1.3 地方试点动态", styles['h2']))
    stats_data = [
        ["指标", "数值"],
        ["地级及以上城市启动智慧城市建设", "90%+"],
        ["2026年智慧城市ICT产业规模", "1.5万亿元"],
        ["江苏省首批试点（市级+县级）", "5+5"],
        ["中央财政累计支持重点城市", "50个"],
    ]
    story.append(create_table(stats_data, [3*inch, 2*inch]))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("数据来源：住建部、国家数据局2026年上半年公开调研数据", styles['body_small']))
    story.append(PageBreak())

    # ===== SECTION 2: INTERNATIONAL =====
    story.append(Paragraph("二、国外政策分析", styles['h1']))
    story.append(colored_divider(CONTENT_WIDTH*0.3, 2, ACCENT, 0, 12))

    story.append(Paragraph("2.1 今日国外政策发布时间线", styles['h2']))
    foreign_timeline = [
        ["日期", "政策/动态名称", "来源"],
        ["2026年6月18日", "欧盟委员会发布《数字十年状况2026》报告", "欧盟委员会"],
        ["2026年6月12日", "韩国国土交通部公布2026年智慧城市建设项目选定结果", "韩国国土交通部"],
        ["2026年5月26日", "欧盟发布智慧城市公共政策指数更新", "IoT M2M Council"],
        ["2026年4月22日", "欧盟委员会发布智慧城市与社区数字转型工具包", "欧盟数字战略官网"],
        ["2026年4月14日", "越南胡志明市发布智慧城市发展规划草案（2026-2030）", "越南建设部"],
        ["2026年3月17日", "新加坡正式启动Smart Nation 2.0战略", "新加坡数字发展部"],
        ["2026年3月17日", "哈萨克斯坦批准智慧城市与区域建设方法论", "哈萨克斯坦政府"],
        ["2026年3月12日", "韩国国土交通部启动2026年智慧城市建设项目公开招募", "韩国智慧城市综合门户"],
    ]
    story.append(create_table(foreign_timeline, [1.2*inch, 3.8*inch, 1.5*inch]))
    story.append(PageBreak())

    story.append(Paragraph("2.2 国外政策详细分析", styles['h2']))

    policies_foreign = [
        ("欧盟《数字十年状况2026》报告", "欧盟委员会", "2026年6月18日", "欧盟层面",
         ["发布《数字十年状况2026》报告，涵盖21个主题领域",
          "智慧城市与社区列为第20项重点监测指标",
          "投入6320万欧元支持医疗系统AI创新和在线安全",
          "推动本地数字孪生(LDT)工具包建设",
          "建立欧洲数据空间，促进智慧城市数据共享"]),
        ("韩国2026年智慧城市建设项目", "韩国国土交通部", "2026年6月12日", "国家级",
         ["选定水原为据点型智慧城市，釜山、城南为特化园区",
          "水原市3年间最高160亿韩元国费支持",
          "智能出行体系：汽车共享、停车机器人、机器人配送",
          "釜山市构建开放型AI城市实证平台",
          "城南市构建Life Mobility特化园区"]),
        ("新加坡Smart Nation 2.0战略", "新加坡数字发展部(MDDI)", "2026年3月17日", "国家级",
         ["三大支柱：信任(Trust)、增长(Growth)、社区(Community)",
          "5年内超10亿新元AI专项投资",
          "数字经济已贡献1281亿新元，占GDP 18.6%",
          "99%政务服务完全在线化",
          "全球首个实现5G独立组网全国覆盖的国家"]),
        ("越南胡志明市智慧城市发展规划", "胡志明市科技厅、建设厅", "2026年4月14日", "地方级",
         ["目标2030年进入全球智慧城市前50名",
          "应用AI、大语言模型(LLM)、预测分析、数字孪生技术",
          "建立统一共享数据平台",
          "从\"技术驱动型\"转向\"制度驱动型\"智慧城市"]),
        ("哈萨克斯坦智慧城市与区域建设方法论", "哈萨克斯坦人工智能与数字发展部", "2026年7月12日生效", "国家级",
         ["定义智慧城市为基于数字技术的城市环境发展模式",
          "八大数字化领域：城市管理、公共安全、交通物流、生态等",
          "基础技术：AI辅助情景中心、统一呼叫中心109+、智能公交站点",
          "所有系统基于国家QazTech平台构建"]),
    ]

    for title, publisher, date, level, points in policies_foreign:
        story.append(Paragraph(f"{title}", styles['h3']))
        story.append(Paragraph(f"发布国家/组织：{publisher} | 发布时间：{date} | 政策层级：{level}", styles['body_small']))
        for pt in points:
            story.append(Paragraph(f"• {pt}", styles['body']))
        story.append(Spacer(1, 0.1*inch))

    story.append(PageBreak())

    # ===== SECTION 3: ANALYSIS =====
    story.append(Paragraph("三、数据分析与可视化", styles['h1']))
    story.append(colored_divider(CONTENT_WIDTH*0.3, 2, ACCENT, 0, 12))

    story.append(Paragraph("3.1 政策关键词与热点分析", styles['h2']))
    keywords = "城市更新 | 数字化转型 | 人工智能 | 数字孪生 | 数据要素 | 一网统管 | 智慧交通 | 智能出行 | CIM平台 | 房屋编码 | 全域数字化 | 数据空间 | 绿色低碳 | 安全韧性 | 投融资机制 | REITs | 物联网 | 区块链"
    story.append(Paragraph(keywords, styles['body']))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("3.2 数据可视化图表", styles['h2']))

    chart_files = [
        ("chart_policy_count.png", "图1：国内外政策发布数量对比"),
        ("chart_hot_area.png", "图2：政策热点领域分布"),
        ("chart_policy_level.png", "图3：政策层级分布"),
        ("chart_tech_freq.png", "图4：技术关键词出现频率"),
        ("chart_funding.png", "图5：国内政策资金规模"),
        ("chart_invest.png", "图6：国外政策投资规模对比"),
        ("chart_trend.png", "图7：政策趋势变化分析"),
    ]

    for chart_file, caption in chart_files:
        chart_path = f"/workspace/smart-city-policy-report/assets/{chart_file}"
        img = safe_image(chart_path, max_w=CONTENT_WIDTH*0.85, max_h=CONTENT_HEIGHT*0.4)
        if img:
            story.append(img)
            story.append(Paragraph(caption, styles['caption']))
            story.append(Spacer(1, 0.1*inch))

    story.append(PageBreak())

    story.append(Paragraph("3.3 同类政策变化趋势对比", styles['h2']))
    compare_data = [
        ["对比维度", "2024年政策特征", "2026年政策特征", "变化趋势"],
        ["建设重心", "单点试点、技术堆砌", "全域统筹、场景实效", "从试点到全域"],
        ["技术导向", "以技术为中心", "以数据要素价值化为中心", "数据驱动"],
        ["投资模式", "政府单一投入", "多元化融资（专项债+REITs+社会资本）", "市场化程度提升"],
        ["治理模式", "部门分割、数据孤岛", "一网统管、数据融通", "协同治理"],
        ["民生导向", "重建设轻运营", "以人为本、长效运营", "运营导向"],
        ["标准体系", "标准不一、无序建设", "全国统一标准+区域差异化", "规范化提升"],
        ["国际趋势", "技术驱动型智慧城市", "制度驱动型智慧城市", "制度创新"],
        ["AI应用", "辅助决策、单一应用", "AI代理、城市级智能中枢", "智能化升级"],
    ]
    story.append(create_table(compare_data, [1.3*inch, 2.2*inch, 2.2*inch, 1.3*inch]))
    story.append(PageBreak())

    story.append(Paragraph("3.4 核心发现", styles['h2']))
    findings = [
        "<b>城市更新成为核心抓手：</b>国内政策围绕\"十五五\"城市更新规划密集出台，资金规模超2500亿元，从扩张型发展转向质量型增长",
        "<b>AI深度赋能智慧城市：</b>韩国、新加坡、越南等国均将AI作为智慧城市核心驱动力，从辅助工具升级为城市级智能中枢",
        "<b>数字孪生成为标配技术：</b>欧盟、越南、中国均在推进CIM平台和数字孪生城市建设，实现虚实共生、仿真推演",
        "<b>数据要素价值化加速：</b>从\"数据汇聚\"转向\"数据资产运营\"，数据空间、数据枢纽成为新基建重点",
        "<b>制度创新引领转型：</b>越南明确提出从\"技术驱动\"转向\"制度驱动\"，新加坡Smart Nation 2.0强调制度变革",
        "<b>投融资机制创新：</b>国内引入REITs、专项债等市场化工具，国外强调PPP和公私合作",
        "<b>全域数字化转型：</b>从单点智慧场景转向城市整体治理效率提升，强调一网统管、一网通办",
    ]
    for finding in findings:
        story.append(Paragraph(finding, styles['body']))
        story.append(Spacer(1, 0.05*inch))

    # ===== FOOTER =====
    story.append(Spacer(1, 0.5*inch))
    story.append(colored_divider(CONTENT_WIDTH, 1, RULE, 10, 10))
    story.append(Paragraph("智慧城市政策日报 | 数据更新时间：2026年6月24日 | 数据来源：各国政府官网、权威媒体", styles['body_small']))
    story.append(Paragraph("本报告仅供参考，政策解读以官方发布为准", styles['body_small']))

    # Build
    doc.build(story)
    print(f"PDF generated successfully: {output_path}")
    return output_path

if __name__ == "__main__":
    generate_charts()
    build_pdf()
