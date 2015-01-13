import zipfile
from cStringIO import StringIO
import re

def extract_corptokens(cur):

	cur.execute("""
DROP TABLE IF EXISTS corptokens;
	""")
	cur.execute("""
CREATE TABLE corptokens
(
  name varchar(15) NOT NULL,
  count int NOT NULL
);
	""")
	cur.execute("""
CREATE INDEX corptokens_names_names_idx
 ON corptokens
 (name);
	""")

	with zipfile.ZipFile("corptokens.zip", 'r') as nameszip:
		for info in nameszip.infolist():
			if not info.filename == 'corptokens.csv':
				continue
			for line in nameszip.read(info).split('\n')[1:]:
				if not line:
					continue
				line = line.split(',')
				cur.execute("INSERT INTO corptokens VALUES (?, ?)", [line[0], line[1]])

if __name__ == '__main__':
	import sqlite3

	conn = sqlite3.connect('data.db')
	cur = conn.cursor()

	extract_corptokens(cur)

	conn.commit()
	conn.close()
