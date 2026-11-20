select
    country,
    cast(avg(order_amount) as decimal(12, 2)) as average_order_value,
    count(*) as order_count
from {{ ref('int_orders_enriched') }}
where order_status = 'completed'
group by country
