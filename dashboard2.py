# dashboard2.py
import streamlit as st
import plotly.express as px
from load_data import load_data

def create_pareto_chart(df, supplier_name, height=None):
    # Filter data for the selected supplier
    supplier_data = df[df['Supplier'] == supplier_name]
    
    # Assuming 'Part Number' column contains the part data
    # Group by part and sum the spend
    spend_per_part = supplier_data.groupby('LHX Part Number', as_index=False)['Future Spend (Price Main * Forecast)'].sum()
    
    # Sort parts by spend and take top 10
    spend_per_part = spend_per_part.sort_values(by='Future Spend (Price Main * Forecast)', ascending=False).head(10)
    
    # Calculate cumulative spend
    spend_per_part['cumulative_spend'] = spend_per_part['Future Spend (Price Main * Forecast)'].cumsum()
    spend_per_part['cumulative_percentage'] = 100 * spend_per_part['cumulative_spend'] / spend_per_part['Future Spend (Price Main * Forecast)'].sum()
    
    # Create a bar chart
    fig = px.bar(spend_per_part, x='LHX Part Number', y='Future Spend (Price Main * Forecast)', text='Future Spend (Price Main * Forecast)')
    
    # Create a line chart for the cumulative percentage
    fig.add_scatter(x=spend_per_part['LHX Part Number'], y=spend_per_part['cumulative_percentage'], mode='lines+markers', name='Cumulative %', yaxis='y2')
    
    # Update layout with secondary y-axis for the cumulative percentage
    fig.update_layout(
        title=f'Top 10 Parts by Spend for {supplier_name}',
        xaxis_title='Part Number',
        yaxis_title='Total Future Spend',
        yaxis=dict(title='Total Future Spend', side='left'),
        yaxis2=dict(title='Cumulative %', overlaying='y', side='right', showgrid=False, range=[0, 100]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=height or 300  # Use provided height or default to 300
    )
    
    # Show the Pareto chart in the Streamlit app
    st.plotly_chart(fig, use_container_width=True)

def search_supplier(df, query):
    if len(query) >= 3:
        matching_supplier = df[df['Supplier'].str.contains(query, case=False, na=False)]
        matching_supplier = matching_supplier['Supplier'].dropna().unique()
        # Use natsorted to sort the parts naturally
        return sorted(matching_supplier)
    return []

def perform_search():
    query = st.session_state.supplier_query
    st.session_state.search_results = search_supplier(st.session_state.data, query)


def display_summary(filtered_df):
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

# def app():
#     st.title("Supplier Explorer")
#     st.subheader("Search for a supplier to view a summary of details and relevant data")

#     df = load_data()

#     # Dropdown to select the supplier name
#     supplier_options = df['Supplier'].dropna().unique().tolist()
#     supplier_name = st.selectbox("Search for Supplier Name:", [""] + supplier_options)
#     st.header("Summary")
#     if supplier_name:
#         filtered_df = df[df['Supplier'] == supplier_name]
#         if not filtered_df.empty:
#             create_pareto_chart(df, supplier_name)
#             display_summary(filtered_df)
#             display_details(filtered_df)
#         else:
#             st.write("No matching suppliers found.")
#     else:
#         st.write("Please select a supplier name to see the details.")

def app():
    st.title("Supplier Explorer")
    st.subheader("Search for a supplier to view a summary of details and relevant data")


    # Load data once and use it across the session
    if 'data' not in st.session_state:
        st.session_state.data = load_data()

    # Text input for part search, with a callback to update the search results
    user_input = st.text_input("Search for Supplier Name:", value="", max_chars=50,
                               on_change=perform_search, key="supplier_query")
    
    

    # If we have search results, display them in a dropdown box for the user to select
    
    if 'search_results' in st.session_state and st.session_state.search_results:
        supplier_name = st.selectbox("Select from search results:", st.session_state.search_results)
        # Assuming 'create_pareto_chart', 'display_summary', 'display_details' functions are defined elsewhere
        if supplier_name:
            st.header("Summary")
            create_pareto_chart(st.session_state.data, supplier_name)  # Display Pareto chart
            filtered_df = st.session_state.data[st.session_state.data['Supplier'] == supplier_name]
            display_summary(filtered_df)  # Display summary metrics
            display_details(filtered_df)  # Display detailed data
    else:
        # Placeholder in case no search has been performed yet or no results
        supplier_name = st.empty()



def set_search_flag():
    st.session_state.search = True
