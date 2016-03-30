CREATE TABLE IF NOT EXISTS pointcloud(id int not null, point geometry, seg_id int, primary key(id));
CREATE TABLE IF NOT EXISTS planes(id int not null, origin geometry, n_x geometry, n_y geometry, n_z geometry, segment int, primary key(id));
CREATE TABLE IF NOT EXISTS building(id SERIAL PRIMARY KEY);
CREATE TABLE IF NOT EXISTS buildingpart(id SERIAL PRIMARY KEY);
CREATE TABLE IF NOT EXISTS roofsurface(id SERIAL PRIMARY KEY, segment int);
CREATE TABLE IF NOT EXISTS wallsurface(id SERIAL PRIMARY KEY, segment int);
CREATE TABLE IF NOT EXISTS groundsurface(id SERIAL PRIMARY KEY, segment int);