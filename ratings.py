import streamlit as st
import mysql.connector

def collect_ratings():
    st.title('Product Ratings')

    try:
        # Establish connection to MySQL
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Shreya',
            database='campuskart'
        )
        cursor = conn.cursor()

        # Get product name and rating from the user
        product_name = st.text_input('Product Name')
        rating = st.slider('Rating', min_value=1, max_value=5, value=3)

        if st.button('Submit'):
            # Get product ID from the products table based on the provided product name
            cursor.execute(f"SELECT id FROM products WHERE name = '{product_name}'")
            product_id = cursor.fetchone()
            cursor.execute(f"SELECT id, username FROM currentuser WHERE currentid = (SELECT MAX(currentid) FROM currentuser)")
            user = cursor.fetchone()
            
            if product_id:
                # Insert the rating into the ratings table
                cursor.execute(
                    "INSERT INTO ratings (pdt_id, rating, user_id, username) VALUES (%s, %s, %s, %s)",
                    (product_id[0], rating, user[0], user[1])
                )
                conn.commit()
                st.success('Rating submitted successfully!')
            else:
                st.error('Product not found. Please check the product name.')

    except mysql.connector.Error as e:
        st.error(f"Error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    collect_ratings()
