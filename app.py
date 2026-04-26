import streamlit as st
import pandas as pd
import plotly.express as px
from pptx import Presentation
from io import BytesIO
import datetime

# ==========================================
# 1. UI & Branding (الطبقة البصرية)
# ==========================================
st.set_page_config(page_title="NIBRAS AI | نبراس", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    * { font-family: 'Cairo', sans-serif; text-align: right; }
    .stApp { background-color: #f8faff; }
    .main-card { background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); border-right: 10px solid #D4AF37; margin-bottom: 20px; }
    .insight-card { background: #fff; border-right: 5px solid #2ecc71; padding: 15px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    .recommendation-card { background: #fff; border-right: 5px solid #3498db; padding: 15px; margin: 10px 0; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. Intelligence Engines (العقول المشغلة)
# ==========================================

def insight_engine(df, target):
    """محرك استخراج النتائج الذكي بناءً على القواعد"""
    avg = df[target].mean()
    current = df[target].iloc[-1]
    growth = ((current - df[target].iloc[0]) / df[target].iloc[0]) * 100
    peak = df[target].max()
    
    insights = []
    # قاعدة النمو
    if growth > 10:
        insights.append(f"ارتفاع ملحوظ: حقق المؤشر نمواً قوياً بنسبة {growth:.1f}%، مما يتجاوز الأهداف الربعية.")
    elif growth < -10:
        insights.append(f"تنبيه فجوة: انخفض الأداء بنسبة {abs(growth):.1f}%، يتطلب الأمر مراجعة فورية للمسببات.")
    else:
        insights.append(f"استقرار نسبي: الأداء ضمن النطاق الطبيعي بنسبة تغير {growth:.1f}%.")
    
    # قاعدة الكفاءة
    if current > avg:
        insights.append(f"كفاءة تشغيلية: القيمة الحالية ({current:,.0f}) أعلى من المتوسط العام، مما يشير لزخم إيجابي.")
        
    return insights, growth, avg, peak

def recommendation_engine(growth):
    """محرك اقتراح القرارات"""
    if growth > 10:
        return ["توسيع الاستثمار في القنوات الحالية", "نقل التجربة الناجحة للأقسام الأخرى", "رفع سقف الأهداف السنوية"]
    elif growth < -10:
        return ["إيقاف مؤقت للإنفاق غير الضروري", "إجراء فحص تدقيق (Deep Dive) للعمليات", "تعديل الاستراتيجية التشغيلية فوراً"]
    return ["الحفاظ على الوتيرة الحالية", "تحسين كفاءة الموارد المتاحة", "مراقبة الأداء بشكل أسبوعي"]

# ==========================================
# 3. Output Engine (نظام الإخراج)
# ==========================================

def create_pro_presentation(target, insights, recs):
    prs = Presentation()
    # شريحة الغلاف
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "NIBRAS AI | تقرير ذكاء القرار"
    slide.placeholders[1].text = f"إعداد المتخصصة: شهد آل مستور\nتاريخ التحليل: {datetime.date.today()}"
    
    # شريحة النتائج
    slide2 = prs.slides.add_slide(prs.slide_layouts[1])
    slide2.shapes.title.text = "أهم النتائج (Key Insights)"
    tf = slide2.shapes.placeholders[1].text_frame
    for ins in insights:
        p = tf.add_paragraph()
        p.text = f"• {ins}"
        
    ppt_io = BytesIO()
    prs.save(ppt_io)
    ppt_io.seek(0)
    return ppt_io

# ==========================================
# 4. User Experience (رحلة المستخدم)
# ==========================================

st.markdown("<div class='main-card'><h1>💎 نبراس AI | Nebras AI</h1><p>نظام تحليل البيانات وصناعة التقارير التنفيذية</p></div>", unsafe_allow_html=True)

# خطوة الإدخال (Input Layer)
with st.sidebar:
    st.header("⚙️ إعدادات التحليل")
    uploaded_file = st.file_uploader("ارفع ملف Excel/CSV", type=['xlsx', 'csv'])
    audience = st.selectbox("الجمهور المستهدف", ["مجلس الإدارة (CEO)", "مدراء الأقسام", "الفريق التقني"])
    report_type = st.radio("نوع التقرير", ["تنفيذي (Executive)", "تفصيلي (Detailed)"])

if uploaded_file:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
    target_col = df.columns[1]
    
    # مرحلة المعالجة (Processing Logic)
    insights, growth, avg, peak = insight_engine(df, target_col)
    recommendations = recommendation_engine(growth)
    
    # عرض النتائج (Results View)
    tab1, tab2, tab3 = st.tabs(["💡 الاستنتاجات", "📊 التحليل البصري", "📦 التصدير"])
    
    with tab1:
        st.subheader("💡 النتائج المستخلصة (Insights)")
        for ins in insights:
            st.markdown(f"<div class='insight-card'>{ins}</div>", unsafe_allow_html=True)
            
        st.subheader("🚀 توصيات القرار (Recommendations)")
        for rec in recommendations:
            st.markdown(f"<div class='recommendation-card'>• {rec}</div>", unsafe_allow_html=True)

    with tab2:
        fig = px.area(df, x=df.columns[0], y=target_col, title=f"تحليل الاتجاه لـ {target_col}", color_discrete_sequence=['#D4AF37'])
        fig.update_layout(font_family="Cairo", paper_bgcolor='white', plot_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("توليد الوثائق النهائية")
        ppt_data = create_pro_presentation(target_col, insights, recommendations)
        st.download_button(
            label="📥 تحميل عرض البوربوينت التنفيذي",
            data=ppt_data,
            file_name=f"Nibras_Report_{datetime.date.today()}.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
        st.success(f"تم تخصيص التقرير لجمهور: {audience}")

else:
    st.info("نظام نبراس بانتظار رفع البيانات للبدء في 'فهمها وتفسيرها'.")

# التوقيع
st.markdown(f"""
    <div style="text-align: center; margin-top: 50px; color: #888; border-top: 1px solid #eee; padding-top: 20px;">
        Developed by: <b>Shahad Ali Al-Mastour</b> | CS Specialist <br>
        <b>Nebras AI v1.0</b>
    </div>
    """, unsafe_allow_html=True)
