CREATE KEYSPACE IF NOT EXISTS trackfinder
  WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1};

USE trackfinder;

-- Fingerprints table:
-- Partition by (bucket, hash) to spread hot keys.
-- Sort by (song_id, t_anchor) inside the partition.
CREATE TABLE IF NOT EXISTS fingerprints_by_hash (
  bucket tinyint,             -- hash % 256
  hash bigint,                -- packed (f1,f2,Δt)
  song_id int,
  t_anchor int,               -- anchor time (frames or ms)
  PRIMARY KEY ((bucket, hash), song_id, t_anchor)
) WITH CLUSTERING ORDER BY (song_id ASC, t_anchor ASC);
