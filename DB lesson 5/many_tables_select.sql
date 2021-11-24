-- количество исполнителей в каждом жанре
select count(*), g.name genre_name
  from artists_genres ag 
  join genres g on ag.genre_id  = g.id
 group by g.name;
 
-- количество треков, вошедших в альбомы 2019-2020 годов
select count(*) track_count
  from tracks t
  join albums a on t.album_id = a.id
 where a.year_of_issue between 2019 and 2020;

-- средняя продолжительность треков по каждому альбому
select avg(t.duration) avg_duration, a.name album_name
  from tracks t
  join albums a on t.album_id = a.id
 group by a.name;
 
-- все исполнители, которые не выпустили альбомы в 2020 году
select a.name artist 
  from artists a 
 where not exists (
   select 1
     from albums a2  
     join albums_artists aa  on a2.id = aa.album_id and aa.artist_id = a.id 
    where a2.year_of_issue = 2020
 );
 
-- названия сборников, в которых присутствует конкретный исполнитель
select c.name collection_name
  from collections c 
  join collections_tracks ct on c.id = ct.collection_id 
  join tracks t on t.id = ct.track_id 
  join albums a on a.id = t.album_id 
  join albums_artists aa on a.id = aa.album_id 
  join artists a2 on a2.id = aa.artist_id 
 where a2.name like 'Queen';

-- название альбомов, в которых присутствуют исполнители более 1 жанра;
select a.name album_name
  from albums a 
 where a.id in (
   select album_id
     from albums_artists aa
     join artists a2 on aa.artist_id  = a2.id 
	 join artists_genres ag on ag.artist_id = a2.id 
   group by aa.album_id
	having count(*) > 1);
	
-- наименование треков, которые не входят в сборники;
select t.name track_name
  from tracks t
  left join collections_tracks ct on ct.track_id  = t.id 
 where ct.collection_id  is null;
 
-- исполнителя(-ей), написавшего самый короткий по продолжительности трек 
select a.name artist_name
  from artists a 
  join albums_artists aa on a.id = aa.artist_id 
  join albums a2 on aa.album_id = a2.id 
  join tracks t on t.album_id = a2.id 
 where t.duration = (select min(duration)from tracks t2);

-- название альбомов, содержащих наименьшее количество треков.
select a.name
  from albums a
  join tracks t on a.id = t.album_id 
  group by a.name
 having count(*) = (
    select count(*) cnt
      from tracks t
     group by album_id
     order by 1
     limit 1
 );
 
