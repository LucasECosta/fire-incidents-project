WITH base AS (
    SELECT
        "Incident Number",
        "Incident Date",
        "Neighborhood District",
        "Battalion",
        "Location"
    FROM {{ ref('fire_incidents_base') }}
)

SELECT
    DATE_TRUNC('month', "Incident Date") AS incident_month,
    "Neighborhood District" AS district,
    "Battalion" AS battalion,
    COUNT("Incident Number") AS total_incidents
FROM
    base
GROUP BY
    incident_month, district, battalion
ORDER BY
    incident_month, district, battalion
