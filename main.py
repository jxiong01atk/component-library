import streamlit as st
import dashboard1
import dashboard2
import dashboard3

def main():
    st.set_page_config(page_title="Component Library Explorer", layout="wide")

    # Custom CSS for styling the sidebar and buttons
    st.markdown("""
        <style>
        /* Make all buttons the same width */
        .sidebar .stButton>button {
            width: 100%;
            box-sizing: border-box; /* Include padding and border in the width */
            margin: 5px 0; /* Spacing between buttons */
        }
        /* Style to make the sidebar less wide */
        .css-1lcbmhc .css-1adrfps {
            width: 250px; /* Adjust the width as needed */
        }
        </style>
        """, unsafe_allow_html=True)

    # Sidebar navigation
    st.sidebar.title("Navigation Menu")

    # Define the button layout and session state mapping
    buttons = {
        "Home": "Home",
        "Part Explorer": "Part Explorer",
        "Supplier Explorer": "Supplier Explorer",
        "Product Explorer": "Product Explorer",
    }

    for label, state in buttons.items():
        if st.sidebar.button(label):
            st.session_state.selected_dashboard = state

    # Check which dashboard is selected based on session state
    selected_dashboard = st.session_state.get('selected_dashboard', 'Home')

    # Render the appropriate dashboard or the home page
    if selected_dashboard == "Home":
        st.title("Component Library Explorer")
        st.subheader("This app allows you to view information for parts, suppliers, and products.")
    elif selected_dashboard == "Part Explorer":
        dashboard1.app()
    elif selected_dashboard == "Supplier Explorer":
        dashboard2.app()
    elif selected_dashboard == "Product Explorer":
        dashboard3.app()

if __name__ == "__main__":
    main()
