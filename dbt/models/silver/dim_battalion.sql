with battalions as (
    select distinct
        battalion as battalion_name
    from {{ ref('bronze_incidents') }}
    where battalion is not null
)
select
    row_number() over (order by battalion_name) as battalion_id,
    battalion_name
from battalions
