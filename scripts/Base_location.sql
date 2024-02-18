-- DROP TABLE IF EXISTS base_locations;
CREATE TABLE IF NOT EXISTS base_locations (
	id int NOT NULL AUTO_INCREMENT,
	name varchar(64) NOT NULL,
	geom GEOMETRY NOT NULL,
	comment varchar(256),
	PRIMARY KEY (id)
	);


INSERT INTO base_locations(name, geom) VALUES
('Granite Falls', ST_GeomFromText('POINT(-121.96885 48.0811)')),
('SnoCo DEM', ST_GeomFromText('POINT(-122.244 47.924)')),
('Taylors Landing', ST_GeomFromText('POINT(-122.08002 47.94740)'));





