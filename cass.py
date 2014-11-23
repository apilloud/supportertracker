import re
import lib.addr

class Address:
	def __init__(self, mail, city='', statecode='', zipcode=''):
		self.data = {'mail': mail, 'city': city, 'statecode': statecode, 'zipcode': zipcode}

	def normalize(self, cur = None):
		""" cur myst be a key/value database cursor """
		address_in = self.data
		address = {'#normalized': True}
		address_stand = lib.addr.AddressStandardizationSolution()

		if 'city' in address_in and address_in['city']:
			address['city'] = address_in['city'].upper()
		if 'statecode' in address_in and address_in['statecode']:
			address['statecode'] = address_in['statecode'].upper()
		if 'zipcode' in address_in and address_in['zipcode'] and address_in['zipcode'].isdigit():
			address['zipcode'] = address_in['zipcode']
		if 'zipcode4' in address_in and address_in['zipcode4'] and address_in['zipcode4'].isdigit():
			address['zipcode4'] = address_in['zipcode4']

		if not ('mail' in address_in and address_in['mail']):
			address_in['mail'] = ''
			if 'stnum' in address_in:
				address_in['mail'] = address_in['mail'] + ' ' + address_in['stnum']
			if 'stfrac' in address_in:
				if len(address_in['stfrac']) > 2:
					address_in['mail'] = address_in['mail'] + ' '
				address_in['mail'] = address_in['mail'] + address_in['stfrac']
			if 'stpredirection' in address_in:
				address_in['mail'] = address_in['mail'] + ' ' + address_in['stpredirection']
			if 'stname' in address_in:
				address_in['mail'] = address_in['mail'] + ' ' + address_in['stname']
			if 'sttype' in address_in:
				address_in['mail'] = address_in['mail'] + ' ' + address_in['sttype']
			if 'stpostdirection' in address_in:
				address_in['mail'] = address_in['mail'] + ' ' + address_in['stpostdirection']
			if 'unittype' in address_in:
				address_in['mail'] = address_in['mail'] + ' ' + address_in['unittype']
			if 'unitnum' in address_in:
				address_in['mail'] = address_in['mail'] + ' ' + address_in['unitnum']

		if 'mail' in address_in and address_in['mail']:
			# Clear address
			address['stnum'] = ''
			address['stfrac'] = ''
			address['stpredirection'] = ''
			address['stname'] = ''
			address['sttype'] = ''
			address['stpostdirection'] = ''
			address['unittype'] = ''
			address['unitnum'] = ''

			address['mail'] = address_stand.AddressLineStandardization(address_in['mail'])

			tokens = address['mail'].split(' ')

			inname = True
			inunit = False

			# find last street direction and suffix
			endstdir = 0
			endstsuffix = 0
			endstname = 0
				
			for key, value in enumerate(tokens):
				# Street name can't end until 2
				if key < 2:
					continue
				if value + '-R' in address_stand.directionals:
					endstdir = key
					continue
				if value + '-R' in address_stand.suffixes:
					endstsuffix = key
					continue
				# A unit number shouldn't count!
				if value + '-R' in address_stand.identifiers:
					break

			# Find the correct end point
			if endstsuffix == (endstdir-1):
				endstname = endstsuffix
			elif endstsuffix > endstdir:
				endstname = endstsuffix
			else:
				endstname = endstdir

			for key, value in enumerate(tokens):
				if key == 0 and value[0].isdigit():
					address['stnum'] = value
					continue
				if key == 1 and len(value) >= 3 and (value[1] == '/' or (len(value) >= 5 and value[2] == '/') or (len(value) >= 7 and value[3] == '/')):
					address['stfrac'] = value
					continue
				if key <= 2 and inname == True and not address['stname'] and not address['stpredirection'] and value + '-R' in address_stand.directionals:
					address['stpredirection'] = value
					continue
				if address['stname']:
					if value + '-R' in address_stand.identifiers:
						inname = False
					elif key >= endstname and (value + '-R' in address_stand.directionals or value + '-R' in address_stand.suffixes):
						inname = False
				if inname:
					if address['stname']:
						address['stname'] = address['stname'] + ' ' + value
					else:
						address['stname'] = value
					continue
				if value + '-R' in address_stand.identifiers:
					address['unittype'] = value
					inunit = True
					continue
				if inunit:
					if address['unitnum']:
						address['unitnum'] = address['unitnum'] + ' ' + value
					else:
						address['unitnum'] = value
					continue
				if value + '-R' in address_stand.suffixes:
					address['sttype'] = value
					continue
				if value + '-R' in address_stand.directionals:
					address['stpostdirection'] = value
					continue
				inunit = True
				address['unitnum'] = value

			# Find PO BOX special case
			if address['unittype'] == 'BOX' and not address['stnum']:
				if address['stname'] == 'PO':
					address['stname'] = 'PO BOX'
				address['stnum'] = address['unitnum']
				address['unittype'] = ''
				address['unitnum'] = ''

			# Require unit number for unit
			if not address['unittype'] and address['unitnum']:
				address['unittype'] = '#'

		if not cur:
			self.data = address
			return address

		# Find city, state, zip from USPS
		if (('city' not in address) or ('statecode' not in address)) and ('zipcode' not in address):
				address['#error'] = 'Please provide a city and state, or zipcode.'
				self.data = address
				return address

		zipmatch = {}
		csmatch = {}

		# Step 1: Find full match
		if 'city' in address and 'statecode' in address and 'zipcode' in address and \
				address['city'] and address['statecode'] and address['zipcode']:
			cur.execute("""SELECT
					zipcode,
					citystatekey,
					financenumber,
					countycode
					FROM usps_cs_detail WHERE
					city = %s AND
					statecode = %s AND
					zipcode = %s
					LIMIT 1""",
					(address['city'],
						address['statecode'],
						address['zipcode']))
			csmatch = zipmatch = cur.fetchone()

		# Step 2: Find city state match
		if not csmatch and 'city' in address and 'statecode' in address and \
				address['city'] and address['statecode']:
			cur.execute("""SELECT
					citystatekey,
					financenumber,
					countycode
					FROM usps_cs_detail WHERE
					city = %s AND
					statecode = %s
					LIMIT 1""",
					(address['city'],
						address['statecode']))
			csmatch = cur.fetchone()

		# Step 3: Find city zip match
		if not zipmatch and 'city' in address and 'zipcode' in address and \
				address['city'] and address['zipcode']:
			cur.execute("""SELECT
					zipcode,
					citystatekey,
					financenumber,
					countycode
					FROM usps_cs_detail WHERE
					city = %s AND
					zipcode = %s
					LIMIT 1""",
					(address['city'],
						address['zipcode']))
			zipmatch = cur.fetchone()

		# Step 4: Find zip match
		if not zipmatch and 'zipcode' in address and address['zipcode']:
			cur.execute("""SELECT
					zipcode,
					preferredcitystatekey citystatekey,
					financenumber
					FROM usps_cs_detail WHERE
					zipcode = %s
					LIMIT 1""",
					(address['zipcode'],))
			zipmatch = cur.fetchone()

		# Lookup logic
		matchrules = []
		if csmatch and zipmatch:
			if csmatch['citystatekey'] == zipmatch['citystatekey']:
				# 1. Exact within zipcode
				# 2. Exact within citystatekey
				# 3. Inexact within zipcode
				# 4. Inexact within citystatekey
				# 5. Exact within finance number
				matchrules = [
						{'zipcode': zipmatch['zipcode'], 'exact': True},
						{'citystatekey': csmatch['citystatekey'], 'exact': True},
						{'zipcode': zipmatch['zipcode'], 'exact': False},
						{'citystatekey': csmatch['citystatekey'], 'exact': False},
						{'financenumber': zipmatch['financenumber'], 'exact': True},
					]
				address['citystatekey'] = csmatch['citystatekey']
				address['countycode'] = csmatch['countycode']
			elif csmatch['financenumber'] == zipmatch['financenumber']:
				# 1. Exact within citystatekey
				# 2. Exact within zipcode
				# 3. Inexact within citystatekey
				# 4. Inexact within zipcode
				# 5. Exact within finance number
				matchrules = [
						{'citystatekey': csmatch['citystatekey'], 'exact': True},
						{'zipcode': zipmatch['zipcode'], 'exact': True},
						{'citystatekey': csmatch['citystatekey'], 'exact': False},
						{'zipcode': zipmatch['zipcode'], 'exact': False},
						{'financenumber': zipmatch['financenumber'], 'exact': True},
					]
			else:
				# 1. Exact within citystatekey
				# 2. Exact within zipcode
				# 3. Inexact within citystatekey
				# 4. Inexact within zipcode
				# 5. Exact within cs finance number
				# 6. Exact within zip finance number
				matchrules = [
						{'citystatekey': csmatch['citystatekey'], 'exact': True},
						{'zipcode': zipmatch['zipcode'], 'exact': True},
						{'citystatekey': csmatch['citystatekey'], 'exact': False},
						{'zipcode': zipmatch['zipcode'], 'exact': False},
						{'financenumber': csmatch['financenumber'], 'exact': True},
						{'financenumber': zipmatch['financenumber'], 'exact': True},
					]
		elif csmatch:
			# 1. Exact within citystatekey
			# 2. Inexact within citystatekey
			# 3. Exact within finance number
			matchrules = [
					{'citystatekey': csmatch['citystatekey'], 'exact': True},
					{'citystatekey': csmatch['citystatekey'], 'exact': False},
					{'financenumber': csmatch['financenumber'], 'exact': True},
				]
			address['citystatekey'] = csmatch['citystatekey']
			address['countycode'] = csmatch['countycode']
		elif zipmatch:
			# 1. Exact within zipcode
			# 2. Inexact within zipcode
			# 3. Exact within finance number
			matchrules = [
					{'zipcode': zipmatch['zipcode'], 'exact': True},
					{'zipcode': zipmatch['zipcode'], 'exact': False},
					{'financenumber': zipmatch['financenumber'], 'exact': True},
				]
			address['preferredcitystatekey'] = zipmatch['citystatekey']
		else:
			address['#error'] = 'City and zipcode not found!'
			self.data = address
			return address

		candidate = {}

		if 'stname' in address and address['stname']:
			for rule in matchrules:
				# Lookup ZIP+4
				query_select = [
						'zip4_detail.updatekey AS zip4key',
						'zip4_detail.stpredirection',
						'zip4_detail.stname',
						'zip4_detail.sttype',
						'zip4_detail.stpostdirection',
						'zip4_detail.unittype',
						'zip4_detail.financenumber',
						'zip4_detail.statecode',
						'zip4_detail.countycode',
						'zip4_detail.congressionaldistrict',
						'zip4_detail.preferredcitystatekey',
						'zip4_detail.stnumlow',
						'zip4_detail.stnumhigh',
						'zip4_detail.stparity',
						'zip4_detail.unitnumlow',
						'zip4_detail.unitnumhigh',
						'zip4_detail.unitparity',
						'zip4_detail.zipcode',
						'zip4_detail.zipcode4low',
						'zip4_detail.zipcode4high',
						'zip4_detail.basealternatecode',
						'zip4_detail.recordtypecode',
						]
				query_select_params = []
				query = ["FROM usps_zip4_detail AS zip4_detail"]
				query_params = []
				query_where = []
				query_where_params = []

				# Always match zipcode ranges
				if 'zipcode' in rule:
					query_where.append('zip4_detail.zipcode = %s')
					query_where_params.append(rule['zipcode'])
				elif 'citystatekey' in rule:
					query.append("JOIN usps_cs_detail AS cs_detail ON cs_detail.zipcode = zip4_detail.zipcode AND cs_detail.citystatekey = %s")
					query_params.append(rule['citystatekey'])
				elif 'financenumber' in rule:
					query.append("JOIN usps_cs_detail AS cs_detail ON cs_detail.zipcode = zip4_detail.zipcode AND cs_detail.financenumber = %s")
					query_params.append(rule['financenumber'])

				# Always match street number ranges
				stnum = ''
				unitnum = ''
				unittype = ''
				if 'stnum' in address and address['stnum']:
					stparity = ('B',)
					stnum = address['stnum']
					unitnum = address['unitnum']
					unittype = address['unittype']
					matches = re.search(r'([0-9])[^0-9]*$', stnum)
					if matches:
						if int(matches.group(1)) % 2 == 0:
							# Even
							stparity = stparity + ('E',)
						else:
							# Odd
							stparity = stparity + ('O',)

					if stnum.isdigit():
						stnum = "%010d" % int(stnum)

					stnum_or = ['zip4_detail.stnumlow <= %s AND zip4_detail.stnumhigh >= %s AND zip4_detail.stparity IN %s']
					stnum_or_params = [stnum, stnum, stparity]

					# Fuzzy address match without trailing letter
					match = re.search(r'[^A-Z][A-Z]$', stnum, re.IGNORECASE)
					if match:
						stnum_sub = stnum[0:-1]
						if stnum_sub.isdigit():
							stnum_sub = "%010d" % int(stnum_sub)
						stnum_or.append('zip4_detail.stnumlow <= %s AND zip4_detail.stnumhigh > %s AND zip4_detail.stparity IN %s')
						stnum_or_params = stnum_or_params + [stnum_sub, stnum_sub, stparity]

					# Only allow fuzzy matches without a unit number, and with an exact zipcode
					if not ('unitnum' in address and address['unitnum']) and 'zipcode' in rule:
						stnum_or.append("zip4_detail.stnumlow = '' AND zip4_detail.stnumhigh = '' AND zip4_detail.recordtypecode IN %s")
						stnum_or_params.append(('S', 'H'))

					query_where.append("((" + ") OR (".join(stnum_or) + "))")
					query_where_params = query_where_params + stnum_or_params

				else:
					query_where.append("zip4_detail.stnumlow = '' AND zip4_detail.stnumhigh = ''")

				# Always match unit number ranges or blank
				if 'unitnum' in address and address['unitnum']:
					unitparity = ('B',)
					unitnum = address['unitnum']
					matches = re.search(r'([0-9])[^0-9]*$', unitnum)
					if matches:
						if int(matches.group(1)) % 2 == 0:
							# Even
							unitparity = unitparity + ('E',)
						else:
							# Odd
							unitparity = unitparity + ('O',)

					if unitnum.isdigit():
						unitnum = "%08d" % int(unitnum)

					unitnum_or = ['zip4_detail.unitnumlow <= %s AND zip4_detail.unitnumhigh >= %s AND zip4_detail.unitparity IN %s']
					unitnum_or_params = [unitnum, unitnum, unitparity]


					unitnum_or.append("zip4_detail.unitnumlow = '' AND zip4_detail.unitnumhigh = '' AND zip4_detail.recordtypecode IN %s")
					unitnum_or_params.append(('S', 'H'))

					query_where.append("((" + ") OR (".join(unitnum_or) + "))")
					query_where_params = query_where_params + unitnum_or_params

				else:
					query_where.append("zip4_detail.unitnumlow = '' AND zip4_detail.unitnumhigh = ''")

				# Partial match: street name
				if rule['exact']:
					query_where.append("zip4_detail.stname = %s")
					query_where_params.append(address['stname'])

				else:
					stname_or = ['zip4_detail.stname = %s']
					stname_or_params = [address['stname']]

					# Strip off any extra street types
					stname_trimed = ''
					for stname_token in address['stname'].split(' '):
						if stname_token in address_stand.suffixes:
							break
						stname_trimed = stname_trimed + ' ' + stname_token
					if stname_trimed and stname_trimed != address['stname']:
						stname_or.append('zip4_detail.stname = %s')
						stname_or_params.append(stname_trimed.strip())

					# Use metaphone on words only and not at finance number scope
					# address_temp => address
					#if (!preg_match('#[\d]#',$address_temp['stname']) && !array_key_exists('financenumber', $rule)) {
					#	$metaphone_names = array(
					#		metaphone($address_temp['stname'], 255),
					#	);
					#	//Predirection is part of name
					#	if ($address_temp['stpredirection']) {
					#		$metaphone_names[] = metaphone($address_stand->directionals[$address_temp['stpredirection'] . '-R'] . $address_temp['stname'], 255);
					#	}
					#	//Type is part of name
					#	if ($address_temp['sttype']) {
					#		$metaphone_names[] = metaphone($address_temp['stname'] . $address_stand->suffixes[$address_temp['sttype'] . '-R'], 255);
					#	}
					#	$stname_or->where('metaphone(zip4_detail.stname, 255) IN (:metaphone_stname)', array(':metaphone_stname' => $metaphone_names));
					#}

					query_where.append("((" + ") OR (".join(stname_or) + "))")
					query_where_params = query_where_params + stname_or_params
				
				# Optional match: other first line tokens
				subquery = []
				subquery_params = []
				subquery.append('zip4_detail.stpredirection = %s')
				subquery_params.append(address['stpredirection'])
				subquery.append('zip4_detail.sttype = %s')
				subquery_params.append(address['sttype'])
				subquery.append('zip4_detail.stpostdirection = %s')
				subquery_params.append(address['stpostdirection'])

				unit_or = []
				if address['unittype'] == '#':
					unit_or.append("zip4_detail.unittype != ''")
				else:
					unit_or.append('zip4_detail.unittype = %s')
					subquery_params.append(address['unittype'])
				unit_or.append("zip4_detail.unittype = '' AND zip4_detail.recordtypecode IN %s")
				subquery_params.append(('S', 'H'))

				subquery.append("((" + ") OR (".join(unit_or) + "))")
		
				if rule['exact']:
					query_where = query_where + subquery
				else:
					query_where.append("((" + ") OR (".join(subquery) + "))")
				query_where_parms = query_where_params + subquery_params

				# Calculate match weight function (of optional match fields)
				matchweight = []
				matchweight_params = []
				matchweight_params_in = {
						'stpredirection': address['stpredirection'],
						'stname': address['stname'],
						'sttype': address['sttype'],
						'stpostdirection': address['stpostdirection'],
						}
				for key, value in matchweight_params_in.items():
					matchweight.append("CAST((zip4_detail." + key + " = %s) AS INTEGER)")
					matchweight_params.append(value)

				if address['unittype'] == '#':
					matchweight.append("CAST((zip4_detail.unittype != '' OR (recordtypecode in ('S', 'H') AND zip4_detail.unittype = '')) AS INTEGER)")

				else:
					matchweight.append("CAST((zip4_detail.unittype = %s OR (recordtypecode in ('S', 'H') AND zip4_detail.unittype = '')) AS INTEGER)")
					matchweight_params.append(address['unittype'])

				query_select.append("(" + " + ".join(matchweight) + ") AS weight")
				query_select_params = query_select_params + matchweight_params


				# Calculate the subweight function (of range match fields)
				query_select.append('(CAST((stnumlow = %s AND stnumhigh = %s) AS INTEGER) + CAST((unitnumlow = %s AND unitnumhigh = %s) AS INTEGER) + CAST((stnumlow <= %s AND stnumhigh >= %s) AS INTEGER) + CAST((unitnumlow <= %s AND unitnumhigh >= %s) AS INTEGER) + CAST((stnumlow <= %s AND stnumhigh >= %s AND length(stnumlow) = length(%s)) AS INTEGER) + CAST((unitnumlow <= %s AND unitnumhigh >= %s AND length(unitnumlow) = length(%s)) AS INTEGER) + CAST((unittype = %s) AS INTEGER)) AS subweight')
				query_select_params = query_select_params + [stnum, stnum, unitnum, unitnum, stnum, stnum, unitnum, unitnum, stnum, stnum, stnum, unitnum, unitnum, unitnum, unittype]

				querysql = "SELECT " + ", ".join(query_select) + " " + " ".join(query) +" WHERE " + " AND ".join(query_where) + " ORDER BY weight DESC, subweight DESC, zip4_detail.zipcode4low"
				querysql_params = query_select_params + query_params + query_where_parms
				cur.execute(querysql, querysql_params)

				candidates = []
				weight = 4 # Full match = 5
				subweight = 0
				for value in cur:
					if value['weight'] < weight:
						break
					weight = value['weight']
					if value['subweight'] < subweight:
						break
					subweight = value['subweight']
					candidates.append(value)

				count = len(candidates)
				if count == 1:
					candidate = candidates[0]
					break
				elif count > 1:
					continue

			if candidate:
				for key, value in dict(candidate).items():
					address[key] = value
				if address['zipcode4low'] != address['zipcode4high']:
					address['zipcode4'] = str(int(address['stnum']) - int(address['stnumlow']) + int(address['zipcode4low']))
				else:
					address['zipcode4'] = address['zipcode4low']

			# Lookup the prefered second line
			if 'preferredcitystatekey' in address and address['preferredcitystatekey']:
				#set details out of database
				cur.execute("""SELECT
						city,
						statecode,
						citystatekey,
						countycode
						FROM usps_cs_detail WHERE
						zipcode = %s AND
						citystatekey = %s
						LIMIT 1""",
						(address['zipcode'],
							address['preferredcitystatekey']))
				values = cur.fetchone()

				if values:
					for key, value in dict(values).items():
						if key == 'countycode' and 'zipcode4' in address and address['zipcode4']:
							continue
						address[key] = value

			# Recalculate street string
			if not address['unittype'] and address['unitnum']:
				address['unittype'] = '#'
			address['mail'] = ''
			if 'stnum' in address and address['stnum']:
				address['mail'] = address['stnum']
			if 'stfrac' in address and address['stfrac']:
				if len(address['stfrac']) > 2:
					address['mail'] = address['mail'] + ' '
				address['mail'] = address['mail'] + address['stfrac']
			if 'stpredirection' in address and address['stpredirection']:
				address['mail'] = address['mail'] + ' ' + address['stpredirection']
			if 'stname' in address and address['stname']:
				if address['stname'] == 'PO BOX':
					address['mail'] = address['stname'] + ' ' + address['mail']
				elif re.match(r'^(RR|HC|PSC|CMR|UNIT) ', address['stname']):
					address['mail'] = address['stname'] + ' BOX ' + address['mail']
				else:
					address['mail'] = address['mail'] + ' ' + address['stname']
			if 'sttype' in address and address['sttype']:
				address['mail'] = address['mail'] + ' ' + address['sttype']
			if 'stpostdirection' in address and address['stpostdirection']:
				address['mail'] = address['mail'] + ' ' + address['stpostdirection']
			if 'unittype' in address and address['unittype']:
				address['mail'] = address['mail'] + ' ' + address['unittype']
			if 'unitnum' in address and address['unitnum']:
				address['mail'] = address['mail'] + ' ' + address['unitnum']
			address['mail'] = address['mail'].strip()

			# Lookup the prefered first line
			if 'basealternatecode' in address and address['basealternatecode'] == 'A' and not ('basealternatecode' in address_in and address_in['basealternatecode'] == 'A'):
				# set details out of database
				address_base = address
				$query = db_select('usps_zip4_detail', 'zip4_detail');
				$query->addField('zip4_detail', 'stnumlow', 'stnum');
				$query->addField('zip4_detail', 'stpredirection');
				$query->addField('zip4_detail', 'stname');
				$query->addField('zip4_detail', 'sttype');
				$query->addField('zip4_detail', 'unittype');
				$query->addField('zip4_detail', 'unitnumlow');
				$query->addField('zip4_detail', 'unitnumhigh');
				$query->addField('zip4_detail', 'stpostdirection');
				$query->addField('zip4_detail', 'recordtypecode');
				$query->condition('zip4_detail.basealternatecode', 'B');
				$query->condition('zip4_detail.zipcode', $address['zipcode']);
				$query->condition('zip4_detail.zipcode4low', $address['zipcode4']);
				$query->condition('zip4_detail.zipcode4high', $address['zipcode4high']);
				$values = $query->range(0, 1)->execute();
				if (count($values) > 0) foreach ($values as $vkey => $vvalue) {
					if ($vvalue->unittype == '') {
						unset($vvalue->unittype);
					}
					if ($vvalue->unitnumlow != '') {
						if ($vvalue->unitnumlow == $vvalue->unitnumhigh) {
							$address_base['unitnum'] = $vvalue->unitnumlow;
						}
						else {
							// Unit number ranges Example: (J65 -> 00000065, 401 -> 401B, 1150 -> 1150, 101A -> A101, A -> 1...)
							preg_match('/^([A-Z]*)([\d]*)([A-Z]*)$/', $address_base['unitnum'], $base_tokens);
							preg_match('/^([A-Z]*)([\d]*)([A-Z]*)$/', ltrim($vvalue->unitnumlow, '0'), $low_tokens);
							preg_match('/^([A-Z]*)([\d]*)([A-Z]*)$/', ltrim($vvalue->unitnumhigh, '0'), $high_tokens);

							// ? -> Numeric
							if ($low_tokens[2] && !$low_tokens[1] && !$low_tokens[3]) {
								// Numeric -> Numeric
								if ($base_tokens[2] >= $low_tokens[2] && $base_tokens[2] <= $high_tokens[2])
								{
									$address_base['unitnum'] = $base_tokens[2];
								}
								// Alpha -> Numeric
								else if (!$base_tokens[2]) {
									$num = (ord($base_tokens[1])-ord('A'))+1;
									if ($num >= $low_tokens[2] && $num <= $high_tokens[2])
									{
										$address_base['unitnum'] = $num;
									}
								}
							}
							// ? -> Alpha
							elseif (!$low_tokens[2] && $low_tokens[1] && !$low_tokens[3]) {
								// Numeric -> Alpha
								if ($base_tokens[2] && !$base_tokens[1] && !$base_tokens[3] && $base_tokens[2] < 27)
								{
									$num = chr($base_tokens[1]+ord('A')+1);
									if ($num >= $low_tokens[3] && $num <= $high_tokens[3])
									{
										$address_base['unitnum'] = $num;
									}
								}
							}
							// ? -> Alpha Numeric
							elseif ($low_tokens[2] && $low_tokens[1] && !$low_tokens[3]) {
								// Numeric Alpha -> Alpha Numeric
								if ($base_tokens[2] >= $low_tokens[2] && $base_tokens[2] <= $high_tokens[2] && $base_tokens[3] >= $low_tokens[1] && $base_tokens[3] <= $high_tokens[1])
								{
									$address_base['unitnum'] = $base_tokens[3] . $base_tokens[2];
								}
							}
							// ? -> Numeric Alpha
							elseif ($low_tokens[2] && !$low_tokens[1] && $low_tokens[3]) {
								// Alpha Numeric -> Numeric Alpha
								if ($base_tokens[2] >= $low_tokens[2] && $base_tokens[2] <= $high_tokens[2] && $base_tokens[1] >= $low_tokens[3] && $base_tokens[1] <= $high_tokens[3])
								{
									$address_base['unitnum'] = $base_tokens[2] . $base_tokens[1];
								}
							}
						}
					}
					foreach ($vvalue as $key => $value) {
						$address_base[$key] = $value;
					}
					$address_base['stnum'] = ltrim($address_base['stnum'], '0');
					$address_base['stfrac'] = '';
					if (!$address_base['unitnum']) {
						$address_base['unitnum'] = $address['stnum'];
					}
					unset($address_base['mail']);
					$address_base = $this->normalize($address_base);
					if ($address_base['unittype'] != '#') {
						$address = $address_base;
					}
				}
			}

			if 'zipcode4' in address and (not address['zipcode4'].isdigit() or int(address['zipcode4']) == 0):
				del address['zipcode4']
			
			# Calculate Delivery Point Code
			if 'zipcode4' in address and 'recordtypecode' in address and address['recordtypecode'] == 'H':
				# Secondary
				unitnum_nofrac = re.sub(r' ?[0-9]+\/[0-9]+( ?[A-Z])?$', '', address['unitnum'], re.IGNORECASE)
				unitnum_clean = re.sub(r'[^0-9A-Z]', '', unitnum_nofrac, re.IGNORECASE)
				x_table = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 41, 42, 43, 44, 45, 46]
				if 'unitnumlow' in address and address['unitnumlow'] == '':
					# Rule 6: Address Matched to a ZIP + 4 Record with Blank Secondary Ranges
					# Rule 7: Address Matching to a Highrise Default Record
					address['deliverypointcode'] = 99
				elif unitnum_clean.isdigit():
					y_top = int(unitnum_clean) % 100
					x_htp = (int(unitnum_clean)/100) % 100
					if x_htp == 0:
						# Rule 1: Numeric Simple Rule
						address['deliverypointcode'] = y_top
					else:
						# Rule 5: Numeric Computed Rule
						address['deliverypointcode'] = 25*(x_htp % 4) + (y_top % 25)

				elif unitnum_clean == '':
					# Rule 8: Fractional Only Secondary Addresses
					address['deliverypointcode'] = 0
				elif re.match(r'^[A-Z]+$', unitnum_clean, re.IGNORECASE):
					# Rule 2: Alphabetic Rule
					address['deliverypointcode'] = ord(unitnum_clean[-1].upper()) - ord('A') + 73
				elif re.search(r'[0-9]+[A-Z]+$', unitnum_clean, re.IGNORECASE):
					# Rule 3: Alphanumeric Rule-Trailing Alpha
					x_alpha = x_table[ord(unitnum_clean[-1].upper()) - ord('A')]
					matches = re.search(r'([0-9])[A-Z]+$', unitnum_clean, re.IGNORECASE)
					y_num = int(matches.group(1))
					address['deliverypointcode'] = (x_alpha + y_num * 10) % 100
				elif re.search(r'[A-Z]+[0-9]+$', unitnum_clean, re.IGNORECASE):
					# Rule 4: Alphanumeric Rule-Trailing Numeric
					matches = re.match(r'^[^A-Z]*([A-Z])', unitnum_clean, re.IGNORECASE)
					x_alpha = x_table[ord(matches.group(1).upper()) - ord('A')]
					y_num = int(unitnum_clean[-1])
					address['deliverypointcode'] = (x_alpha * 10 + y_num) % 100

			elif 'zipcode4' in address and 'recordtypecode' in address:
				# Primary
				if address['stnum'].isdigit():
					# General rule
					address['deliverypointcode'] = int(address['stnum'][-2:])
				elif address['stnum'] == '':
					# No numbers or alpha only
					address['deliverypointcode'] = 99
				elif re.match(r'^[0-9]+[A-Z ]+$', address['stnum'], re.IGNORECASE):
					# Trailing alphas
					matches = re.search(r'([0-9]+)[A-Z ]+$', address['stnum'], re.IGNORECASE)
					address['deliverypointcode'] = int(matches.group(1)[-2:])
				elif re.search(r'[0-9]+$', address['stnum'], re.IGNORECASE):
					# Leading or embeded
					matches = re.search(r'[0-9]+$', address['stnum'], re.IGNORECASE)
					address['deliverypointcode'] = int(matches.group(0)[-2:])
				else:
					address['deliverypointcode'] = 99

			elif 'deliverypointcode' in address:
				del address['deliverypointcode']

			self.data = address
			return address

