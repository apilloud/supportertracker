import zipfile
from cStringIO import StringIO
import re

CSLINE = 129
ZIP4FILE = re.compile("zip4/[0-9]{3}.zip")
ZIP4LINE = 182

def extract_zip4(cur):

	cur.execute("""
DROP TABLE IF EXISTS usps_cs_scheme;
	""")
	cur.execute("""
DROP TABLE IF EXISTS usps_cs_alias;
	""")
	cur.execute("""
DROP TABLE IF EXISTS usps_cs_zone;
	""")
	cur.execute("""
DROP TABLE IF EXISTS usps_cs_detail;
	""")
	cur.execute("""
DROP TABLE IF EXISTS usps_zip4_detail;
	""")
	cur.execute("""
CREATE TABLE usps_cs_scheme
(
  labelzipcode bigint NOT NULL,
  combinedzipcode bigint NOT NULL
);
	""")
	cur.execute("""
CREATE TABLE usps_cs_alias
(
  zipcode bigint NOT NULL,
  astpredirection character varying(2) NOT NULL DEFAULT '',
  astname character varying(28) NOT NULL DEFAULT '',
  asttype character varying(4) NOT NULL DEFAULT '',
  astpostdirection character varying(2) NOT NULL DEFAULT '',
  stpredirection character varying(2) NOT NULL DEFAULT '',
  stname character varying(28) NOT NULL DEFAULT '',
  sttype character varying(4) NOT NULL DEFAULT '',
  stpostdirection character varying(2) NOT NULL DEFAULT '',
  aliastype character(1) NOT NULL DEFAULT '',
  date date,
  stnumlow character varying(10) NOT NULL DEFAULT '',
  stnumhigh character varying(10) NOT NULL DEFAULT '',
  stparity character(1) NOT NULL DEFAULT ''
);
	""")
	cur.execute("""
CREATE TABLE usps_cs_zone
(
  oldzipcode bigint NOT NULL,
  oldcarrierrouteid character varying(4) NOT NULL,
  newzipcode bigint NOT NULL,
  newcarrierrouteid character varying(4) NOT NULL,
  date date NOT NULL
);
	""")
	cur.execute("""
CREATE TABLE usps_cs_detail
(
  zipcode bigint NOT NULL,
  citystatekey character varying(6) NOT NULL,
  zipclasification character(1),
  city character varying(28) NOT NULL,
  cityabbr character varying(13),
  facilitycode character(1),
  mailingnameind character(1),
  preferredcitystatekey character varying(6) NOT NULL,
  deliveryind character(1),
  carrierind character(1),
  uniquenameind character(1),
  financenumber integer NOT NULL,
  statecode character(2) NOT NULL,
  countycode smallint
);
	""")
	cur.execute("""
CREATE TABLE usps_zip4_detail
(
  zipcode bigint NOT NULL,
  updatekey character(10) NOT NULL,
  recordtypecode character(1),
  carrierrouteid character(4) NOT NULL,
  stpredirection character varying(2) NOT NULL DEFAULT '',
  stname character varying(28) NOT NULL DEFAULT '',
  sttype character varying(4) NOT NULL DEFAULT '',
  stpostdirection character varying(2) NOT NULL DEFAULT '',
  stnumlow character varying(10) NOT NULL DEFAULT '',
  stnumhigh character varying(10) NOT NULL DEFAULT '',
  stparity character(1) NOT NULL DEFAULT '',
  buildingfirmname character varying(40) NOT NULL DEFAULT '',
  unittype character varying(4) NOT NULL DEFAULT '',
  unitnumlow character varying(8) NOT NULL DEFAULT '',
  unitnumhigh character varying(8) NOT NULL DEFAULT '',
  unitparity character(1) NOT NULL DEFAULT '',
  zipcode4low character(4) NOT NULL DEFAULT '',
  zipcode4high character(4) NOT NULL DEFAULT '',
  basealternatecode character(1) NOT NULL DEFAULT '',
  lacsstatus character(1) NOT NULL DEFAULT '',
  governmentbuilding character(1) NOT NULL DEFAULT '',
  financenumber integer NOT NULL,
  statecode character(2) NOT NULL,
  countycode smallint NOT NULL,
  congressionaldistrict smallint NOT NULL,
  municipalitycitystatekey character varying(6) NOT NULL,
  urbanizationcitystatekey character varying(6),
  preferredcitystatekey character(6) NOT NULL
);
	""")
	cur.execute("""
CREATE INDEX usps_zip4_detail_zipstnum_idx
 ON usps_zip4_detail
 (zipcode, stname, sttype, stpredirection, stpostdirection, stnumlow, unitnumlow);
	""")
	cur.execute("""
CREATE INDEX usps_cs_detail_zipcode_idx
 ON usps_cs_detail
 (zipcode);
	""")
	cur.execute("""
CREATE INDEX usps_cs_detail_finance_idx
 ON usps_cs_detail
 (financenumber);
	""")
	cur.execute("""
CREATE INDEX usps_cs_detail_cskey_idx
 ON usps_cs_detail
 (citystatekey);
	""")

	with zipfile.ZipFile("natzip4.zip", 'r') as natzip4:
		ctystatedata = StringIO(natzip4.read("ctystate/ctystate.zip"))
		with zipfile.ZipFile(ctystatedata, 'r') as ctystatezip:
			with ctystatezip.open("ctystate.txt") as ctystate:
				line = ctystate.read(CSLINE)
				if line[0] != 'C':
					raise Exception("Bad ctystate.txt")
				countycode_cache = {}
				table = ""
				data = {}
				queries = {}
				while True:
					line = ctystate.read(CSLINE)
					if not line:
						break
					if line[0] == 'S':
						# SCHEME RECORD
						table = "usps_cs_scheme"
						data = {
								'labelzipcode': line[1:6],
								'combinedzipcode': line[6:11],
								}
					elif line[0] == 'A':
						# ALIAS RECORD
						table = "usps_cs_alias"
						data = {
								'zipcode': line[1:6],
								'astpredirection': line[6:8].strip(),
								'astname': line[8:36].strip(),
								'asttype': line[36:40].strip(),
								'astpostdirection': line[40:42].strip(),
								'stpredirection': line[42:44].strip(),
								'stname': line[44:72].strip(),
								'sttype': line[72:76].strip(),
								'stpostdirection': line[76:78].strip(),
								'aliastype': line[78:79],
								'date': line[79:87],
								'stnumlow': line[87:97].strip(),
								'stnumhigh': line[97:107].strip(),
								'stparity': line[107:108],
								}
					elif line[0] == 'Z':
						# ZONE SPLIT RECORD
						table = "usps_cs_zone"
						data = {
								'oldzipcode': line[1:6],
								'oldcarrierrouteid': line[6:10],
								'newzipcode': line[10:15],
								'newcarrierrouteid': line[15:19],
								'date': line[19:27],
								}
					elif line[0] == 'D':
						# DETAIL RECORD
						table = "usps_cs_detail"
						data = {
								'zipcode': line[1:6],
								'citystatekey': line[6:12],
								'zipclasification': line[12:13],
								'city': line[13:41].strip(),
								'cityabbr': line[41:54].strip(),
								'facilitycode': line[54:55],
								'mailingnameind': line[55:56],
								'preferredcitystatekey': line[56:62],
								'deliveryind': line[90:91],
								'carrierind': line[91:92],
								'uniquenameind': line[92:93],
								'financenumber': line[93:99],
								'statecode': line[99:101],
								'countycode': line[101:104].strip(),
								}
						if not data['countycode']:
							data['countycode'] = None
						if 'countycode' in data:
							if data['statecode'] not in countycode_cache:
								countycode_cache[data['statecode']] = []
							if data['countycode'] not in countycode_cache[data['statecode']]:
								countycode_cache[data['statecode']].append(data['countycode'])
								countyname = line[104:129].strip()
								#print (data['statecode'], data['countycode'], countyname)
					elif line[0] == 'N':
						# UNKNOWN RECORD
						continue
					else:
						raise Exception("Unknown ctystate.txt record")
					if table not in queries:
						query = "INSERT INTO " + table + " (" + ','.join(data.keys()) + ") VALUES (" + ','.join(['?']*len(data.keys())) + ")"
						queries[table] = query
					cur.execute(queries[table], data.values())
		
		for info in natzip4.infolist():
			if not ZIP4FILE.match(info.filename):
				continue
			zip4data = StringIO(natzip4.read(info))
			with zipfile.ZipFile(zip4data, 'r') as zip4zip:
				for zip4txt in zip4zip.infolist():
					print zip4txt.filename
					with zip4zip.open(zip4txt) as zip4:
						line = zip4.read(ZIP4LINE)
						if line[0] != 'C':
							raise Exception("Bad zip4: %s", zip4txt.filename)
						while True:
							line = zip4.read(ZIP4LINE)
							if not line:
								break
							table = "usps_zip4_detail"
							queries = {}
							if line[0] == 'D':
								# DETAIL RECORD
								data = {
										'zipcode': line[1:6],
										'updatekey': line[6:17].strip(),
										'recordtypecode': line[17:18].strip(),
										'carrierrouteid': line[18:22].strip(),
										'stpredirection': line[22:24].strip(),
										'stname': line[24:52].strip(),
										'sttype': line[52:56].strip(),
										'stpostdirection': line[56:58].strip(),
										'stnumlow': line[58:68].strip(),
										'stnumhigh': line[68:78].strip(),
										'stparity': line[78:79],
										'buildingfirmname': line[79:119].strip(),
										'unittype': line[119:123].strip(),
										'unitnumlow': line[123:131].strip(),
										'unitnumhigh': line[131:139].strip(),
										'unitparity': line[139:140],
										'zipcode4low': line[140:144],
										'zipcode4high': line[144:148],
										'basealternatecode': line[148:149],
										'lacsstatus': line[149:150],
										'governmentbuilding': line[150:151],
										'financenumber': line[151:157],
										'statecode': line[157:159],
										'countycode': line[159:162],
										'congressionaldistrict': line[162:164],
										'municipalitycitystatekey': line[164:170].strip(),
										'urbanizationcitystatekey': line[170:176].strip(),
										'preferredcitystatekey': line[176:182].strip(),
										}
								if data['congressionaldistrict'] == 'AL':
									data['congressionaldistrict'] = '1'
							else:
								raise Exception("Unknown zip4 record")
							if table not in queries:
								query = "INSERT INTO " + table + " (" + ','.join(data.keys()) + ") VALUES (" + ','.join(['?']*len(data.keys())) + ")"
								queries[table] = query
							cur.execute(queries[table], data.values())


if __name__ == '__main__':
	import sqlite3

	conn = sqlite3.connect('data.db')
	cur = conn.cursor()

	extract_zip4(cur)

	conn.commit()
	conn.close()
