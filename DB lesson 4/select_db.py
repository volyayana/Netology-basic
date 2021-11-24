import sqlalchemy

engine = sqlalchemy.create_engine('postgresql://netol:1111@localhost:5432/netol_db')
connection = engine.connect()

# предварительно удалим все старые данные
connection.execute("""DELETE FROM artists_genres;""")
connection.execute("""DELETE FROM albums_artists;""")
connection.execute("""DELETE FROM collections_tracks;""")
connection.execute("""DELETE FROM collections;""")
connection.execute("""DELETE FROM tracks;""")
connection.execute("""DELETE FROM genres;""")
connection.execute("""DELETE FROM artists;""")
connection.execute("""DELETE FROM albums;""")

connection.execute("""INSERT INTO genres (id, name)
VALUES (1, 'Джаз'), 
       (2, 'Рок'), 
       (3, 'Фолк'), 
       (4, 'Классическая'), 
       (5, 'Кантри');""")

connection.execute("""INSERT INTO artists (id, name)
VALUES (1, 'Петр Чайковский'), 
       (2, 'Вольфганг Амадей Моцарт'), 
       (3, 'Луи Армстронг'), 
       (4, 'Queen'), 
       (5, 'Nirvana'),
       (6, 'Måneskin'), 
       (7, 'Кубанский казачий хор'), 
       (8, 'Джонни Кэш');""")

connection.execute("""INSERT INTO artists_genres (artist_id, genre_id)
VALUES (1, 4), 
       (2, 4), 
       (3, 1), 
       (4, 2), 
       (5, 2),
       (6, 2), 
       (7, 3), 
       (8, 5);""")

connection.execute("""INSERT INTO albums (id, name, year_of_issue)
VALUES (1, 'Двадцать четыре лёгкие пьесы для фортепиано', 1878), 
       (2, 'Overtures', 1995), 
       (3, 'What A Wonderful World', 1967), 
       (4, 'A Night at the Opera', 1975), 
       (5, 'Nevermind', 1991),
       (6, 'Teatro d''ira', 2021), 
       (7, 'Там на Кубани', 1992), 
       (8, 'Songs Of Our Soil', 1959),
       (9, 'Il ballo della vita', 2018),
       (10, 'VENT''ANNI', 2019),
       (11, 'Mixed album', 2020);""")

connection.execute("""INSERT INTO albums_artists (album_id, artist_id)
VALUES (1, 1), 
       (2, 2), 
       (3, 3), 
       (4, 4), 
       (5, 5),
       (6, 6), 
       (7, 7), 
       (8, 8),
       (9, 6),
       (10, 6),
       (11, 1), 
       (11, 3);""")

connection.execute("""INSERT INTO tracks (id, name, duration, album_id)
VALUES (1, 'Зимнее утро', 70, 1), 
       (2, 'Баба-Яга', 71, 1), 
       (3, 'Lucio Silla, K.135: Overture', 512, 2), 
       (4, 'Don Giovanni - Overture', 273, 2), 
       (5, 'What A Wonderful World', 136, 3),
       (6, 'Cabaret', 164, 3), 
       (7, 'Love of My Life', 219, 4), 
       (8, 'Bohemian Rhapsody', 355, 4),
       (9, 'Smells like Teen Spirit', 301, 5), 
       (10, 'Something In The Way', 475, 5), 
       (11, 'Coraline', 300, 6), 
       (12, 'I wanna be your slave', 173, 6), 
       (13, 'Ой, там в саду', 310, 7),
       (14, 'Як служив я в пану', 285, 7), 
       (15, 'It Could Be You', 218, 8), 
       (16, 'My Grandfather''s Clock', 301, 8),
       (17, 'VENT''ANNI', 253, 10);""")

connection.execute("""INSERT INTO collections (id, name, year_of_issue)
VALUES (1, 'Сборник Петра Чайковского', 1964), 
       (2, 'Сборник Вольфганга Амадея Моцарта', 1980), 
       (3, 'Сборник Луи Армстронга', 1985), 
       (4, 'Сборник Queen', 1991), 
       (5, 'Сборник Nirvana', 2019),
       (6, 'Сборник Måneskin', 2020), 
       (7, 'Сборник Кубанского казачьего хора', 2000), 
       (8, 'Сборник Джонни Кэша', 1994);""")

connection.execute("""INSERT INTO collections_tracks (collection_id, track_id)
VALUES (1, 1), 
       (2, 3), 
       (3, 5), 
       (4, 7), 
       (5, 9),
       (6, 11), 
       (7, 13), 
       (8, 15);""")
