select
    order_id,
    customer_id,
    order_date,
    lower(trim(order_status)) as order_status,
    order_amount
from {{ ref('base_orders') }}
