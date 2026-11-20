select
    orders.order_id,
    orders.customer_id,
    orders.order_date,
    orders.order_status,
    orders.order_amount,
    customers.country
from {{ ref('stg_orders') }} as orders
left join {{ ref('stg_customers') }} as customers
    on orders.customer_id = customers.customer_id
