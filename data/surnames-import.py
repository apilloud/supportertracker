import zipfile
from cStringIO import StringIO
import re


def extract_surnames(cur):

    cur.execute("""
DROP TABLE IF EXISTS census_surnames;
	""")
    cur.execute("""
CREATE TABLE census_surnames
(
  name varchar(15) NOT NULL,
  count int NOT NULL,
  white int NOT NULL,
  black int NOT NULL,
  api int NOT NULL,
  aian int NOT NULL,
  multi int NOT NULL,
  hispanic int NOT NULL
);
	""")
    cur.execute("""
CREATE INDEX census_surnames_names_names_idx
 ON census_surnames
 (name);
	""")

    with zipfile.ZipFile("surnames.zip", 'r') as nameszip:
        for info in nameszip.infolist():
            if not info.filename == 'app_c.csv':
                continue
            for line in nameszip.read(info).split('\n')[1:]:
                if not line:
                    continue
                line = line.split(',')
                stats = []
                for stat in line[5:]:
                    if stat == '(S)':
                        stat = 0
                    stats.append(int(float(stat) * 100))
                cur.execute("INSERT INTO census_surnames VALUES (?, ?, ?, ?, ?, ?, ?, ?)", [
                            line[0], line[2]] + stats)

if __name__ == '__main__':
    import sqlite3

    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    extract_surnames(cur)

    conn.commit()
    conn.close()
