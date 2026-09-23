CREATE TABLE satellite_telemetry (
    packet_id VARCHAR(50) PRIMARY KEY,
    latitude DECIMAL(9,6) NOT NULL,
    longitude DECIMAL(9,6) NOT NULL,
    sensor_reading FLOAT NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT 
    packet_id,
    sensor_reading,
    recorded_at,
    ROW_NUMBER() OVER (ORDER BY sensor_reading DESC) as severity_row_num,
    RANK() OVER (ORDER BY sensor_reading DESC) as temperature_rank
FROM 
    satellite_telemetry;

SELECT 
    packet_id,
    sensor_reading,
    recorded_at,
    SUM(sensor_reading) OVER (ORDER BY recorded_at) as cumulative_thermal_load
FROM 
    satellite_telemetry;


OK?
