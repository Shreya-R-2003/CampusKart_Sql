import streamlit as st
import mysql.connector

def sell_products():
    st.title('Sell Products')

    # Form for product details
    st.subheader('Enter Product Details')

    name = st.text_input('Name')
   
    price = st.number_input('Price', value=0.0)

    stock_quantity = st.number_input('Stock Quantity', value=0)
    

    # File upload for image
    uploaded_file = st.file_uploader('Upload Image', type=['jpg', 'png'])

    if st.button('Sell'):
        if name and price and uploaded_file:
            try:
                # Establish connection to MySQL
                conn = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='Shreya',  # Change this to your MySQL password
                    database='campuskart'
                )
                cursor = conn.cursor()

                # Insert the data into the products table
                query = "INSERT INTO products (name, price, image, stock_quantity) VALUES (%s, %s, %s, %s)"
                image_data = uploaded_file.read()
                data_tuple = (name, price, image_data, stock_quantity)
                cursor.execute(query, data_tuple)

                conn.commit()
                st.success('Product sold and data stored successfully!')
            except mysql.connector.Error as e:
                st.error(f"Error: {e}")
            finally:
                if 'conn' in locals() and conn.is_connected():
                    cursor.close()
                    conn.close()
        else:
            st.warning('Please fill in all the fields and upload an image')

if __name__ == '__main__':
    sell_products()
