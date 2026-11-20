-- Ejecutar después de dbt build, desde DBeaver u otro cliente DuckDB.
select * from base.base_orders order by order_id;
select * from staging.stg_customers order by customer_id;
select * from intermediate.int_orders_enriched order by order_id;
select * from marts.mart_sales_by_country order by country;
