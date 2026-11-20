-- Comprobacion de negocio independiente: promedio calculado a partir del CSV.
with expected(country, average_order_value, order_count) as (
    values ('DE', 50.00, 2), ('ES', 116.67, 3), ('FR', 75.00, 2)
), actual as (
    select country, average_order_value, order_count
    from {{ ref('mart_average_order_value_by_country') }}
)
select
    coalesce(expected.country, actual.country) as country
from expected
full outer join actual on expected.country = actual.country
where expected.country is null
    or actual.country is null
    or actual.average_order_value is null
    or actual.average_order_value <> expected.average_order_value
    or actual.order_count is null
    or actual.order_count <> expected.order_count
