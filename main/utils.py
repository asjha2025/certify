# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4, landscape
# from reportlab.lib.colors import Color, black, blue, gold
# from reportlab.pdfbase import pdfutils
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfbase import pdfmetrics
# from reportlab.lib.units import inch
# import os
# from PIL import Image, ImageDraw, ImageFont
# import textwrap
# from arabic_reshaper import ArabicReshaper
# from bidi.algorithm import get_display

# # تسجيل الخط العربي
# font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static", "fonts", "Amiri-1.000", "Amiri-Regular.ttf")
# pdfmetrics.registerFont(TTFont("Amiri-Regular", font_path))

# def generate_certificate(cert, template_path="static/certificate_template.png"):
#     """
#     توليد شهادة PDF محسنة مع تصميم احترافي
#     """
#     # إنشاء مجلد الشهادات إذا لم يكن موجوداً
#     os.makedirs("media/certificates", exist_ok=True)
    
#     file_path = f"media/certificates/{cert.id}.pdf"
    
#     # إعداد الصفحة بالاتجاه الأفقي
#     width, height = landscape(A4)
#     c = canvas.Canvas(file_path, pagesize=landscape(A4))
    
#     # ألوان مخصصة
#     primary_color = Color(0.29, 0.68, 0.99)  # أزرق فاتح
#     secondary_color = Color(0.4, 0.31, 0.64)  # بنفسجي
#     gold_color = Color(1, 0.84, 0)  # ذهبي
    
#     # رسم الخلفية والحدود
#     draw_certificate_background(c, width, height, primary_color, secondary_color)
    
#     # إضافة الشعار إذا كان متوفراً
#     if cert.logo:
#         try:
#             logo_path = cert.logo.path
#             if os.path.exists(logo_path):
#                 c.drawImage(logo_path, width - 150, height - 100, width=80, height=80, mask='auto')
#         except:
#             pass
    
#     # إضافة النصوص
#     add_certificate_text(c, cert, width, height, primary_color, gold_color)
    
#     # إضافة الزخارف والعناصر التزيينية
#     add_decorative_elements(c, width, height, gold_color)
    
#     # حفظ الملف
#     c.save()
#     return file_path

# def draw_certificate_background(c, width, height, primary_color, secondary_color):
#     """
#     رسم خلفية الشهادة مع التدرجات والحدود
#     """
#     # خلفية بيضاء
#     c.setFillColor(Color(1, 1, 1))
#     c.rect(0, 0, width, height, fill=1)
    
#     # حدود خارجية
#     c.setStrokeColor(primary_color)
#     c.setLineWidth(8)
#     c.rect(30, 30, width-60, height-60, fill=0)
    
#     # حدود داخلية
#     c.setStrokeColor(secondary_color)
#     c.setLineWidth(3)
#     c.rect(50, 50, width-100, height-100, fill=0)
    
#     # خط علوي مزخرف
#     c.setStrokeColor(primary_color)
#     c.setLineWidth(4)
#     c.line(100, height-120, width-100, height-120)

# def add_certificate_text(c, cert, width, height, primary_color, gold_color):
#     """
#     إضافة النصوص للشهادة
#     """
#     reshaper = ArabicReshaper({
#         'delete_harakat': False,
#         'support_ligatures': True
#     })

#     # عنوان الشهادة
#     c.setFillColor(primary_color)
#     c.setFont("Amiri-Regular", 36)
#     title = get_display(reshaper.reshape("شهادة إتمام"))
#     title_width = c.stringWidth(title, "Amiri-Regular", 36)
#     c.drawString((width - title_width) / 2, height - 100, title)
    
#     # نص "يشهد بأن"
#     c.setFillColor(black)
#     c.setFont("Amiri-Regular", 18)
#     subtitle = get_display(reshaper.reshape("يشهد بأن"))
#     subtitle_width = c.stringWidth(subtitle, "Amiri-Regular", 18)
#     c.drawString((width - subtitle_width) / 2, height - 140, subtitle)
    
#     # اسم الموظف
#     c.setFillColor(gold_color)
#     c.setFont("Amiri-Regular", 32)
#     name = get_display(reshaper.reshape(cert.employee_name))
#     name_width = c.stringWidth(name, "Amiri-Regular", 32)
#     c.drawString((width - name_width) / 2, height - 200, name)
    
#     # خط تحت الاسم
#     c.setStrokeColor(gold_color)
#     c.setLineWidth(2)
#     c.line((width - name_width) / 2 - 20, height - 210, 
#            (width + name_width) / 2 + 20, height - 210)
    
#     # نص "قد أتم بنجاح"
#     c.setFillColor(black)
#     c.setFont("Amiri-Regular", 18)
#     completion_text = get_display(reshaper.reshape("قد أتم بنجاح"))
#     completion_width = c.stringWidth(completion_text, "Amiri-Regular", 18)
#     c.drawString((width - completion_width) / 2, height - 250, completion_text)
    
#     # عنوان الدورة
#     c.setFillColor(primary_color)
#     c.setFont("Amiri-Regular", 24)
    
#     # تقسيم النص إذا كان طويلاً
#     course_lines = textwrap.wrap(cert.course_title, width=40)
#     y_position = height - 300
    
#     for line in course_lines:
#         reshaped_line = get_display(reshaper.reshape(line))
#         line_width = c.stringWidth(reshaped_line, "Amiri-Regular", 24)
#         c.drawString((width - line_width) / 2, y_position, reshaped_line)
#         y_position -= 30
    
#     # التاريخ
#     c.setFillColor(black)
#     c.setFont("Amiri-Regular", 16)
#     date_text = get_display(reshaper.reshape("تاريخ الإصدار: " + cert.issue_date.strftime("%d/%m/%Y")))
#     date_width = c.stringWidth(date_text, "Amiri-Regular", 16)
#     c.drawString((width - date_width) / 2, 120, date_text)

# def add_decorative_elements(c, width, height, gold_color):
#     """
#     إضافة العناصر التزيينية للشهادة
#     """
#     # نجوم تزيينية
#     c.setFillColor(gold_color)
    
#     # نجمة يسار
#     draw_star(c, 150, height/2, 20)
    
#     # نجمة يمين
#     draw_star(c, width-150, height/2, 20)
    
#     # زخارف في الزوايا
#     c.setStrokeColor(gold_color)
#     c.setLineWidth(2)
    
#     # زاوية علوية يسرى
#     c.arc(70, height-70, 120, height-120, 0, 90)
    
#     # زاوية علوية يمنى
#     c.arc(width-120, height-70, width-70, height-120, 90, 180)
    
#     # زاوية سفلية يسرى
#     c.arc(70, 70, 120, 120, 270, 360)
    
#     # زاوية سفلية يمنى
#     c.arc(width-120, 70, width-70, 120, 180, 270)

# def draw_star(c, x, y, size):
#     """
#     رسم نجمة تزيينية
#     """
#     import math
    
#     points = []
#     for i in range(10):
#         angle = math.pi * i / 5
#         if i % 2 == 0:
#             radius = size
#         else:
#             radius = size * 0.4
        
#         px = x + radius * math.cos(angle - math.pi/2)
#         py = y + radius * math.sin(angle - math.pi/2)
#         points.extend([px, py])
    
#     # رسم النجمة
#     path = c.beginPath()
#     path.moveTo(points[0], points[1])
#     for i in range(2, len(points), 2):
#         path.lineTo(points[i], points[i+1])
#     path.close()
#     c.drawPath(path, fill=1)

# def create_certificate_template():
#     """
#     إنشاء قالب شهادة افتراضي
#     """
#     # يمكن استخدام هذه الوظيفة لإنشاء قوالب مخصصة
#     pass




from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import Color, black, blue, white
from reportlab.pdfbase import pdfutils
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import inch
import os
from PIL import Image, ImageDraw, ImageFont
import textwrap
from arabic_reshaper import ArabicReshaper
from bidi.algorithm import get_display

# تسجيل الخط العربي
font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static", "fonts", "Amiri-1.000", "Amiri-Regular.ttf")
pdfmetrics.registerFont(TTFont("Amiri-Regular", font_path))

# ألوان التصميم الجديد
KSU_BLUE = Color(0.0, 0.4, 0.8)  # الأزرق الخاص بجامعة الملك سعود
KSU_LIGHT_BLUE = Color(0.4, 0.8, 1.0)  # الأزرق الفاتح
GRAY_TEXT = Color(0.3, 0.3, 0.3)  # الرمادي للنصوص

def generate_certificate(cert, template_path="static/certificate_template.png"):
    """
    توليد شهادة PDF بتصميم جامعة الملك سعود
    """
    # إنشاء مجلد الشهادات إذا لم يكن موجوداً
    os.makedirs("media/certificates", exist_ok=True)
    
    file_path = f"media/certificates/{cert.id}.pdf"
    
    # إعداد الصفحة بالاتجاه الأفقي
    width, height = landscape(A4)
    c = canvas.Canvas(file_path, pagesize=landscape(A4))
    
    # رسم الخلفية والتصميم
    draw_ksu_certificate_design(c, width, height)
    
    # إضافة النصوص
    add_ksu_certificate_text(c, cert, width, height)
    
    # حفظ الملف
    c.save()
    return file_path

def draw_ksu_certificate_design(c, width, height):
    """
    رسم تصميم شهادة جامعة الملك سعود
    """
    # خلفية بيضاء
    c.setFillColor(white)
    c.rect(0, 0, width, height, fill=1)
    
    # الشريط الأزرق العلوي
    c.setFillColor(KSU_LIGHT_BLUE)
    c.rect(0, height - 20, width, 20, fill=1)
    
    # رسم الأشكال الهندسية في الأسفل (مثلثات)
    # draw_geometric_shapes(c, width, height)
    
    # رسم شعار الجامعة (مربع أزرق في الأعلى يمين)
    draw_ksu_logo_placeholder(c, width, height)


def draw_ksu_logo_placeholder(c, width, height, logo_path="static/logo.png"):
    """
    إضافة صورة شعار جامعة الملك سعود بدل الرسم اليدوي
    """
    # أبعاد ومكان الشعار
    logo_width = 200
    logo_height = 100
    logo_x = width - logo_width - 30
    logo_y = height - logo_height - 50  # نزوله قليلًا عشان النص أسفل

    if os.path.exists(logo_path):
        # إدراج صورة الشعار
        c.drawImage(logo_path, logo_x, logo_y, logo_width, logo_height, mask='auto')
    else:
        # إذا ما لقى الصورة، يرسم مربع أزرق مكانها مؤقتًا
        c.setFillColor(KSU_BLUE)
        c.rect(logo_x, logo_y, logo_width, logo_height, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(logo_x + logo_width/2, logo_y + logo_height/2, "LOGO")

def add_ksu_certificate_text(c, cert, width, height):
    """
    إضافة النصوص للشهادة بتصميم جامعة الملك سعود
    """
    reshaper = ArabicReshaper({
        'delete_harakat': False,
        'support_ligatures': True
    })

    # عنوان "شهادة تقدير"
    c.setFillColor(KSU_BLUE)
    c.setFont("Amiri-Regular", 48)
    title = get_display(reshaper.reshape("شهادة تقدير"))
    title_width = c.stringWidth(title, "Amiri-Regular", 48)
    c.drawString((width - title_width) / 2, height - 150, title)
    
    # خط تحت العنوان
    c.setStrokeColor(KSU_LIGHT_BLUE)
    c.setLineWidth(3)
    line_start = (width - title_width) / 2
    line_end = line_start + title_width
    c.line(line_start, height - 165, line_end, height - 165)
    
    # نص "لقد أتم الدورة بنجاح"
    c.setFillColor(GRAY_TEXT)
    c.setFont("Amiri-Regular", 20)
    completion_text = get_display(reshaper.reshape("لقد أتم الدورة بنجاح"))
    completion_width = c.stringWidth(completion_text, "Amiri-Regular", 20)
    c.drawString((width - completion_width) / 2, height - 220, completion_text)
    
    # اسم الموظف
    c.setFillColor(KSU_BLUE)
    c.setFont("Amiri-Regular", 36)
    name = get_display(reshaper.reshape(cert.employee_name))
    name_width = c.stringWidth(name, "Amiri-Regular", 36)
    c.drawString((width - name_width) / 2, height - 280, name)
    
    # نص "يبارك التدريب الإلكتروني لـ"
    c.setFillColor(GRAY_TEXT)
    c.setFont("Amiri-Regular", 18)
    training_text = get_display(reshaper.reshape("يبارك التدريب الإلكتروني لـ"))
    training_width = c.stringWidth(training_text, "Amiri-Regular", 18)
    c.drawString((width - training_width) / 2, height - 320, training_text)
    
    # عنوان الدورة
    c.setFillColor(KSU_BLUE)
    c.setFont("Amiri-Regular", 28)
    course_lines = textwrap.wrap(cert.course_title, width=40)
    y_position = height - 370
    
    for line in course_lines:
        reshaped_line = get_display(reshaper.reshape(line))
        line_width = c.stringWidth(reshaped_line, "Amiri-Regular", 28)
        c.drawString((width - line_width) / 2, y_position, reshaped_line)
        y_position -= 35
    
    # النص الطويل (وصف الإنجاز)
    c.setFillColor(GRAY_TEXT)
    c.setFont("Amiri-Regular", 14)
    
    description_lines = [
        "في ضوء الإنجازات الكبيرة التي حققتها خلال فترة عملكم معنا، والنجاحات المتتالية التي",
        "أحرزتها في مسيرتك العملية نتقدم لكم اليوم بجزيل الشكر على جهدك."
    ]
    
    y_pos = height - 450
    for line in description_lines:
        reshaped_line = get_display(reshaper.reshape(line))
        line_width = c.stringWidth(reshaped_line, "Amiri-Regular", 14)
        c.drawString((width - line_width) / 2, y_pos, reshaped_line)
        y_pos -= 25
    
    # نص التهنئة
    c.setFillColor(GRAY_TEXT)
    c.setFont("Amiri-Regular", 16)
    congratulations = get_display(reshaper.reshape("سائلين الله لك دوام التفوق والنجاح والإبداع الدائم"))
    congrat_width = c.stringWidth(congratulations, "Amiri-Regular", 16)
    c.drawString((width - congrat_width) / 2, height - 520, congratulations)
    
    # التاريخ
    c.setFillColor(GRAY_TEXT)
    c.setFont("Amiri-Regular", 14)
    date_text = cert.issue_date.strftime("%d-%m-%Y")
    date_width = c.stringWidth(date_text, "Amiri-Regular", 14)
    c.drawString(100, 100, date_text)
    
    # التوقيع
    c.setFillColor(KSU_BLUE)
    c.setFont("Amiri-Regular", 18)
    signature_text = get_display(reshaper.reshape("التوقيع"))
    signature_width = c.stringWidth(signature_text, "Amiri-Regular", 18)
    c.drawString(width - signature_width - 100, 100, signature_text)

def create_certificate_template():
    """
    إنشاء قالب شهادة افتراضي
    """
    # يمكن استخدام هذه الوظيفة لإنشاء قوالب مخصصة
    pass



