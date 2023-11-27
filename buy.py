import streamlit as st
import mysql.connector
from PIL import Image
from io import BytesIO

def buy_products():
    st.title('Buy Products')
    st.write('Items for sale :\n')

    try:
        # Establish connection to MySQL
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Shreya',
            database='campuskart'
        )
        cursor = conn.cursor()

        # Retrieve product data from the database
        query = "SELECT id, name, price, image, stock_quantity FROM products"
        cursor.execute(query)
        products = cursor.fetchall()

        # Display product information in a grid layout
        col_count = 3  # Number of columns in the grid
        for i, product in enumerate(products, start=1):
            id, name, price, image_data, stock_quantity = product
            image = Image.open(BytesIO(image_data))

            # Adjust the image size
            image.thumbnail((200, 200))  # Resize the image to 200x200 pixels

            # Display the image and product details
            st.image(image, caption=name, width=150)
            st.write(f"Price: {price}")
            st.write(f"Number of pieces available: {stock_quantity}")

            # Add a "Buy" button below each product
            if st.button(f"Buy {name}"):
                try:
                    # Insert the selected product into the cart table
                    insert_query = "INSERT INTO cart (pdt_id, stock_quantity) VALUES (%s, %s)"
                    cursor.execute(insert_query, (id, stock_quantity))
                    conn.commit()
                    st.success(f"You've bought {name}!")
                except mysql.connector.Error as e:
                    st.error(f"Error adding to cart: {e}")
            
            if i % col_count != 0:
                st.write("---")
                # Add a separator after each image in the same row

        # Create a line break to ensure the next images appear in a new row
        st.write("")  

    except mysql.connector.Error as e:
        st.error(f"Error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    buy_products()
