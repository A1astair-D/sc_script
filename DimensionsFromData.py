import json
import os

def clean_underscores(string):
    return string.strip('_')

def combine_dimensions_affected(current_func_dimensions, dimensions_result):
    for key, values in current_func_dimensions.items():
        if key not in dimensions_result:
            dimensions_result[key] = []
        for value in values:
            if value not in dimensions_result[key]:
                dimensions_result[key].append(value)
    return dimensions_result

def combine_dimensions_affected_result(dimensions_affected_1, dimensions_affected_2):
    dimensions_result = {}
    dimensions_keys = ['merchant_id', 'payment_gateway', 'payment_instrument_group']
    # empty_keys = []
    for key in dimensions_keys:
        if (key in dimensions_affected_1) and (key in dimensions_affected_2):
            in_first = set(dimensions_affected_1[key])
            in_second = set(dimensions_affected_2[key])

            in_second_but_not_in_first = in_second - in_first
            result = dimensions_affected_1[key] + list(in_second_but_not_in_first)

            dimensions_result[key] = result
    return dimensions_result

def save_to_json(sc_result, output_file):
    with open(output_file, 'w') as file:
        json.dump(sc_result, file, indent=4)

def load_json_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the file.")
        return None
    
def decode_json(value_string):
    try:
        # Decode the JSON string into a Python object
        json_object = json.loads(value_string)
        return json_object
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON.")
        return None
    
def check_in_dimensions(dimensions_results, cleaned_string, dimensions):
    for dimension, values in dimensions.items():
        if cleaned_string in values:
            if dimension not in dimensions_results:
                dimensions_results[dimension] = []
            if cleaned_string not in dimensions_results[dimension]:
                dimensions_results[dimension].append(cleaned_string)
            return True
    return False

def extract_strings(data):
    result = []
    if isinstance(data, dict):
        for _, value in data.items():
            result.extend(extract_strings(value))
    elif isinstance(data, list):
        for item in data:
            result.extend(extract_strings(item))
    elif isinstance(data, str):
        result.append(data)
    
    return result
    
def makeDimensionsArray():
    dimensions = {
        "merchant_id": ['slice','com.swiggy', 'swiggy-nf', 'licious', 'moneyview', 'tatapay', 'goindigo', 'bms', 'manmatters', 'zepto_commodum', 'zepto_drogheria', 'geddit', 'olacabs', 'firstcry', 'spencers', 'freshtohome', 'zupee', 'bluestone', 'instaeats', 'meesho', 'starhealth', 'milkbasket', 'et', 'milton', 'urbanclap', 'urbanclap_provider_prod', 'nivabupaSBU', 'refitglobal', 'zingoy', 'myntraprod', 'TUL_TMP', 'guyal', 'wiom', 'bigbasket', 'icicipru', 'urbanclapsgp', 'lendenclubborrower', 'dreameleven', 'hoichoi', 'urbanclapuae', 'trynooky', 'arjsolutions', 'adityabirla_health', 'agoda', 'vodafone_app', 'jungleerummy', '1mg', 'mplgaming', 'lazypay', 'pharmeasytech', 'abhibus', 'com_shaadi', 'gameskraft', 'paytmmoney', 'apollo_hospitals', 'playship', 'pocketfm', 'rummytime', 'bestprice', 'impay_enigma', 'Adda52Poker', 'confirmtkt', 'unacademy', 'instamojobyopg', 'irctc', 'dunzo', 'nammayatri', 'branch', 'naviloans', 'ixigoprod', 'railyatri', 'olacabs_main', 'mamaearth', 'ctrlzworld', 'bharatx', 'jiosaavn', 'work_india', 'airfiber', 'tataondc', 'myglamm', 'countrydelight', 'rummycom', 'tanishq', 'boltearth', 'rummyprime', 'getsimpl', 'onecard_prod', 'mpokket', 'rummycircle', '5paisa_margin', 'cashify', 'orangehealth', 'winzo', 'howzat', 'artofliving', 'pokerindia', 'sonyliv', 'lifecell', 'playo', 'adanigroup', 'boldcare', 'jar', 'digit', 'adityabirla_sunlife', 'lalpathdigital2', 'firstcry_ae', 'xiaomi', 'gaana', 'sanskritagain', 'creditmantri', 'ihcl', 'shreemithai', 'snapdeal', 'patoys', 'univest', 'airtel', '8454', 'passiongaming', 'nivabupa', 'Curefit', 'swiggy-dineout', 'gingerhotels', 'stxavier', 'zoomin', 'kukufmnew', 'vodafone_web', 'RUMMYPRIME', 'stageott', 'smu', 'eazydiner', 'ccil', 'STJCH', 'trulymadly', 'hungerbox', 'rummyverse', 'farmery', 'zee5', 'CSAS', 'budli', 'snapecabs', 'getplus', 'physics', 'kotakinsurance', 'rebelfoods', 'zinka_commerce', 'arhamedia', 'htott', 'bewakoof', 'amity', 'watcho', 'shemaroo', 'kapiva', 'instaastro', 'myscoot', 'purplle.com', 'testbook', 'acko_pp', 'lenskart', 'themomsco', 'orhprod', 'A23Games', 'nuawellness', 'tatabinge', 'frnd', 'rapido', 'floweraura', 'brevistay', 'cred_store', 'ballebaazi', 'dishtv', 'dreamplug_live', 'donottouch', '33740', 'tataaia', 'ajio_prod', 'pice', 'mewt', 'vegease', 'rushgaming', 'magicbricks', 'redbus_in', 'sporfy', 'swiggy-go', 'hopscotch', 'starbucks', 'milaap', 'croma', 'bbinstant', 'reliancebeauty', 'zoop', 'sugar', 'zoomcar', 'winni', 'tamasha', 'floweraura_gifts', 'TheSouledStore', 'unipin', '33024', '33862', 'savana', 'religare', 'bestseller_only', 'kissht', 'healthifyme_pp', 'myteam11', 'citymall', 'cloudkitch', 'lendenclub', '1565', 'PRSUR', 'sirona', 'tatasky', 'porter', 'tatafiber', 'vodafone_ct', '33736', 'microsoft', 'allen', 'pvrcinemas', 'sahaj', 'firstcry-ksa', 'vijaysales', 'platos', 'vrlbus', 'cleartrip', 'dishd2h', 'playerzpot', 'hudle', '33735', 'amexgbt', 'voiceclub', 'practo', 'chicnutrix', 'hypd', 'fancode', 'eloelo', 'navibbps', 'bestseller_veromoda', '35553', 'mybyk', 'swiggy-liquor', 'fitpass', 'werize', 'dunzob2b', 'u-next', '33731', 'slice', 'quikr', 'burgerking', 'myparkplus', 'smallcase', 'stockgro', 'mxplayer', 'sangam', 'apnibus', 'ausfbank', 'swiggy-wallet', '33734', 'jungleeludo', 'buystars', 'neo_web', 'flipkarthealth', 'marrowmed', '36027', 'navi', 'gyftr', 'nuvama', '33733', 'vedantu', 'oyorooms', '35194', 'apollo247', '33737', 'spicejet', '35209', 'velocity', 'wakefit', 'cred_checkout', 'acko_tech', 'astroyogi', 'ausfbcc', 'pokerbaazi', 'truefan', 'Rentomojo_prod', 'livemint', 'ring', 'realme', 'cred_rentpay', 'lalpathdigital', 'qmin', 'naviamc', 'travelota', 'tatapower', 'cleartax', 'littlejoys', 'reingames', 'newme', 'insurancedekho', 'betteropinions', 'hungama', 'clumsy_bumsy', 'zivame', 'karmakraft', 'travclan', 'dealshare', 'zachofficial', 'be10x', 'bharatpe', '34952', 'sixdreams', 'jockey', 'getmeganew', 'xavier', 'gamezy', 'porterdriver', '33732', 'HRPL', '34492', 'swishclub', 'circlechess', 'navidigigold', 'yatrisathi', 'appsforbharat', 'ClassicRummy', 'paydeck', 'm2mferry', 'TimesPrime', 'industrybuying', 'DHP630315', 'd2cstorebeta', 'upstox', 'postpe', '32575', 'topgames', 'goinfire', 'uaeflowers', '34500', 'starquik', 'nuego', 'tripjack', 'AGNNM', 'sidsfarm', 'supersixvusport', 'cellbell', '36034', 'capresevip', 'oneplus', 'jt_wallet', '35464', 'redbusmy', 'biryanibykilo', 'KMFL', 'tendercuts', 'tickertape', 'nutristar', 'udaan', 'creditsaison', '35769', 'zingbus', 'orixindia', 'vi_enterprise', 'condenast', 'atlys', 'pinkthreads', 'bodywise', 'inc42', 'bestseller_selectedhomme', 'tatasky_new', 'decodeage', '33741', 'skillovilla', 'ninjacart', 'NBOE', 'vistarooms', 'rummybaazi', 'bestseller_jacknjones', 'smokeshow', 'jhumri', 'tecsox', 'mirraw', '34126', 'shoppersstop', 'turftown', 'pokerstars', 'upsurge', 'pocket52', 'onsurity', '35054', 'sober', 'aboveminimum', 'mylo', 'abfrl', 'news9', '34436', 'sachargaming', 'k9vitalityy', 'tfgame', '35919', 'fantasykhiladi', 'indianhobby', '34286', 'sostronk', 'shipyaari', 'zestmoney_prod', 'gullak', 'damensch', 'toothsi', 'cloverventures', 'zaaroz', 'candere', 'medikabazaar', 'upcase', 'gabit', 'toolsvilla', 'joshtalks', 'cybbcd', 'thirdwave', 'theoriginalknit', 'SonyLiv', '35162', 'GULLAK', 'sensesindia', 'fly91', 'ABSPL', 'daarulkitab', 'redbussg', 'incred', 'clawsnpaws', 'petsy', 'shopse', 'laundrymate', '30247', 'esthreall', 'spartanpoker', 'herbolabIndia', 'kancchalannka', 'tyke', 'livehindustan', 'ting', 'fortum', 'connectandheal', 'mintree', 'cipzer', 'fastandup', 'suspire', 'puretivebotanics', 'iffcogarden', 'nammayatriBAP', 'happylife', 'spicebasket', 'beyondsnack', 'letstrack', 'vitalylabs', 'supersixsports', 'cybstimezone', 'dchica', 'lohono', 'ttkservices', 'lenskartae', 'shoffr', 'egencia', '7097', 'shopfootball', 'fleek', 'maxprotein', 'nxtwave', 'faballey', 'godigitlife', '35934', '34646', '32nd', 'pluckk', 'gograbbit', 'indeekos', 'beato', 'minus30', 'lovableindia', 'getbinks', 'playfrenzy', 'typsybeauty', 'counselindia', 'nutrabay', '34503', 'nammafoundation', 'local_remote_instamojo', 'CCSU', 'betterhalf', 'rankerbuddy', 'BDIN', 'jiosaavn_int', 'hindustantimes', 'souqannisa', 'houseofx', 'splootmobile', 'peore', 'falconclothing', 'capizal', 'netmeds', 'gochillaoo', 'amirandsons', 'ocacademy', 'koinonia', 'oneiric', 'tigermarron', 'TenderCuts', 'statiq', 'ssbeauty', 'kaarr', 'icicilombard', '33319', 'mysoresaree', 'vedaaz', 'MRGOV', 'clickastro', 'senrysa', 'svasthyaa', 'royalmart', 'a2glifestyle', 'cuemath', 'salarybox', 'SXCS_TEST', '9915', 'thecocolove', 'hustleculture', 'phab', '32541', 'krvvy', '35657', 'highnessmotors', '35746', 'esckey', 'techaircraft', 'spicta', 'vudu', 'lenskartsg', 'eatiko', 'urbanic', 'udit_juspay', 'furniselan', 'loccitane', 'pahadidukan', 'jewelbox', 'suggaa', 'lmes', 'anfarm', 'sukuto', 'supersmart', 'uniglobe', 'utsav', 'kiayaaccessories', '34958', 'chillbuddha', 'travelyaari', 'd2cstore', 'cozycorners', 'avenue', 'jetsynthesys', 'shopyvision', '30373', 'outerwoods', 'cars24', 'athlos', 'pokercircle', 'turtlewings', 'd2cshop', 'admireme', 'jewellerykhazana', '34261', 'acko_drive', 'eazypeace', 'flicka', 'tatamed', 'CommonFloor', 'silisoul', 'jariera', 'zodiac', 'tmc_prod', 'acciojobs', 'Bethel', '32576', '34042', 'arugil', 'flyo', 'ejaa', 'thedripcorugs', 'freshmenu', '34684', 'ProdTestHdfc2', 'deoxdeer', 'wework', '32917', 'damenschppg', '35155', 'designcafe', 'chorki', 'ElectroniksIn', 'thestruttstore', 'flaws', '33320', 'paypal-juspay', 'hsntek', 'yatrisathizoo', 'ausfbankca', 'tetro', 'junglee11', 'lingerie', 'furtados', 'uncuffed', 'livelinen', '35223', 'dancingleaf', 'mccoymart', '35922', 'dimplery', 'townscript', '30988', 'zoomcartest', 'a23cdc', 'purifit', 'instasport', 'zillion', 'bikanervala', 'jp_yesbank', '32570', 'cinepolis', 'CRWA', 'lenskartth', 'eldahealth', 'traya', 'travelxp', 'totalroutine', 'talkcharge', 'masalabox', 'coralhaze', 'murshmallow', 'theoutfitco', 'mepiform', '35442', '32929', '35921', 'lenskartus', 'ayushclub', 'workdayNutrition', 'guitarbro', '35540', 'accentmirror', 'indiqube', '35867', 'BDPR', 'daintishop', 'bonviesnacks', 'dmimpex', 'koshayoga', 'ackolife', '33532', '35112', 'homegrounds', 'friendlydiamonds', 'woodenfactory', 'aroka', 'tripsygames', 'wingslifestyle', 'travelsees', 'quackquacknew', 'realitees', 'bokunotrends', 'threadcurry', 'goodbutter', 'atpi', 'doggybakery', 'greenhermitage', 'styloswag', 'jaipurmasala', 'tatamotorsev', 'wsfl', 'whysoblue', 'unleash_wellness', 'GYJY', 'newtonschool', 'loyka', 'tradegold', 'atomhealth', 'pawgypets', 'DrLalPathLabs', 'oddnoteven', 'spicexpress', 'tealfeed', 'chikupiku', 'komparify', '32577', 'bapida', '1finance', '25877', 'thenaturnest', 'bombaytrooper', 'animedevta', '1lessidiot', 'walawali', 'bioayurveda', 'mitsu', 'hersay', 'classicsuperapp', '35493', 'DAVNC', 'sorta', 'lemonberry', '35696', '33317', 'swiggy-daily', 'Aangan', 'adeeavee', 'floofyou', '28916', '35453', 'zimero', 'foursen', 'luxurytech', '34725', '35417', '36032', 'evor', 'vokitoki', 'baalajewels', 'bblunt', 'Ihcl', 'nirasceramics', 'Microtek', '32572', 'timesprime', 'CSCU', 'neeraj_juspay_prod', 'Toffle', 'tatamotors', 'froggmag', 'galaxyhealth', 'tfpl', 'tiqr', 'dineout_b2c', 'albumnest', '3777', '35866', '36300', '19319', 'thetrost', '34712', 'pochampallysaree', '32573', '34975', 'sleepaxa', 'gethorizon', 'cosfrag', 'atmanirbhar', 'bxiworld', 'alphazacked', 'grest', 'tuckd', 'braclo', 'pahadiamrut', '35841', '35860', 'unfilter', '34519', 'orgaskin', 'rti_tata', 'elfy', '34837', 'papaya', '6618', 'fastemi', 'sploot', 'thebubblesbathco', 'nude', 'anagram', '10054', 'pncpopcorn', '35757', '25183', 'byzwiz', 'ajio_business', 'mepl', 'shreyahomedecor', 'elfenwatches', '35231', '35452', 'homedale', 'flipkartHealth', 'dementiks', 'hypeelixir', 'intellipaat', 'safeokid', 'aasaan', 'naturetherapy', 'medurahealthcare', 'uomo', '35206', 'fitasf', '34615', 'cratlyonline', 'KHGY', 'savehaul', 'nurstore', 'gadgetwagon', 'swiftiethrifts', '34770', '35671', 'absolutemat', 'packmygo', '35061', 'ipec', 'angajasilver', 'kalakshwatches', '21605', 'bigcash', '35100', '36275', 'orae', 'happayexpense', 'loyola', 'finesilverjewels', 'erotissch', 'bikano', 'GANP', 'uability', 'bhanzupp', 'qalafa', 'gosporty1', '10313', 'ordnance', 'furrycastle', 'ballar', 'beckyspickles', 'honesthome', 'trychikankari', '36096', 'ckiict', 'picasso', 'freshbuspvtltd', '35689', '35070', 'hollyhoq', '32678', 'bronoun', '34835', 'justickets', '36098', '34963', 'indiahikes', 'tazohome', '34409', 'bagstud', 'owndays', 'DHP349895', 'ultrapop', 'navinmart', 'lenskartsa', 'juspay_manikanta', 'littlejungle', 'handicraft', 'flutelifestyle', 'emori', '35469', 'obleka', 'asquareretailllp', 'fomo', '34967', 'danidanials', 'buyz', 'sinderella', 'silvaa', 'branded10', 'stillweave', 'cibt', 'sunscape', 'santalli', 'STXA', '34803', '35095', 'nofinish', '33450', 'cybsuratdiamond', 'zooplive', 'youthrobe', 'kroozz', 'ngvclub', 'CSSJ', 'RAWO', 'themakeupbar', 'naughtydough', 'aksharfees', 'HouseofVandy', 'thamehadesigns', 'ticketgenienew', 'hnathleisure', 'nataura', 'planetdsg', '34949', 'memoriesinsite', 'humblebeancoffee', 'tiethebun', 'revurge', 'maaspickles', 'scentira', 'juspaymerchKunal', 'rupifi', '35008', 'Moarmouz', 'bijakb2c', 'genzlifestyle', 'soup', '35761', 'villagecompany', '32571', 'Beautiful', 'TimesInternet', '35057', 'backspaced', '34781', '34976', '36235', '36247', 'kashejewels', 'vikifurniture', '32161', 'firewand', 'hululu', 'DHP998477', 'tenhills', 'outprfm', 'drjain', '35481', 'bionaturals', 'risemetrix', '34287', 'indianfish', '35654', '35641', 'SHRT', 'togazin', 'g3uae', 'studio', '35017', 'kutumb', 'maxsafe', 'aaritya', '34616', '90CAL', 'gvkinger', 'irutom', 'highape', '34440', '34753', 'Cityscope', '36010', 'speedo', 'littleclothings', 'brewcha', '35028', '35658', 'revaa', '35936', 'kenkohealth', 'thakur93', '35496', '35874', 'SRIAS', 'bawseofficial', '35242', 'houseofdawn', '9195', 'truehome', '33318', 'aaragallore', 'APCCG', '35245', 'moonair', '34736', '36357', '36465', 'kriyafit', 'houseofbio', '35055', '17774', 'letsmultiply', '28655', 'zoozle', 'paulstreet', '22048', '36082', 'oriveorganics', 'happay', 'authentize', '35137', 'praja', '34951', 'mylestech', 'codesilver', 'mylestechsecurity', 'kasturidiamond', 'codeapto', 'cybscitadiness', 'amazg', '36005', '34251', '35859', 'magecurious', 'OPNED', '34049', 'thyrocare', 'NDCommerce', 'theacwala', 'pockt', '35869', '35252', '34817', '36006', '35247', '35246', 'nexgeniots', '35251', '35249', '35253', 'testCanada', '35248', '28425', '35250', '35777', '35029', 'ebanxProd', 'testmerchant1', 'TMSL', 'monochrome', '35211', 'avamiapparels', 'aathiyam', 'spiceplatter', 'masalasoda', 'karibykriti', 'flyaf', 'scentialsworld', '35027', 'WELEIND', 'deccanmudra', '35555', '34957', 'dhan', '36022', 'shraddha_test_2', '36408', '35755', '35014', '33992', '33406', '35931', '35935', 'swiffylabs', 'aashralya', '36237', 'entri', '34852', 'tuzo', '35205', '36052', 'HKG628828', 'santabling', '33971', '35489', '34482', '35800', '36079', 'triadkube', '36000', '36093', '33685', '35414', '34582', 'akalinfo', 'coastlineclub', 'godachionline', '35988', '35302', 'houseofzelena', '33863', '35534', '32574', 'aruj', '34259', 'rayyn', 'babiesofwonder', 'riitek', 'serpentcs', '35830', 'credhive', '34740', '34716', '34606', 'juspaymigration', '34743', '35435', '36319', 'DHAN', '34638', '36178', '35740', '36301', 'fairpick', 'bornreborn', '36309', 'quest2travel', 'organixmantra', '34944', '35509', '35868', '32579', '28173', '35399', 'itsfoy', 'pankhudiyan', '35879', '35495', 'stylearoma', '34968', 'happified', 'shopify', 'augustcharms', 'okcredit_prod', 'bhashabharat', '35807', '34447', 'futurefinds', '35538', 'SXAV', 'WHPS', 'caarabi', '35801', 'enguru', 'varalife', '36260', '36138', '36028', '36590', 'crossbeats', '12club', '35448', '36575', 'grofoo', 'perfumeplus', '36201', 'gorr', 'mydr', '36458', 'droogernow', '35847', '35033', '33556', 'brightn', 'decort', 'cleekify', '35506', '35849', '35424', '1stwellness', 'datalogicsindia', 'thejoe', 'KOLAR', 'dolphinskart', '35504', 'offers_prod', 'thetemplehouse', 'earnmall', '34348', '34938', '35210', '35195', 'Firstcry_main', '36396', '35692', '35697', '35560', 'ausfinsurance', 'giftingheaven', '34340', '33581', 'gulabizilla', 'msprod', '35288', 'pinktree', 'smk', '34940', '35767', '35290', '35812', 'eassylife', '34979', '35291', '34279', '34861', 'timescard', 'LLIT', '32567', 'lyfe', 'malaki', '35870', 'worldofsol', '35940', '35650', 'nitara', '35160', '34604', 'agati', '36068', 'SMTO', '35478', '35644', '36183', 'demostudio', 'tryfunky', 'herbsgem', 'sysbolt', '35230', '35537', '35319', '35541', '35411', '36009', 'krossgames', '35295', 'marvans', '35561', 'belinoz', '35645', '34726', 'natboard', '35840', '35499', 'radiantroshni', 'consultkiya', 'sippincider', '35829', 'celebrationhut', '35079', 'real4u', 'nutkash', '35643', '35016', 'wrapgame', 'flash', 'floral', 'buyblynk', 'goatfit', '35916', 'gxr', 'sswift', '35117', '36671', 'skindeli', '35676', 'newtestankit', 'nitrkl', '35244', 'thugil', '36419', '35752', '34948', 'evenhealthcare', 'carpetDiem', 'seatadda', '9534', 'SMBF', 'PRAS', 'excelr', 'varini', 'hotelsanjaigrandinn', '35060', 'netshopping', 'remuse', 'diningcouture', '36033', '36278', '35316', 'ACCU', 'cybsbeenas', '36203', '36042', 'infinix', '35836', 'ayushclubcom', '34463', 'aavaranaa', '34909', '35025', '36284', 'girnarornaments', '35065', 'vasstramclothing', 'jooli', 'nexus', '35691', '35145', '36433', 'slayzone', 'GWMDA', '35930', '35136', 'magiclamps', '34069', '35240', '35438', '35674', 'houseoftaya', '34895', 'tata_rooftop', '34685', '32924', '35739', '35216', '35217', '35218', '35220', '36529', 'kokoro', 'dayer', 'kanooda', '36670', 'gossipstore', '36217', 'megamart', '36185', 'sprig', 'pfcclub', '35454', '23633', 'bloomsflora', 'allapkteenpatti', 'RASC', 'the_nature_story', 'PMYK', 'theindiantrunk', '35764', '35766', '35768', '35765', 'sastitrip', 'juspay_pa', 'icicibank', '35213', 'shriji', 'newmidtesting', '35946', 'freaker', '34502', 'fcmtravels', 'corba', 'hydropreneurs', 'pragyatt', '35539', 'teststudio', '34689', '36290', '35798', '35722', 'amaanatonline', 'firsthub', '35864', 'metagani', '35741', 'DJGC', 'bank-test', '35968', '36397', 'tatagcstore', 'wedberry', '35059', 'noorlawns', '36202', 'nirvasahc', 'itilite', 'littlebansi', 'freightos', 'khanacademy', '36399', '36013', '36617', 'unicef', 'diybytok', '32156', 'cybsgemsparadise', '36515', '35462', '35294', '35999', 'tippytop', 'gemstonegala', 'hpcl', '36576', 'awwhunnie', '35015', '34741', '36021', '36023', '35827', 'thefuture', 'justickets_userwallet_testing', 'sarkkart', '36432', '34345', 'printedman', 'offersTest', 'AHEN_TEST', 'monicakhosla', 'zoella', '35550', '36712', '34465', 'digirasa', '34901', 'redgorillas', 'ticketgenieapp', '36125', 'offcuts', 'APCPG', 'topmate', '34441', '35023', '34966', 'commonfloor', 'nanthelabel', '35721', 'vaadan', '35972', '34609', '36320', '35142', '34653', '35804', 'pcitest', '35212', 'DAVJ', '36563', 'seasonearth', '34299', '34761', '36629', '35884', '36143', 'thetrendy', '34729', 'longroadbrands', 'parmeluxe', '34766', '36196', '36610', '36213', '35754', '30106', '35845', '35109'],
        "payment_gateway": ['ADYEN', 'AIRPAY', 'AIRTELMONEY', 'AMAZONPAY', 'AMEX', 'ATOM', 'AXIS_BIZ', 'AXIS_UPI', 'BAJAJFINSERV', 'BHARATX', 'BILLDESK', 'BOKU', 'CAMSPAY', 'CAPITALFLOAT', 'CAREEMPAY', 'CASH', 'CCAVENUE_V2', 'CHECKOUT', 'CRED', 'CYBERSOURCE', 'DIGIO', 'DUMMY', 'EASEBUZZ', 'EBS_V3', 'EPAYLATER', 'FAWRYPAY', 'FREECHARGE', 'GOCASHFREE', 'GOOGLEPAY', 'HDFC', 'HDFC_CC_EMI', 'HDFC_UPI', 'HSBC', 'HSBC_UPI', 'HYPERPAY', 'HYPERPG', 'HYPER_PG', 'IATAPAY', 'ICICI_UPI', 'INDUS_PAYU', 'IPG', 'ITZCASH', 'JIOMONEY', 'LAZYPAY', 'LOANTAP', 'LOTUSPAY', 'LSP', 'MERCHANT_CONTAINER', 'MIGS', 'MOBIKWIK', 'MOBIKWIKZIP', 'MORPHEUS', 'MPGS', 'NAVITAIRE', 'NOON', 'OLAPOSTPAID', 'PAYFORT', 'PAYGLOCAL', 'PAYPAL', 'PAYTM', 'PAYTM_V2', 'PAYU', 'PAYZAPP', 'PHONEPE', 'PINELABS', 'QWIKCILVER', 'RAZORPAY', 'RBL_BIZ', 'SBI', 'SHOPSE', 'SIKA_SIMPL', 'SIMPL', 'SNAPMINT', 'SODEXO', 'STRIPE', 'TAP', 'TATAPAY', 'TATAPAYLATER', 'TATA_PA', 'TPSL', 'TWID', 'TWID_V2', 'TWOC_TWOP', 'WORLDPAY', 'YESBANK_UPI', 'YES_BIZ', 'ZAAKPAY'],
        "payment_instrument_group": ['AADHAAR', 'CARD', 'CASH', 'CONSUMER_FINANCE', 'CREDIT CARD', 'DEBIT CARD', 'MERCHANT_CONTAINER', 'NET BANKING', 'REWARD', 'RTP', 'UPI', 'VIRTUAL_ACCOUNT', 'WALLET'],
        'extra': ['NB'],
    }
    return dimensions

def dimensionsAffectedObject(stringJsonValue, dimensions):
    jsonValue = decode_json(stringJsonValue)
    string_list_new_value = extract_strings(jsonValue)
    # print(string_list_new_value)
    dimensions_results = {}
    for val in string_list_new_value:
        check_in_dimensions(dimensions_results, val, dimensions)
    return dimensions_results

def find_and_add_dimension_from_word(dimensions_results, remaining_string, dimensions):
    cleaned_string = clean_underscores(remaining_string)
    broken_string = cleaned_string.split('_')
    dimensions_in_string = {}
    #check for each substring
    for j in range(len(broken_string), 0, -1):
        for i in range(0, j):
            temp_string = '_'.join(broken_string[i:j])
            check_in_dimensions(dimensions_in_string, temp_string, dimensions)
    #add everything to result
    for dim_key, dim_value in dimensions_in_string.items():
        dimensions_results[dim_key] = dim_value

def handle_no_match_case(original_str, dimensions):
    dimensions_results = {}
    words = original_str.split('_')
    #check first 3 words
    for i in range(1, min(4, len(words) + 1)):
        remaining_string = '_'.join(words[:i])
        find_and_add_dimension_from_word(dimensions_results, remaining_string, dimensions)
    #check last 3 words
    for i in range(1, min(4, len(words) + 1)):
        remaining_string = '_'.join(words[-i:])
        find_and_add_dimension_from_word(dimensions_results, remaining_string, dimensions)
    #add to result
    return dimensions_results

def replace_extra_dimensions(result):
    extraDict = {
        "NB": {"payment_instrument_group": ['NET BANKING']},
    }
    if 'extra' in result:
        extra_values = result.pop('extra', [])
        for extra_value in extra_values:
            if extra_value in extraDict:
                for dim_key, dim_values in extraDict[extra_value].items():
                    if dim_key not in result:
                        result[dim_key] = []
                    for dim_val in dim_values:
                        if dim_val not in result[dim_key]:
                            result[dim_key].append(dim_val)
    return result

def main():
    # Specify the path to your JSON file
    file_path = 'BSJson5.json'
    dimensions = makeDimensionsArray()

    # Load the JSON object from the file
    json_data = load_json_from_file(file_path)

    resultList = []
    rows = []

    if "rows" in json_data:
        rows = json_data["rows"]
    for row_item in rows:
        configName = row_item["configName"]
        newValue = row_item["newValue"]
        dimAffectedNew = dimensionsAffectedObject(newValue, dimensions)
        dimAffectedNew = replace_extra_dimensions(dimAffectedNew)

        currentValue = row_item["currentValue"]
        dimAffectedCurrent = dimensionsAffectedObject(currentValue, dimensions)
        dimAffectedCurrent = replace_extra_dimensions(dimAffectedCurrent)    

        dimAffectedCombined = combine_dimensions_affected(dimAffectedNew, dimAffectedCurrent)

        if dimAffectedCombined == {}:
            dimAffectedCombined = handle_no_match_case(configName, dimensions)
            dimAffectedCombined = replace_extra_dimensions(dimAffectedCombined)

        result_item = {
            "configName"          : configName,
            "dimensions_affected" : dimAffectedCombined,
        }
        resultList.append(result_item)

    
    finalDimensionAffected = resultList[0]["dimensions_affected"]

    for result in resultList[1:]:
        dimAffectedCombined = result["dimensions_affected"]
        finalDimensionAffected = combine_dimensions_affected_result(finalDimensionAffected, dimAffectedCombined)

    finalDimensionAffectedObject = {
        "configName"          : "Comined_Dimensions_Affected",
        "dimensions_affected" : finalDimensionAffected,
    }

    resultList.append(finalDimensionAffectedObject)

    output_dir = "results_directory2"
    os.makedirs(output_dir, exist_ok=True)

    output_file = "dimensions_affected.json"

    output_file_path = os.path.join(output_dir, output_file)
    save_to_json(resultList, output_file_path)
    print(f"SC_Results have been saved to {output_file_path}")
    

if __name__ == "__main__":
    main()
