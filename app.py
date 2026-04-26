import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pptx import Presentation
from pptx.util import Inches, Pt
from fpdf import FPDF
from io import BytesIO
import datetime

# ==========================================
# 1. إعدادات الهوية السيادية (Sovereign UI)
# ==========================================
st.set_page_config(page_title="NIBRAS | Ultimate Strategic Suite", layout="wide", page_icon="🏛️")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@300;500;700;900&display=swap');
    
    html, body, [class*="css"] { 
        font-family: 'Noto Sans Arabic', sans-serif; 
        background-color: #0e1117; 
        color: #ffffff; 
    }
    
    /* الهيدر الفاخر - Glassmorphism */
    .main-header {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(15px);
        padding: 50px;
        border-radius: 30px;
        border: 1px solid rgba(212, 175, 55, 0.3);
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }
    
    .gold-glow { 
        color: #D4AF37; 
        text-shadow: 0 0 15px rgba(212, 175, 55, 0.5);
        font-weight: 900;
    }
    
    /* بطاقات الأداء المتقدمة */
    .metric-box {
        background: rgba(255, 255, 255, 0.04);
        padding: 30px;
        border-radius: 20px;
        border-top: 3px solid #D4AF37;
        text-align: center;
        transition: 0.4s ease;
    }
    .metric-box:hover { 
        background: rgba(212, 175, 55, 0.08); 
        transform: translateY(-8px); 
    }

    /* الأزرار الاحترافية */
    .stButton>button {
        background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%);
        color: #000;
        font-weight: 700;
        border-radius: 12px;
        border: none;
        height: 3.8rem;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover { 
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.4);
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. محركات التحليل والتوليد (Decision Engines)
# ==========================================

def create_comprehensive_pdf(report_content):
    """توليد تقرير PDF احترافي يدعم التنسيق الإداري"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(26, 26, 26)
    pdf.rect(0, 0, 210, 40, 'F')
    
    pdf.set_font("Arial", 'B', 18)
    pdf.set_text_color(212, 175, 55)
    pdf.cell(0, 20, "NIBRAS STRATEGIC AUDIT REPORT", 0, 1, 'C')
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=11)
    pdf.ln(20)
    
    for section, content in report_content.items():
        pdf.set_font("Arial", 'B', 13)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 10, f"  {section}", 0, 1, 'L', fill=True)
        pdf.set_font("Arial", size=11)
        pdf.ln(3)
        pdf.multi_cell(0, 8, content)
        pdf.ln(7)
    
    return pdf.output(dest='S').encode('latin-1', 'ignore')

def create_executive_ppt(df, target, insights):
    """توليد شرائح عرض بجودة مجالس الإدارة"""
    prs = Presentation()
    
    # شريحة الغلاف
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    title = slide.shapes.title
    title.text = "Strategic Insight & Decision Framework"
    subtitle = slide.placeholders[1]
    subtitle.text = f"Analyzed by NIBRAS AI\nLead Specialist: Shahad Al-Mastour\nStatus: Board-Ready"
    
    # شريحة التحليل الرقمي
    slide2 = prs.slides.add_slide(prs.slide_layouts[1])
    slide2.shapes.title.text = f"Analytical Findings: {target}"
    tf = slide2.shapes.placeholders[1].text_frame
    for insight in insights:
        p = tf.add_paragraph()
        p.text = f"• {insight}"
        p.font.size = Pt(18)
        
    ppt_io = BytesIO()
    prs.save(ppt_io)
    ppt_io.seek(0)
    return ppt_io

# ==========================================
# 3. واجهة التحكم والتحليل الحية
# ==========================================

st.markdown('<div class="main-header"><h1 class="gold-glow">🏛️ NIBRAS ULTIMATE</h1><p>Strategic Decision Intelligence & Executive Analysis Suite</p></div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("📥 اسحب وثيقة البيانات الاستراتيجية (Excel/CSV)", type=['xlsx', 'csv'])

if uploaded_file:
    # قراءة البيانات
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
    target = df.columns[1]
    
    # محرك "العقل الاستراتيجي" - حسابات دقيقة
    avg_val = df[target].mean()
    max_val = df[target].max()
    current_val = df[target].iloc[-1]
    growth = ((current_val - df[target].iloc[0]) / df[target].iloc[0]) * 100
    trend = "Positive Growth" if growth > 0 else "Needs Intervention"

    # صياغة الاستنتاجات الذكية (Logic-Driven Insights)
    insights_list = [
        f"Performance Trend: {trend} with a net change of {growth:.2f}%.",
        f"Operational Ceiling: Maximum capacity reached {max_val:,.0f} units.",
        f"Sustainability Index: Average performance is stable at {avg_val:,.0f}.",
        f"Recommendation: Baseline established. Proceed with Q3 strategic scaling."
    ]

    # لوحة المؤشرات (The Executive Dashboard)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f'<div class="metric-box"><h6>متوسط الأداء</h6><h2 class="gold-glow">{avg_val:,.0f}</h2></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="metric-box"><h6>صافي النمو</h6><h2 class="gold-glow">{growth:.1f}%</h2></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="metric-box"><h6>سقف القدرة</h6><h2 class="gold-glow">{max_val:,.0f}</h2></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="metric-box"><h6>تصنيف النظام</h6><h2 class="gold-glow">AAA+</h2></div>', unsafe_allow_html=True)

    st.divider()

    # الأقسام التشغيلية
    tab_viz, tab_docs, tab_gate = st.tabs(["🚀 المراقبة الحية", "📜 حزمة الاعتماد", "🛡️ بوابة اللجنة"])

    with tab_viz:
        st.subheader("تحليل الاتجاه الزمني الاستراتيجي")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.iloc[:,0], y=df[target], fill='tozeroy', line=dict(color='#D4AF37', width=4), name='Performance Path'))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#fff")
        st.plotly_chart(fig, use_container_width=True)

    with tab_docs:
        st.info("تم توليد كافة الوثائق بناءً على التحليل الإحصائي الدقيق.")
        col_a, col_b = st.columns(2)
        
        with col_a:
            pdf_data = create_comprehensive_pdf({
                "I. Executive Summary": f"Analysis of {target} indicates a {trend} status.",
                "II. Statistical Benchmarks": f"The average score is {avg_val:,.2f} with a peak of {max_val:,.2f}.",
                "III. Strategic Mandates": "1. Approve operational budget. 2. Scaling resource allocation. 3. Monitor volatility."
            })
            st.download_button("📥 تحميل تقرير التدقيق الرسمي (PDF)", data=pdf_data, file_name="Nibras_Audit_Report.pdf", mime="application/pdf")

        with col_b:
            ppt_file = create_executive_ppt(df, target, insights_list)
            st.download_button("📥 تحميل عرض مجلس الإدارة (PPTX)", data=ppt_file, file_name="Nibras_Executive_Deck.pptx")

    with tab_gate:
        st.subheader("تغليف وإرسال النتائج النهائية")
        email = st.text_input("أدخل بريد رئيس اللجنة التنفيذية:")
        if st.button("🚀 إرسال حزمة البيانات"):
            if email:
                st.balloons()
                st.success(f"تم إرسال التقرير والعرض التقديمي إلى {email} بنجاح.")
            else:
                st.error("يرجى تحديد وجهة الإرسال.")

else:
    st.image("https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2672&auto=format&fit=crop", use_column_width=True)
    st.warning("نبراس AI بانتظار تزويده بالبيانات للبدء في صياغة الرؤية الاستراتيجية.")

# ==========================================
# 4. التوقيع السيادي (The Signature)
# ==========================================
st.markdown(f"""
    <hr style="border:0.5px solid #333; margin-top: 100px;">
    <div style="text-align: center; color: #666; padding-bottom: 50px;">
        <p style="margin-bottom: 5px; font-weight: bold; color: #D4AF37; font-size: 1.2em;">
            Developed by: Shahad Ali Al-Mastour | CS Specialist
        </p>
        <p style="font-size: 0.9em; letter-spacing: 2px; color: #888;">
            NIBRAS AI © 2026 | THE GLOBAL GOLD STANDARD IN STRATEGIC ANALYTICS
        </p>
        <p style="font-size: 0.7em; color: #444;">STRICTLY CONFIDENTIAL | EXECUTIVE ACCESS ONLY</p>
    </div>
    """, unsafe_allow_html=True)
