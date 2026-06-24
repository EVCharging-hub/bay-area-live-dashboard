import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Bay Area Electrification Incentives Dashboard",
    layout="wide"
)

DATA_FILE = Path(__file__).parent / "bay_area_electrification_incentive_dashboard.xlsx"

@st.cache_data
def load_data():
    xls = pd.ExcelFile(DATA_FILE)
    sheets = {name: pd.read_excel(DATA_FILE, sheet_name=name) for name in xls.sheet_names}
    return sheets

sheets = load_data()

st.title("Bay Area Electrification Incentives Dashboard")
st.caption("Interactive dashboard for electrification programs, rebates, incentives, and utility territory mapping.")

# Try common sheet names, otherwise fall back to first sheet
matrix_sheet_name = None
for candidate in ["Incentive_Matrix", "Incentives", "Programs", "Matrix"]:
    if candidate in sheets:
        matrix_sheet_name = candidate
        break
if matrix_sheet_name is None:
    matrix_sheet_name = list(sheets.keys())[0]

df = sheets[matrix_sheet_name].copy()
df.columns = [str(c).strip() for c in df.columns]

st.sidebar.header("Filters")

def filter_if_column(label, possible_cols):
    for col in possible_cols:
        if col in df.columns:
            values = sorted([x for x in df[col].dropna().unique()])
            selected = st.sidebar.multiselect(label, values)
            if selected:
                return df[col].isin(selected)
            return pd.Series(True, index=df.index)
    return pd.Series(True, index=df.index)

mask = pd.Series(True, index=df.index)
mask &= filter_if_column("Technology", ["Technology", "Technology Category", "Measure"])
mask &= filter_if_column("Customer Type", ["Customer Type", "Customer Segment", "Segment"])
mask &= filter_if_column("City", ["City", "Cities", "Applicable City"])
mask &= filter_if_column("Utility / IOU", ["Utility (IOU)", "Utility", "Utility Territory", "Electric Utility"])
mask &= filter_if_column("CCA / Local Provider", ["CCA / Local Provider", "CCA", "Local Provider"])
mask &= filter_if_column("Program Status", ["Status", "Program Status"])
mask &= filter_if_column("Program Type", ["Program Type", "Incentive Type", "Type"])

filtered = df[mask].copy()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Visible Programs", len(filtered))
kpi2.metric("Total Programs", len(df))
if "Technology" in df.columns:
    kpi3.metric("Technologies", filtered["Technology"].nunique())
else:
    kpi3.metric("Technologies", "—")
if "City" in df.columns:
    kpi4.metric("Cities", filtered["City"].nunique())
else:
    kpi4.metric("Cities", "—")

st.subheader("Incentive Matrix")
st.dataframe(filtered, use_container_width=True, hide_index=True)

csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download filtered results as CSV",
    data=csv,
    file_name="bay_area_filtered_incentives.csv",
    mime="text/csv"
)

st.divider()

if "City_Territories" in sheets:
    st.subheader("City / Utility Territory Mapping")
    city_df = sheets["City_Territories"].copy()
    city_df.columns = [str(c).strip() for c in city_df.columns]
    st.dataframe(city_df, use_container_width=True, hide_index=True)

with st.expander("Available workbook sheets"):
    st.write(list(sheets.keys()))

with st.expander("Data source"):
    st.write(f"Loaded from: `{DATA_FILE.name}`")
