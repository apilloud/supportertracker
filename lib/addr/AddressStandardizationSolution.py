import re

#**
#* A python port of the
#* Address Standardization Solution, PHP Edition.
#*
#* Address Standardization Solution is a trademark of The Analysis
#* and Solutions Company.
#*
#* @package AddressStandardizationSolution
#* @author Daniel Convissor <danielc@analysisandsolutions.com>
#* @copyright The Analysis and Solutions Company, 2001-2010
#* @license http:#www.analysisandsolutions.com/software/license.htm Simple Public License
#* @link http:#www.analysisandsolutions.com/software/addr/addr.htm
#*


#**
#* Formats a Delivery Address Line according to the United States Postal
#* Service's Addressing Standards
#*
#*
#* @package AddressStandardizationSolution
#* @author Daniel Convissor <danielc@analysisandsolutions.com>
#* @copyright The Analysis and Solutions Company, 2001-2010
#* @license http:#www.analysisandsolutions.com/software/license.htm Simple Public License
#* @link http:#www.analysisandsolutions.com/software/addr/addr.htm
#*
class AddressStandardizationSolution:

	def __init__(self):
		#An array with compass directions as keys and abbreviations as values
		self.directionals = {
				'E' : 'E',
				'EAST' : 'E',
				'E-R' : 'EAST',
				'N' : 'N',
				'NO' : 'N',
				'NORTH' : 'N',
				'N-R' : 'NORTH',
				'NE' : 'NE',
				'NORTHEAST' : 'NE',
				'NE-R' : 'NORTHEAST',
				'NORTHWEST' : 'NW',
				'NW-R' : 'NORTHWEST',
				'NW' : 'NW',
				'S' : 'S',
				'SO' : 'S',
				'SOUTH' : 'S',
				'S-R' : 'SOUTH',
				'SE' : 'SE',
				'SOUTHEAST' : 'SE',
				'SE-R' : 'SOUTHEAST',
				'SOUTHWEST' : 'SW',
				'SW-R' : 'SOUTHWEST',
				'SW' : 'SW',
				'W' : 'W',
				'WEST' : 'W',
				'W-R' : 'WEST',
				}

		# An array with room types as keys and abbreviations as values
		self.identifiers = {
				'APARTMENT' : 'APT',
				'APT-R' : 'APARTMENT',
				'APT' : 'APT',
				'BLDG' : 'BLDG',
				'BUILDING' : 'BLDG',
				'BLDG-R' : 'BUILDING',
				'BOX' : 'BOX',
				'BOX-R' : 'BOX',
				'BASEMENT' : 'BSMT',
				'BSMT-R' : 'BASEMENT',
				'BSMT' : 'BSMT',
				'DEPARTMENT' : 'DEPT',
				'DEPT-R' : 'DEPARTMENT',
				'DEPT' : 'DEPT',
				'FL' : 'FL',
				'FLOOR' : 'FL',
				'FL-R' : 'FLOOR',
				'FRNT' : 'FRNT',
				'FRONT' : 'FRNT',
				'FRNT-R' : 'FRONT',
				'HANGER' : 'HNGR',
				'HNGR-R' : 'HANGER',
				'HNGR' : 'HNGR',
				'KEY' : 'KEY',
				'KEY-R' : 'KEY',
				'LBBY' : 'LBBY',
				'LOBBY' : 'LBBY',
				'LBBY-R' : 'LOBBY',
				'LOT' : 'LOT',
				'LOT-R' : 'LOT',
				'LOWER' : 'LOWR',
				'LOWR-R' : 'LOWER',
				'LOWR' : 'LOWR',
				'OFC' : 'OFC',
				'OFFICE' : 'OFC',
				'OFC-R' : 'OFFICE',
				'PENTHOUSE' : 'PH',
				'PH-R' : 'PENTHOUSE',
				'PH' : 'PH',
				'PIER' : 'PIER',
				'PIER-R' : 'PIER',
				'PMB' : 'PMB',
				'PMB-R' : 'PMB',
				'REAR' : 'REAR',
				'REAR-R' : 'REAR',
				'RM' : 'RM',
				'ROOM' : 'RM',
				'RM-R' : 'ROOM',
				'SIDE' : 'SIDE',
				'SIDE-R' : 'SIDE',
				'SLIP' : 'SLIP',
				'SLIP-R' : 'SLIP',
				'SPACE' : 'SPC',
				'SPC-R' : 'SPACE',
				'SPC' : 'SPC',
				'STE' : 'STE',
				'SUITE' : 'STE',
				'STE-R' : 'SUITE',
				'MAILSTOP' : 'STOP',
				'STOP' : 'STOP',
				'STOP-R' : 'STOP',
				'TRAILER' : 'TRLR',
				'TRLR-R' : 'TRAILER',
				'TRLR' : 'TRLR',
				'UNIT' : 'UNIT',
				'UNIT-R' : 'UNIT',
				'UPPER' : 'UPPR',
				'UPPR-R' : 'UPPER',
				'UPPR' : 'UPPR',
				'UPR' : 'UPPR',
				'#-R' : '#',
				'#' : '#',
				}

		 # An array with numeric words as keys and numbers as values
		self.numbers = {
				'FIRST' : '1',
				'ONE' : '1',
				'TEN' : '10',
				'TENTH' : '10',
				'ELEVEN' : '11',
				'ELEVENTH' : '11',
				'TWELFTH' : '12',
				'TWELVE' : '12',
				'THIRTEEN' : '13',
				'THIRTEENTH' : '13',
				'FOURTEEN' : '14',
				'FOURTEENTH' : '14',
				'FIFTEEN' : '15',
				'FIFTEENTH' : '15',
				'SIXTEEN' : '16',
				'SIXTEENTH' : '16',
				'SEVENTEEN' : '17',
				'SEVENTEENTH' : '17',
				'EIGHTEEN' : '18',
				'EIGHTEENTH' : '18',
				'NINETEEN' : '19',
				'NINETEENTH' : '19',
				'SECOND' : '2',
				'TWO' : '2',
				'TWENTIETH' : '20',
				'TWENTY' : '20',
				'THIRD' : '3',
				'THREE' : '3',
				'FOUR' : '4',
				'FOURTH' : '4',
				'FIFTH' : '5',
				'FIVE' : '5',
				'SIX' : '6',
				'SIXTH' : '6',
				'SEVEN' : '7',
				'SEVENTH' : '7',
				'EIGHT' : '8',
				'EIGHTH' : '8',
				'NINE' : '9',
				'NINTH' : '9',
				}

		 # An array with state names as keys and abbreviations as values
		self.states = {
				'ARMED FORCES AMERICA' : 'AA',
				'ARMED FORCES EUROPE' : 'AE',
				'ALASKA' : 'AK',
				'ALABAMA' : 'AL',
				'ARMED FORCES PACIFIC' : 'AP',
				'ARKANSAS' : 'AR',
				'ARIZONA' : 'AZ',
				'CALIFORNIA' : 'CA',
				'COLORADO' : 'CO',
				'CONNECTICUT' : 'CT',
				'DISTRICT OF COLUMBIA' : 'DC',
				'DELAWARE' : 'DE',
				'FLORIDA' : 'FL',
				'GEORGIA' : 'GA',
				'HAWAII' : 'HI',
				'IOWA' : 'IA',
				'IDAHO' : 'ID',
				'ILLINOIS' : 'IL',
				'INDIANA' : 'IN',
				'KANSAS' : 'KS',
				'KENTUCKY' : 'KY',
				'LOUISIANA' : 'LA',
				'MASSACHUSETTS' : 'MA',
				'MARYLAND' : 'MD',
				'MAINE' : 'ME',
				'MICHIGAN' : 'MI',
				'MINNESOTA' : 'MN',
				'MISSOURI' : 'MO',
				'MISSISSIPPI' : 'MS',
				'MONTANA' : 'MT',
				'NORTH CAROLINA' : 'NC',
				'NORTH DAKOTA' : 'ND',
				'NEBRASKA' : 'NE',
				'NEW HAMPSHIRE' : 'NH',
				'NEW JERSEY' : 'NJ',
				'NEW MEXICO' : 'NM',
				'NEVADA' : 'NV',
				'NEW YORK' : 'NY',
				'OHIO' : 'OH',
				'OKLAHOMA' : 'OK',
				'OREGON' : 'OR',
				'PENNSYLVANIA' : 'PA',
				'RHODE ISLAND' : 'RI',
				'SOUTH CAROLINA' : 'SC',
				'SOUTH DAKOTA' : 'SD',
				'TENNESSEE' : 'TN',
				'TEXAS' : 'TX',
				'UTAH' : 'UT',
				'VIRGINIA' : 'VA',
				'VERMONT' : 'VT',
				'WASHINGTON' : 'WA',
				'WISCONSIN' : 'WI',
				'WEST VIRGINIA' : 'WV',
				'WYOMING' : 'WY',
				}

		# An array with street types as keys and abbreviations as values
		self.suffixes = {
				'ALLEE' : 'ALY',
				'ALLEY' : 'ALY',
				'ALY-R' : 'ALLEY',
				'ALLY' : 'ALY',
				'ALY' : 'ALY',
				'ANEX' : 'ANX',
				'ANNEX' : 'ANX',
				'ANX-R' : 'ANNEX',
				'ANNX' : 'ANX',
				'ANX' : 'ANX',
				'ARC' : 'ARC',
				'ARCADE' : 'ARC',
				'ARC-R' : 'ARCADE',
				'AV' : 'AVE',
				'AVE' : 'AVE',
				'AVEN' : 'AVE',
				'AVENU' : 'AVE',
				'AVENUE' : 'AVE',
				'AVE-R' : 'AVENUE',
				'AVN' : 'AVE',
				'AVNUE' : 'AVE',
				'BCH' : 'BCH',
				'BEACH' : 'BCH',
				'BCH-R' : 'BEACH',
				'BG' : 'BG',
				'BURG' : 'BG',
				'BG-R' : 'BURG',
				'BGS' : 'BGS',
				'BURGS' : 'BGS',
				'BGS-R' : 'BURGS',
				'BLF' : 'BLF',
				'BLUF' : 'BLF',
				'BLUFF' : 'BLF',
				'BLF-R' : 'BLUFF',
				'BLFS' : 'BLFS',
				'BLUFFS' : 'BLFS',
				'BLFS-R' : 'BLUFFS',
				'BLVD' : 'BLVD',
				'BLVRD' : 'BLVD',
				'BOUL' : 'BLVD',
				'BOULEVARD' : 'BLVD',
				'BLVD-R' : 'BOULEVARD',
				'BOULOVARD' : 'BLVD',
				'BOULV' : 'BLVD',
				'BOULVRD' : 'BLVD',
				'BULAVARD' : 'BLVD',
				'BULEVARD' : 'BLVD',
				'BULLEVARD' : 'BLVD',
				'BULOVARD' : 'BLVD',
				'BULVD' : 'BLVD',
				'BEND' : 'BND',
				'BND-R' : 'BEND',
				'BND' : 'BND',
				'BR' : 'BR',
				'BRANCH' : 'BR',
				'BR-R' : 'BRANCH',
				'BRNCH' : 'BR',
				'BRDGE' : 'BRG',
				'BRG' : 'BRG',
				'BRGE' : 'BRG',
				'BRIDGE' : 'BRG',
				'BRG-R' : 'BRIDGE',
				'BRK' : 'BRK',
				'BROOK' : 'BRK',
				'BRK-R' : 'BROOK',
				'BRKS' : 'BRKS',
				'BROOKS' : 'BRKS',
				'BRKS-R' : 'BROOKS',
				'BOT' : 'BTM',
				'BOTTM' : 'BTM',
				'BOTTOM' : 'BTM',
				'BTM-R' : 'BOTTOM',
				'BTM' : 'BTM',
				'BYP' : 'BYP',
				'BYPA' : 'BYP',
				'BYPAS' : 'BYP',
				'BYPASS' : 'BYP',
				'BYP-R' : 'BYPASS',
				'BYPS' : 'BYP',
				'BAYOO' : 'BYU',
				'BAYOU' : 'BYU',
				'BYU-R' : 'BAYOU',
				'BYO' : 'BYU',
				'BYOU' : 'BYU',
				'BYU' : 'BYU',
				'CIR' : 'CIR',
				'CIRC' : 'CIR',
				'CIRCEL' : 'CIR',
				'CIRCL' : 'CIR',
				'CIRCLE' : 'CIR',
				'CIR-R' : 'CIRCLE',
				'CRCL' : 'CIR',
				'CRCLE' : 'CIR',
				'CIRCELS' : 'CIRS',
				'CIRCLES' : 'CIRS',
				'CIRS-R' : 'CIRCLES',
				'CIRCLS' : 'CIRS',
				'CIRCS' : 'CIRS',
				'CIRS' : 'CIRS',
				'CRCLES' : 'CIRS',
				'CRCLS' : 'CIRS',
				'CLB' : 'CLB',
				'CLUB' : 'CLB',
				'CLB-R' : 'CLUB',
				'CLF' : 'CLF',
				'CLIF' : 'CLF',
				'CLIFF' : 'CLF',
				'CLF-R' : 'CLIFF',
				'CLFS' : 'CLFS',
				'CLIFFS' : 'CLFS',
				'CLFS-R' : 'CLIFFS',
				'CLIFS' : 'CLFS',
				'CMN' : 'CMN',
				'COMMON' : 'CMN',
				'CMN-R' : 'COMMON',
				'COMN' : 'CMN',
				'COR' : 'COR',
				'CORN' : 'COR',
				'CORNER' : 'COR',
				'COR-R' : 'CORNER',
				'CRNR' : 'COR',
				'CORNERS' : 'CORS',
				'CORS-R' : 'CORNERS',
				'CORNRS' : 'CORS',
				'CORS' : 'CORS',
				'CRNRS' : 'CORS',
				'CAMP' : 'CP',
				'CP-R' : 'CAMP',
				'CMP' : 'CP',
				'CP' : 'CP',
				'CAPE' : 'CPE',
				'CPE-R' : 'CAPE',
				'CPE' : 'CPE',
				'CRECENT' : 'CRES',
				'CRES' : 'CRES',
				'CRESCENT' : 'CRES',
				'CRES-R' : 'CRESCENT',
				'CRESENT' : 'CRES',
				'CRSCNT' : 'CRES',
				'CRSENT' : 'CRES',
				'CRSNT' : 'CRES',
				'CK' : 'CRK',
				'CR' : 'CRK',
				'CREEK' : 'CRK',
				'CRK-R' : 'CREEK',
				'CREK' : 'CRK',
				'CRK' : 'CRK',
				'COARSE' : 'CRSE',
				'COURSE' : 'CRSE',
				'CRSE-R' : 'COURSE',
				'CRSE' : 'CRSE',
				'CREST' : 'CRST',
				'CRST-R' : 'CREST',
				'CRST' : 'CRST',
				'CAUSEWAY' : 'CSWY',
				'CSWY-R' : 'CAUSEWAY',
				'CAUSEWY' : 'CSWY',
				'CAUSWAY' : 'CSWY',
				'CAUSWY' : 'CSWY',
				'CSWY' : 'CSWY',
				'CORT' : 'CT',
				'COURT' : 'CT',
				'CT-R' : 'COURT',
				'CRT' : 'CT',
				'CT' : 'CT',
				'CEN' : 'CTR',
				'CENT' : 'CTR',
				'CENTER' : 'CTR',
				'CTR-R' : 'CENTER',
				'CENTR' : 'CTR',
				'CENTRE' : 'CTR',
				'CNTER' : 'CTR',
				'CNTR' : 'CTR',
				'CTR' : 'CTR',
				'CENS' : 'CTRS',
				'CENTERS' : 'CTRS',
				'CTRS-R' : 'CENTERS',
				'CENTRES' : 'CTRS',
				'CENTRS' : 'CTRS',
				'CENTS' : 'CTRS',
				'CNTERS' : 'CTRS',
				'CNTRS' : 'CTRS',
				'CTRS' : 'CTRS',
				'COURTS' : 'CTS',
				'CTS-R' : 'COURTS',
				'CTS' : 'CTS',
				'CRV' : 'CURV',
				'CURV' : 'CURV',
				'CURVE' : 'CURV',
				'CURV-R' : 'CURVE',
				'COV' : 'CV',
				'COVE' : 'CV',
				'CV-R' : 'COVE',
				'CV' : 'CV',
				'COVES' : 'CVS',
				'CVS-R' : 'COVES',
				'COVS' : 'CVS',
				'CVS' : 'CVS',
				'CAN' : 'CYN',
				'CANYN' : 'CYN',
				'CANYON' : 'CYN',
				'CYN-R' : 'CANYON',
				'CNYN' : 'CYN',
				'CYN' : 'CYN',
				'DAL' : 'DL',
				'DALE' : 'DL',
				'DL-R' : 'DALE',
				'DL' : 'DL',
				'DAM' : 'DM',
				'DM-R' : 'DAM',
				'DM' : 'DM',
				'DR' : 'DR',
				'DRIV' : 'DR',
				'DRIVE' : 'DR',
				'DR-R' : 'DRIVE',
				'DRV' : 'DR',
				'DRIVES' : 'DRS',
				'DRS-R' : 'DRIVES',
				'DRIVS' : 'DRS',
				'DRS' : 'DRS',
				'DRVS' : 'DRS',
				'DIV' : 'DV',
				'DIVD' : 'DV',
				'DIVID' : 'DV',
				'DIVIDE' : 'DV',
				'DV-R' : 'DIVIDE',
				'DV' : 'DV',
				'DVD' : 'DV',
				'EST' : 'EST',
				'ESTA' : 'EST',
				'ESTATE' : 'EST',
				'EST-R' : 'ESTATE',
				'ESTAS' : 'ESTS',
				'ESTATES' : 'ESTS',
				'ESTS-R' : 'ESTATES',
				'ESTS' : 'ESTS',
				'EXP' : 'EXPY',
				'EXPR' : 'EXPY',
				'EXPRESS' : 'EXPY',
				'EXPRESSWAY' : 'EXPY',
				'EXPY-R' : 'EXPRESSWAY',
				'EXPRESWAY' : 'EXPY',
				'EXPRSWY' : 'EXPY',
				'EXPRWY' : 'EXPY',
				'EXPW' : 'EXPY',
				'EXPWY' : 'EXPY',
				'EXPY' : 'EXPY',
				'EXWAY' : 'EXPY',
				'EXWY' : 'EXPY',
				'EXT' : 'EXT',
				'EXTEN' : 'EXT',
				'EXTENSION' : 'EXT',
				'EXT-R' : 'EXTENSION',
				'EXTENSN' : 'EXT',
				'EXTN' : 'EXT',
				'EXTNSN' : 'EXT',
				'EXTENS' : 'EXTS',
				'EXTENSIONS' : 'EXTS',
				'EXTS-R' : 'EXTENSIONS',
				'EXTENSNS' : 'EXTS',
				'EXTNS' : 'EXTS',
				'EXTNSNS' : 'EXTS',
				'EXTS' : 'EXTS',
				'FAL' : 'FALL',
				'FALL' : 'FALL',
				'FALL-R' : 'FALL',
				'FIELD' : 'FLD',
				'FLD-R' : 'FIELD',
				'FLD' : 'FLD',
				'FIELDS' : 'FLDS',
				'FLDS-R' : 'FIELDS',
				'FLDS' : 'FLDS',
				'FALLS' : 'FLS',
				'FLS-R' : 'FALLS',
				'FALS' : 'FLS',
				'FLS' : 'FLS',
				'FLAT' : 'FLT',
				'FLT-R' : 'FLAT',
				'FLT' : 'FLT',
				'FLATS' : 'FLTS',
				'FLTS-R' : 'FLATS',
				'FLTS' : 'FLTS',
				'FORD' : 'FRD',
				'FRD-R' : 'FORD',
				'FRD' : 'FRD',
				'FORDS' : 'FRDS',
				'FRDS-R' : 'FORDS',
				'FRDS' : 'FRDS',
				'FORG' : 'FRG',
				'FORGE' : 'FRG',
				'FRG-R' : 'FORGE',
				'FRG' : 'FRG',
				'FORGES' : 'FRGS',
				'FRGS-R' : 'FORGES',
				'FRGS' : 'FRGS',
				'FORK' : 'FRK',
				'FRK-R' : 'FORK',
				'FRK' : 'FRK',
				'FORKS' : 'FRKS',
				'FRKS-R' : 'FORKS',
				'FRKS' : 'FRKS',
				'FOREST' : 'FRST',
				'FRST-R' : 'FOREST',
				'FORESTS' : 'FRST',
				'FORREST' : 'FRST',
				'FORRESTS' : 'FRST',
				'FORRST' : 'FRST',
				'FORRSTS' : 'FRST',
				'FORST' : 'FRST',
				'FORSTS' : 'FRST',
				'FRRESTS' : 'FRST',
				'FRRST' : 'FRST',
				'FRRSTS' : 'FRST',
				'FRST' : 'FRST',
				'FERRY' : 'FRY',
				'FRY-R' : 'FERRY',
				'FERY' : 'FRY',
				'FRRY' : 'FRY',
				'FRY' : 'FRY',
				'FORT' : 'FT',
				'FT-R' : 'FORT',
				'FRT' : 'FT',
				'FT' : 'FT',
				'FREEWAY' : 'FWY',
				'FWY-R' : 'FREEWAY',
				'FREEWY' : 'FWY',
				'FREWAY' : 'FWY',
				'FREWY' : 'FWY',
				'FRWAY' : 'FWY',
				'FRWY' : 'FWY',
				'FWY' : 'FWY',
				'GARDEN' : 'GDN',
				'GDN-R' : 'GARDEN',
				'GARDN' : 'GDN',
				'GDN' : 'GDN',
				'GRDEN' : 'GDN',
				'GRDN' : 'GDN',
				'GARDENS' : 'GDNS',
				'GDNS-R' : 'GARDENS',
				'GARDNS' : 'GDNS',
				'GDNS' : 'GDNS',
				'GRDENS' : 'GDNS',
				'GRDNS' : 'GDNS',
				'GLEN' : 'GLN',
				'GLN-R' : 'GLEN',
				'GLENN' : 'GLN',
				'GLN' : 'GLN',
				'GLENNS' : 'GLNS',
				'GLENS' : 'GLNS',
				'GLNS-R' : 'GLENS',
				'GLNS' : 'GLNS',
				'GREEN' : 'GRN',
				'GRN-R' : 'GREEN',
				'GREN' : 'GRN',
				'GRN' : 'GRN',
				'GREENS' : 'GRNS',
				'GRNS-R' : 'GREENS',
				'GRENS' : 'GRNS',
				'GRNS' : 'GRNS',
				'GROV' : 'GRV',
				'GROVE' : 'GRV',
				'GRV-R' : 'GROVE',
				'GRV' : 'GRV',
				'GROVES' : 'GRVS',
				'GRVS-R' : 'GROVES',
				'GROVS' : 'GRVS',
				'GRVS' : 'GRVS',
				'GATEWAY' : 'GTWY',
				'GTWY-R' : 'GATEWAY',
				'GATEWY' : 'GTWY',
				'GATWAY' : 'GTWY',
				'GTWAY' : 'GTWY',
				'GTWY' : 'GTWY',
				'HARB' : 'HBR',
				'HARBOR' : 'HBR',
				'HBR-R' : 'HARBOR',
				'HARBR' : 'HBR',
				'HBR' : 'HBR',
				'HRBOR' : 'HBR',
				'HARBORS' : 'HBRS',
				'HBRS-R' : 'HARBORS',
				'HBRS' : 'HBRS',
				'HILL' : 'HL',
				'HL-R' : 'HILL',
				'HL' : 'HL',
				'HILLS' : 'HLS',
				'HLS-R' : 'HILLS',
				'HLS' : 'HLS',
				'HLLW' : 'HOLW',
				'HLLWS' : 'HOLW',
				'HOLLOW' : 'HOLW',
				'HOLW-R' : 'HOLLOW',
				'HOLLOWS' : 'HOLW',
				'HOLOW' : 'HOLW',
				'HOLOWS' : 'HOLW',
				'HOLW' : 'HOLW',
				'HOLWS' : 'HOLW',
				'HEIGHT' : 'HTS',
				'HEIGHTS' : 'HTS',
				'HTS-R' : 'HEIGHTS',
				'HGTS' : 'HTS',
				'HT' : 'HTS',
				'HTS' : 'HTS',
				'HAVEN' : 'HVN',
				'HVN-R' : 'HAVEN',
				'HAVN' : 'HVN',
				'HVN' : 'HVN',
				'HIGHWAY' : 'HWY',
				'HWY-R' : 'HIGHWAY',
				'HIGHWY' : 'HWY',
				'HIWAY' : 'HWY',
				'HIWY' : 'HWY',
				'HWAY' : 'HWY',
				'HWY' : 'HWY',
				'HYGHWAY' : 'HWY',
				'HYWAY' : 'HWY',
				'HYWY' : 'HWY',
				'INLET' : 'INLT',
				'INLT-R' : 'INLET',
				'INLT' : 'INLT',
				'ILAND' : 'IS',
				'ILND' : 'IS',
				'IS' : 'IS',
				'ISLAND' : 'IS',
				'IS-R' : 'ISLAND',
				'ISLND' : 'IS',
				'ILE' : 'ISLE',
				'ISLE' : 'ISLE',
				'ISLE-R' : 'ISLE',
				'ISLES' : 'ISLE',
				'ILANDS' : 'ISS',
				'ILNDS' : 'ISS',
				'ISLANDS' : 'ISS',
				'ISS-R' : 'ISLANDS',
				'ISLDS' : 'ISS',
				'ISLNDS' : 'ISS',
				'ISS' : 'ISS',
				'JCT' : 'JCT',
				'JCTION' : 'JCT',
				'JCTN' : 'JCT',
				'JUNCTION' : 'JCT',
				'JCT-R' : 'JUNCTION',
				'JUNCTN' : 'JCT',
				'JUNCTON' : 'JCT',
				'JCTIONS' : 'JCTS',
				'JCTNS' : 'JCTS',
				'JCTS' : 'JCTS',
				'JUNCTIONS' : 'JCTS',
				'JCTS-R' : 'JUNCTIONS',
				'JUNCTONS' : 'JCTS',
				'JUNGTNS' : 'JCTS',
				'KNL' : 'KNL',
				'KNOL' : 'KNL',
				'KNOLL' : 'KNL',
				'KNL-R' : 'KNOLL',
				'KNLS' : 'KNLS',
				'KNOLLS' : 'KNLS',
				'KNLS-R' : 'KNOLLS',
				'KNOLS' : 'KNLS',
				'KEY' : 'KY',
				'KY-R' : 'KEY',
				'KY' : 'KY',
				'KEYS' : 'KYS',
				'KYS-R' : 'KEYS',
				'KYS' : 'KYS',
				'LAND' : 'LAND',
				'LAND-R' : 'LAND',
				'LCK' : 'LCK',
				'LOCK' : 'LCK',
				'LCK-R' : 'LOCK',
				'LCKS' : 'LCKS',
				'LOCKS' : 'LCKS',
				'LCKS-R' : 'LOCKS',
				'LDG' : 'LDG',
				'LDGE' : 'LDG',
				'LODG' : 'LDG',
				'LODGE' : 'LDG',
				'LDG-R' : 'LODGE',
				'LF' : 'LF',
				'LOAF' : 'LF',
				'LF-R' : 'LOAF',
				'LGT' : 'LGT',
				'LIGHT' : 'LGT',
				'LGT-R' : 'LIGHT',
				'LT' : 'LGT',
				'LGTS' : 'LGTS',
				'LIGHTS' : 'LGTS',
				'LGTS-R' : 'LIGHTS',
				'LTS' : 'LGTS',
				'LAKE' : 'LK',
				'LK-R' : 'LAKE',
				'LK' : 'LK',
				'LAKES' : 'LKS',
				'LKS-R' : 'LAKES',
				'LKS' : 'LKS',
				'LA' : 'LN',
				'LANE' : 'LN',
				'LN-R' : 'LANE',
				'LANES' : 'LN',
				'LN' : 'LN',
				'LNS' : 'LN',
				'LANDG' : 'LNDG',
				'LANDING' : 'LNDG',
				'LNDG-R' : 'LANDING',
				'LANDNG' : 'LNDG',
				'LNDG' : 'LNDG',
				'LNDNG' : 'LNDG',
				'LOOP' : 'LOOP',
				'LOOP-R' : 'LOOP',
				'LOOPS' : 'LOOP',
				'MALL' : 'MALL',
				'MALL-R' : 'MALL',
				'MDW' : 'MDW',
				'MEADOW' : 'MDW',
				'MDW-R' : 'MEADOW',
				'MDWS' : 'MDWS',
				'MEADOWS' : 'MDWS',
				'MDWS-R' : 'MEADOWS',
				'MEDOWS' : 'MDWS',
				'MEDWS' : 'MDWS',
				'MEWS' : 'MEWS',
				'MEWS-R' : 'MEWS',
				'MIL' : 'ML',
				'MILL' : 'ML',
				'ML-R' : 'MILL',
				'ML' : 'ML',
				'MILLS' : 'MLS',
				'MLS-R' : 'MILLS',
				'MILS' : 'MLS',
				'MLS' : 'MLS',
				'MANOR' : 'MNR',
				'MNR-R' : 'MANOR',
				'MANR' : 'MNR',
				'MNR' : 'MNR',
				'MANORS' : 'MNRS',
				'MNRS-R' : 'MANORS',
				'MANRS' : 'MNRS',
				'MNRS' : 'MNRS',
				'MISN' : 'MSN',
				'MISSION' : 'MSN',
				'MSN-R' : 'MISSION',
				'MISSN' : 'MSN',
				'MSN' : 'MSN',
				'MSSN' : 'MSN',
				'MNT' : 'MT',
				'MOUNT' : 'MT',
				'MT-R' : 'MOUNT',
				'MT' : 'MT',
				'MNTAIN' : 'MTN',
				'MNTN' : 'MTN',
				'MOUNTAIN' : 'MTN',
				'MTN-R' : 'MOUNTAIN',
				'MOUNTIN' : 'MTN',
				'MTIN' : 'MTN',
				'MTN' : 'MTN',
				'MNTNS' : 'MTNS',
				'MOUNTAINS' : 'MTNS',
				'MTNS-R' : 'MOUNTAINS',
				'MTNS' : 'MTNS',
				'MOTORWAY' : 'MTWY',
				'MTWY-R' : 'MOTORWAY',
				'MOTORWY' : 'MTWY',
				'MOTRWY' : 'MTWY',
				'MOTWY' : 'MTWY',
				'MTRWY' : 'MTWY',
				'MTWY' : 'MTWY',
				'NCK' : 'NCK',
				'NECK' : 'NCK',
				'NCK-R' : 'NECK',
				'NEK' : 'NCK',
				'OPAS' : 'OPAS',
				'OVERPAS' : 'OPAS',
				'OVERPASS' : 'OPAS',
				'OPAS-R' : 'OVERPASS',
				'OVERPS' : 'OPAS',
				'OVRPS' : 'OPAS',
				'ORCH' : 'ORCH',
				'ORCHARD' : 'ORCH',
				'ORCH-R' : 'ORCHARD',
				'ORCHRD' : 'ORCH',
				'OVAL' : 'OVAL',
				'OVAL-R' : 'OVAL',
				'OVL' : 'OVAL',
				'PARK' : 'PARK',
				'PARK-R' : 'PARK',
				'PARKS' : 'PARK',
				'PK' : 'PARK',
				'PRK' : 'PARK',
				'PAS' : 'PASS',
				'PASS' : 'PASS',
				'PASS-R' : 'PASS',
				'PATH' : 'PATH',
				'PATH-R' : 'PATH',
				'PATHS' : 'PATH',
				'PIKE' : 'PIKE',
				'PIKE-R' : 'PIKE',
				'PIKES' : 'PIKE',
				'PARKWAY' : 'PKWY',
				'PKWY-R' : 'PARKWAY',
				'PARKWAYS' : 'PKWY',
				'PARKWY' : 'PKWY',
				'PKWAY' : 'PKWY',
				'PKWY' : 'PKWY',
				'PKWYS' : 'PKWY',
				'PKY' : 'PKWY',
				'PL' : 'PL',
				'PLAC' : 'PL',
				'PLACE' : 'PL',
				'PL-R' : 'PLACE',
				'PLASE' : 'PL',
				'PLAIN' : 'PLN',
				'PLN-R' : 'PLAIN',
				'PLN' : 'PLN',
				'PLAINES' : 'PLNS',
				'PLAINS' : 'PLNS',
				'PLNS-R' : 'PLAINS',
				'PLNS' : 'PLNS',
				'PLAZ' : 'PLZ',
				'PLAZA' : 'PLZ',
				'PLZ-R' : 'PLAZA',
				'PLZ' : 'PLZ',
				'PLZA' : 'PLZ',
				'PZ' : 'PLZ',
				'PINE' : 'PNE',
				'PNE-R' : 'PINE',
				'PNE' : 'PNE',
				'PINES' : 'PNES',
				'PNES-R' : 'PINES',
				'PNES' : 'PNES',
				'PR' : 'PR',
				'PRAIR' : 'PR',
				'PRAIRIE' : 'PR',
				'PR-R' : 'PRAIRIE',
				'PRARE' : 'PR',
				'PRARIE' : 'PR',
				'PRR' : 'PR',
				'PRRE' : 'PR',
				'PORT' : 'PRT',
				'PRT-R' : 'PORT',
				'PRT' : 'PRT',
				'PORTS' : 'PRTS',
				'PRTS-R' : 'PORTS',
				'PRTS' : 'PRTS',
				'PASG' : 'PSGE',
				'PASSAGE' : 'PSGE',
				'PSGE-R' : 'PASSAGE',
				'PASSG' : 'PSGE',
				'PSGE' : 'PSGE',
				'PNT' : 'PT',
				'POINT' : 'PT',
				'PT-R' : 'POINT',
				'PT' : 'PT',
				'PNTS' : 'PTS',
				'POINTS' : 'PTS',
				'PTS-R' : 'POINTS',
				'PTS' : 'PTS',
				'RAD' : 'RADL',
				'RADIAL' : 'RADL',
				'RADL-R' : 'RADIAL',
				'RADIEL' : 'RADL',
				'RADL' : 'RADL',
				'RAMP' : 'RAMP',
				'RAMP-R' : 'RAMP',
				'RD' : 'RD',
				'ROAD' : 'RD',
				'RD-R' : 'ROAD',
				'RDG' : 'RDG',
				'RDGE' : 'RDG',
				'RIDGE' : 'RDG',
				'RDG-R' : 'RIDGE',
				'RDGS' : 'RDGS',
				'RIDGES' : 'RDGS',
				'RDGS-R' : 'RIDGES',
				'RDS' : 'RDS',
				'ROADS' : 'RDS',
				'RDS-R' : 'ROADS',
				'RIV' : 'RIV',
				'RIVER' : 'RIV',
				'RIV-R' : 'RIVER',
				'RIVR' : 'RIV',
				'RVR' : 'RIV',
				'RANCH' : 'RNCH',
				'RNCH-R' : 'RANCH',
				'RANCHES' : 'RNCH',
				'RNCH' : 'RNCH',
				'RNCHS' : 'RNCH',
				'RAOD' : 'RD',
				'ROW' : 'ROW',
				'ROW-R' : 'ROW',
				'RAPID' : 'RPD',
				'RPD-R' : 'RAPID',
				'RPD' : 'RPD',
				'RAPIDS' : 'RPDS',
				'RPDS-R' : 'RAPIDS',
				'RPDS' : 'RPDS',
				'REST' : 'RST',
				'RST-R' : 'REST',
				'RST' : 'RST',
				'ROUTE' : 'RTE',
				'RTE-R' : 'ROUTE',
				'RT' : 'RTE',
				'RTE' : 'RTE',
				'RUE' : 'RUE',
				'RUE-R' : 'RUE',
				'RUN' : 'RUN',
				'RUN-R' : 'RUN',
				'SHL' : 'SHL',
				'SHOAL' : 'SHL',
				'SHL-R' : 'SHOAL',
				'SHOL' : 'SHL',
				'SHLS' : 'SHLS',
				'SHOALS' : 'SHLS',
				'SHLS-R' : 'SHOALS',
				'SHOLS' : 'SHLS',
				'SHOAR' : 'SHR',
				'SHORE' : 'SHR',
				'SHR-R' : 'SHORE',
				'SHR' : 'SHR',
				'SHOARS' : 'SHRS',
				'SHORES' : 'SHRS',
				'SHRS-R' : 'SHORES',
				'SHRS' : 'SHRS',
				'SKWY' : 'SKWY',
				'SKYWAY' : 'SKWY',
				'SKWY-R' : 'SKYWAY',
				'SKYWY' : 'SKWY',
				'SMT' : 'SMT',
				'SUMIT' : 'SMT',
				'SUMITT' : 'SMT',
				'SUMMIT' : 'SMT',
				'SMT-R' : 'SUMMIT',
				'SUMT' : 'SMT',
				'SPG' : 'SPG',
				'SPNG' : 'SPG',
				'SPRING' : 'SPG',
				'SPG-R' : 'SPRING',
				'SPRNG' : 'SPG',
				'SPGS' : 'SPGS',
				'SPNGS' : 'SPGS',
				'SPRINGS' : 'SPGS',
				'SPGS-R' : 'SPRINGS',
				'SPRNGS' : 'SPGS',
				'SPR' : 'SPUR',
				'SPRS' : 'SPUR',
				'SPUR' : 'SPUR',
				'SPUR-R' : 'SPUR',
				'SPURS' : 'SPUR',
				'SQ' : 'SQ',
				'SQAR' : 'SQ',
				'SQR' : 'SQ',
				'SQRE' : 'SQ',
				'SQU' : 'SQ',
				'SQUARE' : 'SQ',
				'SQ-R' : 'SQUARE',
				'SQARS' : 'SQS',
				'SQRS' : 'SQS',
				'SQS' : 'SQS',
				'SQUARES' : 'SQS',
				'SQS-R' : 'SQUARES',
				'ST' : 'ST',
				'STR' : 'ST',
				'STREET' : 'ST',
				'ST-R' : 'STREET',
				'STRT' : 'ST',
				'STA' : 'STA',
				'STATION' : 'STA',
				'STA-R' : 'STATION',
				'STATN' : 'STA',
				'STN' : 'STA',
				'STRA' : 'STRA',
				'STRAV' : 'STRA',
				'STRAVE' : 'STRA',
				'STRAVEN' : 'STRA',
				'STRAVENUE' : 'STRA',
				'STRA-R' : 'STRAVENUE',
				'STRAVN' : 'STRA',
				'STRVN' : 'STRA',
				'STRVNUE' : 'STRA',
				'STREAM' : 'STRM',
				'STRM-R' : 'STREAM',
				'STREME' : 'STRM',
				'STRM' : 'STRM',
				'STREETS' : 'STS',
				'STS-R' : 'STREETS',
				'STS' : 'STS',
				'TER' : 'TER',
				'TERACE' : 'TER',
				'TERASE' : 'TER',
				'TERR' : 'TER',
				'TERRACE' : 'TER',
				'TER-R' : 'TERRACE',
				'TERRASE' : 'TER',
				'TERRC' : 'TER',
				'TERRICE' : 'TER',
				'TPK' : 'TPKE',
				'TPKE' : 'TPKE',
				'TRNPK' : 'TPKE',
				'TRPK' : 'TPKE',
				'TURNPIKE' : 'TPKE',
				'TPKE-R' : 'TURNPIKE',
				'TURNPK' : 'TPKE',
				'TRACK' : 'TRAK',
				'TRAK-R' : 'TRACK',
				'TRACKS' : 'TRAK',
				'TRAK' : 'TRAK',
				'TRK' : 'TRAK',
				'TRKS' : 'TRAK',
				'TRACE' : 'TRCE',
				'TRCE-R' : 'TRACE',
				'TRACES' : 'TRCE',
				'TRCE' : 'TRCE',
				'TRAFFICWAY' : 'TRFY',
				'TRFY-R' : 'TRAFFICWAY',
				'TRAFFICWY' : 'TRFY',
				'TRAFWAY' : 'TRFY',
				'TRFCWY' : 'TRFY',
				'TRFFCWY' : 'TRFY',
				'TRFFWY' : 'TRFY',
				'TRFWY' : 'TRFY',
				'TRFY' : 'TRFY',
				'TR' : 'TRL',
				'TRAIL' : 'TRL',
				'TRL-R' : 'TRAIL',
				'TRAILS' : 'TRL',
				'TRL' : 'TRL',
				'TRLS' : 'TRL',
				'THROUGHWAY' : 'TRWY',
				'TRWY-R' : 'THROUGHWAY',
				'THROUGHWY' : 'TRWY',
				'THRUWAY' : 'TRWY',
				'THRUWY' : 'TRWY',
				'THRWAY' : 'TRWY',
				'THRWY' : 'TRWY',
				'THWY' : 'TRWY',
				'TRWY' : 'TRWY',
				'TUNEL' : 'TUNL',
				'TUNL' : 'TUNL',
				'TUNLS' : 'TUNL',
				'TUNNEL' : 'TUNL',
				'TUNL-R' : 'TUNNEL',
				'TUNNELS' : 'TUNL',
				'TUNNL' : 'TUNL',
				'UN' : 'UN',
				'UNION' : 'UN',
				'UN-R' : 'UNION',
				'UNIONS' : 'UNS',
				'UNS-R' : 'UNIONS',
				'UNS' : 'UNS',
				'UDRPS' : 'UPAS',
				'UNDERPAS' : 'UPAS',
				'UNDERPASS' : 'UPAS',
				'UPAS-R' : 'UNDERPASS',
				'UNDERPS' : 'UPAS',
				'UNDRPAS' : 'UPAS',
				'UNDRPS' : 'UPAS',
				'UPAS' : 'UPAS',
				'VDCT' : 'VIA',
				'VIA' : 'VIA',
				'VIADCT' : 'VIA',
				'VIADUCT' : 'VIA',
				'VIA-R' : 'VIADUCT',
				'VIS' : 'VIS',
				'VIST' : 'VIS',
				'VISTA' : 'VIS',
				'VIS-R' : 'VISTA',
				'VST' : 'VIS',
				'VSTA' : 'VIS',
				'VILLE' : 'VL',
				'VL-R' : 'VILLE',
				'VL' : 'VL',
				'VILG' : 'VLG',
				'VILL' : 'VLG',
				'VILLAG' : 'VLG',
				'VILLAGE' : 'VLG',
				'VLG-R' : 'VILLAGE',
				'VILLG' : 'VLG',
				'VILLIAGE' : 'VLG',
				'VLG' : 'VLG',
				'VILGS' : 'VLGS',
				'VILLAGES' : 'VLGS',
				'VLGS-R' : 'VILLAGES',
				'VLGS' : 'VLGS',
				'VALLEY' : 'VLY',
				'VLY-R' : 'VALLEY',
				'VALLY' : 'VLY',
				'VALY' : 'VLY',
				'VLLY' : 'VLY',
				'VLY' : 'VLY',
				'VALLEYS' : 'VLYS',
				'VLYS-R' : 'VALLEYS',
				'VLYS' : 'VLYS',
				'VIEW' : 'VW',
				'VW-R' : 'VIEW',
				'VW' : 'VW',
				'VIEWS' : 'VWS',
				'VWS-R' : 'VIEWS',
				'VWS' : 'VWS',
				'WALK' : 'WALK',
				'WALK-R' : 'WALK',
				'WALKS' : 'WALK',
				'WLK' : 'WALK',
				'WALL' : 'WALL',
				'WALL-R' : 'WALL',
				'WAY' : 'WAY',
				'WAY-R' : 'WAY',
				'WY' : 'WAY',
				'WAYS' : 'WAYS',
				'WAYS-R' : 'WAYS',
				'WEL' : 'WL',
				'WELL' : 'WL',
				'WL-R' : 'WELL',
				'WL' : 'WL',
				'WELLS' : 'WLS',
				'WLS-R' : 'WELLS',
				'WELS' : 'WLS',
				'WLS' : 'WLS',
				'CROSING' : 'XING',
				'CROSNG' : 'XING',
				'CROSSING' : 'XING',
				'XING-R' : 'CROSSING',
				'CRSING' : 'XING',
				'CRSNG' : 'XING',
				'CRSSING' : 'XING',
				'CRSSNG' : 'XING',
				'XING' : 'XING',
				'CROSRD' : 'XRD',
				'CROSSRD' : 'XRD',
				'CROSSROAD' : 'XRD',
				'XRD-R' : 'CROSSROAD',
				'CRSRD' : 'XRD',
				'XRD' : 'XRD',
				'XROAD' : 'XRD',
				}

		# An array with things that look like street types but are actually names
		self.suffixSimiles = {
				'LA' : 'LA',
				'ST' : 'SAINT',
				'VIA' : 'VIA',
				}


	#**
	#* Formats a Delivery Address Line according to the United States Postal
	#* Service's Addressing Standards
	#*
	#* This comes in VERY handy when searching for records by address.
	#* Let's say a data entry person put an address in as
	#* "Two N Boulevard."  Later, someone else searches for them using
	#* "2 North Blvd."  Unfortunately, that query won't find them.  Such
	#* problems are averted by using this method before storing and
	#* searching for data.
	#*
	#* Standardization can also help obtain lower bulk mailing rates.
	#*
	#* Based upon USPS Publication 28, November 1997.
	#*
	#* @param string address  the address to be converted
	#*
	#* @return string  the cleaned up address
	#*
	#* @link http:#pe.usps.gov/cpim/ftp/pubs/Pub28/pub28.pdf
	#*
	def AddressLineStandardization(self, address):
		if not address:
			return ''

		# General input sanitization.

		address = address.upper()

		# Replace bogus characters with spaces.
		address = re.sub(r'[^A-Z0-9 /#.-]', ' ', address)

		# Remove starting and ending spaces.
		address = address.strip()

		# Remove periods from ends.
		address = re.sub(r'\.$', '', address)

		# Add spaces around hash marks to simplify later processing.
		address = address.replace('#', ' # ')

		# Remove duplicate separators and spacing around separators,
		# simplifying the next few steps.
		address = re.sub(r' *([/.-])+ *', '\\1', address)

		# Remove dashes between numberic/non-numerics combinations
		# at ends of lines (for apartment numbers "32-D" -> "32D").
		address = re.sub(r'(?<=[0-9])-(?=[^0-9]+$)', '', address)
		address = re.sub(r'(?<=[^0-9])-(?=[0-9]+$)', '', address)

		# Replace remaining separators with spaces.
		address = re.sub(r'(?<=[^0-9])[/.-](?=[^0-9])', ' ', address)
		address = re.sub(r'(?<=[0-9])[/.-](?=[^0-9])', ' ', address)
		address = re.sub(r'(?<=[^0-9])[/.-](?=[0-9])', ' ', address)

		# Remove duplilcate spaces.
		address = re.sub(r'\s+', ' ', address)

		# Remove hash marks where possible.
		atom = re.match(r'(.+ )([A-Z]+)( #)( .+)', address)
		if atom:
			if atom.group(2) in self.identifiers:
				address = atom.group(1) + atom.group(2) + atom.group(4)

		address = address.strip()

		if not address:
			return ''

		# Convert numeric words to integers.
		parts = address.split(' ')
		for key, val in enumerate(parts):
			if val in self.numbers:
				parts[key] = self.numbers[val]

		address = ' '.join(parts)

		# XXX: Expression Disabled
		#address = re.sub(r' ([0-9]+)(ST|ND|RD|TH)? ?(?>FLOOR|FLR|FL)(?! [0-9])', r' FL \\1', address)
		address = re.sub(r'(NORTH|SOUTH) (EAST|WEST)', '\\1\\2', address)


		# Check for special addresses.

		rural_alternatives = r'RR|RFD ROUTE|RURAL ROUTE|RURAL RTE|RURAL RT|RURAL DELIVERY|RD ROUTE|RD RTE|RD RT'
		atom = re.match(r'^(' + rural_alternatives + r') ?([0-9]+)([A-Z #]+)([0-9A-Z]+)(.*)$', address)
		if atom:
			return "RR " + atom.group(2) + " BOX " + atom.group(4)
		atom = re.match(r'^(BOX|BX)([ #]*)([0-9A-Z]+) (' + rural_alternatives + r') ?([0-9]+)(.*)$', address)
		if atom:
			return "RR " + atom.group(5) + " BOX " + atom.group(3)

		atom = re.match(r'^((((POST|P) ?(OFFICE|O) ?)?(BOX|BX|B) |(POST|P) ?(OFFICE|O) ?)|FIRM CALLER|CALLER|BIN|LOCKBOX|DRAWER)( ?(# )*)([0-9A-Z-]+)(.*)$', address)
		if atom:
			return "PO BOX " + atom.group(11)

		highway_alternatives = r'HIGHWAY|HIGHWY|HIWAY|HIWY|HWAY|HWY|HYGHWAY|HYWAY|HYWY'
		atom = re.match(r'^([0-9A-Z.-]+ ?[0-9/]* ?)(.*)( CNTY| COUNTY) (' + highway_alternatives + r')( NO | # | )?([0-9A-Z]+)(.*)$', address)
		if atom:
			state = atom.group(2)
			if state in self.states:
				state = self.states[state]

			identifier = atom.group(6)
			if identifier in identifier:
				identifier = self.identifiers[identifier]
				number = atom.group(7).replace(' #', '')
				return atom.group(1) + state + " COUNTY HWY " + identifier + number
			return atom.group(1) + state + " COUNTY HIGHWAY " + identifier + self.getEolAbbr(atom.group(7))

		atom = re.match(r'^([0-9A-Z.-]+ ?[0-9/]* ?)(.*)( CR |( CNTY| COUNTY) (ROAD|RD))( NO | # | )?([0-9A-Z]+)(.*)$', address)
		if atom:
			state = atom.group(2)
			if state in self.states:
				state = self.states[state]

			identifier = atom.group(7)
			if identifier in self.identifiers:
				identifier = self.identifiers[identifier]
				number = atom.group(8).replace(' #', '')
				return atom.group(1) + state + " COUNTY RD " + identifier + number
			return atom.group(1) + state + " COUNTY ROAD " + identifier + self.getEolAbbr(atom.group(8))

		atom = re.match(r'^([0-9A-Z.-]+ ?[0-9/]* ?)(.*)( SR|( STATE| ST) (ROAD|RD))( NO | # | )?([0-9A-Z]+)(.*)$', address)
		if atom:
			state = atom.group(2)
			if state in self.states:
				state = self.states[state]

			identifier = atom.group(7)
			if identifier in self.identifiers:
				identifier = self.identifiers[identifier]
				number = atom.group(8).replace(' #', '')
				return atom.group(1) + state + " STATE RD " + identifier + number
			return atom.group(1) + state + " STATE ROAD " + identifier + self.getEolAbbr(atom.group(8))

		atom = re.match(r'^([0-9A-Z.-]+ ?[0-9/]* ?)(.*)( STATE| ST) (ROUTE|RTE|RT)( NO | # | )?([0-9A-Z]+)(.*)$', address)
		if atom:
			state = atom.group(2)
			if state in self.states:
				state = self.states[state]

			identifier = atom.group(6)
			if identifier in self.identifiers:
				identifier = self.identifiers[identifier]
				number = atom.group(7).replace(' #', '')
				return atom.group(1) + state + " STATE RTE " + identifier + number
			return atom.group(1) + state + " STATE ROUTE " + identifier + self.getEolAbbr(atom.group(7))

		atom = re.match(r'^([0-9A-Z.-]+ [0-9/]* ?)(INTERSTATE|INTRST|INT|I) ?(' + highway_alternatives + r'|H)? ?([0-9]+)(.*)$', address)
		if atom:
			number = atom.group(5).replace(' BYP ', ' BYPASS ')
			return atom.group(1) + "INTERSTATE " + atom.group(4) + self.getEolAbbr(number)

		atom = re.match(r'^([0-9A-Z.-]+ ?[0-9/]* ?)(.*)( STATE| ST) (' + highway_alternatives + r')( NO | # | )?([0-9A-Z]+)(.*)$', address)
		if atom:
			state = atom.group(2)
			if state in self.states:
				state = self.states[state]

			identifier = atom.group(6)
			if identifier in self.identifiers:
				identifier = self.identifiers[identifier]
				number = atom.group(7).replace(' #', '')
				return atom.group(1) + state + " STATE HWY " + identifier + number
			return atom.group(1) + state + " STATE HIGHWAY " + identifier + self.getEolAbbr(atom.group(7))

		atom = re.match(r'^([0-9A-Z.-]+ ?[0-9/]* ?)(.*)( US| U S|UNITED STATES) (' + highway_alternatives + r')( NO | # | )?([0-9A-Z]+)(.*)$', address)
		if atom:
			state = atom.group(2)
			if state in self.states:
				state = self.states[state]

			identifier = atom.group(6)
			if identifier in self.identifiers:
				identifier = self.identifiers[identifier]
				number = atom.group(7).replace(' #', '')
				return atom.group(1) + state + " US HWY " + identifier + number
			return atom.group(1) + state + " US HIGHWAY " + identifier + self.getEolAbbr(atom.group(7))

		atom = re.match(r'^([0-9A-Z.-]+ ?[0-9/]* ?)(.*) (' + highway_alternatives + r')( NO | # | )?([0-9A-Z]+)(.*)$', address)
		if atom:
			state = atom.group(2)
			if state in self.states:
				state = self.states[state]

			identifier = atom.group(5)
			if identifier in self.identifiers:
				identifier = self.identifiers[identifier]
				number = atom.group(6).replace(' #', '')
				return atom.group(1) + state + " HWY " + identifier + number
			return atom.group(1) + state + " HIGHWAY " + identifier + self.getEolAbbr(atom.group(6))

		atom = re.match(r'^((' + highway_alternatives + r'|H) ?(CONTRACT|C)|STAR) ?(ROUTE|RTE|RT|R)?( NO | # | )?([0-9]+) ?([A-Z]+)(.*)$', address)
		if atom:
			return "HC " + atom.group(6) + " BOX" + self.getEolAbbr(atom.group(8))

		atom = re.match(r'^([0-9A-Z.-]+ [0-9/]* ?)(RANCH )(ROAD|RD)( NO | # | )?([0-9A-Z]+)(.*)$', address)
		if atom:
			identifier = atom.group(5)
			if identifier in self.identifiers:
				identifier = self.identifiers[identifier]
				number = atom.group(6).replace(' #', '')
				return atom.group(1) + "RANCH RD " + identifier + number
			return atom.group(1) + "RANCH ROAD " + identifier + self.getEolAbbr(atom.group(6))

		address = re.sub(r'^([0-9A-Z.-]+) ([0-9][/][0-9])', '\\1%\\2', address)

		atom = re.match(r'^([0-9A-Z/%.-]+ )(ROAD|RD)([A-Z #]+)([0-9A-Z]+)(.*)$', address)
		if atom:
			prefix = atom.group(1).replace('%', ' ')
			return prefix + "ROAD " + atom.group(4) + self.getEolAbbr(atom.group(5))

		atom = re.match(r'^([0-9A-Z/%.-]+ )(ROUTE|RTE|RT)([A-Z #]+)([0-9A-Z]+)(.*)$', address)
		if atom:
			prefix = atom.group(1).replace('%', ' ')
			return prefix + "ROUTE " + atom.group(4) + self.getEolAbbr(atom.group(5))

		atom = re.match(r'^([0-9A-Z/%.-]+ )(AVENUE|AVENU|AVNUE|AVEN|AVN|AVE|AV) ([A-Z]+)(.*)$', address)
		if atom:
			prefix = atom.group(1).replace('%', ' ')
			return prefix + "AVENUE " + atom.group(3) + self.getEolAbbr(atom.group(4))

		atom = re.match(r'^([0-9A-Z/%.-]+ )(BOULEVARD|BOULV|BOUL|BLVD) ([A-Z]+)(.*)$', address)
		if atom:
			prefix = atom.group(1).replace('%', ' ')
			return prefix + "BOULEVARD " + self.getEolAbbr(atom.group(3) + atom.group(4))


		# Handle normal addresses.

		parts = address.split(' ')
		count = len(parts) - 1
		firstsuff = None
		suff = 0
		id_count = 0
		out = [None] * len(parts)

		for counter in range(count, -1, -1):
			out[counter] = parts[counter]

			if parts[counter] in self.suffixes:
				if not suff:
					# The first suffix (from the right).
					firstsuff = counter

					if counter + 2 < count and (not out[counter+1]) and (not out[counter+2]):
						switch = out[counter+1] + ' ' + out[counter+2]
						if 'EAST W' != switch and \
							'WEST E' != switch and \
							'NORTH S' != switch and \
							'SOUTH N' != switch:
								out[counter] = self.suffixes[parts[counter]]
					else:
						out[counter] = self.suffixes[parts[counter]]
					if counter == count:
						id_count += 1

				else: 
					# A subsequent suffix, display as full word,
					# but could be a name (ie: LA, SAINT or VIA).

					if parts[counter] in self.suffixSimiles \
						and not out[counter+1] in self.suffixes:
						out[counter] = self.suffixSimiles[parts[counter]]
					else:
						out[counter] = self.suffixes[parts[counter]]
						out[counter] = self.suffixes[out[counter] + "-R"]

				suff += 1

			elif parts[counter] in self.identifiers:
				prior = counter - 1
				if prior >= 0 and parts[prior] in self.identifiers and id_count == 0:
					# Don't touch unit numbers
					pass
				else:
					out[counter] = self.identifiers[parts[counter]]
					if suff > 0:
						out[counter] = self.identifiers[out[counter] + "-R"]
					id_count += 1

			elif parts[counter] in self.directionals:
				prior = counter - 1
				nextv = counter + 1
				if prior >= 0 and parts[prior] in self.identifiers and id_count == 0:
					# Don't touch unit numbers
					pass

				elif count >= nextv \
						and nextv == firstsuff:
					out[counter] = self.directionals[parts[counter]]
					if suff <= 1:
						out[counter] = self.directionals[out[counter] + "-R"]

				elif counter > 2 \
					and nextv <= count \
					and parts[nextv] \
					and parts[nextv] in self.directionals:
					# Already set.
					pass

				elif counter == 2 \
						and parts[prior] in self.directionals:
					# Already set.
					pass
				else:
					out[counter] = self.directionals[parts[counter]]
					if count < 2:
						out[counter] = self.directionals[out[counter] + "-R"]

				if counter == count:
					id_count = 1
			elif re.match(r'^[0-9]+$', parts[counter]) \
					  and counter > 0 \
					  and counter < count:
				if suff:
					switch = int(parts[counter][-2:])
					if 11 == parts or \
						12 == parts or \
						13 == parts:
						out[counter] = parts[counter] + 'TH'
					else:
						switch = int(parts[counter][-1:])
						if 1 == switch:
							out[counter] = parts[counter] + 'ST'
						elif 2 == switch:
							out[counter] = parts[counter] + 'ND'
						elif 3 == switch:
							out[counter] = parts[counter] + 'RD'
						else:
							out[counter] = parts[counter] + 'TH'

		out[0] = out[0].replace('%', ' ')

		#ksort($out);
		return ' '.join(out)

	#**
	#* Implement abbreviations for words at the ends of certain address lines
	#*
	#* @param string $string  the address fragments to be analyzed
	#*
	#* @return string  the cleaned up string
	#*
	def getEolAbbr(self, string):
		suff = 0
		id_count = 0

		parts = string.split(' ')
		count = len(parts) - 1
		out = [None] * len(parts)

		for counter in range(count, -1, -1):
			if parts[counter] in self.suffixes:
				if not suff:
					out[counter] = self.suffixes[parts[counter]]
					suff += 1
					if counter == count:
						id_count = 1
				else:
					out[counter] = parts[counter]

			elif parts[counter] in self.identifiers:
				out[counter] = self.identifiers[parts[counter]]
				id_count = 1

			elif parts[counter] in self.directionals:
				out[counter] = self.directionals[parts[counter]]
				if counter == count:
					id_count = 1

			else:
				out[counter] = parts[counter]

		#ksort($out);
		return ' '.join(out)

