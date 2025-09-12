with source as (
    select *
    from {{ source('raw', 'customers') }}
)

select
    customer_id,
    name,
    email
from source

