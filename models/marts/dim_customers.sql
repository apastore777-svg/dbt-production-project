with stg as (
    select *
    from {{ ref('stg_customers') }}
)

select
    customer_id,
    name,
    email
from stg

