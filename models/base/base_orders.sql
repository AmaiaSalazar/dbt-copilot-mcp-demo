select
    cast(order_id as integer) as order_id,
    cast(customer_id as integer) as customer_id,
    cast(order_date as date) as order_date,
    cast(status as varchar) as order_status,
    cast(amount as decimal(12, 2)) as order_amount
from {{ source('raw', 'orders') }}
