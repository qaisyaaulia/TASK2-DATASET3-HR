import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HR Data Analytics Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── GLOBAL CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', system-ui, sans-serif !important;
}

/* ── Dark gradient background ── */
.stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #0f172a 40%, #0a0e1a 100%);
    color: #e2e8f0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1a1f35 100%) !important;
    border-right: 1px solid rgba(99,102,241,0.3);
}
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #a5b4fc !important;
    font-weight: 700 !important;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    background: rgba(99,102,241,0.4) !important;
}
[data-testid="stSidebar"] hr { border-color: rgba(99,102,241,0.25) !important; }

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(120deg,
        rgba(99,102,241,0.25) 0%,
        rgba(168,85,247,0.18) 40%,
        rgba(6,182,212,0.2) 100%);
    border: 1px solid rgba(99,102,241,0.4);
    border-radius: 20px;
    padding: 28px 36px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,255,255,0.04);
}
.hero-banner::before {
    content: '';
    position: absolute; top: -40%; right: -5%;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(168,85,247,0.15) 0%, transparent 70%);
    pointer-events: none;
}
.hero-banner::after {
    content: '';
    position: absolute; bottom: -40%; left: 5%;
    width: 250px; height: 250px;
    background: radial-gradient(circle, rgba(6,182,212,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-size: 2rem; font-weight: 900; letter-spacing: -0.03em; margin: 0;
    background: linear-gradient(90deg, #a5b4fc 0%, #c084fc 40%, #67e8f9 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-sub {
    color: #94a3b8; font-size: 0.95rem; margin: 6px 0 0; font-weight: 400;
}
.hero-badge {
    display: inline-block; padding: 4px 12px;
    background: rgba(99,102,241,0.25); border: 1px solid rgba(99,102,241,0.5);
    border-radius: 20px; font-size: 0.75rem; font-weight: 600;
    color: #a5b4fc; margin-bottom: 10px; letter-spacing: 0.05em;
}

/* ── KPI Cards ── */
.kpi-wrap {
    background: rgba(15,23,42,0.7);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 20px;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
    height: 100%;
}
.kpi-wrap:hover {
    transform: translateY(-3px);
    border-color: rgba(255,255,255,0.15);
    box-shadow: 0 16px 40px rgba(0,0,0,0.3);
}
.kpi-glow {
    position: absolute; top: -20px; right: -20px;
    width: 90px; height: 90px;
    border-radius: 50%;
    opacity: 0.25;
    filter: blur(20px);
}
.kpi-icon {
    font-size: 1.6rem; margin-bottom: 8px; display: block;
}
.kpi-label {
    font-size: 0.72rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.08em; color: #64748b; margin-bottom: 4px;
}
.kpi-value {
    font-size: 1.85rem; font-weight: 800; letter-spacing: -0.02em;
    line-height: 1.1;
}
.kpi-sub {
    font-size: 0.73rem; margin-top: 5px; font-weight: 500; color: #64748b;
}

/* ── Chart Cards ── */
.chart-card {
    background: rgba(15,23,42,0.7);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 20px 20px 8px;
    backdrop-filter: blur(10px);
    margin-bottom: 20px;
    transition: border-color 0.3s;
}
.chart-card:hover { border-color: rgba(99,102,241,0.35); }
.chart-label {
    font-size: 0.7rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.1em; color: #6366f1; margin-bottom: 2px;
}
.chart-title-text {
    font-size: 1.05rem; font-weight: 700; color: #f1f5f9; margin-bottom: 4px;
}

/* ── Insight Section ── */
.insight-header {
    background: linear-gradient(120deg, rgba(16,185,129,0.2), rgba(6,182,212,0.15));
    border: 1px solid rgba(16,185,129,0.35);
    border-radius: 18px;
    padding: 24px 28px;
    margin-top: 10px;
    margin-bottom: 16px;
}
.insight-header h2 {
    font-size: 1.45rem; font-weight: 800;
    background: linear-gradient(90deg, #34d399, #22d3ee);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0 0 4px;
}
.insight-header p { color: #94a3b8; margin: 0; font-size: 0.88rem; }

.insight-card {
    background: rgba(15,23,42,0.75);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 12px;
    transition: all 0.25s ease;
    backdrop-filter: blur(6px);
}
.insight-card:hover {
    border-color: rgba(99,102,241,0.4);
    box-shadow: 0 8px 30px rgba(0,0,0,0.25);
}
.insight-tag {
    display: inline-block; padding: 3px 10px; border-radius: 999px;
    font-size: 0.7rem; font-weight: 700; letter-spacing: 0.06em;
    margin-bottom: 8px; text-transform: uppercase;
}
.insight-title {
    font-size: 0.95rem; font-weight: 700; color: #f1f5f9; margin-bottom: 5px;
}
.insight-body { font-size: 0.84rem; color: #94a3b8; line-height: 1.6; }

/* ── Metric pills ── */
.metric-pill {
    display: inline-block; padding: 2px 10px; border-radius: 999px;
    font-size: 0.75rem; font-weight: 600; margin: 2px;
}

/* ── Misc ── */
#MainMenu, footer { visibility: hidden; }
.stDownloadButton button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
    color: #fff !important; border: none !important;
    border-radius: 8px !important; font-weight: 600 !important;
    padding: 8px 16px !important;
}
</style>
""", unsafe_allow_html=True)


# ─── Load Data ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_excel("CLEAN DATA - HR.xlsx")
    df["Join_Date"] = pd.to_datetime(df["Join_Date"], errors="coerce")
    df["Join_Year"] = df["Join_Date"].dt.year
    return df

df_raw = load_data()

# ─── Color palette ────────────────────────────────────────────────────────────
CHART_COLORS = ["#6366f1","#8b5cf6","#06b6d4","#10b981","#f59e0b","#ef4444",
                "#ec4899","#3b82f6","#84cc16","#f97316","#a855f7","#14b8a6"]
PLOTLY_DARK = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#cbd5e1", size=12),
    margin=dict(l=12, r=12, t=40, b=12),
)

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎛️ Filter Panel")
    st.markdown("---")

    all_depts = sorted(df_raw["Department"].dropna().unique().tolist())
    st.markdown("**🏢 Department**")
    sel_dept = st.multiselect("Department", all_depts, default=[], label_visibility="collapsed", placeholder="All departments…")

    st.markdown("**📍 Region**")
    all_regions = sorted(df_raw["Region"].dropna().unique().tolist())
    sel_region = st.multiselect("Region", all_regions, default=[], label_visibility="collapsed", placeholder="All regions…")

    st.markdown("**📌 Status**")
    all_status = sorted(df_raw["Status"].dropna().unique().tolist())
    sel_status = st.multiselect("Status", all_status, default=[], label_visibility="collapsed", placeholder="All statuses…")

    st.markdown("**⭐ Performance Score**")
    all_perf = sorted(df_raw["Performance_Score"].dropna().unique().tolist())
    sel_perf = st.multiselect("Performance", all_perf, default=[], label_visibility="collapsed", placeholder="All scores…")

    st.markdown("**📅 Join Year**")
    min_yr = int(df_raw["Join_Year"].min())
    max_yr = int(df_raw["Join_Year"].max())
    yr_range = st.slider("Join Year", min_yr, max_yr, (min_yr, max_yr), label_visibility="collapsed")

    st.markdown("---")
    st.markdown("<span style='color:#475569;font-size:.75rem;'>HR Analytics Dashboard v3.0<br>Powered by Streamlit + Plotly</span>", unsafe_allow_html=True)

# ─── Apply Filters ────────────────────────────────────────────────────────────
df = df_raw.copy()
if sel_dept:    df = df[df["Department"].isin(sel_dept)]
if sel_region:  df = df[df["Region"].isin(sel_region)]
if sel_status:  df = df[df["Status"].isin(sel_status)]
if sel_perf:    df = df[df["Performance_Score"].isin(sel_perf)]
df = df[(df["Join_Year"].fillna(yr_range[0]).astype(int) >= yr_range[0]) &
        (df["Join_Year"].fillna(yr_range[1]).astype(int) <= yr_range[1])]

# ─── Hero Banner ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">✦ LIVE ANALYTICS</div>
    <h1 class="hero-title">🚀 HR Data Analytics Dashboard</h1>
    <p class="hero-sub">Real-time workforce intelligence · Human Capital Management · Executive Insights</p>
</div>
""", unsafe_allow_html=True)

if df.empty:
    st.warning("⚠️ Tidak ada data yang cocok dengan filter. Silakan ubah pilihan filter.")
    st.stop()

# ─── KPI Computations ────────────────────────────────────────────────────────
total       = len(df)
active_n    = (df["Status"].str.lower() == "active").sum()
inactive_n  = (df["Status"].str.lower() == "inactive").sum()
avg_sal     = df["Salary"].mean()
avg_age     = df["Age"].mean()
remote_n    = (df["Remote_Work"].str.lower() == "yes").sum()
pct_remote  = remote_n / total * 100 if total else 0
pct_active  = active_n / total * 100 if total else 0

# ─── KPI Cards Row ───────────────────────────────────────────────────────────
kc = st.columns(6)
kpis = [
    ("👥", "Total Karyawan",   f"{total:,}",         f"{total} records aktif",   "#6366f1"),
    ("✅", "Karyawan Aktif",   f"{active_n:,}",       f"{pct_active:.1f}% dari total", "#10b981"),
    ("💵", "Rata-rata Gaji",   f"${avg_sal:,.0f}",    "per tahun",                "#f59e0b"),
    ("🎂", "Rata-rata Usia",   f"{avg_age:.1f} thn",  "usia rata-rata karyawan",  "#06b6d4"),
    ("💻", "% Remote Work",    f"{pct_remote:.1f}%",  f"{remote_n:,} orang remote","#8b5cf6"),
    ("⛔", "Jumlah Inactive",  f"{inactive_n:,}",     f"{inactive_n/total*100:.1f}% dari total" if total else "–", "#ef4444"),
]
for col, (icon, lbl, val, sub, color) in zip(kc, kpis):
    with col:
        st.markdown(f"""
        <div class="kpi-wrap">
            <div class="kpi-glow" style="background:{color}"></div>
            <span class="kpi-icon">{icon}</span>
            <div class="kpi-label">{lbl}</div>
            <div class="kpi-value" style="color:{color}">{val}</div>
            <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<div style='margin:18px 0'></div>", unsafe_allow_html=True)

# ─── HELPER: chart wrapper ────────────────────────────────────────────────────
def chart_header(tag, title):
    st.markdown(f"""
    <div class="chart-card">
        <div class="chart-label">{tag}</div>
        <div class="chart-title-text">{title}</div>
    </div>""", unsafe_allow_html=True)

# ─── ROW 1: Bar Dept | Pie Status ────────────────────────────────────────────
r1a, r1b = st.columns([1.45, 1])

with r1a:
    chart_header("📊 Headcount", "Employee Count by Department")
    dept_cnt = df["Department"].value_counts().reset_index()
    dept_cnt.columns = ["Department", "Count"]
    dept_cnt = dept_cnt.sort_values("Count")
    fig = px.bar(dept_cnt, x="Count", y="Department", orientation="h",
                 text="Count", color="Department",
                 color_discrete_sequence=CHART_COLORS)
    fig.update_traces(textposition="outside", textfont=dict(size=11, color="#cbd5e1"),
                      marker_line_width=0)
    fig.update_layout(**PLOTLY_DARK, height=370,
                      showlegend=False, bargap=0.22,
                      xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", title=""),
                      yaxis=dict(showgrid=False, title=""))
    st.plotly_chart(fig, use_container_width=True)

with r1b:
    chart_header("🥧 Distribution", "Employee Status Breakdown")
    sc = df["Status"].value_counts().reset_index()
    sc.columns = ["Status","Count"]
    status_colors = {"Active":"#10b981","Inactive":"#ef4444","Pending":"#f59e0b","Contract":"#06b6d4"}
    fig = px.pie(sc, names="Status", values="Count", hole=0,
                 color="Status", color_discrete_map=status_colors)
    fig.update_traces(textinfo="label+percent", textfont=dict(size=12),
                      marker=dict(line=dict(color="#0a0e1a", width=2.5)),
                      pull=[0.06]*len(sc))
    fig.update_layout(**PLOTLY_DARK, height=370, showlegend=True,
                      legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center",
                                  font=dict(size=11)))
    st.plotly_chart(fig, use_container_width=True)

# ─── ROW 2: Donut Remote | Treemap Region ────────────────────────────────────
r2a, r2b = st.columns([1, 1.45])

with r2a:
    chart_header("🍩 Remote Work", "Remote vs Onsite Distribution")
    rc = df["Remote_Work"].value_counts().reset_index()
    rc.columns = ["Type","Count"]
    rc["Label"] = rc["Type"].map({"Yes":"🌐 Remote","No":"🏢 Onsite"})
    fig = px.pie(rc, names="Label", values="Count",
                 color="Type", color_discrete_map={"Yes":"#8b5cf6","No":"#334155"},
                 hole=0.62)
    fig.update_traces(textinfo="value+percent", textfont=dict(size=12),
                      marker=dict(line=dict(color="#0a0e1a", width=2.5)))
    fig.add_annotation(text=f"<b>{total:,}</b><br><span style='font-size:11px'>Total</span>",
                       x=0.5, y=0.5, showarrow=False,
                       font=dict(size=22, color="#f1f5f9", family="Inter"),
                       xref="paper", yref="paper")
    fig.update_layout(**PLOTLY_DARK, height=350, showlegend=True,
                      legend=dict(orientation="h", y=-0.12, x=0.5, xanchor="center",
                                  font=dict(size=11)))
    st.plotly_chart(fig, use_container_width=True)

with r2b:
    chart_header("🗺️ Salary Map", "Total Salary Sum by Region (Treemap)")
    reg_sal = df.groupby("Region")["Salary"].sum().reset_index()
    reg_sal.columns = ["Region","Total_Salary"]
    reg_sal["Label"] = reg_sal["Total_Salary"].apply(lambda x: f"${x/1e6:.2f}M")
    fig = px.treemap(reg_sal, path=["Region"], values="Total_Salary",
                     color="Region", color_discrete_sequence=CHART_COLORS,
                     custom_data=["Label"])
    fig.update_traces(
        texttemplate="<b>%{label}</b><br>%{customdata[0]}",
        textfont=dict(size=13, color="#ffffff"),
        marker=dict(line=dict(width=3, color="#0a0e1a")),
    )
    fig.update_layout(**PLOTLY_DARK, height=350)
    st.plotly_chart(fig, use_container_width=True)

# ─── ROW 3: Avg Salary per Dept | Avg Salary per Perf ────────────────────────
r3a, r3b = st.columns(2)

with r3a:
    chart_header("💰 Salary Analysis", "Average Salary by Department")
    ds = df.groupby("Department")["Salary"].mean().reset_index().rename(columns={"Salary":"Avg"})
    ds = ds.sort_values("Avg", ascending=False)
    fig = px.bar(ds, x="Department", y="Avg",
                 text=ds["Avg"].apply(lambda x: f"${x:,.0f}"),
                 color="Department", color_discrete_sequence=CHART_COLORS)
    fig.update_traces(textposition="outside", textfont=dict(size=10, color="#cbd5e1"),
                      marker_line_width=0)
    fig.update_layout(**PLOTLY_DARK, showlegend=False, height=370, bargap=0.3,
                      xaxis=dict(tickangle=-35, showgrid=False, title=""),
                      yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)",
                                 zeroline=False, title="Avg Salary ($)"))
    st.plotly_chart(fig, use_container_width=True)

with r3b:
    chart_header("⭐ Performance Pay", "Average Salary by Performance Score")
    perf_order = ["Excellent","Good","Average","Poor"]
    perf_colors = {"Excellent":"#10b981","Good":"#6366f1","Average":"#f59e0b","Poor":"#ef4444"}
    ps = df.groupby("Performance_Score")["Salary"].mean().reset_index().rename(columns={"Salary":"Avg"})
    ps["Performance_Score"] = pd.Categorical(ps["Performance_Score"], categories=perf_order, ordered=True)
    ps = ps.sort_values("Performance_Score")
    fig = px.bar(ps, x="Performance_Score", y="Avg",
                 text=ps["Avg"].apply(lambda x: f"${x:,.0f}"),
                 color="Performance_Score", color_discrete_map=perf_colors)
    fig.update_traces(textposition="outside", textfont=dict(size=12, color="#cbd5e1"),
                      marker_line_width=0)
    fig.update_layout(**PLOTLY_DARK, showlegend=False, height=370, bargap=0.35,
                      xaxis=dict(showgrid=False, title=""),
                      yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)",
                                 zeroline=False, title="Avg Salary ($)"))
    st.plotly_chart(fig, use_container_width=True)

# ─── ROW 4: Headcount Region | Trend ─────────────────────────────────────────
r4a, r4b = st.columns(2)

with r4a:
    chart_header("📍 Headcount Map", "Employee Count by Region")
    rc2 = df["Region"].value_counts().reset_index().rename(columns={"Region":"Region","count":"Count"})
    rc2 = rc2.sort_values("Count", ascending=False)
    fig = px.bar(rc2, x="Region", y="Count", text="Count",
                 color="Region", color_discrete_sequence=CHART_COLORS)
    fig.update_traces(textposition="outside", textfont=dict(size=12, color="#cbd5e1"),
                      marker_line_width=0)
    fig.update_layout(**PLOTLY_DARK, showlegend=False, height=350, bargap=0.3,
                      xaxis=dict(showgrid=False, title=""),
                      yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)",
                                 zeroline=False, title="Karyawan"))
    st.plotly_chart(fig, use_container_width=True)

with r4b:
    chart_header("📈 Hiring Trend", "Headcount by Join Year")
    yr = df.groupby("Join_Year").size().reset_index(name="Count").dropna()
    yr["Join_Year"] = yr["Join_Year"].astype(int)
    fig = px.area(yr, x="Join_Year", y="Count", markers=True,
                  color_discrete_sequence=["#6366f1"], text="Count")
    fig.update_traces(
        textposition="top center", textfont=dict(size=11, color="#cbd5e1"),
        line=dict(width=3), fillcolor="rgba(99,102,241,0.18)",
        marker=dict(size=9, color="#a5b4fc", line=dict(color="#6366f1", width=2))
    )
    fig.update_layout(**PLOTLY_DARK, height=350,
                      xaxis=dict(dtick=1, showgrid=False, title="Tahun Bergabung"),
                      yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)",
                                 zeroline=False, title="Karyawan"))
    st.plotly_chart(fig, use_container_width=True)

# ─── BONUS ROW: Salary Distribution Histogram | Performance Headcount ─────────
r5a, r5b = st.columns(2)

with r5a:
    chart_header("📉 Salary Distribution", "Histogram Distribusi Gaji")
    fig = px.histogram(df, x="Salary", nbins=30,
                       color_discrete_sequence=["#8b5cf6"])
    fig.update_traces(marker_line_width=0, opacity=0.85)
    fig.add_vline(x=avg_sal, line_dash="dot", line_color="#f59e0b",
                  annotation_text=f"Avg: ${avg_sal:,.0f}",
                  annotation_font=dict(color="#f59e0b", size=12))
    fig.update_layout(**PLOTLY_DARK, height=320, bargap=0.05,
                      xaxis=dict(title="Salary ($)", showgrid=False),
                      yaxis=dict(title="Frekuensi", showgrid=True,
                                 gridcolor="rgba(255,255,255,0.06)", zeroline=False))
    st.plotly_chart(fig, use_container_width=True)

with r5b:
    chart_header("🏅 Performance Spread", "Headcount per Performance Score")
    pf = df["Performance_Score"].value_counts().reset_index()
    pf.columns = ["Score","Count"]
    pf["Score"] = pd.Categorical(pf["Score"], categories=perf_order, ordered=True)
    pf = pf.sort_values("Score")
    colors_p = [perf_colors.get(s, "#6366f1") for s in pf["Score"]]
    fig = go.Figure(go.Bar(
        x=pf["Score"], y=pf["Count"],
        text=pf["Count"], textposition="outside",
        textfont=dict(size=13, color="#cbd5e1"),
        marker_color=colors_p, marker_line_width=0
    ))
    fig.update_layout(**PLOTLY_DARK, height=320, showlegend=False, bargap=0.35,
                      xaxis=dict(showgrid=False, title=""),
                      yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)",
                                 zeroline=False, title="Karyawan"))
    st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ─── INSIGHTS & RECOMMENDATIONS MODULE ────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<div style='margin-top:24px'></div>", unsafe_allow_html=True)
st.markdown("""
<div class="insight-header">
    <h2>🔍 Insights & Rekomendasi</h2>
    <p>Analisis otomatis berbasis data yang tersaring — kesimpulan strategis & saran tindak lanjut</p>
</div>
""", unsafe_allow_html=True)

# ── Auto-compute insight values ────────────────────────────────────────────────
top_dept     = df["Department"].value_counts().idxmax()
top_dept_n   = df["Department"].value_counts().max()
bot_dept     = df["Department"].value_counts().idxmin()
bot_dept_n   = df["Department"].value_counts().min()

top_sal_dept = df.groupby("Department")["Salary"].mean().idxmax()
top_sal_val  = df.groupby("Department")["Salary"].mean().max()
bot_sal_dept = df.groupby("Department")["Salary"].mean().idxmin()
bot_sal_val  = df.groupby("Department")["Salary"].mean().min()

top_region   = df["Region"].value_counts().idxmax()
top_region_n = df["Region"].value_counts().max()
perf_dist    = df["Performance_Score"].value_counts(normalize=True) * 100
excellent_pct= perf_dist.get("Excellent", 0)
poor_pct     = perf_dist.get("Poor", 0)
avg_pct_perf = perf_dist.get("Average", 0)
good_pct_perf= perf_dist.get("Good", 0)

top_perf_sal = df.groupby("Performance_Score")["Salary"].mean().get("Excellent", 0)
poor_perf_sal= df.groupby("Performance_Score")["Salary"].mean().get("Poor", 0)
sal_gap      = top_perf_sal - poor_perf_sal

inactive_pct = inactive_n / total * 100 if total else 0
contract_n   = (df["Status"].str.lower() == "contract").sum()
pending_n    = (df["Status"].str.lower() == "pending").sum()

age_min      = df["Age"].min()
age_max      = df["Age"].max()

# ── Insight Cards Grid ─────────────────────────────────────────────────────────
ic1, ic2, ic3 = st.columns(3)

with ic1:
    dept_health = "⚠️ Perlu Perhatian" if bot_dept_n < 30 else "✅ Sehat"
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-tag" style="background:rgba(99,102,241,0.2);color:#a5b4fc;">
            📊 WORKFORCE DISTRIBUTION
        </div>
        <div class="insight-title">Distribusi Karyawan per Departemen</div>
        <div class="insight-body">
            Departemen <b style='color:#a5b4fc'>{top_dept}</b> memiliki headcount terbesar
            dengan <b>{top_dept_n:,}</b> karyawan, sementara <b style='color:#f87171'>{bot_dept}</b>
            adalah departemen terkecil dengan hanya <b>{bot_dept_n}</b> karyawan.
            <br><br>
            <span class="metric-pill" style="background:rgba(99,102,241,0.2);color:#a5b4fc">Terbesar: {top_dept}</span>
            <span class="metric-pill" style="background:rgba(239,68,68,0.2);color:#fca5a5">Terkecil: {bot_dept}</span>
        </div>
        <div style="margin-top:10px;padding:8px 12px;background:rgba(16,185,129,0.1);border-radius:8px;border-left:3px solid #10b981">
            <span style="font-size:.78rem;color:#6ee7b7;font-weight:600">💡 SARAN:</span>
            <span style="font-size:.78rem;color:#94a3b8"> Evaluasi kebutuhan rekrutmen di departemen <b style='color:#f87171'>{bot_dept}</b> untuk memastikan kapasitas operasional yang memadai.</span>
        </div>
    </div>""", unsafe_allow_html=True)

with ic2:
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-tag" style="background:rgba(245,158,11,0.2);color:#fcd34d;">
            💵 SALARY INSIGHT
        </div>
        <div class="insight-title">Kesenjangan Gaji Antar Departemen</div>
        <div class="insight-body">
            Departemen <b style='color:#fcd34d'>{top_sal_dept}</b> membayar rata-rata tertinggi
            (<b>${top_sal_val:,.0f}</b>), sedangkan <b style='color:#f87171'>{bot_sal_dept}</b>
            membayar paling rendah (<b>${bot_sal_val:,.0f}</b>).
            <br><br>
            Gap sebesar <b style='color:#fb923c'>${top_sal_val - bot_sal_val:,.0f}</b> menunjukkan
            adanya diferensiasi kompensasi yang signifikan.
            <br><br>
            <span class="metric-pill" style="background:rgba(245,158,11,0.2);color:#fcd34d">Tertinggi: {top_sal_dept}</span>
            <span class="metric-pill" style="background:rgba(239,68,68,0.2);color:#fca5a5">Terendah: {bot_sal_dept}</span>
        </div>
        <div style="margin-top:10px;padding:8px 12px;background:rgba(245,158,11,0.1);border-radius:8px;border-left:3px solid #f59e0b">
            <span style="font-size:.78rem;color:#fcd34d;font-weight:600">💡 SARAN:</span>
            <span style="font-size:.78rem;color:#94a3b8"> Lakukan salary benchmarking di departemen <b style='color:#fca5a5'>{bot_sal_dept}</b> agar kompetitif di pasar dan mengurangi risiko turnover.</span>
        </div>
    </div>""", unsafe_allow_html=True)

with ic3:
    status_note = "tinggi" if inactive_pct > 20 else ("moderat" if inactive_pct > 10 else "rendah")
    status_color = "#ef4444" if inactive_pct > 20 else ("#f59e0b" if inactive_pct > 10 else "#10b981")
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-tag" style="background:rgba(239,68,68,0.2);color:#fca5a5;">
            ⛔ RETENTION RISK
        </div>
        <div class="insight-title">Analisis Status & Retensi Karyawan</div>
        <div class="insight-body">
            Dari total <b>{total:,}</b> karyawan (tersaring), sebanyak
            <b style='color:#4ade80'>{active_n:,}</b> berstatus Aktif (<b>{pct_active:.1f}%</b>),
            <b style='color:{status_color}'>{inactive_n:,}</b> Inactive ({inactive_pct:.1f}%),
            {f'<b style="color:#f59e0b">{pending_n}</b> Pending, dan ' if pending_n > 0 else ''}
            <b style='color:#06b6d4'>{contract_n}</b> Contract.
            <br><br>
            Tingkat Inactive dinilai <b style='color:{status_color}'>{status_note}</b>.
        </div>
        <div style="margin-top:10px;padding:8px 12px;background:rgba(239,68,68,0.1);border-radius:8px;border-left:3px solid #ef4444">
            <span style="font-size:.78rem;color:#fca5a5;font-weight:600">💡 SARAN:</span>
            <span style="font-size:.78rem;color:#94a3b8">
            {"Lakukan exit interview & analisis penyebab attrition. Pertimbangkan program retensi seperti benefit tambahan atau jenjang karier yang lebih jelas." if inactive_pct > 10 else "Pertahankan program engagement dan onboarding yang sudah berjalan baik."}
            </span>
        </div>
    </div>""", unsafe_allow_html=True)

# ── Second row of insights ─────────────────────────────────────────────────────
ic4, ic5, ic6 = st.columns(3)

with ic4:
    remote_label = "dominan" if pct_remote > 50 else ("seimbang" if pct_remote > 35 else "minoritas")
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-tag" style="background:rgba(139,92,246,0.2);color:#c4b5fd;">
            💻 REMOTE WORK TREND
        </div>
        <div class="insight-title">Pola Kerja Remote vs Onsite</div>
        <div class="insight-body">
            <b style='color:#c4b5fd'>{pct_remote:.1f}%</b> karyawan ({remote_n:,} orang) bekerja secara
            <b>Remote</b>, sementara <b>{100-pct_remote:.1f}%</b> ({total-remote_n:,} orang) masih Onsite.
            <br><br>
            Mode kerja remote saat ini bersifat <b style='color:#c4b5fd'>{remote_label}</b> dalam komposisi workforce.
        </div>
        <div style="margin-top:10px;padding:8px 12px;background:rgba(139,92,246,0.1);border-radius:8px;border-left:3px solid #8b5cf6">
            <span style="font-size:.78rem;color:#c4b5fd;font-weight:600">💡 SARAN:</span>
            <span style="font-size:.78rem;color:#94a3b8">
            {"Kembangkan kebijakan hybrid work yang lebih terstruktur, lengkap dengan SOP kolaborasi virtual dan monitoring produktivitas." if pct_remote > 30 else "Pertimbangkan perluasan opsi remote work untuk menarik talent dari luar kota tanpa biaya relokasi."}
            </span>
        </div>
    </div>""", unsafe_allow_html=True)

with ic5:
    perf_risk = poor_pct > 15
    perf_great = excellent_pct > 30
    perf_color_tag = "#ef4444" if perf_risk else ("#10b981" if perf_great else "#f59e0b")
    perf_emoji = "🔴" if perf_risk else ("🟢" if perf_great else "🟡")
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-tag" style="background:rgba(16,185,129,0.2);color:#6ee7b7;">
            ⭐ PERFORMANCE GAP
        </div>
        <div class="insight-title">Korelasi Performa & Kompensasi</div>
        <div class="insight-body">
            Karyawan <b style='color:#10b981'>Excellent</b> mendapat rata-rata
            <b>${top_perf_sal:,.0f}</b>, sedangkan <b style='color:#ef4444'>Poor</b>
            hanya <b>${poor_perf_sal:,.0f}</b> — gap sebesar
            <b style='color:#fb923c'>${sal_gap:,.0f}</b>.
            <br><br>
            Distribusi: Excellent <b>{excellent_pct:.0f}%</b> · Good <b>{good_pct_perf:.0f}%</b>
            · Average <b>{avg_pct_perf:.0f}%</b> · Poor <b style='color:{perf_color_tag}'>{poor_pct:.0f}%</b>
            {perf_emoji}
        </div>
        <div style="margin-top:10px;padding:8px 12px;background:rgba(16,185,129,0.1);border-radius:8px;border-left:3px solid #10b981">
            <span style="font-size:.78rem;color:#6ee7b7;font-weight:600">💡 SARAN:</span>
            <span style="font-size:.78rem;color:#94a3b8">
            {"Rancang program Performance Improvement Plan (PIP) untuk karyawan berkinerja Poor, dan perkuat merit-based pay system." if perf_risk else "Lanjutkan sistem apresiasi performa. Pastikan insentif berbasis KPI rutin di-review untuk menjaga motivasi."}
            </span>
        </div>
    </div>""", unsafe_allow_html=True)

with ic6:
    top_r = df["Region"].value_counts().idxmax()
    top_r_n = df["Region"].value_counts().max()
    top_r_pct = top_r_n / total * 100
    small_r = df["Region"].value_counts().idxmin()
    small_r_n = df["Region"].value_counts().min()
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-tag" style="background:rgba(6,182,212,0.2);color:#67e8f9;">
            🌎 REGIONAL SPREAD
        </div>
        <div class="insight-title">Distribusi Geografis Karyawan</div>
        <div class="insight-body">
            Region <b style='color:#67e8f9'>{top_r}</b> menjadi pusat tenaga kerja terbesar
            dengan <b>{top_r_n:,}</b> karyawan (<b>{top_r_pct:.1f}%</b> total workforce).
            <br><br>
            Region <b style='color:#f87171'>{small_r}</b> memiliki kehadiran terkecil
            dengan <b>{small_r_n}</b> karyawan — peluang ekspansi rekrutmen lokal.
            <br><br>
            <span class="metric-pill" style="background:rgba(6,182,212,0.2);color:#67e8f9">Usia: {age_min}–{age_max} thn</span>
        </div>
        <div style="margin-top:10px;padding:8px 12px;background:rgba(6,182,212,0.1);border-radius:8px;border-left:3px solid #06b6d4">
            <span style="font-size:.78rem;color:#67e8f9;font-weight:600">💡 SARAN:</span>
            <span style="font-size:.78rem;color:#94a3b8"> Pertimbangkan program talent acquisition lokal di region <b style='color:#fca5a5'>{small_r}</b> untuk diversifikasi geografi dan mengurangi ketergantungan pada satu lokasi.</span>
        </div>
    </div>""", unsafe_allow_html=True)

# ── Executive Summary ──────────────────────────────────────────────────────────
st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)
overall_health = "Baik" if pct_active > 60 and inactive_pct < 20 and poor_pct < 15 else (
                  "Perlu Perhatian" if pct_active > 40 else "Kritis")
health_color = "#10b981" if overall_health == "Baik" else ("#f59e0b" if overall_health == "Perlu Perhatian" else "#ef4444")
health_emoji = "🟢" if overall_health == "Baik" else ("🟡" if overall_health == "Perlu Perhatian" else "🔴")

# Pre-compute rgba string outside f-string to avoid SyntaxError
if overall_health == 'Baik':
    health_rgba = '16,185,129'
elif overall_health == 'Perlu Perhatian':
    health_rgba = '245,158,11'
else:
    health_rgba = '239,68,68'

st.markdown(f"""
<div style="background:linear-gradient(120deg,rgba(99,102,241,0.12),rgba(168,85,247,0.1));
            border:1px solid rgba(99,102,241,0.3);border-radius:16px;padding:24px 28px;margin-top:4px">
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px">
        <span style="font-size:1.4rem">📋</span>
        <h3 style="margin:0;color:#f1f5f9;font-size:1.1rem;font-weight:800">Executive Summary</h3>
        <span style="margin-left:auto;padding:4px 14px;border-radius:999px;
              background:rgba({health_rgba},0.2);
              color:{health_color};font-size:.78rem;font-weight:700;border:1px solid {health_color}40">
            {health_emoji} Status Organisasi: {overall_health}
        </span>
    </div>
    <div style="color:#94a3b8;font-size:.87rem;line-height:1.9">
        Berdasarkan analisis <b style='color:#f1f5f9'>{total:,} karyawan</b> (data tersaring), organisasi memiliki
        tingkat aktivitas <b style='color:#4ade80'>{pct_active:.1f}%</b> dengan rata-rata gaji
        <b style='color:#fcd34d'>${avg_sal:,.0f}/tahun</b> dan usia rata-rata
        <b style='color:#67e8f9'>{avg_age:.1f} tahun</b>.
        <br>
        Departemen <b style='color:#a5b4fc'>{top_dept}</b> merupakan departemen terbesar, dan
        <b style='color:#fcd34d'>{top_sal_dept}</b> membayar gaji tertinggi.
        Sebanyak <b style='color:#c4b5fd'>{pct_remote:.1f}%</b> workforce beroperasi secara remote.
        Karyawan dengan performa <i>Excellent</i> mendapat kompensasi
        <b style='color:#34d399'>${sal_gap:,.0f}</b> lebih tinggi dibanding performa <i>Poor</i>.
        <br><br>
        <b style='color:#f1f5f9'>Prioritas Tindakan:</b>
        {"① Tingkatkan program retensi untuk mengurangi inactive rate. " if inactive_pct > 10 else ""}
        {"② Audit kesenjangan gaji antar departemen secara berkala. "}
        {"③ Kembangkan PIP untuk karyawan Poor Performance. " if poor_pct > 10 else ""}
        {"④ Perkuat rekrutmen di region yang masih minim karyawan."}
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Data Table ───────────────────────────────────────────────────────────────
st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)
with st.expander(f"📄 Detail Data Karyawan — {total:,} records", expanded=False):
    cols = ["Employee_ID","First_Name","Last_Name","Age","Department","Region",
            "Status","Salary","Performance_Score","Remote_Work","Join_Date"]
    st.dataframe(df[cols], use_container_width=True, hide_index=True)
    csv = df[cols].to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Filtered Data (CSV)", data=csv,
                       file_name="filtered_hr_data.csv", mime="text/csv")