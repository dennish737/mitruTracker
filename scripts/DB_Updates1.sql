

CREATE TABLE IF NOT EXISTS motion (
  id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  v_id int NOT NULL,
  last_reading datetime NOT NULL,
  dt int DEFAULT 0,
  dlen int DEFAULT 0,
  speed int DEFAULT 0,
  dalt int DEFAULT 0
);

CREATE TABLE IF NOT EXISTS move_status (
   id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
   v_id int NOT NULL,
   moving tinyint DEFAULT 0
  );

 INSERT INTO move_status (v_id, moving)
    VALUES (1, 0), (2, 0), (3, 0);
   
  
INSERT INTO motion (v_id, last_reading, dt, dlen, speed, dalt)
WITH changes AS (
SELECT id, v_id, last_reading, loc, altitude_m,
  LAG(loc)
    OVER (PARTITION BY v_id ORDER BY id ASC)  AS previous_loc,
  LAG(last_reading)
    OVER (PARTITION BY v_id ORDER BY id ASC) AS previous_reading,  
  LAG(altitude_m)
    OVER (PARTITION BY v_id ORDER BY id ASC) AS previous_altitude_m
  FROM locations 
  ORDER BY v_id, id
)
SELECT  a.v_id, a.last_reading, 
      ROUND(TIMESTAMPDIFF(SECOND, a.previous_reading, a.last_reading),0) as dt,
      ROUND(ST_Distance_Sphere(a.previous_loc, a.loc),0) as dlen,
      ROUND(ROUND(ST_Distance_Sphere(a.previous_loc, a.loc),0)/
        ROUND(TIMESTAMPDIFF(SECOND, a.previous_reading, a.last_reading),0),0) as speed,
      ROUND((a.previous_altitude_m - a.altitude_m),0) as dalt
FROM changes a
ORDER BY a.id;

UPDATE motion 
SET dlen = 0,
    dt = 0,
    speed = 0,
    dalt = 0
WHERE id IN (1,2,3);

select * from motion limit 10;
select * from motion where speed > 0;


select id, v_id, 
	CASE 
		WHEN speed > 1 THEN 1 
		ELSE 0 
	END AS moveing
FROM motion
WHERE speed > 1 and v_id = 2
ORDER BY id;

select count(*) from motion where speed > 0 and v_id = 2;
	
WITH move AS (
	SELECT v_id, speed,
	COALESCE(LAG(speed, 1)
    	OVER (PARTITION BY v_id ORDER BY id DESC), 0)AS speed1,
    COALESCE(LAG(speed, 2)
    	OVER (PARTITION BY v_id ORDER BY id DESC),0)AS speed2
FROM motion
), is_moving AS (
SELECT v_id, 
	CASE 
		WHEN speed = 0 and speed1 = 0 and speed2 = 0 THEN 0
		-- WHEN speed > 0 or speed1 > 0 or speed2 > 0 THEN 1
		WHEN speed > 0  THEN 1
		-- ELSE 0
	END as moving
FROM move
)
SELECT moving FROM is_moving 
WHERE  v_id = 2
LIMIT 1; -- 45
 