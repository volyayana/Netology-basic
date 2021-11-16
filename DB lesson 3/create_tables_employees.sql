create table departments (
  id   serial primary key,
  name varchar(50) not null
);

create table employees (
  id serial primary key,
  department_id int references departments(id),
  leader_id int references employees(id)
);