import streamlit as st
from load_data import load_data

def display_summary(filtered_df):
    st.header("Summary")
    cols = st.columns(5)
    metrics = [
        ("Distinct Suppliers", filtered_df['Supplier'].nunique()),
        ("Distinct MPNs", filtered_df['MPN'].nunique()),
        # Assuming each component has exactly one UOM and ECCN Classification
        ("UOM", filtered_df['UOM'].iloc[0]),
        ("ECCN Classification", filtered_df['ECCN Classification'].iloc[0]),
        ("Total Future Spend", f"${filtered_df['Future Spend (Price Main * Forecast)'].sum():,.0f}")
    ]
    for col, (label, value) in zip(cols, metrics):
        with col:
            st.metric(label=label, value=value)

def display_details(filtered_df):
    st.header("Data for this part")
    # Define which columns to disable: all except 'Product'
    disabled_columns = ["Source/Date", "Component Name", "LHX Part Number", "MPN", "UOM", 
                        "Sprint", "Description (Forecast)", "Description (Spend Cube)", 
                        "Description (BOM)", "Description (Main)", "Supplier", 
                        "ECCN Classification", "Filename (BOM)", "Historical Price (BOM)", 
                        "Historical Price (Spend Cube)", "Historical Price (Forecast)", 
                        "Historical Price (Main)", "Overhead Cost (BOM)", 
                        "Historical Volume (BOM)", "Historical Volume (Spend Cube)", 
                        "Volume (Forecast)", "Future Spend (Price Main * Forecast)"]
    st.data_editor(data=filtered_df, disabled=disabled_columns)

def app():
    st.title("Part Explorer")
    st.subheader("Search for a part to view a summary of details and relevant data")

    df = load_data()

    # Dropdown to select the component name
    component_options = df['Component Name'].dropna().unique().tolist()
    component_name = st.selectbox("Search for Part:", [""] + component_options)
    if component_name:
        filtered_df = df[df['Component Name'] == component_name]
        if not filtered_df.empty:
            display_summary(filtered_df)
            display_details(filtered_df)
        else:
            st.write("No matching parts found.")
    else:
        st.write("Please select a part name to see the details.")
