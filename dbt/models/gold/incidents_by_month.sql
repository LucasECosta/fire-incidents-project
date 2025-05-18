select
    b.battalion_name,
    date_trunc('month', f.incident_date) as month,
    count(*) as total_incidents
from {{ ref('fact_incident') }} f
left join {{ ref('dim_battalion') }} b on f.battalion_id = b.battalion_id
where f.incident_date is not null
group by 1, 2
