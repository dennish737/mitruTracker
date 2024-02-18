-- DROP TABLE IF EXISTS base_locations;
CREATE TABLE IF NOT EXISTS base_locations (
	id int auto_increment,
	name varchar(64) not null,
	base_loc point DEFAULT NULL,
	comments varchar(255),
	primary key(id)
);


INSERT INTO base_locations(name,base_loc,comments)
VALUES (('SnoCoDEM', PointFromText('POINT (-122.244 47.924)'), 'Equipment stored in gated parking.'),
        ('EvergreenFair', PointFromText('POINT (-121.9887 47.8682)'), 'Equipment stored in gated parking.')
       );