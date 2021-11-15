create table if not exists sites (
  id serial primary key
);

create table if not exists genres (
  id 		serial primary key,
  name		varchar(100) not null
);

create table if not exists artists (
  id 		serial primary key,
  name		varchar(100) not null,	
  site_id   int references sites(id),
  genre_id 	int references genres(id)
 );

create table if not exists albums (
  id 			 serial primary key,
  name			 varchar(100) not null,	
  year_of_issue  int not null,
  artist_id      int references artists(id) not null
 );

create table if not exists tracks (
  id 			 serial primary key,
  name			 varchar(100) not null,	
  duration	     int not null,
  album_id       int references albums(id)
 );

