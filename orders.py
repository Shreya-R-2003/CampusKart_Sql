import streamlit as st
import mysql.connector
from login import user_id

def orders():
    st.title('Your Orders')

    try:
        # Establish connection to MySQL
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Shreya',
            database='campuskart'
        )
        cursor = conn.cursor()
        # cursor.execute("SELECT id FROM currentuser WHERE currentid = (SELECT MAX(currentid) FROM currentuser)")
        # result = cursor.fetchone()

        # if result:
        #     current_user_id = result[0]
        # # Retrieve orders from the database
        query = """
        SELECT
            orders.id AS order_id,
            orders.pdt_id,
            products.name,
            products.price,
            products.image,
            orders.stock_quantity, 
            orders.order_date,
            orders.order_time
        FROM orders
        JOIN products ON orders.pdt_id = products.id
        WHERE orders.user_id =(SELECT id FROM currentuser WHERE currentid = (SELECT MAX(currentid) FROM currentuser))

        """
        cursor.execute(query)
        order_items = cursor.fetchall()

        # Display order items
        total_price = 0  # Initialize total price
        for item in order_items:
            order_id, pdt_id, name, price, image_data, stock_quantity, order_date, order_time = item
            st.image(image_data, caption=name, width=150)
            st.write(f"Price: {price}")
            st.write(f"Stock Quantity: {stock_quantity}")
            st.write(f"Date: {order_date}")
            st.write(f"Time: {order_time}")
            st.write(f"Price: {price}")
            total_price += price * stock_quantity  # Add each item's total price to the total
            st.write("---")

        # Display total price
        st.write(f"Total Price of Orders: {total_price}")

    except mysql.connector.Error as e:
        st.error(f"Error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    display_orders()
