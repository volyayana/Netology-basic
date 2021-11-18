drop table if exists artists_genres;
drop table if exists albums_artists;
drop table if exists collections_tracks;
drop table if exists collections;
drop table if exists tracks;
drop table if exists albums;
drop table if exists artists;
drop table if exists genres;
drop table if exists sites;

create table if not exists sites (
  id serial primary key,
  name 		varchar(100) not null
);

create table if not exists genres (
  id   serial primary key,
  name varchar(100) not null
);

create table if not exists artists (
  id 		serial primary key,
  name		varchar(100) not null,	
  site_id   int references sites(id)
 );

create table if not exists artists_genres (
  artist_id int references artists(id) not null,
  genre_id 	int references genres(id) not null,
  constraint artists_genres_pk primary key (artist_id, genre_id)
 );

create table if not exists albums (
  id 			 serial primary key,
  name			 varchar(100) not null,	
  year_of_issue  int not null
 );

create table if not exists albums_artists (
  album_id       int references albums(id) not null,
  artist_id      int references artists(id) not null,
  constraint albums_artists_pk primary key (album_id, artist_id)
 );

create table if not exists tracks (
  id 			 serial primary key,
  name			 varchar(100) not null,	
  duration	     int not null,
  album_id       int references albums(id)
 );

create table if not exists collections (
  id 			 serial primary key,
  name			 varchar(100) not null,	
  year_of_issue  int not null
);

create table if not exists collections_tracks (
  collection_id       int references collections(id) not null,
  track_id      int references tracks(id) not null,
  constraint collections_tracks_pk primary key (collection_id, track_id)
 );
