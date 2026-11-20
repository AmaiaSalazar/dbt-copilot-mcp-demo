select
    country,
    cast(sum(order_amount) as decimal(12, 2)) as total_sales,
    count(*) as order_count
from {{ ref('int_orders_enriched') }}
where order_status = 'completed'
group by country
