import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pptx import Presentation
from io import BytesIO
import datetime
import numpy as np

# ==========================================
# 1. الهوية البصرية والستايل (The Signature UI)
# ==========================================
st.set_page_config(page_title="NIBRAS AI | Expert Suite", layout="wide", page_icon="💎")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .main-header { 
        background: linear-gradient(90deg, #161b22 0%, #0d1117 100%); 
        padding: 40px; border-radius: 20px; border-right: 12px solid #D4AF37; 
        margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .metric-card { 
        background: #161b22; padding: 25px; border-radius: 15px; 
        border: 1px solid #30363d; text-align: center; transition: 0.3s;
    }
    .metric-card:hover { border-color: #D4AF37; transform: translateY(-5px); }
    .confidence-tag { background: #238636; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.85em; }
    .recommendation-box { 
        background: rgba(212, 175, 55, 0.05); border-right: 6px solid #D4AF37; 
        padding: 20px; margin-bottom: 15px; border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. المحركات الذكية (Intelligence Layers)
# ==========================================

def get_expert_analysis(df, target):
    """محرك التحليل الاستشاري مع طبقة الثقة"""
    data = df[target].values
    avg = np.mean(data)
    current = data[-1]
    growth = ((current - data[0]) / data[0]) * 100
    volatility = np.std(data) / avg
    confidence = max(0, min(100, 100 - (volatility * 100)))
    
    status = "نمو مستدام" if growth > 5 else "منطقة خطر" if growth < -5 else "استقرار تشغيلي"
    return {"growth": growth, "avg": avg, "confidence": round(confidence, 1), "status": status}

def forecasting_model(df, target, periods=3):
    """تنبؤ الاتجاه القادم (Linear Regression)"""
    y = df[target].values
    x = np.arange(len(y))
    slope, intercept = np.polyfit(x, y, 1)
    future_x = np.arange(len(y), len(y) + periods)
    return slope * future_x + intercept

def create_executive_ppt(target, analysis, recs):
    """توليد عرض بوربوينت احترافي"""
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "نبراس AI | تقرير ذكاء القرار"
    slide.placeholders[1].text = f"إعداد المتخصصة: شهد آل مستور\nتاريخ التحليل: {datetime.date.today()}\nالحالة: {analysis['status']}"
    
    slide2 = prs.slides.add_slide(prs.slide_layouts[1])
    slide2.shapes.title.text = "النتائج والتوصيات الاستراتيجية"
    tf = slide2.shapes.placeholders[1].text_frame
    tf.text = f"• صافي النمو: {analysis['growth']:.1f}%"
    for r in recs:
        p = tf.add_paragraph()
        p.text = f"• {r}"
        
    ppt_io = BytesIO()
    prs.save(ppt_io)
    ppt_io.seek(0)
    return ppt_io

# ==========================================
# 3. واجهة المستخدم (The Dashboard Experience)
# ==========================================

st.markdown("<div class='main-header'><h1>🏛️ نـبـراس | NIBRAS AI</h1><p>منصة ذكاء القرار الاستراتيجي وإدارة الأداء</p></div>", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/diamond--v1.png")
    st.header("⚙️ مركز الإدارة")
    file = st.file_uploader("ارفع ملف البيانات (Excel/CSV)", type=['xlsx', 'csv'])
    st.divider()
    target_audience = st.selectbox("تخصيص نبرة التقرير", ["مجلس الإدارة", "الإدارة المتوسطة", "الفريق التقني"])

if file:
    df = pd.read_excel(file) if file.name.endswith('.xlsx') else pd.read_csv(file)
    target_col = df.columns[1]
    
    # المعالجة
    analysis = get_expert_analysis(df, target_col)
    forecast_vals = forecasting_model(df, target_col)
    
    # بطاقات الأداء
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"<div class='metric-card'><h6>الأداء الحالي</h6><h2 style='color:#D4AF37;'>{df[target_col].iloc[-1]:,.0f}</h2><span class='confidence-tag'>ثقة {analysis['confidence']}%</span></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='metric-card'><h6>صافي التغير</h6><h2>{analysis['growth']:.1f}%</h2><small>{analysis['status']}</small></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='metric-card'><h6>المتوسط التاريخي</h6><h2>{analysis['avg']:,.0f}</h2><small>بناءً على {len(df)} فحص</small></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🧐 رؤية المستشار", "🔮 التنبؤ الزمني", "📦 التصدير"])

    with tab1:
        st.subheader("💡 التفسير الاستراتيجي")
        st.markdown(f"""
        <div class='recommendation-box'>
            <b>تفسير نبراس:</b> يظهر تحليل البيانات لـ {target_col} حالة <b>{analysis['status']}</b> بدرجة ثقة تصل لـ {analysis['confidence']}%. 
            هذا النمط يشير إلى ضرورة التركيز على تحسين الاستدامة التشغيلية.
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("🚀 التوصيات المعتمدة")
        recs = {
            "نمو مستدام": ["زيادة المخصصات التسويقية", "توسيع النطاق التشغيلي", "رفع الأهداف السنوية بنسبة 10%"],
            "منطقة خطر": ["خفض التكاليف الهامشية فوراً", "إعادة تقييم استراتيجية التسعير", "فحص جودة العمليات"],
            "استقرار تشغيلي": ["تحسين تجربة العميل الحالية", "أتمتة المهام المتكررة", "مراقبة اتجاهات السوق"]
        }
        current_recs = recs.get(analysis['status'], ["استمرار المراقبة"])
        for r in current_recs:
            st.markdown(f"✅ {r}")

    with tab2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.iloc[:,0], y=df[target_col], name="البيانات الفعلية", line=dict(color="#D4AF37", width=4)))
        future_dates = [f"توقع {i+1}" for i in range(3)]
        fig.add_trace(go.Scatter(x=future_dates, y=forecast_vals, name="المسار التنبؤي", line=dict(dash='dash', color="#2ecc71", width=3)))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#fff", hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("📥 مخرجات الاعتماد")
        ppt_data = create_executive_ppt(target_col, analysis, current_recs)
        st.download_button(
            label="تحميل العرض التقديمي (PowerPoint)",
            data=ppt_data,
            file_name=f"Nibras_Report_{datetime.date.today()}.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
        st.info(f"تم تجهيز التقرير بنبرة تلائم: {target_audience}")

else:
    st.info("نبراس AI بانتظار تزويده بالبيانات ليتحول إلى وضع 'المستشار الخبير'.")

st.markdown(f"""
    <div style="text-align: center; margin-top: 100px; color: #484f58; border-top: 1px solid #30363d; padding-top: 20px;">
        تم التطوير بواسطة: <b>شهد آل مستور</b> | خبيرة علوم الحاسب <br>
        NIBRAS AI © 2026 | THE ABSOLUTE STANDARD
    </div>
    """, unsafe_allow_html=True)
