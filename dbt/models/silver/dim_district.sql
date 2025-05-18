with districts as (
    select distinct
        district as district_name
    from {{ ref('bronze_incidents') }}
    where district is not null
)
select
    row_number() over (order by district_name) as district_id,
    district_name
from districts
