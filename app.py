import streamlit as st
from login import login
from home import home
from sell import sell_products

def main():
    if st.session_state.get('logged_in') == 1:  # Flag for 'Seller' user
        sell_products()
        exit()
    if not st.session_state.get('logged_in'):
        login_successful = login()
        st.session_state['logged_in'] = login_successful

    if st.session_state.get('logged_in')==2:
        home()
        exit()

if __name__ == '__main__':
    main()
