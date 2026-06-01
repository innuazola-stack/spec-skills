from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent
PDF_OUT = ROOT / "od_urla_menu_zh.pdf"
ORIGINAL_PDF = Path(r"C:\Users\54256213\Downloads\od_urla_menue_mart_2026_4cce16c439.pdf")
APPENDIX_OUT = ROOT / "od_urla_original_plus_zh_menu.pdf"
FONT_PATH = Path(r"C:\Windows\Fonts\simhei.ttf")


pdfmetrics.registerFont(TTFont("SimHei", str(FONT_PATH)))


def p(text, style):
    return Paragraph(text, style)


def bullet_list(items, styles):
    return ListFlowable(
        [ListItem(Paragraph(item, styles["BulletText"]), leftIndent=0) for item in items],
        bulletType="bullet",
        start="circle",
        leftIndent=14,
        bulletFontName="SimHei",
        bulletFontSize=8,
    )


def price_table(rows, styles):
    data = [[Paragraph("菜品", styles["TableHeader"]), Paragraph("价格", styles["TableHeader"])]]
    data.extend([[Paragraph(item, styles["TableCell"]), Paragraph(price, styles["TablePrice"])] for item, price in rows])
    table = Table(data, colWidths=[128 * mm, 28 * mm], repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EEE7DA")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#2D2926")),
                ("FONTNAME", (0, 0), (-1, -1), "SimHei"),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#D7CDBF")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("ALIGN", (1, 1), (1, -1), "RIGHT"),
            ]
        )
    )
    return table


def build_pdf():
    doc = SimpleDocTemplate(
        str(PDF_OUT),
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="OD Urla 简体中文菜单",
        author="Codex",
    )

    base = getSampleStyleSheet()
    styles = {
        "Title": ParagraphStyle(
            "Title",
            parent=base["Title"],
            fontName="SimHei",
            fontSize=24,
            leading=30,
            textColor=colors.HexColor("#2D2926"),
            spaceAfter=8,
        ),
        "Subtitle": ParagraphStyle(
            "Subtitle",
            parent=base["Normal"],
            fontName="SimHei",
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#6D6256"),
            alignment=1,
            spaceAfter=16,
        ),
        "H1": ParagraphStyle(
            "H1",
            parent=base["Heading1"],
            fontName="SimHei",
            fontSize=16,
            leading=22,
            textColor=colors.HexColor("#544739"),
            spaceBefore=14,
            spaceAfter=7,
        ),
        "H2": ParagraphStyle(
            "H2",
            parent=base["Heading2"],
            fontName="SimHei",
            fontSize=12.5,
            leading=17,
            textColor=colors.HexColor("#7A5A36"),
            spaceBefore=10,
            spaceAfter=5,
        ),
        "Body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="SimHei",
            fontSize=9.5,
            leading=15,
            textColor=colors.HexColor("#2D2926"),
            spaceAfter=6,
        ),
        "Price": ParagraphStyle(
            "Price",
            parent=base["BodyText"],
            fontName="SimHei",
            fontSize=10.5,
            leading=16,
            textColor=colors.HexColor("#2D2926"),
            spaceAfter=3,
        ),
        "BulletText": ParagraphStyle(
            "BulletText",
            parent=base["BodyText"],
            fontName="SimHei",
            fontSize=9.5,
            leading=14,
            textColor=colors.HexColor("#2D2926"),
        ),
        "TableHeader": ParagraphStyle(
            "TableHeader",
            parent=base["BodyText"],
            fontName="SimHei",
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor("#2D2926"),
        ),
        "TableCell": ParagraphStyle(
            "TableCell",
            parent=base["BodyText"],
            fontName="SimHei",
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#2D2926"),
        ),
        "TablePrice": ParagraphStyle(
            "TablePrice",
            parent=base["BodyText"],
            fontName="SimHei",
            fontSize=9,
            leading=13,
            alignment=2,
            textColor=colors.HexColor("#2D2926"),
        ),
        "Note": ParagraphStyle(
            "Note",
            parent=base["BodyText"],
            fontName="SimHei",
            fontSize=8.5,
            leading=12.5,
            textColor=colors.HexColor("#5A5148"),
            spaceAfter=4,
        ),
    }

    story = []
    story.append(p("OD Urla 简体中文菜单", styles["Title"]))
    story.append(p("来源：od_urla_menue_mart_2026_4cce16c439.pdf ｜ 币种：土耳其里拉（TL）", styles["Subtitle"]))

    story.append(p("餐厅寄语", styles["H1"]))
    intro = [
        "如今留给我们最珍贵的遗产，是我们所处的这片土地。无论身在世界何处，我们始终记得自己的根源：出生的地方、成长的城市、走过的道路，最终共同塑造了我们是谁。",
        "这份遗产的故事，会通过我们从当下的土地与水中创造出的味道，传递给下一代。菜单中的食材生长于爱琴海地区的水土之中，经过细致挑选并组合成一道道菜式。",
        "作为主厨，我把一生中获得的灵感与经验融入这套品鉴菜单，并将它命名为“主厨之旅”。菜单中的每一道菜都使用应季食材，以符合伦理的方式生产，并来自优秀的本地生产者。",
    ]
    for text in intro:
        story.append(p(text, styles["Body"]))

    story.append(p("主厨之旅", styles["H1"]))
    for line in ["每位：5950 TL", "本地葡萄酒配餐，6 杯：4500 TL", "侍酒师精选葡萄酒配餐，6 杯：7500 TL"]:
        story.append(p(line, styles["Price"]))
    story.append(
        bullet_list(
            [
                "腌渍海鲷",
                "荨麻汤",
                "甜菜根、Armola 奶酪",
                "烟熏鱼、刺山柑",
                "海鲈鱼塔塔、Radika 野菜、水芹",
                "芦笋、散养鸡蛋、土耳其风干牛肉",
                "海鲷、根芹、Bornova Misket 葡萄酒酱",
                "虾、Tarhana 发酵汤底、鸟舌面",
                "欧芹雪葩",
                "牛肋排、羊肚菌、青麦碎、松露",
                "巧克力、森林莓果",
                "土耳其咖啡焦糖米布丁",
                "黑桑葚果冻",
                "烤鹰嘴豆",
                "花生",
            ],
            styles,
        )
    )

    story.append(PageBreak())
    story.append(p("四道式菜单", styles["H1"]))
    for line in ["每位：4950 TL", "本地葡萄酒配餐，4 杯：3250 TL", "侍酒师精选葡萄酒配餐，4 杯：5250 TL"]:
        story.append(p(line, styles["Price"]))

    prix_fixe_sections = [
        (
            "第一道任选一款",
            [
                "鱿鱼、蛤蜊、Gambilya 蚕豆泥、芝麻菜",
                "虾、朝鲜蓟、柑橘",
                "海鲈鱼塔塔、Radika 野菜、水芹",
                "芦笋、散养鸡蛋、土耳其风干牛肉",
                "羊肚菌",
            ],
        ),
        (
            "第二道任选一款",
            [
                "虾、Tarhana 发酵汤底、鸟舌面",
                "根芹土耳其饺、鱿鱼",
                "蘑菇土耳其饺、羊胸腺、孜然",
                "山羊奶酪土耳其饺、焦糖梨、可可",
                "章鱼、土豆、石榴糖浆",
                "牛尾、薄饼、无花果糖蜜牛肉汁、焦糖洋葱",
            ],
        ),
        (
            "主菜任选一款",
            [
                "海鲷、根芹、Bornova Misket 葡萄酒酱",
                "羊肉、朝鲜蓟、野茴香叶",
                "牛肋排、羊肚菌、青麦碎、松露",
                "当日鲜鱼、虾、黑贻贝、蛤蜊、烟熏鱼酱",
            ],
        ),
        (
            "甜品任选一款",
            ["榛子、咸焦糖、松露", "草莓、罗勒", "巧克力千层酥、森林莓果"],
        ),
    ]
    for title, items in prix_fixe_sections:
        story.append(p(title, styles["H2"]))
        story.append(bullet_list(items, styles))
    story.append(p("精品奶酪", styles["H2"]))
    story.append(p("本地手工奶酪拼盘：1150 TL。餐厅建议在甜品前加点奶酪。", styles["Body"]))

    story.append(PageBreak())
    story.append(p("13:00-18:00 单点菜单", styles["H1"]))
    tables = [
        (
            "第一道",
            [
                ("鱿鱼、蛤蜊、Gambilya 蚕豆泥、芝麻菜", "1550 TL"),
                ("虾、朝鲜蓟、柑橘", "1650 TL"),
                ("海鲈鱼塔塔、Radika 野菜、水芹", "1550 TL"),
                ("芦笋、散养鸡蛋、土耳其风干牛肉", "1450 TL"),
                ("羊肚菌", "1450 TL"),
            ],
        ),
        (
            "第二道",
            [
                ("虾、Tarhana 发酵汤底、鸟舌面", "1700 TL"),
                ("根芹土耳其饺、鱿鱼", "1500 TL"),
                ("蘑菇土耳其饺、羊胸腺、孜然", "1450 TL"),
                ("山羊奶酪土耳其饺、焦糖梨、可可", "1450 TL"),
                ("章鱼、土豆、石榴糖浆", "1650 TL"),
                ("牛尾、薄饼、无花果糖蜜牛肉汁、焦糖洋葱", "1500 TL"),
            ],
        ),
        (
            "主菜",
            [
                ("海鲷、根芹、Bornova Misket 葡萄酒酱", "2100 TL"),
                ("羊肉、朝鲜蓟、野茴香叶", "2100 TL"),
                ("牛肋排、羊肚菌、青麦碎、松露", "2200 TL"),
                ("当日鲜鱼、虾、黑贻贝、蛤蜊、烟熏鱼酱", "2300 TL"),
            ],
        ),
        (
            "甜品",
            [
                ("榛子、咸焦糖、松露", "900 TL"),
                ("草莓、罗勒", "900 TL"),
                ("巧克力千层酥、森林莓果", "900 TL"),
            ],
        ),
        ("精品奶酪", [("本地手工奶酪拼盘", "1400 TL")]),
    ]
    for title, rows in tables:
        story.append(p(title, styles["H2"]))
        story.append(price_table(rows, styles))
        story.append(Spacer(1, 5 * mm))

    story.append(PageBreak())
    story.append(p("用餐说明", styles["H1"]))
    for note in [
        "素菜品在原菜单中以图标标注；如需纯素选项，请咨询主厨团队。",
        "固定菜单为了保证服务流程顺畅，仅当同桌所有客人共同选择时提供。",
        "如有食物过敏，请提前告知服务人员。",
        "所有价格均为土耳其里拉。",
    ]:
        story.append(p(note, styles["Note"]))

    story.append(p("食材名说明", styles["H1"]))
    glossary = [
        "Radika：土耳其及爱琴海地区常见的野菜，常译作野菊苣或蒲公英类野菜。",
        "Gambilya：爱琴海地区豆类食材，常用于制作 fava 豆泥。",
        "Tarhana：土耳其传统发酵谷物/酸奶汤底。",
        "Bornova Misket：土耳其葡萄品种，可用于酿制芳香型葡萄酒。",
        "Firik：烘烤青麦制成的谷物，也可译作青麦碎。",
        "Pastırma：土耳其风干牛肉。",
        "Mantı：土耳其饺子。",
    ]
    story.append(bullet_list(glossary, styles))

    doc.build(story)


def append_to_original():
    writer = PdfWriter()
    for page in PdfReader(str(ORIGINAL_PDF)).pages:
        writer.add_page(page)
    for page in PdfReader(str(PDF_OUT)).pages:
        writer.add_page(page)
    with APPENDIX_OUT.open("wb") as handle:
        writer.write(handle)


if __name__ == "__main__":
    build_pdf()
    append_to_original()
    print(PDF_OUT)
    print(APPENDIX_OUT)
