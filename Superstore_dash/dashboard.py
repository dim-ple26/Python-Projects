import streamlit as st 
import plotly.express as px 
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

# Streamlit configuration
st.set_page_config(page_title="Superstore", page_icon=":bar_chart:", layout="wide")
st.title(":bar_chart: Sample Superstore EDA")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

# File uploader or fallback to default
fl = st.file_uploader(":file_folder: Upload a file", type=["csv", "txt", "xlsx", "xls"])
if fl is not None:
    df = pd.read_csv(fl, encoding="ISO-8859-1")
else:
    os.chdir(r"D:\python projects\Superstore_dash")
    df = pd.read_csv("Superstore.csv", encoding="ISO-8859-1")

# Clean and standardize column names
df.columns = df.columns.str.strip().str.lower()

# Date filtering
col1, col2 = st.columns((2))
df["order date"] = pd.to_datetime(df["order date"])

start_date = df["order date"].min()
end_date = df["order date"].max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start date", start_date))
with col2:
    date2 = pd.to_datetime(st.date_input("End date", end_date))

filtered_df = df[(df["order date"] >= date1) & (df["order date"] <= date2)].copy()

# Sidebar filters
st.sidebar.header("Choose Your Filter:")
region = st.sidebar.multiselect("Pick your Region", filtered_df["region"].unique())
state = st.sidebar.multiselect("Pick the State", filtered_df["state"].unique())
city = st.sidebar.multiselect("Pick the City", filtered_df["city"].unique())

# Filter data based on sidebar selections
if region:
    filtered_df = filtered_df[filtered_df["region"].isin(region)]
if state:
    filtered_df = filtered_df[filtered_df["state"].isin(state)]
if city:
    filtered_df = filtered_df[filtered_df["city"].isin(city)]

# Grouped data for Category Sales
if "sales" not in filtered_df.columns or "category" not in filtered_df.columns:
    st.error("Required columns 'Sales' or 'Category' are missing. Please check your data.")
    st.stop()

category_df = filtered_df.groupby(by="category", as_index=False)["sales"].sum()

# Category Sales Bar Chart
col1, col2 = st.columns(2)
with col1:
    st.subheader("Category Wise Sales")
    fig = px.bar(category_df, x="category", y="sales",
                 text=['${:,.2f}'.format(x) for x in category_df["sales"]],
                 template="seaborn")
    st.plotly_chart(fig, use_container_width=True)

# Region Wise Sales Pie Chart
with col2:
    st.subheader("Region Wise Sales")
    region_sales = filtered_df.groupby(by="region", as_index=False)["sales"].sum()
    fig = px.pie(region_sales, values="sales", names="region", hole=0.5)
    fig.update_traces(textposition="outside", textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True)

# Time Series Analysis
st.subheader("Time Series Analysis")
filtered_df["month_year"] = filtered_df["order date"].dt.to_period("M")
linechart = filtered_df.groupby(filtered_df["month_year"].astype(str))["sales"].sum().reset_index()
linechart.rename(columns={"sales": "Total Sales", "month_year": "Month-Year"}, inplace=True)

fig2 = px.line(linechart, x="Month-Year", y="Total Sales",
               labels={"Total Sales": "Sales Amount"}, template="plotly", height=500)
st.plotly_chart(fig2, use_container_width=True)

# TreeMap
st.subheader(":tree_map: Hierarchical view of Sales")
fig3 = px.treemap(filtered_df, path=["region", "category", "sub-category"],
                  values="sales", color="sub-category", hover_data=["sales"])
fig3.update_layout(margin=dict(t=25, l=0, r=0, b=25))
st.plotly_chart(fig3, use_container_width=True)

# Segment and Category Wise Sales
chart1, chart2 = st.columns(2)
with chart1:
    st.subheader(":pie_chart: Segment Wise Sales")
    fig = px.pie(filtered_df, values="sales", names="segment", template="plotly_dark")
    fig.update_traces(textposition="outside", textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True)

with chart2:
    st.subheader(":pie_chart: Category Wise Sales")
    fig = px.pie(filtered_df, values="sales", names="category", template="gridon")
    fig.update_traces(textposition="outside", textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True)

# Summary Table
st.subheader(":point_right: Month Wise Sub-Category Sales Summary")
with st.expander("Summary Table"):
    filtered_df["month"] = filtered_df["order date"].dt.month_name()
    sub_category_summary = pd.pivot_table(data=filtered_df, values="sales",
                                          index=["sub-category"], columns="month", aggfunc="sum")
    st.write(sub_category_summary.style.background_gradient(cmap="Blues"))

# Scatter Plot
st.subheader("Relationship Between Sales and Profits")
scatter_fig = px.scatter(filtered_df, x="sales", y="profit", size="quantity",
                         title="Relationship between Sales and Profits", template="plotly")
st.plotly_chart(scatter_fig, use_container_width=True)

# Download Data
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("Download Filtered Data", data=csv, file_name="Filtered_Superstore.csv", mime="text/csv")
