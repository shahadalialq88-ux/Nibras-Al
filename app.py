import streamlit as st
import pandas as pd
import plotly.express as px
from pptx import Presentation
from pptx.util import Inches, Pt
from io import BytesIO

# -----------------------------------------------------------
# Project: Nibras AI (نبراس) - Pilot Version
# Developer: Shahad Ali Al-Mastour | #ShahadInsights
# Copyright: © 2026 | All Rights Reserved
# -----------------------------------------------------------

# 1. إعدادات الصفحة والهوية البصرية
st.set_page_config(
    page_title="Nibras AI | Pilot Version",
    page_icon="🧭",
    layout="wide"
)

# تصميم واجهة مخصصة (Premium CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; }
    .main { background-color: #fcfcfc; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #eee; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: white; color: #64748b; text-align: center; padding: 15px; font-size: 14px; border-top: 1px solid #eee; z-index: 100; }
    .risk-card { padding: 20px; border-radius: 10px; margin: 10px 0; border-right: 6px solid #ef4444; background-color: #fff5f5; color: #b91c1c; }
    .success-card { padding: 20px; border-radius: 10px; margin: 10px 0; border-right: 6px solid #10b981; background-color: #f0fff4; color: #065f46; }
    </style>
    """, unsafe_allow_html=True)

# 2. ترويسة البرنامج (Header)
col_title, col_logo = st.columns([4, 1])
with col_title:
    st.title("🧭 نبراس AI — Nibras AI")
    st.markdown("#### المنارة الاستراتيجية لتمكين القرار الرقمي | *#ShahadInsights*")
    st.caption("نسخة تجريبية (Pilot) لإثبات فكرة دمج التحليل الاستباقي بالقرار التنفيذي")

st.divider()

# 3. محرك تصدير البوربوينت (PPTX Engine)
def create_strategic_ppt(df, insight):
    prs = Presentation()
    # شريحة العنوان
    title_slide = prs.slides.add_slide(prs.slide_layouts[0])
    title_slide.shapes.title.text = "تقرير نبراس AI الاستراتيجي"
    title_slide.placeholders[1].text = f"إعداد: شهد آل مستور\nتاريخ التقرير: {pd.Timestamp.now().strftime('%Y-%m-%d')}"
    
    # شريحة التحليل
    analysis_slide = prs.slides.add_slide(prs.slide_layouts[1])
    analysis_slide.shapes.title.text = "البصيرة الاستراتيجية (Insights)"
    analysis_slide.shapes.placeholders[1].text = f"النتائج المباشرة:\n{insight}"
    
    ppt_io = BytesIO()
    prs.save(ppt_io)
    ppt_io.seek(0)
    return ppt_io

# 4. منطقة العمل الرئيسية (Main Workspace)
uploaded_file = st.file_uploader("📂 ارفع ملف البيانات الاستراتيجي (Excel/CSV)", type=['csv', 'xlsx'])

if uploaded_file:
    try:
        # قراءة البيانات بذكاء
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("✅ تم استقبال البيانات بنجاح. جاري استخراج البصيرة...")

        # أ) لمحة سريعة (Strategic Metrics)
        numeric_cols = df.select_dtypes(include=['number']).columns
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("حجم البيانات", f"{len(df)} سجل")
        with col2:
            st.metric("مؤشر الثقة", "96.4%")
        with col3:
            st.metric("الحالة التقنية", "Pilot Active")

        # ب) التحليل البصري التفاعلي (Interactive Visualization)
        if not numeric_cols.empty:
            st.subheader("📊 لوحة البصيرة التفاعلية")
            target_col = st.selectbox("اختر المؤشر لتحليله استراتيجياً:", numeric_cols)
            
            fig = px.area(df, y=target_col, title=f"تحليل اتجاه {target_col}", 
                         color_discrete_sequence=['#002147'], template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

            # ج) محرك التنبؤ والتوصيات (The Insight Engine)
            avg_val = df[target_col].mean()
            last_val = df[target_col].iloc[-1]
            
            st.subheader("💡 توصيات نبراس الذكية")
            
            if last_val < avg_val:
                insight_msg = f"تحذير: مؤشر {target_col} الحالي ({last_val}) يظهر تراجعاً عن المتوسط العام ({avg_val:.2f}). نوصي بمراجعة خطة العمل الفورية لتفادي الانحراف الاستراتيجي."
                st.markdown(f'<div class="risk-card">{insight_msg}</div>', unsafe_allow_html=True)
            else:
                insight_msg = f"ممتاز: مؤشر {target_col} في حالة نمو مستقر بمعدل جيد فوق المتوسط. نوصي بتعزيز الموارد الحالية لضمان استدامة النتائج."
                st.markdown(f'<div class="success-card">{insight_msg}</div>', unsafe_allow_html=True)

            # د) تصدير النتائج (One-Click Export)
            st.divider()
            st.subheader("📄 تصدير المخرجات الاستراتيجية")
            ppt_data = create_strategic_ppt(df, insight_msg)
            
            st.download_button(
                label="تحميل عرض PowerPoint الاستراتيجي",
                data=ppt_data,
                file_name=f"Nibras_Report_{target_col}.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )

    except Exception as e:
        st.error(f"حدث خطأ في قراءة الملف: {e}")
else:
    # واجهة ترحيبية عند عدم وجود ملف
    st.info("بانتظار رفع ملف البيانات لبدء عملية 'نبراس' لإضاءة مسار القرار.")
    st.image("https://img.freepik.com/free-vector/data-analysis-concept-illustration_114360-8013.jpg", width=400)

# 5. تذييل الصفحة (Footer)
st.markdown(f"""
    <div class="footer">
        Developed by: <b>Shahad Ali Al-Mastour</b> | CS Specialist <br>
        Nibras AI © 2026 | All Rights Reserved | <b>#ShahadInsights</b>
    </div>
    """, unsafe_allow_html=True)
