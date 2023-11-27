import streamlit as st
from buy import buy_products
from cart import cart
from orders import orders
from ratings import collect_ratings
# from profile import profile

def home():
    st.title('CampusKart')
    

    # Sidebar navigation
    st.sidebar.title('Navigation')
    selected_page = st.sidebar.radio('Go to', ('Buy Products', 'Cart', 'Orders','Ratings'))

    if selected_page == 'Buy Products':
        buy_products()
    # elif selected_page == 'Back to Login':
    #     login()
    elif selected_page == 'Cart':
        cart()
    elif selected_page == 'Orders':
        orders()
    elif selected_page == 'Ratings':
        collect_ratings()


if __name__ == '__main__':
    home()
