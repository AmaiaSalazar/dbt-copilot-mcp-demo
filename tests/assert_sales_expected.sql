-- Comprobación de negocio independiente: importes calculados a partir del CSV.
with expected(country, total_sales, order_count) as (
    values ('ES', 350.00, 3), ('DE', 100.00, 2), ('FR', 150.00, 2)
), actual as (
    select country, total_sales, order_count
    from {{ ref('mart_sales_by_country') }}
)
select
    coalesce(expected.country, actual.country) as country
from expected
full outer join actual on expected.country = actual.country
where expected.country is null
    or actual.country is null
    or actual.total_sales is distinct from expected.total_sales
    or actual.order_count is distinct from expected.order_count
