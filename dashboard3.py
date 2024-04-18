import streamlit as st

# dashboard3.py
import streamlit as st
from load_data import load_data

def display_summary(filtered_df):
    st.header("Summary")
    cols = st.columns(3)

    # Calculate the metrics
    unique_products = filtered_df['Product'].nunique()
    product_with_top_spend = filtered_df.groupby('Product')['Future Spend (Price Main * Forecast)'].sum().idxmax()
    product_with_top_quantity = filtered_df.groupby('Product')['Volume (Forecast)'].sum().idxmax()

    metrics = [
        ("Unique Products", unique_products),
        ("Largest Product by Spend", product_with_top_spend),
        ("Largest Product by Quantity", product_with_top_quantity)
    ]
    for col, (label, value) in zip(cols, metrics):
        with col:
            st.metric(label=label, value=value)

def display_details(filtered_df):
    st.header("Data for this part")

    # Group by Product and calculate sums of numeric columns
    product_grouped = filtered_df.groupby('Product').agg({
        'Future Spend (Price Main * Forecast)': 'sum',
        'Volume (Forecast)': 'sum',
        # Add other aggregations for columns of interest here
    }).reset_index()

    # Define which columns to disable: assuming all columns should be disabled for editing
    disabled_columns = {col: True for col in product_grouped.columns}
    st.data_editor(data=product_grouped, disabled=disabled_columns)

def app():
    st.title("Product Explorer")
    st.subheader("Search for a part to view a summary of products and relevant data")

    df = load_data()

    # Dropdown to select the part name
    part_options = df['Component Name'].dropna().unique().tolist()
    part_name = st.selectbox("Search for Part Name:", [""] + part_options)
    if part_name:
        filtered_df = df[df['Component Name'] == part_name]
        if not filtered_df.empty:
            display_summary(filtered_df)
            display_details(filtered_df)
        else:
            st.write("No matching parts found.")
    else:
        st.write("Please select a part name to see the details.")
