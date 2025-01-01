use orders;
-- top 10 highest revenue generating products
select * from order2;
select sub_category,product_id, sum(quantity * selling_price) as total_revenue 
from order2 
group by sub_category,product_id
order by total_revenue desc limit 10;  

-- Top 5 cities with the highest profit margins
select 
order1.city,
sum(order2.profit) as total_profit
from order1
inner join order2
on order1.order_id = order2.order_id 
group by order1.city
having sum(order2.profit) > 0
order by total_profit desc ;

-- the total discount given for each category
select category, sum(discount_percent) from order2 group by category;

-- average sale price per product category
select category, avg(selling_price) from order2 group by category;

-- region with the highest average sale price
select order1.city,avg(order2.selling_price) as avg_sale_price from order1 
inner join order2 on order1.order_id=order2.order_id group by order1.city 
having avg(order2.selling_price) > 0 order by avg_sale_price desc limit 5;
		
--  total profit per category
select category, sum(profit) as category_profit from order2 group by category order by category_profit desc limit 5;

-- top 3 segments with the highest quantity of orders
select order1.segment,order2.category, sum(order2.quantity) as total_quantity from  order1 
inner join order2 on order1.order_id = order2.order_id group by order1.segment,order2.category order by total_quantity desc limit 5;

--  the average discount percentage given per region
select order1.region,avg(discount_percent) as avg_dis_price
from order1
inner join order2
on order1.order_id = order2.order_id group by region order by avg_dis_price desc ;

-- product category with the highest total profit
select category, sum(profit) as total_profit from order2 group by category order by total_profit desc;

-- the total revenue generated per year
-- 2023
select order1.country, sum(order2.selling_price) as total_revenue_2023 from order1 
inner join order2 on order1.order_id = order2.order_id
where order1.order_date between '2023-01-01' and '2023-12-31' group by order1.country
order by total_revenue_2023 ;
-- 2022
select order1.country, sum(order2.selling_price) as total_revenue_2022 from order1 
inner join order2 on order1.order_id = order2.order_id
where order1.order_date between '2022-01-01' and '2022-12-31' group by order1.country
order by total_revenue_2022;
-- least selling product
select category, sub_category, sum(quantity) as total_sold from order2 group by category, sub_category order by total_sold asc;
-- less margin product
select category, sub_category, sum(profit) as margin from order2 group by category, sub_category order by margin asc;
-- city with high sales
select order1.city,order2.category,sum(order2.quantity) as sales from order1 inner join order2 on order1.order_id = order2.order_id 
group by order1.city,order2.category order by sales desc;
-- Total sales and profit by segment
select order1.segment,sum(order2.profit) as profits,sum(order2.quantity) as sales from order1 inner join order2 on order1.order_id = order2.order_id
group by  order1.segment order by profits, sales ;
-- revenue by shipping mode
select order1.ship_mode,sum(order2.selling_price) as revenue from order1 inner join order2 on order1.order_id = order2.order_id
group by order1.ship_mode order by revenue desc;
-- shipping modes with high discount
select order1.ship_mode,sum(order2.discount_price) as discount from order1 inner join order2 on order1.order_id = order2.order_id
group by order1.ship_mode order by discount desc;
-- AVG cost to list price ratio
select category, sub_category,  AVG(cost_price / NULLIF(list_price, 0)) as ratio from order2 group by category, sub_category order by ratio desc;
-- customer segment with highest order values
select order1.segment,sum(order2.selling_price) as high_value,order2.category from order1 inner join order2 on order1.order_id = order2.order_id
group by order1.segment,order2.category order by high_value desc;
-- profit of each region
select order1.region, sum(order2.profit) as region_profit from  order1 inner join order2 on order1.order_id = order2.order_id
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
references order1(order_id);
-- city id with high margin
select order1.city,order2.city_id,sum(order2.profit) as margin from order1 inner join order2 on order2.order_id = order1.order_id
group by order1.city,order2.city_id order by margin desc limit 5;