select
    distinct to_date(incident_date) as date_day,
    extract(year from incident_date) as year,
    extract(month from incident_date) as month,
    extract(day from incident_date) as day
from {{ ref('bronze_incidents') }}
where incident_date is not null
