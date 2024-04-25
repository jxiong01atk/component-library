import streamlit as st
import pandas as pd
import plotly.express as px
from load_data import load_data
from natsort import natsorted
from data_handles import get_parts, get_searched_parts, get_part_numbers, get_searched_part_numbers, get_component_library_part_number

def create_pareto_chart(df, part_name, height=None):
    # Filter data for the selected part
    part_data = df[df['Component Name'] == part_name]
    
    # Group by supplier and sum the spend
    spend_per_supplier = part_data.groupby('Supplier', as_index=False)['Future Spend (Price Main * Forecast)'].sum()
    
    # Sort suppliers by spend and take top 10
    spend_per_supplier = spend_per_supplier.sort_values(by='Future Spend (Price Main * Forecast)', ascending=False).head(10)
    
    # Calculate cumulative spend
    spend_per_supplier['cumulative_spend'] = spend_per_supplier['Future Spend (Price Main * Forecast)'].cumsum()
    spend_per_supplier['cumulative_percentage'] = 100 * spend_per_supplier['cumulative_spend'] / spend_per_supplier['Future Spend (Price Main * Forecast)'].sum()
    
    # Create a bar chart
    fig = px.bar(spend_per_supplier, x='Supplier', y='Future Spend (Price Main * Forecast)', text='Future Spend (Price Main * Forecast)')

    # Create a line chart for the cumulative percentage
    fig.add_scatter(x=spend_per_supplier['Supplier'], y=spend_per_supplier['cumulative_percentage'], mode='lines+markers', name='Cumulative %', yaxis='y2')

    # Update layout with secondary y-axis for the cumulative percentage
    fig.update_layout(
        title='Top 10 Suppliers by Spend',
        xaxis_title='Supplier',
        yaxis_title='Total Future Spend',
        yaxis=dict(title='Total Future Spend', side='left'),
        yaxis2=dict(title='Cumulative %', overlaying='y', side='right', showgrid=False, range=[0, 100]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),        
        height=height or 300  # Use provided height or default
    )
    
    # Show the Pareto chart in the Streamlit app
    st.plotly_chart(fig, use_container_width=True)

def search_parts(df, query):
    if len(query) >= 3:
        matching_parts = df[df['Component Name'].str.contains(query, case=False, na=False)]
        matching_parts = matching_parts['Component Name'].dropna().unique()
        # Use natsorted to sort the parts naturally
        return sorted(matching_parts)
    return []

def perform_search():
    query = st.session_state.part_query
    st.session_state.search_results = search_parts(st.session_state.data, query)

def display_summary(filtered_df):
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

def load_searched_part_numbers():
    if st.session_state.search:  # Only run if there's a search term
        with st.spinner('Fetching data...'):
            tuples = list(get_searched_part_numbers(st.session_state.search))
            st.session_state['part_results'] = [part_number[0] for part_number in tuples]

    # else: load_parts()

# def load_parts():
#     with st.spinner('Fetching data...'):
#             tuples = list(get_part_numbers(st.session_state.search))
#             st.session_state['part_results'] = [part_number[0] for part_number in tuples]

def app():
    # Generate a list of years from 2020 to 2030
    years = list(range(2020, 2030))

    # Create columns with weights that push the selectbox to the right
    col1, col2 = st.columns([3, 1])  # Adjust the weights as needed

    # Use the second column to display the selectbox in the upper right
    with col2:
        selected_year = st.selectbox("Select a year:", years)

    st.title("Part Explorer")
    st.subheader("Search for a part to view a summary of details and relevant data")

    # Load data once and use it across the session
    # if 'data' not in st.session_state:
    #     st.session_state.data = load_data()
    # if 'part_results' not in st.session_state:
    #     load_parts()      # Load all parts on first load

    search_input = st.text_input("Search for part", key="search",placeholder="Press enter to search parts database",on_change=load_searched_part_numbers)

    # Text input for part search, with a callback to update the search results
    # user_input = st.text_input("Search for part:", value="", max_chars=50,
    #                            on_change=perform_search, key="part_query")

    # If we have search results, display them in a dropdown box for the user to select
    
    #part number instead of component name
    #Part Number, MPN, Description (Main), Supplier, Product, Sector, Volume, Baseline Cost (Selected), Total Spend, Sprint, ECCN 
    #differentiators: MPN, Supplier, Product, Year (backend full download data only)
    #Cost instead of price
    #preview only has main/processed view, download includes all
    #total forecasted volume (2024) in summary view
    #add dropdown to select year for summary view (2020-max)
    #No need to attribute price to year
    #Source type column for all that has "selected" values
    #Distinct Products, Distinct Ideas instead of UOM
    #Baseline Cost (Selected/source)
    #Supplier pareto and product pareto, sectorr pareto (selector to toggle between displays)

    # if 'search_results' in st.session_state and st.session_state.search_results:
    #     part_name = st.selectbox("Select from search results:", st.session_state.search_results)
    #     # Assuming 'create_pareto_chart', 'display_summary', 'display_details' functions are defined elsewhere
    #     if part_name:
    #         st.header("Summary")
    #         create_pareto_chart(st.session_state.data, part_name)  # Display Pareto chart
    #         filtered_df = st.session_state.data[st.session_state.data['Component Name'] == part_name]
    #         display_summary(filtered_df)  # Display summary metrics
    #         display_details(filtered_df)  # Display detailed data

    if 'part_results' in st.session_state and st.session_state.part_results:
        part_name = st.selectbox("Select from search results:", st.session_state.part_results)
        df = pd.DataFrame(get_component_library_part_number(part_name))
        df.columns=[
        "Part Number",
        "MPN",
        "Description",
        "Supplier",
        "Last Cost",
        "Last Quantity",
        "Date"
    ]
        st.write(df)
        # # Assuming 'create_pareto_chart', 'display_summary', 'display_details' functions are defined elsewhere
        # if part_name:
        #     st.header("Summary")
        #     create_pareto_chart(st.session_state.data, part_name)  # Display Pareto chart
        #     filtered_df = st.session_state.data[st.session_state.data['Component Name'] == part_name]
        #     display_summary(filtered_df)  # Display summary metrics
        #     display_details(filtered_df)  # Display detailed data
    else:
        # Placeholder in case no search has been performed yet or no results
        part_name = st.empty()



def set_search_flag():
    st.session_state.search = True

### add idea explorer
### add pareto to the dashboard
