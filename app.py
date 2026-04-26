import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from io import BytesIO

# 1. إعدادات المنصة الاحترافية (Executive Theme)
st.set_page_config(page_title="NIBRAS Strategic Intelligence", layout="wide", page_icon="⚖️")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans Arabic', sans-serif; background-color: #f4f7f9; }
    
    /* تصميم بطاقات القيادة */
    .executive-card { background: white; padding: 30px; border-radius: 20px; border-top: 5px solid #b8860b; box-shadow: 0 15px 35px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .stButton>button { background: linear-gradient(135deg, #1a1c20 0%, #434343 100%); color: #d4af37; border: none; padding: 15px; border-radius: 12px; font-weight: bold; width: 100%; transition: 0.4s; }
    .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 8px 15px rgba(0,0,0,0.2); color: white; }
    
    /* صناديق التحليل الاستراتيجي */
    .swot-box { padding: 15px; border-radius: 10px; margin-bottom: 10px; border-right: 5px solid; }
    .strength { background: #f0fff4; border-color: #22c55e; color: #166534; }
    .risk { background: #fff5f5; border-color: #ef4444; color: #991b1b; }
    </style>
    """, unsafe_allow_html=True)

# 2. محرك إنشاء العروض التنفيذية (The Professional PPTX Engine)
def create_executive_deck(df, analysis_results):
    prs = Presentation()
    
    # وظيفة لتنسيق خلفية الشريحة
    def apply_pro_style(slide, title_text):
        title_shape = slide.shapes.title
        title_shape.text = title_text
        title_shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(26, 28, 32)
        title_shape.text_frame.paragraphs[0].font.bold = True

    # الشريحة 1: الغلاف الاستراتيجي
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "نبراس AI: تقرير ذكاء القرار"
    slide.placeholders[1].text = f"إعداد المحلل الآلي الذكي لنظام نبراس\nالتاريخ: {pd.Timestamp.now().strftime('%Y-%m-%d')}"

    # الشريحة 2: ملخص التنفيذ (Executive Summary)
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    apply_pro_style(slide, "الملخص التنفيذي والاستنتاجات")
    tf = slide.shapes.placeholders[1].text_frame
    tf.text = analysis_results

    # الشريحة 3: التحليل الرقمي المقارن
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    apply_pro_style(slide, "مؤشرات الأداء الرئيسية (KPIs)")
    # (يمكن هنا إضافة جداول أو صور شارتات في النسخة المتقدمة)

    ppt_io = BytesIO()
    prs.save(ppt_io)
    ppt_io.seek(0)
    return ppt_io

# 3. واجهة التحكم (The Mission Control)
st.title("⚖️ منصة نبراس للذكاء الاستراتيجي")
st.caption("نظام مستقل لتحليل البيانات واتخاذ القرار - إصدار الاحتراف التنفيذي")

uploaded_file = st.file_uploader("📂 اسحب ملف البيانات لتحليله فوراً", type=['xlsx', 'csv'])

if uploaded_file:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
    target = df.columns[1] # افترضنا العمود الثاني هو الهدف
    avg_val = df[target].mean()
    last_val = df[target].iloc[-1]
    
    # منطقة التحليل الاستراتيجي
    col_data, col_analysis = st.columns([2, 1])

    with col_data:
        st.markdown('<div class="executive-card">', unsafe_allow_html=True)
        st.subheader(f"📊 تحليل اتجاه {target}")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.iloc[:,0], y=df[target], mode='lines+markers', line=dict(color='#b8860b', width=4), fill='tozeroy', fillcolor='rgba(184, 134, 11, 0.1)'))
        fig.update_layout(plot_bgcolor='white', margin=dict(l=0,r=0,t=20,b=0), height=400)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_analysis:
        st.subheader("💡 المختبر الاستراتيجي")
        
        # تحليل SWOT آلي
        if last_val > avg_val:
            st.markdown('<div class="swot-box strength"><b>نقطة قوة:</b> الأداء الحالي يتجاوز المتوسط بنسبة ' + f"{((last_val-avg_val)/avg_val*100):.1f}%" + '. استمر في الزخم الحالي.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="swot-box risk"><b>مخاطر محتملة:</b> تراجع في المؤشر يستوجب تدخل "فريق العمليات" لتصحيح المسار.</div>', unsafe_allow_html=True)

        # التوصية الآلية
        st.info(f"*توصية نبراس:* بناءً على البيانات، ننصح بزيادة الاستثمار في قطاع {target} خلال الدورة القادمة لضمان الريادة.")

    st.divider()
    
    # التصدير للاعتماد
    st.subheader("📜 المخرجات الجاهزة للاعتماد")
    analysis_summary = f"تم رصد أداء مستقر لـ {target}. المتوسط العام هو {avg_val:,.2f}. القيمة الأخيرة المحققة هي {last_val:,.2f}."
    ppt_file = create_executive_deck(df, analysis_summary)
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        st.download_button("📂 تحميل التقرير الاستراتيجي (PPTX)", data=ppt_file, file_name="Nibras_Executive_Report.pptx")
    with col_btn2:
        st.button("📧 إرسال للجنة الاعتماد (محاكاة)")

else:
    st.markdown('<div style="text-align:center; padding:100px; color:#666"><h3>بانتظار تزويد النظام بالبيانات الاستراتيجية...</h3></div>', unsafe_allow_html=True)
