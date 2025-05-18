select
    i.incident_number,
    d.district_id,
    b.battalion_id,
    to_date(i.incident_date) as incident_date,
    i.location
from {{ ref('bronze_incidents') }} i
left join {{ ref('dim_district') }} d on i.district = d.district_name
left join {{ ref('dim_battalion') }} b on i.battalion = b.battalion_name
