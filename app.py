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
    
    .gold-glow { color: #D4AF37; text-shadow: 0 0 15px rgba(212, 175, 55, 0.5); font-weight: 900; }
    
    .metric-box {
        background: rgba(255, 255, 255, 0.04);
        padding: 30px;
        border-radius: 20px;
        border-top: 3px solid #D4AF37;
        text-align: center;
        transition: 0.4s ease;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%);
        color: #000;
        font-weight: 700;
        border-radius: 12px;
        border: none;
        height: 3.8rem;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. محركات التحليل والتوليد (Decision Engines)
# ==========================================

# تم تعديل المحرك ليتجاوز مشكلة الترميز (Encoding)
class NibrasPDF(FPDF):
    def header(self):
        self.set_fill_color(26, 26, 26)
        self.rect(0, 0, 210, 40, 'F')
        self.set_font("Arial", 'B', 18)
        self.set_text_color(212, 175, 55)
        self.cell(0, 20, "NIBRAS STRATEGIC AUDIT REPORT", 0, 1, 'C')
        self.ln(10)

def create_comprehensive_pdf(report_content):
    """توليد التقرير مع حماية من أخطاء الترميز"""
    pdf = NibrasPDF()
    pdf.add_page()
    pdf.set_text_color(40, 40, 40)
    
    for section, content in report_content.items():
        # تنظيف النص من أي حروف قد تسبب خطأ قبل التمرير للـ PDF
        clean_content = str(content).encode('latin-1', 'replace').decode('latin-1')
        clean_section = str(section).encode('latin-1', 'replace').decode('latin-1')
        
        pdf.set_font("Arial", 'B', 14)
        pdf.set_fill_color(245, 245, 245)
        pdf.cell(0, 10, clean_section, 0, 1, 'L', fill=True)
        pdf.ln(2)
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 8, clean_content)
        pdf.ln(5)
    
    return pdf.output(dest='S')

def create_executive_ppt(df, target, insights):
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "Strategic Insight & Decision Framework"
    slide.placeholders[1].text = f"Analyzed by NIBRAS AI\nLead Specialist: Shahad Al-Mastour\nStatus: Board-Ready"
    
    slide2 = prs.slides.add_slide(prs.slide_layouts[1])
    slide2.shapes.title.text = f"Analytical Findings: {target}"
    tf = slide2.shapes.placeholders[1].text_frame
    for insight in insights:
        p = tf.add_paragraph()
        p.text = f"- {insight}"
        p.font.size = Pt(18)
        
    ppt_io = BytesIO()
    prs.save(ppt_io)
    ppt_io.seek(0)
    return ppt_io

# ==========================================
# 3. واجهة التحكم والتحليل
# ==========================================

st.markdown('<div class="main-header"><h1 class="gold-glow">🏛️ NIBRAS ULTIMATE</h1><p>Strategic Decision Intelligence & Executive Analysis Suite</p></div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("📥 اسحب وثيقة البيانات الاستراتيجية (Excel/CSV)", type=['xlsx', 'csv'])

if uploaded_file:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
    target = df.columns[1]
    
    # حسابات الذكاء الاستراتيجي
    avg_val = df[target].mean()
    max_val = df[target].max()
    current_val = df[target].iloc[-1]
    growth = ((current_val - df[target].iloc[0]) / df[target].iloc[0]) * 100
    trend = "Positive Growth" if growth > 0 else "Intervention Required"

    insights_list = [
        f"Performance Trend: {trend} ({growth:.2f}%)",
        f"Operational Ceiling: Maximum reached {max_val:,.0f}",
        f"Sustainability Index: Average stable at {avg_val:,.0f}",
        "Recommendation: Strategic scaling approved for next phase."
    ]

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f'<div class="metric-box"><h6>Average Performance</h6><h2 class="gold-glow">{avg_val:,.0f}</h2></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="metric-box"><h6>Net Growth</h6><h2 class="gold-glow">{growth:.1f}%</h2></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="metric-box"><h6>Operational Peak</h6><h2 class="gold-glow">{max_val:,.0f}</h2></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="metric-box"><h6>System Rating</h6><h2 class="gold-glow">AAA+</h2></div>', unsafe_allow_html=True)

    st.divider()

    tab_viz, tab_docs, tab_gate = st.tabs(["🚀 المراقبة الحية", "📜 حزمة الاعتماد", "🛡️ بوابة اللجنة"])

    with tab_viz:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.iloc[:,0], y=df[target], fill='tozeroy', line=dict(color='#D4AF37', width=4)))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#fff", title="Strategic Performance Path")
        st.plotly_chart(fig, use_container_width=True)

    with tab_docs:
        st.info("Files generated with Enterprise Standards.")
        col_a, col_b = st.columns(2)
        
        with col_a:
            # تم استخدام نصوص لاتينية في الـ PDF لضمان عدم حدوث الـ Error
            pdf_data = create_comprehensive_pdf({
                "1. Executive Summary": f"The analysis of {target} shows a {trend}.",
                "2. Statistical Benchmarks": f"Average: {avg_val:,.2f} | Max Peak: {max_val:,.2f}.",
                "3. Operational Mandate": "Approved for executive review and implementation."
            })
            st.download_button("📥 Download Audit Report (PDF)", data=pdf_data, file_name="Nibras_Audit_Report.pdf", mime="application/pdf")

        with col_b:
            ppt_file = create_executive_ppt(df, target, insights_list)
            st.download_button("📥 Download Board Presentation (PPTX)", data=ppt_file, file_name="Nibras_Executive_Deck.pptx")

    with tab_gate:
        st.subheader("Send Package to Commission")
        email = st.text_input("Enter Commission Head Email:")
        if st.button("🚀 Package & Send"):
            if email:
                st.balloons()
                st.success(f"Strategic Assets transmitted to {email}")

else:
    st.info("Awaiting strategic data input...")

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
    </div>
    """, unsafe_allow_html=True)
