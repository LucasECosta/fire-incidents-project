SELECT 
    incident_month,
    district,
    battalion,
    total_incidents
FROM fire_incidents_aggregated
ORDER BY incident_month DESC, district, battalion;
