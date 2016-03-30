CREATE TABLE IF NOT EXISTS pointcloud(id int not null, point geometry, seg_id int, primary key(id));
CREATE TABLE IF NOT EXISTS planes(id int not null, origin geometry, n_x geometry, n_y geometry, n_z geometry, segment int, primary key(id));
CREATE TABLE IF NOT EXISTS building(id int not null, primary key(id));
CREATE TABLE IF NOT EXISTS buildingpart(id int not null, primary key(id));
CREATE TABLE IF NOT EXISTS roofsurface(id int not null, segment int, primary key(id));
CREATE TABLE IF NOT EXISTS wallsurface(id int not null, segment int, primary key(id));
CREATE TABLE IF NOT EXISTS groundsurface(id int not null, segment int, primary key(id));