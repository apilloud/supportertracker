import zipfile
from cStringIO import StringIO
import re

YOBFILE = re.compile("yob[12][089]\d\d.txt")


def extract_babynames(cur):

    cur.execute("""
DROP TABLE IF EXISTS ss_babynames;
	""")
    cur.execute("""
CREATE TABLE ss_babynames
(
  name varchar(15) NOT NULL,
  count int NOT NULL,
  male int NOT NULL,
  female int NOT NULL
);
	""")
    cur.execute("""
CREATE INDEX ss_babynames_names_idx
 ON ss_babynames
 (name);
	""")

    with zipfile.ZipFile("babynames.zip", 'r') as nameszip:
        table = {}
        for info in nameszip.infolist():
            if not YOBFILE.match(info.filename):
                continue
            for line in nameszip.read(info).split('\r\n'):
                if not line:
                    continue
                line = line.split(',')
                if line[0] not in table:
                    table[line[0]] = {'M': 0, 'F': 0}
                table[line[0]][line[1]] += int(line[2])
        for name in table:
            male = table[name]['M']
            female = table[name]['F']
            total = male + female
            male = male * 100 / total
            female = female * 100 / total
            cur.execute("INSERT INTO ss_babynames VALUES (?, ?, ?, ?)", [
                        name.upper(), total, male, female])


if __name__ == '__main__':
    import sqlite3

    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    extract_babynames(cur)

    conn.commit()
    conn.close()
