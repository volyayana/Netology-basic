drop table if exists white_lists;
drop table if exists black_lists;
drop table if exists found_users;
drop table if exists cities;
drop table if exists countries;

create table if not exists countries (
  id   int primary key,
  name varchar(100) not null
);

create table if not exists cities (
  id serial  primary key,
  name 		 varchar(100) not null,
  country_id int references countries(id) not null
);

create table if not exists found_users (
  user_id 	int  not null,
  found_user_id 	int not null,
  constraint found_users_pk primary key (user_id, found_user_id)
);

create table if not exists black_lists (
  user_id 		int  primary key,
  black_user_id int not null,
  del_date 		date
);

create table if not exists white_lists (
  user_id 		int  primary key,
  white_user_id int not null,
  del_date 		date
);