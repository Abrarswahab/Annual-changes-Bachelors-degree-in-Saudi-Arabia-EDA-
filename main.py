import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#stle.py
from webStyle.style import inject_css, dark_layout, insight, pct, YC, YEARS, DARK_TEXT, DARK_AXIS, DARK_GRID, DARK_BG, DARK_PAPER, FONT

st.set_page_config(
    page_title="التغيرات السنوية · بكالوريوس السعودية",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

#Dataset
@st.cache_data
def load():
    df = pd.read_csv("csvfiles/main_dataset.csv")
    return df[(df["المرحلة الدراسية"] == "بكالوريوس") & (df["حالة_الطالب"] == "مستجد")].copy()

df = load()

Y   = "السنة الدراسية"
REG = "المنطقة الإدارية"
ORG = "الجهة التعليمية"
FLD = "المجال الواسع"
GEN = "الجنس"
NAT = "الجنسية"
CNT = "العدد"
STS = "حالة_الطالب"
PCT = "النسبة المئوية"

# Sidebar
with st.sidebar:
    st.markdown("## فلاتر المقارنة")
    st.markdown("---")
    sel_reg = st.multiselect(" المنطقة", sorted(df[REG].unique()), default=sorted(df[REG].unique()))
    sel_gen = st.multiselect(" الجنس",    sorted(df[GEN].unique()), default=sorted(df[GEN].unique()))
    sel_nat = st.multiselect(" الجنسية",  sorted(df[NAT].unique()), default=sorted(df[NAT].unique()))
    st.info(" الطلاب المستجدون فقط")
    st.markdown("---")
    st.markdown("**المرحلة:** بكالوريوس فقط")
    st.markdown("**السنوات:** ٢٠٢١ · ٢٠٢٢ · ٢٠٢٣")

fdf = df[df[REG].isin(sel_reg) & df[GEN].isin(sel_gen) & df[NAT].isin(sel_nat)].copy()

#Annual totals
annual_total = fdf.groupby(Y)[CNT].sum()
grand_total  = int(annual_total.sum())
t21 = int(annual_total.get(2021, 0))
t22 = int(annual_total.get(2022, 0))
t23 = int(annual_total.get(2023, 0))

def delta_str(new, old):
    if old == 0: return "", ""
    d = new - old; p = d / old * 100
    sign = "▲" if d > 0 else "▼"; cls = "up" if d > 0 else "down"
    return f'{sign} {abs(d):,} ({abs(p):.1f}٪)', cls

d22s, d22c = delta_str(t22, t21)
d23s, d23c = delta_str(t23, t22)

# hero
st.markdown("""
<div class="hero">
  <div class="hero-title"> التغيرات السنوية في أعداد طلاب البكالوريوس</div>
  <div class="hero-sub">تحليل الطلاب المستجدين · مقارنة بين أعوام ٢٠٢١ و٢٠٢٢ و٢٠٢٣ — الجامعات الحكومية السعودية · الأرقام كنسب مئوية من إجمالي كل عام</div>
</div>""", unsafe_allow_html=True)

# tab table
tab_labels = [
    "وصف البيانات",
    # "عينة من البيانات",
    "إجمالي الطلاب",
    "التغير حسب المجال", 
    "أكثر المجالات نمواً وتراجعاً", 
    "التغير الإقليمي",
    "مستجد مقابل خريج", 
    
    # "📋 جدول التغيرات",
]
tabs = st.tabs(tab_labels)

# tab 0
with tabs[0]:
    st.markdown(f"""
    <div class="desc">
      <p>تتتبع هذه اللوحة <strong>التغيرات السنوية في أعداد الطلاب المستجدين</strong> بمرحلة البكالوريوس في الجامعات الحكومية السعودية عبر ثلاثة أعوام: <strong>٢٠٢١ و٢٠٢٢ و٢٠٢٣</strong>. <strong>جميع المخططات تعرض النسب المئوية من إجمالي كل عام</strong> لتسهيل المقارنة الهيكلية بين الأعوام.</p>
      <p>تشمل البيانات <strong>{int(df[CNT].sum()):,} طالباً وطالبة</strong> موزعين على <strong>١٣ منطقة إدارية</strong> و<strong>{df[ORG].nunique()} جهة تعليمية</strong> و<strong>١١ مجالاً دراسياً</strong>.</p>
      <div class="tags">
        <span class="tag"> ٢٠٢١ – ٢٠٢٢ – ٢٠٢٣</span>
        <span class="tag"> {int(df[CNT].sum()):,} طالب بكالوريوس</span>
        <span class="tag"> ١٣ منطقة</span>
        <span class="tag"> {df[ORG].nunique()} جهة تعليمية</span>
        <span class="tag"> نسب مئوية من إجمالي كل عام</span>
      </div>
    </div>""", unsafe_allow_html=True)

    st.dataframe(df.sample(10, random_state=42).reset_index(drop=True), use_container_width=True, height=388)

# tab 1 
# with tabs[1]:
#     st.dataframe(df.sample(10, random_state=42).reset_index(drop=True), use_container_width=True, height=388)

# tab 1: إجمالي الطلاب 
with tabs[1]:
    # Bar: share of grand total per year
    yr_raw = fdf.groupby(Y)[CNT].sum().reset_index()
    yr_raw[PCT] = (yr_raw[CNT] / grand_total * 100).round(1)
    yr_raw["اللون"] = yr_raw[Y].map(YC)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[str(int(y)) for y in yr_raw[Y]],
        y=yr_raw[PCT],
        marker_color=yr_raw["اللون"].tolist(),
        text=[f"{p:.1f}٪" for p in yr_raw[PCT]],
        textposition="outside",
        textfont=dict(size=13, color=DARK_TEXT),
        showlegend=False,
    ))

    dark_layout(fig, "نسبة كل عام من إجمالي الطلاب الكلي (٢٠٢١–٢٠٢٣)", h=380, ml=20, mr=20)
    fig.update_layout(
        showlegend=False,
        barmode="group",
        xaxis=dict(
            showgrid=False,
            color=DARK_AXIS,
            type="category",          
            categoryorder="array",
            categoryarray=[str(int(y)) for y in sorted(yr_raw[Y])],
        ),
        yaxis=dict(
            gridcolor=DARK_GRID,
            range=[0, yr_raw[PCT].max() * 1.2],
            color=DARK_AXIS,
            ticksuffix="٪",
        ),
    )
    st.plotly_chart(fig, use_container_width=True)

    insight("استنتاجات — حصة كل عام من الإجمالي الكلي", [
        "استأثر عام <span class='highlight-up'>٢٠٢٢</span> بأكبر حصة من الإجمالي الكلي (<span class='highlight-up'>36.3٪</span>)، يليه ٢٠٢١ بـ <span class='highlight-gold'>34.0٪</span>، ثم ٢٠٢٣ بأدنى حصة (<span class='highlight-down'>30.8٪</span>).",
        "الفارق بين أعلى عام (٢٠٢٢) وأدناه (٢٠٢٣) يبلغ <span class='highlight-down'>5.5 نقطة مئوية</span>، مما يعكس تراجعاً ملحوظاً في الالتحاق خلال الفترة.",
    ])

    # Pie charts: % of each year's total by gender × nationality
    gn = fdf.groupby([Y, NAT, GEN])[CNT].sum().reset_index()
    gn["الفئة"] = gn[NAT] + " · " + gn[GEN]

    SEGMENT_COLORS = {
        "سعودي · ذكر":      "#4DA6FF", "سعودي · أنثى":     "#E05C8A",
        "غير سعودي · ذكر":  "#FFB347", "غير سعودي · أنثى": "#9B59B6",
    }
    YEAR_LABELS = {2021: "٢٠٢١", 2022: "٢٠٢٢", 2023: "٢٠٢٣"}

    fig = go.Figure()
    for idx, yr_ in enumerate(YEARS):
        sub    = gn[gn[Y] == yr_]
        yr_tot = annual_total.get(yr_, 1)
        labels = sub["الفئة"].tolist()
        values = [round(v / yr_tot * 100, 1) for v in sub[CNT].tolist()]
        colors = [SEGMENT_COLORS.get(l, "#888") for l in labels]
        fig.add_trace(go.Pie(
            labels=labels, values=values, name=str(yr_),
            title=dict(text=f"<b>{YEAR_LABELS[yr_]}</b>", font=dict(size=16, color=DARK_TEXT)),
            marker=dict(colors=colors, line=dict(color=DARK_BG, width=2)),
            textinfo="label+percent",
            textfont=dict(size=11, color="#fff"),
            hovertemplate="<b>%{label}</b><br>النسبة: %{value:.1f}٪<extra></extra>",
            hole=0.38,
            domain=dict(x=[idx/3+0.02, (idx+1)/3-0.02], y=[0, 1]),
            showlegend=(idx == 0),
        ))
    fig.update_layout(
        title=dict(text="توزيع الطلاب (٪ من إجمالي كل عام) حسب الجنسية والجنس",
                   x=0.5, font=dict(size=15, color=DARK_TEXT)),
        paper_bgcolor=DARK_PAPER, plot_bgcolor=DARK_BG,
        font_family=FONT, font_color=DARK_TEXT,
        height=420, margin=dict(l=20, r=20, t=60, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.14, xanchor="center", x=0.5,
                    font=dict(color=DARK_TEXT, size=12), bgcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig, use_container_width=True)

    insight("استنتاجات — توزيع الجنس والجنسية (نسبي)", [
        "الطالبات السعوديات يمثّلن ما يزيد على <span class='highlight-gold'>56٪</span> من مستجدي كل عام، مؤكدةً هيمنتهن المستمرة على الالتحاق ببرامج البكالوريوس.",
        "نسبة غير السعوديين ارتفعت بوضوح عام ٢٠٢٣ لتصل إلى نحو <span class='highlight-up'>6.8٪</span> مقارنةً بـ <span class='highlight-gold'>3.3٪</span> عام ٢٠٢١، مما يعكس انفتاحاً متزايداً على القبول الدولي.",
        "حصة الطلاب السعوديين (ذكوراً وإناثاً) تراجعت نسبياً من <span class='highlight-gold'>96.7٪</span> إلى <span class='highlight-down'>93.2٪</span> خلال الفترة.",
    ])


    st.markdown("### كاشف الشذوذ في أعداد المستجدين")

    # IQR calculation
    Q1 = fdf['العدد'].quantile(0.25)
    Q3 = fdf['العدد'].quantile(0.75)
    IQR = Q3 - Q1
    upper_bound = Q3 + 1.5 * IQR
    lower_bound = Q1 - 1.5 * IQR

    outliers = fdf[(fdf['العدد'] < lower_bound) | (fdf['العدد'] > upper_bound)]
    clean_df  = fdf[(fdf['العدد'] >= lower_bound) & (fdf['العدد'] <= upper_bound)]

    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("الحد الأدنى (IQR)", f"{lower_bound:.1f}")
    col2.metric("الحد الأعلى (IQR)", f"{upper_bound:.1f}")
    col3.metric("صفوف شاذة", f"{len(outliers):,}")
    col4.metric("نسبة الشذوذ", f"{len(outliers)/len(fdf)*100:.1f}٪")

    # Boxplot via Plotly (no matplotlib/sns needed)
    fig = go.Figure()
    for yr_ in YEARS:
        sub = fdf[fdf[Y] == yr_]
        fig.add_trace(go.Box(
            y=sub['العدد'],
            name=str(yr_),
            marker_color=YC[yr_],
            boxmean=True,
        ))
    dark_layout(fig, "Boxplot — توزيع أعداد الطلاب المستجدين حسب السنة", h=420)
    fig.update_layout(
        yaxis=dict(gridcolor=DARK_GRID, color=DARK_AXIS),
        xaxis=dict(showgrid=False, color=DARK_AXIS),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Outlier rows table
    st.markdown(" الصفوف الشاذة")
    st.dataframe(
        outliers[[Y, 'المنطقة الإدارية', 'الجهة التعليمية', 'المجال الواسع', 'الجنس', 'العدد']]
        .sort_values('العدد', ascending=False)
        .reset_index(drop=True),
        use_container_width=True,
        height=300,
    )

    insight("استنتاجات — الشذوذات", [
        f"الحد الأعلى وفق IQR هو <span class='highlight-gold'>{upper_bound:.0f} طالباً</span> — أي صف يتجاوزه يُعدّ شاذاً إحصائياً.",
        f"تم رصد <span class='highlight-down'>{len(outliers):,} صفاً شاذاً</span> من أصل <span class='highlight-gold'>{len(fdf):,}</span> ({len(outliers)/len(fdf)*100:.1f}٪)، وتمثّل مؤسسات كبيرة أو تخصصات ذات إقبال استثنائي.",
        "يمكن استبعاد هذه الصفوف عند الحاجة لتحليل نمط التوزيع العام دون تأثير القيم المتطرفة.",
    ])

#  tab 2: التغير حسب المجال 
with tabs[2]:
   
    fld_raw = fdf.groupby([Y, FLD])[CNT].sum().reset_index()
    fld_raw[PCT] = fld_raw.apply(lambda r: pct(r[CNT], annual_total.get(r[Y], 1)), axis=1)
    fld_raw[Y]   = fld_raw[Y].astype(str)
    field_order  = fdf.groupby(FLD)[CNT].sum().sort_values(ascending=True).index.tolist()

    fp = fdf.groupby([Y, FLD])[CNT].sum().unstack(fill_value=0)
    for yr_ in YEARS:
        if yr_ not in fp.index: fp.loc[yr_] = 0
    fp = fp.sort_index()

    # row 1
    fig = px.bar(
        fld_raw, x=PCT, y=FLD, color=Y, barmode="group", orientation="h",
        title="نسبة الطلاب (٪ من إجمالي العام) حسب المجال",
        labels={PCT: "النسبة ٪", FLD: "", Y: "السنة"},
        color_discrete_map={"2021": YC[2021], "2022": YC[2022], "2023": YC[2023]},
        category_orders={FLD: field_order},
    )
    fig.update_traces(texttemplate="%{x:.1f}٪", textposition="outside",
                      textfont_size=10, textfont_color=DARK_TEXT)
    dark_layout(fig, "نسبة الطلاب (٪ من إجمالي العام) حسب المجال", h=460, ml=230, mr=60)
    fig.update_layout(
        xaxis=dict(gridcolor=DARK_GRID, color=DARK_AXIS, ticksuffix="٪"),
        yaxis=dict(showgrid=False, color=DARK_AXIS),
    )
    st.plotly_chart(fig, use_container_width=True)

    # row 2
    fld_yr = fdf.groupby([Y, FLD])[CNT].sum().reset_index()
    fld_yr[PCT] = fld_yr.apply(lambda r: pct(r[CNT], annual_total.get(r[Y], 1)), axis=1)
    palette = px.colors.qualitative.Bold
    fields  = sorted(fld_yr[FLD].unique().tolist())

    fig = go.Figure()
    for i, field in enumerate(fields):
        sub   = fld_yr[fld_yr[FLD] == field].sort_values(Y)
        color = palette[i % len(palette)]
        xs = sub[Y].tolist(); ys = sub[PCT].tolist()
        fig.add_scatter(
            x=xs, y=ys, mode="lines+markers", name=field,
            line=dict(color=color, width=2.5), marker=dict(size=9), showlegend=False,
        )
        if xs:
            fig.add_annotation(
                x=2023, y=ys[-1], text=f"<b>{field}</b>",
                xref="x", yref="y", xanchor="left", yanchor="middle", xshift=12,
                showarrow=False, font=dict(size=10, color=color, family=FONT),
                bgcolor="rgba(13,21,38,0.6)", borderpad=2,
            )
    dark_layout(fig, "مسار الحصة النسبية (٪) لكل مجال دراسي — ٢٠٢١ إلى ٢٠٢٣", h=500, ml=60, mr=20)
    fig.update_layout(
        xaxis=dict(showgrid=False, tickvals=YEARS, ticktext=["٢٠٢١","٢٠٢٢","٢٠٢٣"],
                   color=DARK_AXIS, range=[2020.6, 2025.0]),
        yaxis=dict(gridcolor=DARK_GRID, color=DARK_AXIS, ticksuffix="٪"),
    )
    st.plotly_chart(fig, use_container_width=True)

    
    insight("استنتاجات — الوزن النسبي للمجالات ومساراتها ٢٠٢١ ← ٢٠٢٣", [
        "المخطط الأول يُسهّل <strong>مقارنة المجالات مع بعضها</strong> في كل عام، بينما يكشف المخطط الثاني <strong>اتجاه كل مجال عبر الزمن</strong> — معاً يُقدّمان صورة هيكلية كاملة.",
        "مجال <span class='highlight-gold'>الأعمال والإدارة والقانون</span> يستحوذ على نحو <span class='highlight-gold'>20٪</span> باستمرار، وهو ما يبدو واضحاً في ثبات شريطه في الأول واستقرار منحناه في الثاني.",
        "حصة <span class='highlight-up'>تقنية الاتصالات والمعلومات</span> تضاعفت من <span class='highlight-gold'>4.8٪</span> إلى <span class='highlight-up'>10.0٪</span> — المنحنى الصاعد في الثاني يؤكد أن هذا النمو متواصل وليس قفزة عارضة.",
        "منحنى <span class='highlight-down'>الفنون والإنسانيات</span> هو الأشد هبوطاً في الرسم البياني الثاني، ويُترجَم في الأول إلى تضيّق شريطه من <span class='highlight-gold'>26.4٪</span> إلى <span class='highlight-down'>13.2٪</span> — أي فقد نصف وزنه النسبي خلال عامين.",
    ])

    # Net Δ% bar
    fp = fdf.groupby([Y, FLD])[CNT].sum().unstack(fill_value=0)
    for yr_ in YEARS:
        if yr_ not in fp.index: fp.loc[yr_] = 0
    fp = fp.sort_index()

    pct_df = pd.DataFrame({"المجال": fp.columns})
    for yr_ in YEARS:
        tot = annual_total.get(yr_, 1)
        pct_df[str(yr_)] = (fp.loc[yr_].values / tot * 100).round(2)
    pct_df["Δ٪ ٢٠٢١←٢٠٢٣"] = (pct_df["2023"] - pct_df["2021"]).round(2)
    pct_df = pct_df.sort_values("Δ٪ ٢٠٢١←٢٠٢٣")

    colors = ["#2ECC71" if v >= 0 else "#E74C3C" for v in pct_df["Δ٪ ٢٠٢١←٢٠٢٣"]]
    fig = go.Figure(go.Bar(
        x=pct_df["Δ٪ ٢٠٢١←٢٠٢٣"], y=pct_df["المجال"], orientation="h",
        marker_color=colors,
        text=[f"{'+' if v>0 else ''}{v:.2f}٪" for v in pct_df["Δ٪ ٢٠٢١←٢٠٢٣"]],
        textposition="outside", textfont_size=12, textfont_color=DARK_TEXT,
    ))
    fig.add_vline(x=0, line_color="rgba(255,255,255,0.4)", line_width=1.5)
    dark_layout(fig, "صافي التغير في الحصة النسبية ٢٠٢١ ← ٢٠٢٣ (نقاط مئوية)", h=460, ml=230, mr=90)
    fig.update_layout(
        xaxis=dict(gridcolor=DARK_GRID, zeroline=False, color=DARK_AXIS, ticksuffix="٪"),
        yaxis=dict(showgrid=False, color=DARK_AXIS),
    )
    st.plotly_chart(fig, use_container_width=True)

    insight("استنتاجات — صافي التغير النسبي ٢٠٢١ ← ٢٠٢٣", [
        "خسر مجال <span class='highlight-down'>الفنون والإنسانيات</span> ما يقارب <span class='highlight-down'>13 نقطة مئوية</span> من حصته، وهو أكبر تراجع نسبي على الإطلاق.",
        "كسب مجال <span class='highlight-up'>تقنية الاتصالات والمعلومات</span> نحو <span class='highlight-up'>5 نقاط مئوية</span>، يليه <span class='highlight-up'>الصحة والرفاه</span> بزيادة ملموسة.",
        "التحوّل النسبي يعكس إعادة توزيع هيكلية حقيقية في تفضيلات الطلاب، وليس مجرد تغيّر في الأحجام المطلقة.",
    ])

#  tab 3: أكثر المجالات نمواً وتراجعاً 
with tabs[3]:
    fp2 = fdf.groupby([Y, FLD])[CNT].sum().unstack(fill_value=0)
    for yr_ in YEARS:
        if yr_ not in fp2.index: fp2.loc[yr_] = 0
    fp2 = fp2.sort_index()

    t21_tot = annual_total.get(2021, 1); t23_tot = annual_total.get(2023, 1)
    change_pct = pd.DataFrame({"المجال": fp2.columns})
    change_pct["٢٠٢١٪"] = (fp2.loc[2021].values / t21_tot * 100).round(2)
    change_pct["٢٠٢٣٪"] = (fp2.loc[2023].values / t23_tot * 100).round(2)
    change_pct["Δ٪"]    = (change_pct["٢٠٢٣٪"] - change_pct["٢٠٢١٪"]).round(2)

    gainers = change_pct.nlargest(5, "Δ٪")
    losers  = change_pct.nsmallest(5, "Δ٪")
    palette = px.colors.qualitative.Bold

    fig = go.Figure()
    for i, (_, row) in enumerate(gainers.iterrows()):
        fig.add_scatter(
            x=[2021, 2023], y=[row["٢٠٢١٪"], row["٢٠٢٣٪"]],
            mode="lines+markers+text", name=row["المجال"],
            line=dict(width=2.5, color=palette[i % len(palette)]), marker=dict(size=10),
            text=[f"{row['٢٠٢١٪']:.1f}٪", f"{row['٢٠٢٣٪']:.1f}٪  {'+' if row['Δ٪']>0 else ''}{row['Δ٪']:.1f}نق"],
            textposition=["middle left", "middle right"],
            textfont_size=11, textfont_color=DARK_TEXT,
        )
    dark_layout(fig, "📈 أكثر ٥ مجالات نمواً في الحصة النسبية", h=380, ml=20, mr=180)
    fig.update_layout(
        xaxis=dict(showgrid=False, tickvals=[2021,2023], ticktext=["٢٠٢١","٢٠٢٣"], color=DARK_AXIS),
        yaxis=dict(gridcolor=DARK_GRID, color=DARK_AXIS, ticksuffix="٪"),
        legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="center", x=0.5, font_size=11, font_color=DARK_TEXT, bgcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig, use_container_width=True)

    insight("استنتاجات — أكثر المجالات نمواً (نسبياً)", [
        "<span class='highlight-up'>تقنية الاتصالات والمعلومات</span> قفزت حصتها من <span class='highlight-gold'>4.8٪</span> إلى <span class='highlight-up'>10.0٪</span>، أي مكسب <span class='highlight-up'>+5.2 نقطة مئوية</span> وهو الأعلى بين جميع المجالات.",
        "<span class='highlight-up'>الصحة والرفاه</span> رفعت حصتها بمقدار <span class='highlight-up'>+4.6 نقطة</span>، وهو نمو مستدام يعكس التوسّع في البنية التحتية الصحية ورؤية ٢٠٣٠.",
        "النمو النسبي لهذه المجالات يُثبت أن التحوّل نحو التقنية والصحة ليس مجرد أثر لزيادة الأحجام، بل توجّه هيكلي حقيقي.",
    ])

    fig = go.Figure()
    for i, (_, row) in enumerate(losers.iterrows()):
        fig.add_scatter(
            x=[2021, 2023], y=[row["٢٠٢١٪"], row["٢٠٢٣٪"]],
            mode="lines+markers+text", name=row["المجال"],
            line=dict(width=2.5, dash="dot", color=palette[i % len(palette)]), marker=dict(size=10),
            text=[f"{row['٢٠٢١٪']:.1f}٪", f"{row['٢٠٢٣٪']:.1f}٪  {row['Δ٪']:.1f}نق"],
            textposition=["middle left", "middle right"],
            textfont_size=11, textfont_color=DARK_TEXT,
        )
    dark_layout(fig, "📉 أكثر ٥ مجالات تراجعاً في الحصة النسبية", h=380, ml=20, mr=180)
    fig.update_layout(
        xaxis=dict(showgrid=False, tickvals=[2021,2023], ticktext=["٢٠٢١","٢٠٢٣"], color=DARK_AXIS),
        yaxis=dict(gridcolor=DARK_GRID, color=DARK_AXIS, ticksuffix="٪"),
        legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="center", x=0.5, font_size=11, font_color=DARK_TEXT, bgcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig, use_container_width=True)

    insight("استنتاجات — أكثر المجالات تراجعاً (نسبياً)", [
        "<span class='highlight-down'>الفنون والعلوم الإنسانية</span> خسرت <span class='highlight-down'>13.1 نقطة مئوية</span> من حصتها (من 26.4٪ إلى 13.3٪)، أي فقدت نصف وزنها النسبي خلال عامين.",
        "<span class='highlight-down'>البرامج العامة والمؤهلات</span> تراجعت بـ <span class='highlight-down'>10.1 نقطة</span>، مؤكدةً أن الطلاب يبتعدون عن التخصصات غير المحددة.",
        "مجتمعاً خسر هذان المجالان ما يقارب <span class='highlight-down'>23 نقطة مئوية</span>، وهي الحصة التي التهمتها مجالات التقنية والصحة والهندسة.",
    ])


#  tab 4: التغير الإقليمي 
with tabs[4]:
    reg_raw = fdf.groupby([Y, REG])[CNT].sum().reset_index()
    reg_raw[PCT] = reg_raw.apply(lambda r: pct(r[CNT], annual_total.get(r[Y], 1)), axis=1)
    reg_raw[Y]   = reg_raw[Y].astype(str)
    reg_order    = fdf.groupby(REG)[CNT].sum().sort_values(ascending=True).index.tolist()

    fig = px.bar(
        reg_raw, x=PCT, y=REG, color=Y, barmode="group", orientation="h",
        title="نسبة الطلاب (٪ من إجمالي العام) حسب المنطقة",
        labels={PCT: "النسبة ٪", REG: "", Y: "السنة"},
        color_discrete_map={"2021": YC[2021], "2022": YC[2022], "2023": YC[2023]},
        category_orders={REG: reg_order},
    )
    fig.update_traces(texttemplate="%{x:.1f}٪", textposition="outside",
                      textfont_size=10, textfont_color=DARK_TEXT)
    dark_layout(fig, "نسبة الطلاب (٪ من إجمالي العام) حسب المنطقة", h=480, ml=175, mr=60)
    fig.update_layout(
        xaxis=dict(gridcolor=DARK_GRID, color=DARK_AXIS, ticksuffix="٪"),
        yaxis=dict(showgrid=False, color=DARK_AXIS),
    )
    st.plotly_chart(fig, use_container_width=True)

    insight("استنتاجات — الوزن الإقليمي النسبي", [
        "<span class='highlight-gold'>منطقة مكة المكرمة</span> تستحوذ على ما بين <span class='highlight-gold'>29٪ و30٪</span> من إجمالي المستجدين في كل عام، محتفظةً بالصدارة المطلقة.",
        "<span class='highlight-up'>منطقة الرياض</span> رفعت حصتها من <span class='highlight-gold'>17٪</span> إلى <span class='highlight-up'>19.4٪</span> عام ٢٠٢٢ قبل أن تستقر عام ٢٠٢٣، مما يعكس قوة جذبها المتنامية.",
        "<span class='highlight-down'>منطقة الجوف</span> و<span class='highlight-down'>منطقة القصيم</span> شهدتا تراجعاً ملحوظاً في حصتهما النسبية، مما قد يشير إلى هجرة الطلاب نحو مناطق ذات عروض أكاديمية أوسع.",
    ])

    # Heatmap 
    rp = fdf.groupby([Y, REG])[CNT].sum().unstack(fill_value=0)
    pct_reg = pd.DataFrame(index=rp.columns)
    for yr_ in YEARS:
        tot = annual_total.get(yr_, 1)
        pct_reg[yr_] = (rp.loc[yr_] / tot * 100).round(2) if yr_ in rp.index else 0

    delta_reg = pd.DataFrame(index=rp.columns)
    if 2021 in rp.index and 2022 in rp.index:
        delta_reg["٢٠٢١←٢٠٢٢"] = (pct_reg[2022] - pct_reg[2021]).round(2)
    if 2022 in rp.index and 2023 in rp.index:
        delta_reg["٢٠٢٢←٢٠٢٣"] = (pct_reg[2023] - pct_reg[2022]).round(2)
    if 2021 in rp.index and 2023 in rp.index:
        delta_reg["٢٠٢١←٢٠٢٣"] = (pct_reg[2023] - pct_reg[2021]).round(2)

    fig = go.Figure(go.Heatmap(
        z=delta_reg.values, x=delta_reg.columns.tolist(), y=delta_reg.index.tolist(),
        colorscale=[[0,"#C0392B"],[0.5,"#1A2035"],[1,"#1E8449"]],
        zmid=0,
        hovertemplate="<b>%{y}</b><br>%{x}<br>Δ٪: <b>%{z:+.2f}٪</b><extra></extra>",
        colorbar=dict(title="Δ٪", tickfont_color=DARK_TEXT, titlefont_color=DARK_TEXT),
        text=delta_reg.values, texttemplate="%{z:+.2f}٪",
        textfont_size=11, textfont_color=DARK_TEXT,
    ))
    dark_layout(fig, "صافي التغير في الحصة النسبية (نقاط مئوية) حسب المنطقة", h=480, ml=175, mr=20)
    st.plotly_chart(fig, use_container_width=True)

    insight("استنتاجات — خريطة التغير الإقليمي النسبي", [
        "الألوان الحمراء في عمود <span class='highlight-down'>٢٠٢٢←٢٠٢٣</span> تسود في معظم المناطق، مُثبتةً أن التراجع الحاد تمركز في هذه الفترة بالذات.",
        "<span class='highlight-up'>منطقة الرياض</span> هي الوحيدة بميزان إيجابي في العمود الإجمالي، مما يُرسّخ مكانتها كوجهة التعليم الأولى والأسرع نمواً.",
        "<span class='highlight-down'>منطقة الجوف</span> تظهر باللون الأحمر في كلا العمودين دون تعافٍ، مما يستوجب مراجعة القدرة الاستيعابية لمؤسساتها التعليمية.",
    ])

# tab 5: مستجد مقابل خريج 
with tabs[5]:
    @st.cache_data
    def load_status_comparison():
        df_full = pd.read_csv("csvfiles/main_dataset.csv")
        return df_full[
            (df_full["المرحلة الدراسية"] == "بكالوريوس") &
            (df_full["حالة_الطالب"].isin(["مستجد", "خريج"]))
        ].copy()

    df_status = load_status_comparison()
    df_status = df_status[
        df_status[REG].isin(sel_reg) & df_status[GEN].isin(sel_gen) & df_status[NAT].isin(sel_nat)
    ]
    status_annual = df_status.groupby(Y)[CNT].sum()

    sts_long = df_status.groupby([Y, STS])[CNT].sum().reset_index()
    sts_long[PCT] = sts_long.apply(lambda r: pct(r[CNT], status_annual.get(r[Y], 1)), axis=1)
    sts_long[Y]   = sts_long[Y].astype(str)

    fig = px.bar(
        sts_long, x=Y, y=PCT, color=STS, barmode="group",
        title="نسبة المستجدين مقابل الخريجين (٪ من مجموع الحالتين) لكل عام",
        labels={PCT: "النسبة ٪", Y: "السنة", STS: "الحالة"},
        color_discrete_map={"مستجد": "#4DA6FF", "خريج": "#2ECC71"},
        text=PCT,
    )
    fig.update_traces(texttemplate="%{text:.1f}٪", textposition="outside",
                      textfont_size=11, textfont_color=DARK_TEXT)
    dark_layout(fig, "نسبة المستجدين مقابل الخريجين لكل عام", h=400, ml=20, mr=20)
    fig.update_layout(
        xaxis=dict(showgrid=False, color=DARK_AXIS),
        yaxis=dict(gridcolor=DARK_GRID, range=[0, sts_long[PCT].max()*1.2],
                   color=DARK_AXIS, ticksuffix="٪"),
    )
    st.plotly_chart(fig, use_container_width=True)

    insight("استنتاجات — المستجدون مقابل الخريجون (نسبي)", [
        "عام ٢٠٢١ كان الخريجون يمثّلون <span class='highlight-down'>52.6٪</span> مقابل <span class='highlight-gold'>47.4٪</span> للمستجدين، أي أن الخريجين يفوقون الداخلين الجدد.",
        "انعكست المعادلة جذرياً عام ٢٠٢٢: المستجدون <span class='highlight-up'>55.4٪</span> مقابل الخريجين <span class='highlight-down'>44.6٪</span>، مما يعني موجة قبول واسعة.",
        "عام ٢٠٢٣ استمر تفوّق المستجدين (<span class='highlight-up'>53.1٪</span>) على الخريجين (<span class='highlight-down'>46.9٪</span>)، مشيراً إلى استمرار تراجع معدلات التخرج.",
    ])

   
    sts_yr = df_status.groupby([Y, STS])[CNT].sum().unstack(fill_value=0).reset_index()
    sts_yr.columns.name = None
    new_pct = []; grad_pct = []
    for yr_ in YEARS:
        row = sts_yr[sts_yr[Y] == yr_]
        s_tot = status_annual.get(yr_, 1)
        nv = int(row["مستجد"].values[0]) if len(row) and "مستجد" in row.columns else 0
        gv = int(row["خريج"].values[0])  if len(row) and "خريج"  in row.columns else 0
        new_pct.append(round(nv / s_tot * 100, 1))
        grad_pct.append(round(gv / s_tot * 100, 1))
    gap_pct = [n - g for n, g in zip(new_pct, grad_pct)]

    fig = go.Figure()
    fig.add_scatter(
        x=YEARS + YEARS[::-1], y=new_pct + grad_pct[::-1],
        fill="toself", fillcolor="rgba(77,166,255,0.08)",
        line=dict(color="rgba(0,0,0,0)"), showlegend=False, hoverinfo="skip",
    )
    fig.add_scatter(
        x=YEARS, y=new_pct, mode="lines+markers+text", name="مستجد",
        line=dict(color="#4DA6FF", width=3), marker=dict(size=11),
        text=[f"{v:.1f}٪" for v in new_pct],
        textposition="top center", textfont_size=12, textfont_color=DARK_TEXT,
    )
    fig.add_scatter(
        x=YEARS, y=grad_pct, mode="lines+markers+text", name="خريج",
        line=dict(color="#2ECC71", width=3), marker=dict(size=11),
        text=[f"{v:.1f}٪" for v in grad_pct],
        textposition="bottom center", textfont_size=12, textfont_color=DARK_TEXT,
    )
    for i, yr_ in enumerate(YEARS):
        g = gap_pct[i]; clr = "#4DA6FF" if g > 0 else "#E74C3C"
        sign = "▲ فائض" if g > 0 else "▼ عجز"
        fig.add_annotation(
            x=yr_, y=(new_pct[i] + grad_pct[i]) / 2,
            text=f'<b style="color:{clr}">{sign} {abs(g):.1f}٪</b>',
            showarrow=False, font_size=11, font_family=FONT, xshift=55,
        )
    dark_layout(fig, "الفجوة النسبية بين المستجدين والخريجين (نقاط مئوية)", h=400, ml=20, mr=20)
    fig.update_layout(
        xaxis=dict(showgrid=False, tickvals=YEARS, ticktext=["٢٠٢١","٢٠٢٢","٢٠٢٣"], color=DARK_AXIS),
        yaxis=dict(gridcolor=DARK_GRID, color=DARK_AXIS, ticksuffix="٪"),
    )
    st.plotly_chart(fig, use_container_width=True)

    insight("استنتاجات — الفجوة النسبية بين المستجدين والخريجين", [
        "تحوّل الميزان من <span class='highlight-down'>عجز 5.2 نقطة</span> لصالح الخريجين عام ٢٠٢١ إلى <span class='highlight-up'>فائض 10.8 نقطة</span> لصالح المستجدين عام ٢٠٢٢.",
        "استمر الفائض عام ٢٠٢٣ بـ <span class='highlight-up'>6.2 نقطة</span>، غير أن تضيّق الفجوة يعني تقارباً تدريجياً بين الحالتين.",
        "الاتجاه التنازلي في أعداد الخريجين يستدعي مراجعة نسب الإتمام والاحتفاظ بالطلاب داخل المنظومة الجامعية.",
    ])