import streamlit as st
import mysql.connector
from sell import sell_products

user_id = 0


def login():
    st.title('Login Page')

    # Database connection configuration
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Shreya',
        'database': 'campuskart'
    }

    try:
        # Establish a connection to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
         # Query to check if the provided credentials exist in the database
        query = f"SELECT * FROM login WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        result = cursor.fetchone()

        if st.button('Login'):
            if username == 'Seller' and password == 'abc123':
                st.success('Logged in successfully!')
                sell_products()
                return 1          

            elif result:
                user_id = result[0]
                try:
                    cursor.execute(f"INSERT INTO currentuser (id, username) VALUES ({user_id}, '{username}')")
                    conn.commit()
                    st.success('Logged in successfully!')
                    return 2
                except mysql.connector.Error as e:
                    st.error(f"Error inserting into currentuser table: {e}")
                    return False
            else:
                st.error('Invalid username or password')
                return False

    except mysql.connector.Error as e:
        st.error(f"Database connection error: {e}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
