import streamlit as st
import plotly.express as px
from load_data import load_data

def check_password():
    """Simple password check."""
    correct_password = 'password123'
    password = st.sidebar.text_input("Enter your password:", value="", type="password")

    if st.sidebar.button('Login'):
        if password == correct_password:
            st.session_state['authenticated'] = True
        else:
            st.sidebar.error("Incorrect Password")
            st.session_state['authenticated'] = False

#products where used and relevant data

def create_pareto_chart(df, part_name, height=None):
    # Filter data for the selected part
    part_data = df[df['Component Name'] == part_name]

    # Group the data by product and sum the spend
    spend_per_product = part_data.groupby('Product')['Future Spend (Price Main * Forecast)'].sum().reset_index()

    # Sort products by spend and take top 10
    sorted_products = spend_per_product.sort_values(by='Future Spend (Price Main * Forecast)', ascending=False).head(10)

    # Calculate cumulative spend
    sorted_products['cumulative_spend'] = sorted_products['Future Spend (Price Main * Forecast)'].cumsum()
    sorted_products['cumulative_percentage'] = 100 * sorted_products['cumulative_spend'] / sorted_products['Future Spend (Price Main * Forecast)'].sum()

    # Create a bar chart
    fig = px.bar(sorted_products, x='Product', y='Future Spend (Price Main * Forecast)', text='Future Spend (Price Main * Forecast)')

    # Create a line chart for the cumulative percentage
    fig.add_scatter(x=sorted_products['Product'], y=sorted_products['cumulative_percentage'], mode='lines+markers', name='Cumulative %', yaxis='y2')

    # Update layout with secondary y-axis for the cumulative percentage
    fig.update_layout(
        title='Top 10 Products by Spend',
        xaxis_title='Product',
        yaxis_title='Total Future Spend',
        yaxis=dict(title='Total Future Spend', side='left'),
        yaxis2=dict(title='Cumulative %', overlaying='y', side='right', showgrid=False, range=[0, 100]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=height or 300  # Adjust the height if needed
    )

    # Show the Pareto chart in the Streamlit app
    st.plotly_chart(fig, use_container_width=True)

def display_summary(filtered_df):
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
    # Initialize session state for authentication
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    # Check if authenticated
    if not st.session_state['authenticated']:
        check_password()
        return  # Stop further execution until authenticated

    st.title("Product Explorer")
    st.subheader("Search for a part to view a summary of products and relevant data")

    df = load_data()

    # Dropdown to select the component name
    part_options = df['Component Name'].dropna().unique().tolist()
    part_name = st.selectbox("Search for Part Name:", part_options)
    st.header("Summary")
    
    if part_name:
        create_pareto_chart(df, part_name)  # Display Pareto chart

        filtered_df = df[df['Component Name'] == part_name]
        if not filtered_df.empty:
            display_summary(filtered_df)  # Display summary metrics
            display_details(filtered_df)  # Display detailed data
        else:
            st.write("No matching parts found.")
    else:
        st.write("Please select a part name to see the details.")