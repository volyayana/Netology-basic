import sqlalchemy
from pprint import pprint

engine = sqlalchemy.create_engine('postgresql://netol:1111@localhost:5432/netol_db')
connection = engine.connect()

# название и год выхода альбомов, вышедших в 2018 году;
print('Название и год выхода альбомов, вышедших в 2018 году')
pprint(connection.execute("""
SELECT name, year_of_issue 
  FROM albums a 
 WHERE year_of_issue = 2018;
""").fetchall()); 

# название и продолжительность самого длительного трека;
print('\nНазвание и продолжительность самого длительного трека')
pprint(connection.execute("""
SELECT t.name, t.duration
  FROM tracks t 
 ORDER BY duration DESC
 LIMIT 1;
""").fetchall()); 

# название треков, продолжительность которых не менее 3,5 минуты;
print('\nНазвание треков, продолжительность которых не менее 3,5 минуты')
pprint(connection.execute("""
SELECT t.name, t.duration
  FROM tracks t 
 WHERE duration >= 210;
""").fetchall());

# названия сборников, вышедших в период с 2018 по 2020 год включительно;
print('\nНазвания сборников, вышедших в период с 2018 по 2020 год включительно')
pprint(connection.execute("""
SELECT name, year_of_issue 
  FROM collections s 
 WHERE year_of_issue between 2018 and 2020;
""").fetchall()); 

# исполнители, чье имя состоит из 1 слова;
print('\nИсполнители, чье имя состоит из 1 слова')
pprint(connection.execute("""
SELECT *
  FROM artists a 
 WHERE name not like '%% %%';
""").fetchall()); 

# название треков, которые содержат слово "мой"/"my".
print('\nНазвание треков, которые содержат слово "мой"/"my"')
pprint(connection.execute("""
SELECT name
  FROM tracks a 
 WHERE lower(name) like '%%my%%'
    OR lower(name) like '%%мой%%';
""").fetchall()); 