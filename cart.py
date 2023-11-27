import streamlit as st
import mysql.connector

def cart():
    st.title('Your Cart')

    try:
        # Establish connection to MySQL
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Shreya',
            database='campuskart'
        )
        cursor = conn.cursor()

        # Retrieve cart items from the database
        query = """
        SELECT 
            cart.id AS cart_id,
            cart.pdt_id,
            products.name,
            products.price,
            products.image,
            products.stock_quantity ,
            (SELECT AVG(rating) FROM ratings WHERE pdt_id = products.id) AS avg_rating

        FROM cart
        JOIN products ON cart.pdt_id = products.id
        """

        cursor.execute(query)
        cart_items = cursor.fetchall()


        # Display cart items
        total_price = 0  # Initialize total price
        for item in cart_items:
            id, item_id, name, price, image_data, stock_quantity, avgrat = item
            st.image(image_data, caption=name, width=150)
            st.write(f"Price: {price}")
            st.write(f"Rating: {avgrat}")

            if st.button(f"Remove Item {item_id}"):
                # Execute SQL query to remove the item from the cart
                cursor.execute("DELETE FROM cart WHERE pdt_id = %s", (item_id,))

                # # Update the stock_quantity in the products table
                # cursor.execute("UPDATE products SET stock_quantity = stock_quantity + 1 WHERE id = %s", (item_id,))
                conn.commit()
                
                st.success("Item removed from the cart.")

           
            total_price += price  # Add each item's price to the total
            st.write("---")
        # cursor.execute("SELECT SUM(price) FROM cart;")
        # total_price = cursor.fetchone()[0]

        # Display total price
        st.write(f"Total Price: {total_price}")
        cursor.execute("SELECT id FROM currentuser WHERE currentid = (SELECT MAX(currentid) FROM currentuser);")
        current_user_id = cursor.fetchone()[0]

        if st.button("Order Now"):
            try:

                # Calculate the total price using an aggregate query
                cursor.execute("SELECT SUM(products.price) FROM cart JOIN products ON cart.pdt_id = products.id;")
                total_price = cursor.fetchone()[0]

                # Perform the action to clear the cart using procedures
                cursor.execute("CALL clear_cart;")

                for item in cart_items:
                    id, pdt_id, name, price, _, stock_quantity, _ = item
                    cursor.execute(
                    "INSERT INTO orders (pdt_id, stock_quantity, user_id, order_date, order_time) VALUES (%s, %s, %s, CURDATE(), CURTIME())",
                        (pdt_id, 1, current_user_id)
                    )

                
                conn.commit()

                st.success(f"Order placed successfully! Your total amount is: {total_price}")
            except mysql.connector.Error as e:
                st.error(f"Error placing order: {e}")

    except mysql.connector.Error as e:
        st.error(f"Error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    cart()
