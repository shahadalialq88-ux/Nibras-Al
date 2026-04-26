import streamlit as st
import pandas as pd
import plotly.express as px
from pptx import Presentation
from io import BytesIO
import datetime

# ==========================================
# 1. إعدادات المنصة والهوية البصرية
# ==========================================
st.set_page_config(page_title="NIBRAS AI | نبراس", layout="wide")

# تصميم واجهة مستخدم نظيفة وفخمة (Luxury Minimalist)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    * { font-family: 'Cairo', sans-serif; }
    .stApp { background-color: #fcfcfc; }
    .main-header { 
        color: #1a1a1a; 
        text-align: right; 
        border-right: 8px solid #D4AF37; 
        padding-right: 20px; 
        margin-bottom: 30px;
    }
    .metric-card { 
        background: white; 
        padding: 25px; 
        border-radius: 15px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); 
        border-bottom: 4px solid #D4AF37;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. وظائف معالجة المخرجات (PPTX Engine)
# ==========================================
def create_executive_ppt(target_name, growth_rate, average_val):
    """توليد عرض بوربوينت احترافي يدعم العربية"""
    prs = Presentation()
    
    # شريحة الغلاف
    slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    title.text = "نبراس AI - تقرير الأداء الاستراتيجي"
    
    subtitle = slide.placeholders[1]
    subtitle.text = f"إعداد: شهد آل مستور\nتاريخ التحليل: {datetime.date.today()}\nنظام ذكاء القرار المعتمد"

    # شريحة البيانات الأساسية
    slide_layout_2 = prs.slides.add_slide(prs.slide_layouts[1])
    slide_layout_2.shapes.title.text = "النتائج التحليلية الرئيسية"
    body_shape = slide_layout_2.shapes.placeholders[1]
    tf = body_shape.text_frame
    tf.text = f"• المؤشر المحلل: {target_name}"
    p = tf.add_paragraph()
    p.text = f"• معدل النمو المحقق: {growth_rate:.2f}%"
    p2 = tf.add_paragraph()
    p2.text = f"• متوسط كفاءة الأداء: {average_val:,.0f}"

    ppt_io = BytesIO()
    prs.save(ppt_io)
    ppt_io.seek(0)
    return ppt_io

# ==========================================
# 3. الهيكل التشغيلي للمنصة
# ==========================================
st.markdown("<h1 class='main-header'>💎 نـبـراس | NIBRAS AI<br><small style='font-size:0.5em; color:#666;'>منصة ذكاء القرار الاستراتيجي</small></h1>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📂 ارفعي ملف البيانات للبدء (Excel / CSV)", type=['xlsx', 'csv'])

if uploaded_file:
    try:
        # معالجة الملف
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
        
        target_column = df.columns[1] # افترضنا العمود الثاني هو الهدف
        
        # محرك الحسابات الذكي
        avg_performance = df[target_column].mean()
        latest_value = df[target_column].iloc[-1]
        initial_value = df[target_column].iloc[0]
        growth_percentage = ((latest_value - initial_value) / initial_value) * 100
        
        # عرض بطاقات الأداء (Metrics Cards)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div class='metric-card'><h6>متوسط الأداء</h6><h2 style='color:#D4AF37;'>{avg_performance:,.0f}</h2></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-card'><h6>صافي النمو</h6><h2 style='color:#D4AF37;'>{growth_percentage:.1f}%</h2></div>", unsafe_allow_html=True)
        with col3:
            status = "إيجابي" if growth_percentage > 0 else "تراجع"
            color = "#2ecc71" if growth_percentage > 0 else "#e74c3c"
            st.markdown(f"<div class='metric-card'><h6>حالة المؤشر</h6><h2 style='color:{color};'>{status}</h2></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # الرسم البياني التفاعلي
        st.subheader(f"📈 تحليل المسار الزمني لـ {target_column}")
        fig = px.area(df, x=df.columns[0], y=target_column, line_shape="spline", color_discrete_sequence=['#D4AF37'])
        fig.update_layout(font_family="Cairo", paper_bgcolor='white', plot_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)

        # مخرجات الاعتماد
        st.divider()
        st.subheader("📦 مخرجات لجنة الاعتماد")
        col_btn, col_info = st.columns([1, 2])
        
        with col_btn:
            ppt_output = create_executive_ppt(target_column, growth_percentage, avg_performance)
            st.download_button(
                label="📥 تحميل عرض البوربوينت الرسمي",
                data=ppt_output,
                file_name="Nibras_Executive_Report.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
        
        with col_info:
            st.info("تم تجهيز العرض التقديمي ليحتوي على كافة الإحصائيات مع ضمان ظهور حقوق الملكية (شهد آل مستور).")

    except Exception as e:
        st.error(f"حدث خطأ أثناء معالجة الملف. يرجى التأكد من تنسيق البيانات. الرمز: {e}")

else:
    st.info("نبراس AI بانتظار البيانات لتحويلها إلى رؤى استراتيجية.")
    st.image("https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=2426&auto=format&fit=crop", use_column_width=True)

# الحاشية السيادية
st.markdown(f"""
    <div style="text-align: center; margin-top: 80px; padding: 20px; border-top: 1px solid #eee; color: #888;">
        <p><b>Developed by: Shahad Ali Al-Mastour</b> | CS Specialist</p>
        <p>© 2026 NIBRAS AI | الإصدار المعتمد 1.0</p>
    </div>
    """, unsafe_allow_html=True)
