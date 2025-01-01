import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error

# Database connection details (use environment variables for better security)
host = "localhost"
user = "root"
password = "tonystark"
database = "orders"

st.title("Project-1")
st.header("Order Sales")

def check_connection():
    """Check if the connection to the database is successful."""
    try:
        # Establish connection
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if conn.is_connected():
            st.write("Connection to the database is successful!")
        else:
            st.write("Failed to connect to the database.")
    except Error as e:
        st.error(f"Error connecting to the database: {e}")
    finally:
        if conn.is_connected():
            conn.close()

check_connection()
def execute_query(query):
    """Execute a SQL query and return the results as a Pandas DataFrame."""
    try:
        # Establish connection
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if conn.is_connected():
            # Fetch data into a DataFrame
            df = pd.read_sql(query, conn)
            return df
    except Error as e:
        st.error(f"Error connecting to the database: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error
    finally:
        if conn.is_connected():
            conn.close()

# Query for the dropdown menu
query_revenue = """
SELECT sub_category, product_id, SUM(quantity * selling_price) AS total_revenue
FROM order2
GROUP BY sub_category, product_id
ORDER BY total_revenue DESC
LIMIT 10
"""

# Dropdown menu options
menu_options = ["Select an option", 
                "Top 10 Revenue",
                "Top 5 cities with the highest profit margins",
                "the total discount given for each category",
                "average sale price per product category",
                "region with the highest average sale price",
                "total profit per category",
                "top 3 segments with the highest quantity of orders",
                "the average discount percentage given per region",
                "product category with the highest total profit",
                "the total revenue generated per year"]

# Create dropdown menu
selected_option = st.selectbox("Choose a query to run:", menu_options)

# Run query and display results based on the selected option
if selected_option == "Top 10 Revenue":
    st.info("Fetching Top 10 Revenue data...")
    result_data = execute_query(query_revenue)
    if not result_data.empty:
        st.table(result_data)
    else:
        st.warning("No data found.")

query_highestprofit = """select 
order1.city,sum(order2.profit) as total_profit from order1 inner join order2
on order1.order_id = order2.order_id 
group by order1.city
having sum(order2.profit) > 0
order by total_profit desc limit 5"""
if selected_option == "Top 5 cities with the highest profit margins":
    st.info("Fetching Top 5 cities with the highest profit margins")
    result_data = execute_query(query_highestprofit)
    if not result_data.empty:
        st.table(result_data)
    else:
        st.warning("No data found.")

query_totaldiscount = """select category, sum(discount_percent) as discount from order2 group by category"""

if selected_option == "the total discount given for each category":
    st.info("fetching the total discount given for each category")
    result_data = execute_query(query_totaldiscount)
    if not result_data.empty:
        st.table(result_data)
    else:
        st.warning("No data found.")

query_avgsaleprice = "select category, avg(selling_price) from order2 group by category"

if selected_option == "average sale price per product category":
    st.info("fetching average sale price per product category")
    result_data = execute_query(query_avgsaleprice)
    if not result_data.empty:
        st.table(result_data)
    else:
        st.warning("No data found.")

query_regionavgsaleprice = """select order1.city,avg(order2.selling_price) as avg_sale_price from order1 inner join order2 on order1.order_id=order2.order_id group by order1.city 
having avg(order2.selling_price) > 0 order by avg_sale_price desc limit 5"""

if selected_option == "region with the highest average sale price":
    st.info("fetching region with the highest average sale price")
    result_data = execute_query(query_regionavgsaleprice)
    if not result_data.empty:
        st.table(result_data)
    else:
        st.warning("No data found.")

query_totalprofitpercat = "select category, sum(profit) as category_profit from order2 group by category order by category_profit desc limit 5"

if selected_option == "total profit per category":
    st.info("fetching total profit per category")
    result_data = execute_query(query_totalprofitpercat)
    if not result_data.empty:
        st.table(result_data)
    else:
        st.warning("No data found.")

query_top3segment = """select order1.segment,order2.category, sum(order2.quantity) as total_quantity from  order1 
inner join order2 on order1.order_id = order2.order_id group by order1.segment,order2.category order by total_quantity desc limit 5"""

if selected_option == " top 3 segments with the highest quantity of orders":
    st.info("fetching  top 3 segments with the highest quantity of orders")
    result_data = execute_query(query_top3segment)
    if not result_data.empty:
        st.table(result_data)
    else:
        st.warning("No data found.")


query_avgdisperregion = """select order1.region,avg(discount_percent) as avg_dis_price
from order1
inner join order2
on order1.order_id = order2.order_id group by region order by avg_dis_price desc"""

if selected_option == "the average discount percentage given per region":
    st.info("fetching the average discount percentage given per region")
    result_data = execute_query(query_avgdisperregion)
    if not result_data.empty:
        st.table(result_data)
    else:
        st.warning("No data found.")


query_highprofitcat = "select category, sum(profit) as total_profit from order2 group by category order by total_profit desc"

if selected_option == "product category with the highest total profit":
    st.info("fetching product category with the highest total profit")
    result_data = execute_query(query_highprofitcat)
    if not result_data.empty:
        st.table(result_data)
    else:
        st.warning("No data found.")


query_totalrevenueperyear2023 = """select order1.country, sum(order2.selling_price) as total_revenue_2023 from order1 
inner join order2 on order1.order_id = order2.order_id
where order1.order_date between '2023-01-01' and '2023-12-31' group by order1.country
order by total_revenue_2023"""
query_totalrevenueperyear2022 = """select order1.country, sum(order2.selling_price) as total_revenue_2022 from order1 
inner join order2 on order1.order_id = order2.order_id
where order1.order_date between '2022-01-01' and '2022-12-31' group by order1.country
order by total_revenue_2022"""

if selected_option == "the total revenue generated per year":
    st.info("fetching the total revenue generated per year")
    data_2023 = execute_query(query_totalrevenueperyear2023)
    data_2022 = execute_query(query_totalrevenueperyear2022)
    if not data_2023.empty and not data_2022.empty:
        merged_data = pd.merge(
            data_2023, 
            data_2022, 
            on="country", 
            how="outer"
        ).fillna(0)
        st.table(merged_data)
    else:
        st.warning("No data found.")

menu_options1 = ["least selling product",
                 "less margin product",
                 "city with high sales",
                 "Total sales and profit by segment",
                 "revenue by shipping mode",
                 "shipping modes with high discount",
                 "AVG cost to list price ratio",
                 "customer segment with highest order values",
                 "profit of each region",
                 "city id with high margin"]
selected_option = st.selectbox("choose query",menu_options1)

query_leastselling = """select category, sub_category, sum(quantity) as total_sold from order2 group by category, sub_category order by total_sold asc"""

if selected_option == "least selling product":
    st.info("fetching least selling product")
    result_data = execute_query(query_leastselling)
    if not result_data.empty:
        st.table(result_data)
    else:
        st.warning("No data found.")

query_lessmargin = "select category, sub_category, sum(profit) as margin from order2 group by category, sub_category order by margin asc"

if selected_option == "less margin product":
    st.info("fetching less margin product")
    result_data = execute_query(query_lessmargin)
    if not result_data.empty:
        st.table(result_data)
    else:
        st.warning("No data found.")

query_highcitysales = """select order1.city,order2.category,sum(order2.quantity) as sales from order1 inner join order2 on order1.order_id = order2.order_id 
group by order1.city,order2.category order by sales desc"""

if selected_option == "city with high sales":
    st.info("fetching city with high sales")
    result_data = execute_query(query_highcitysales)
    if not result_data.empty:
        st.table(result_data)
    else:
        st.warning("No data found.")

query_totalsaleandprofitpersegment = """select order1.segment,sum(order2.profit) as profits,sum(order2.quantity) as sales from order1 inner join order2 on order1.order_id = order2.order_id
group by  order1.segment order by profits, sales """

if selected_option == "Total sales and profit by segment":
    st.info("fetchig Total sales and profit by segment")
    result_data = execute_query(query_totalsaleandprofitpersegment)
    if not result_data.empty:
        st.table(result_data)
    else:
        st.warning("No data found.")


query_revenueshipping = """select order1.ship_mode,sum(order2.selling_price) as revenue from order1 inner join order2 on order1.order_id = order2.order_id
group by order1.ship_mode order by revenue desc"""

if selected_option == "revenue by shipping mode":
    st.info("fetching revenue by shipping mode")
    result_data = execute_query(query_revenueshipping)
    if not result_data.empty:
        st.table(result_data)
    else:
        st.warning("No data found.")

query_shipdis = """select order1.ship_mode,sum(order2.discount_price) as discount from order1 inner join order2 on order1.order_id = order2.order_id
group by order1.ship_mode order by discount desc"""

if selected_option == "shipping modes with high discount":
    st.info("fetching shipping modes with high discount")
    result_data = execute_query(query_shipdis)
    if not result_data.empty:
        st.table(result_data)
    else:
        st.warning("No data found.")

query_avgctol = "select category, sub_category,  AVG(cost_price / NULLIF(list_price, 0)) as ratio from order2 group by category, sub_category order by ratio desc"

if selected_option == "AVG cost to list price ratio":
    st.info("fetching AVG cost to list price ratio")
    result_data = execute_query(query_avgctol)
    if not result_data.empty:
        st.table(result_data)
    else:
        st.warning("No data found.")

query_hov = """select order1.segment,sum(order2.selling_price) as high_value,order2.category from order1 inner join order2 on order1.order_id = order2.order_id
group by order1.segment,order2.category order by high_value desc"""

if selected_option == "customer segment with highest order values":
    st.info("fetching customer segment with highest order values ")
    result_data = execute_query(query_hov)
    if not result_data.empty:
        st.table(result_data)
    else:
        st.warning("No data found.")

query_profitregion = """select order1.region, sum(order2.profit) as region_profit from  order1 inner join order2 on order1.order_id = order2.order_id
group by order1.region order by region_profit desc;
-- Adding foreign key to order2
alter table order2
add column city_id int ;
update order2 
inner join order1 on order2.order_id = order1.order_id
set order2.city_id = 
case 
	when order1.city = 'Henderson' then '101'
    when order1.city = 'New york city' then '102'
    when order1.city = 'San Francisco' then '103'
    when order1.city = 'Philadelphia' then '104'
    when order1.city = 'Seattle' then '105'
    when order1.city = 'Houston' then '106'
    when order1.city = 'Chicago' then '107'
    when order1.city = 'Los Angeles' then '108'
    when order1.city = 'Columbus' then '109'
    when order1.city = 'Springfield' then '110'
    else 999 
end;
alter table order2
add constraint fk_order2_city_id
foreign key (city_id)
references order1(order_id)"""

if selected_option == "profit of each region":
    st.info("fetching profit of each region")
    result_data = execute_query(query_profitregion)
    if not result_data.empty:
        st.table(result_data)
    else:
        st.warning("No data found.")

query_cityid = """select order1.city,order2.city_id,sum(order2.profit) as margin from order1 inner join order2 on order2.order_id = order1.order_id
group by order1.city,order2.city_id order by margin desc limit 5"""

if selected_option == "city id with high margin":
    st.info("fetching city id with high margin")
    result_data = execute_query(query_cityid)
    if not result_data.empty:
        st.table(result_data)
    else:
        st.warning("No data found.")
