# dashboard2.py
import streamlit as st
from load_data import load_data

def display_summary(filtered_df):
    st.header("Summary")
    cols = st.columns(5)
    
    # Assuming there's one sector with the most future spend and one product with the most future spend for simplicity
    largest_sector_by_spend = filtered_df.groupby('Sector')['Future Spend (Price Main * Forecast)'].sum().idxmax()
    largest_product_by_spend = filtered_df.loc[filtered_df['Future Spend (Price Main * Forecast)'].idxmax(), 'Product']

    metrics = [
        ("Unique Parts", filtered_df['LHX Part Number'].nunique()),
        ("Largest Sector by Spend", largest_sector_by_spend),
        ("Unique Products", filtered_df['Product'].nunique()),
        ("Largest Product by Spend", largest_product_by_spend),
        ("Total Future Spend", f"${filtered_df['Future Spend (Price Main * Forecast)'].sum():,.0f}")
    ]
    for col, (label, value) in zip(cols, metrics):
        with col:
            st.metric(label=label, value=value)

def display_details(filtered_df):
    st.header("Data for this supplier")
    # Define which columns to disable: assuming all columns should be disabled for editing
    disabled_columns = {col: True for col in filtered_df.columns}
    st.data_editor(data=filtered_df, disabled=disabled_columns)

def app():
    st.title("Supplier Explorer")
    st.subheader("Search for a supplier to view a summary of details and relevant data")

    df = load_data()

    # Dropdown to select the supplier name
    supplier_options = df['Supplier'].dropna().unique().tolist()
    supplier_name = st.selectbox("Search for Supplier Name:", [""] + supplier_options)
    if supplier_name:
        filtered_df = df[df['Supplier'] == supplier_name]
        if not filtered_df.empty:
            display_summary(filtered_df)
            display_details(filtered_df)
        else:
            st.write("No matching suppliers found.")
    else:
        st.write("Please select a supplier name to see the details.")
