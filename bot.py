import requests
import threading
import time
import re
import json
import os
import random
import phonenumbers
from phonenumbers import geocoder
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import asyncio
import ssl
import html
from urllib.parse import urlencode
try:
    import websockets
except ImportError:
    websockets = None

API_URL = "http://147.135.212.197/crapi/had/viewstats"
TOKEN = "SlJSQjRSQldcko9XYX9Yh4p4eX5kl2tlRGKHYWhgWEhGgph7Undu"

API_URLS_NEW = [
    "https://api-junaid-production.up.railway.app/api/ps?type=sms",
    "https://api-junaid-production.up.railway.app/api/np?type=sms",
]

API_URL_MAIN = "https://api-junaid-production.up.railway.app/api/ps?type=sms"
POLL_INTERVAL = 10

BOT_TOKEN = "8995918624:AAGzj1VfH42YshRbJLRhpFmDZNkJxMF-m7I"

# Currency conversion: 1 USD = 180 Rs (approximate)
RS_PER_USD = 160.0
OTP_REWARD_MILESTONE = 200
OTP_REWARD_RS = 50
MAX_OTP_PER_NUMBER = 5
ADMIN_IDS = [5385377266, 8700952672, 6154383311]  # 3 Admin slots, replace placeholders with real IDs

CHANNEL_LINK = "https://t.me/KRYON_JI"
CHAT_LINK = "https://t.me/TH3GALAXY"
PANEL_LINK = "https://t.me/otppanelsellingbot?start=8995918624"

FORCE_CHANNELS = [
    {"link": "https://t.me/KRYON_JI", "name": "𝗠𝗮𝗶𝗻 𝗖𝗵𝗮𝗻𝗻𝗲𝗹"},
    {"link": "https://t.me/TH3GALAXY", "name": "𝗠𝗿 𝗖𝗵𝗮𝗻𝗻𝗲𝗹"},
    {"link": "https://t.me/SASSY_SQUAD", "name": "𝗯𝗼𝘁𝘀 𝗖𝗵𝗮𝗻𝗻𝗲𝗹"},
    {"link": "https://t.me/ABOUTKUSH", "name": "𝗠𝗲𝘁𝗵𝗼𝗱𝘀 𝗖𝗵𝗮𝗻𝗻𝗲𝗹"},
]
FORCE_GROUP = {"link": "https://t.me/KRYON_JI", "name": "𝗦𝘂𝗽𝗽𝗼𝗿𝘁 𝗚𝗿𝗼𝘂𝗽"}

def _extract_username(link):
    return "@" + link.replace("https://t.me/", "").replace("http://t.me/", "").split("/")[0]

DB_FILE = "bot_data.json"
_db_lock = threading.Lock()

CE = {
    "fire": "5337267511261960341",
    "time": "5336983442125001376",
    "globe": "5224450179368767019",
    "phone": "6204108584381322968",
    "key": "5197288647275071607",
    "msg": "5337302974806922068",
    "channel": "6206080502651164081",
    "number": "5352862640592949843",
    "ok": "5352694861990501856",
    "no": "5420130255174145507",
    "warn": "5336944168944047463",
    "money": "6206155797722830770",
    "link": "5420517437885943844",
    "pin": "5352922460897452503",
    "graph": "5352877703043258544",
    "rocket": "5188481279963715781",
    "star": "5352552689983067014",
    "phone2": "6204108584381322968",
    "electriccl": "5989800724312101453",
    "hi": "5353027129250453493",
    "world": "5224450179368767019",
    "search": "5463352748751753567",
    "broadcast": "6269303009658802514",
    "ntick": "6206479140040743133",
    "call": "6204108584381322968",
    "verified": "5841528141037705335",
    "crown": "6206319341487527808",
    "boss": "6267019543051244106",
    "check": "6298670698948724690",
    "otpkey": "5420626637429432217",
    "plus": "6206375377925839184",
    "redtick": "6206094834957031192",
    "moneybag": "6190336264940559752",
    "downarrow": "6204177183598974956",
    "admin": "5353022963132174959",
    "user": "5353027129250453493",
    "settings": "5352922460897452503",
    "back": "5255703720078879038",
    "coin": "5251632168391688253",
    "mobile": "5111709173339390480",
    "vip": "6267128480601741166",
    "lock": "5353022963132174959",
    "clipboard": "5352862640592949843",
    "stats": "6206343625232619150",
    "hacker": "6235572922086331108",
    "ban": "6206396878532121864",
    "first": "6206419981161211268",
    "second": "6206222099132978580",
    "third": "6206311275538946838",
    "free": "6203750195130274981",
    "pin2": "6206190608432764318",
    "pencil": "6204162490515855272",
    "chain": "6206497372176913599",
    "top": "6206090539989734881",
    "trash": "6206108815075579644",
    "downarrow2": "6206368810920841771",
    "getnum": "6237864166879663987",
    "best": "6206080502651164081",
    "live": "6206141323683042874",
    "clock": "5382194935057372936",
    "rightarrow": "6147815573314082674",
    "megaphone": "6269303009658802514",
    "gift": "6242498410822244114",
    "join": "5224450179368767019",
    "copy": "5352862640592949843",
    "first": "6206419981161211268",
    "second": "6206222099132978580",
    "third": "6206311275538946838",
    "free": "6203750195130274981",
    "pin": "6206190608432764318",
    "electric": "6204104220694550861",
    "pencil": "6204162490515855272",
    "top": "6206090539989734881",
    "trash": "6206108815075579644",
    "king2": "6206096153511990389",
    "best": "6206080502651164081",
    "downarrow2": "6206368810920841771",
    "newking": "6237864166879663987",
    "live": "6206141323683042874",
    "clock": "5382194935057372936",
}

SERVICE_LOGOS = {
    "WhatsApp": "5226815671261763813",
    "WhatsApp Business": "5267457160077415807",
    "Binance": "5251632168391688253",
    "Telegram": "5330237710655306682",
    "Instagram": "5330375003579890327",
    "Google": "5456150110071178646",
    "Facebook": "5332341566025515614",
    "IMO": "5226479577185949100",
    "YouTube": "5330134940677849089",
    "Apple": "5451965905686775304",
    "TikTok": "5327982530702359565",
    "SMS": "5337302974806922068",
    "TK cash": "5337302974806922068",
    "PayPal": "5364111181415996352",
    "AUTHMSG": "5337302974806922068",
    "LNST": "5352877703043258544",
    "Qsms": "5327959866159938948",
    "SLACK": "5352877703043258544",
    "SinchVerify": "5420626637429432217",
    "Sumsub": "5352922460897452503",
    "WELTRADE": "6206155797722830770",
    "X App": "5352552689983067014",
    "Yango": "5224450179368767019",
    "Appointfix": "5352877703043258544",
    "PremierBet": "5251632168391688253",
    "13854817184": "6204108584381322968",
    "279600003002517": "6204108584381322968",
    "Red Note": "5334707727933390944",
    "Unknown": "6172631000997171252",
    "Microsoft": "5370857634440170316",
    "Meta": "5321447183910716259",
    "Viber": "5332449498553663205",
}

COUNTRY_FLAGS = {
    "AF": {"id": "5222096009009575868", "name": "Afghanistan"},
    "AL": {"id": "5224312057515486246", "name": "Albania"},
    "DZ": {"id": "5294048127240655242", "name": "Algeria"},
    "AD": {"id": "5221987861733061751", "name": "Andorra"},
    "AG": {"id": "5224544866217765554", "name": "Antigua and Barbuda"},
    "AR": {"id": "5221980461504411710", "name": "Argentina"},
    "AM": {"id": "5224369957969603463", "name": "Armenia"},
    "AU": {"id": "5224659803837574114", "name": "Australia"},
    "AT": {"id": "5224520754271366661", "name": "Austria"},
    "AZ": {"id": "5224426544163728284", "name": "Azerbaijan"},
    "BS": {"id": "5224504167107668172", "name": "Bahamas"},
    "BH": {"id": "5224492892818518587", "name": "Bahrain"},
    "BD": {"id": "5224407289825340729", "name": "Bangladesh"},
    "BB": {"id": "5222156533688712094", "name": "Barbados"},
    "BY": {"id": "5280820319458707404", "name": "Belarus"},
    "BE": {"id": "5224513182244024630", "name": "Belgium"},
    "BM": {"id": "5222482143749353810", "name": "Bermuda"},
    "BA": {"id": "5224496092569155254", "name": "Bosnia and Herzegovina"},
    "BW": {"id": "5224288456670196085", "name": "Botswana"},
    "BR": {"id": "5224688610183228070", "name": "Brazil"},
    "BN": {"id": "5224435958732042406", "name": "Brunei"},
    "BO": {"id": "5294201479047957700", "name": "Bolivia"},
    "BG": {"id": "5222092074819530668", "name": "Bulgaria"},
    "CA": {"id": "5222001124592071204", "name": "Canada"},
    "CL": {"id": "5222000927023577045", "name": "Chile"},
    "CH": {"id": "5913299849167507310", "name": "Chad"},
    "CN": {"id": "5224435456220868088", "name": "China"},
    "DE": {"id": "5222165617544542414", "name": "Germany"},
    "EE": {"id": "5222195463272281351", "name": "Estonia"},
    "EG": {"id": "5293992082212409502", "name": "Egypt"},
    "SV": {"id": "5224337131534559907", "name": "El Salvador"},
    "GQ": {"id": "5222172811614762423", "name": "Equatorial Guinea"},
    "ES": {"id": "5222024776976970940", "name": "Spain"},
    "ET": {"id": "5224467805914542024", "name": "Ethiopia"},
    "FJ": {"id": "5221962676044838178", "name": "Fiji"},
    "FI": {"id": "5224282903277482188", "name": "Finland"},
    "FR": {"id": "5222029789203804982", "name": "France"},
    "GA": {"id": "5224669733801963467", "name": "Gabon"},
    "GM": {"id": "5221949872747330159", "name": "Gambia"},
    "GE": {"id": "5222152195771742239", "name": "Georgia"},
    "GH": {"id": "5224511339703056124", "name": "Ghana"},
    "GR": {"id": "5222463490706389920", "name": "Greece"},
    "GD": {"id": "5222234560359577687", "name": "Grenada"},
    "GT": {"id": "5222128302868672826", "name": "Guatemala"},
    "GN": {"id": "5222337588035073000", "name": "Guinea"},
    "GW": {"id": "5224705704153066489", "name": "Guinea-Bissau"},
    "GY": {"id": "5224570532942329532", "name": "Guyana"},
    "HT": {"id": "5224683146984831315", "name": "Haiti"},
    "HN": {"id": "5222229234600130045", "name": "Honduras"},
    "HU": {"id": "5224691998912427164", "name": "Hungary"},
    "IS": {"id": "5222063229819172521", "name": "Iceland"},
    "IN": {"id": "5222300011366200403", "name": "India"},
    "ID": {"id": "5224405893960969756", "name": "Indonesia"},
    "IR": {"id": "5224374154152653367", "name": "Iran"},
    "IQ": {"id": "5221980268230882832", "name": "Iraq"},
    "CI": {"id": "5293991322003200135", "name": "Ivory Coast"},
    "IE": {"id": "5224257017509588818", "name": "Ireland"},
    "IL": {"id": "5224720599099648709", "name": "Israel"},
    "JM": {"id": "5222007034467074185", "name": "Jamaica"},
    "JP": {"id": "5222390089715299207", "name": "Japan"},
    "JO": {"id": "5222292177345853436", "name": "Jordan"},
    "KZ": {"id": "5222276376161171525", "name": "Kazakhstan"},
    "KE": {"id": "5222089648163009103", "name": "Kenya"},
    "KI": {"id": "5224652244695134610", "name": "Kiribati"},
    "KW": {"id": "5221949726718442491", "name": "Kuwait"},
    "KG": {"id": "5224388147156102493", "name": "Kyrgyzstan"},
    "LA": {"id": "5224200843632324642", "name": "Laos"},
    "LV": {"id": "5224401229626484931", "name": "Latvia"},
    "LB": {"id": "5294193108156699621", "name": "Lebanon"},
    "LS": {"id": "5224245850594619415", "name": "Lesotho"},
    "LR": {"id": "5221998371518034740", "name": "Liberia"},
    "LY": {"id": "5291858711826946840", "name": "Libya"},
    "LT": {"id": "5224245902134226386", "name": "Lithuania"},
    "LU": {"id": "5224499567197700690", "name": "Luxembourg"},
    "MG": {"id": "5222042605386217334", "name": "Madagascar"},
    "MY": {"id": "5291858351049696702", "name": "Malaysia"},
    "MV": {"id": "5224393700548814960", "name": "Maldives"},
    "ML": {"id": "5224322352552096671", "name": "Mali"},
    "MT": {"id": "5224731388057497620", "name": "Malta"},
    "MH": {"id": "5224538449536624503", "name": "Marshall Islands"},
    "MU": {"id": "5224238347286752315", "name": "Mauritius"},
    "MX": {"id": "5221971386238514431", "name": "Mexico"},
    "FM": {"id": "5222280486444873367", "name": "Micronesia"},
    "MD": {"id": "5224216473018314447", "name": "Moldova"},
    "MC": {"id": "5221937224068640464", "name": "Monaco"},
    "MN": {"id": "5224192257992701543", "name": "Mongolia"},
    "ME": {"id": "5224463399278096980", "name": "Montenegro"},
    "MZ": {"id": "5294086708931874940", "name": "Mozambique"},
    "NA": {"id": "5224690826386351746", "name": "Namibia"},
    "NP": {"id": "5222444378101925267", "name": "Nepal"},
    "NL": {"id": "5224516489368841614", "name": "Netherlands"},
    "NZ": {"id": "5224573595254009705", "name": "New Zealand"},
    "NE": {"id": "5222099049846420864", "name": "Niger"},
    "NG": {"id": "5294456308047563965", "name": "Nigeria"},
    "NO": {"id": "5291761718580502030", "name": "Norway"},
    "OM": {"id": "5222396686785066306", "name": "Oman"},
    "PK": {"id": "5291825606219029010", "name": "Pakistan"},
    "PA": {"id": "5222111719999945107", "name": "Panama"},
    "PE": {"id": "5224482026551258766", "name": "Peru"},
    "PG": {"id": "5224500164198149905", "name": "Papua New Guinea"},
    "PY": {"id": "5222152565138929235", "name": "Paraguay"},
    "PH": {"id": "5222152565138929235", "name": "Philippines"},
    "PL": {"id": "5224670399521892983", "name": "Poland"},
    "PT": {"id": "5224482026551258766", "name": "Portugal"},
    "QA": {"id": "5911260864983339619", "name": "Qatar"},
    "RO": {"id": "5224220115150582423", "name": "Romania"},
    "RU": {"id": "5294335323113807278", "name": "Russia"},
    "RW": {"id": "5222225596762830469", "name": "Rwanda"},
    "VC": {"id": "5224541228380467535", "name": "Saint Vincent and the Grenadines"},
    "WS": {"id": "5224660353593387686", "name": "Samoa"},
    "ST": {"id": "5221953304426198315", "name": "Sao Tome and Principe"},
    "SA": {"id": "5294163983983463099", "name": "Saudi Arabia"},
    "SN": {"id": "5224358988623130949", "name": "Senegal"},
    "RS": {"id": "5222145396838512729", "name": "Serbia"},
    "SC": {"id": "5224467496676896871", "name": "Seychelles"},
    "SL": {"id": "5224420995065983217", "name": "Sierra Leone"},
    "SG": {"id": "5224194023224257181", "name": "Singapore"},
    "SK": {"id": "5222401879400528047", "name": "Slovakia"},
    "SI": {"id": "5224660718665607511", "name": "Slovenia"},
    "SB": {"id": "5222290588207954120", "name": "Solomon Islands"},
    "SO": {"id": "5222370504664428325", "name": "Somalia"},
    "ZA": {"id": "5224696216570309138", "name": "South Africa"},
    "KR": {"id": "5222345550904439270", "name": "South Korea"},
    "SS": {"id": "5224618146949773268", "name": "South Sudan"},
    "LK": {"id": "5224277294050192388", "name": "Sri Lanka"},
    "SD": {"id": "5224372990216514135", "name": "Sudan"},
    "SR": {"id": "5224567367551428669", "name": "Suriname"},
    "SE": {"id": "5222201098269373561", "name": "Sweden"},
    "CH": {"id": "5224707263226194753", "name": "Switzerland"},
    "TJ": {"id": "5222217865821696536", "name": "Tajikistan"},
    "TZ": {"id": "5224397364155923150", "name": "Tanzania"},
    "TH": {"id": "5224638530864556281", "name": "Thailand"},
    "TG": {"id": "5222408051268532030", "name": "Togo"},
    "TT": {"id": "5224391883777651050", "name": "Trinidad and Tobago"},
    "TN": {"id": "5221991375016310330", "name": "Tunisia"},
    "TR": {"id": "5224601903383457698", "name": "Turkey"},
    "TM": {"id": "5224256935905208951", "name": "Turkmenistan"},
    "UG": {"id": "5222464040462200940", "name": "Uganda"},
    "UA": {"id": "5222250679371839695", "name": "Ukraine"},
    "AE": {"id": "5224565851427976312", "name": "UAE"},
    "GB": {"id": "5224518800061245598", "name": "United Kingdom"},
    "US": {"id": "5224321781321442532", "name": "United States"},
    "UY": {"id": "5222466849370813232", "name": "Uruguay"},
    "UZ": {"id": "5222404546575219535", "name": "Uzbekistan"},
    "VU": {"id": "5222126748090512778", "name": "Vanuatu"},
    "VE": {"id": "5294476442854247878", "name": "Venezuela"},
    "VA": {"id": "5222420266155520507", "name": "Vatican City"},
    "VN": {"id": "5222359651282071925", "name": "Vietnam"},
    "YE": {"id": "5294058972033076492", "name": "Yemen"},
    "ZM": {"id": "5294100109229838880", "name": "Zambia"},
    "ZW": {"id": "5294422158762592930", "name": "Zimbabwe"},
    "XK": {"id": "5222197129719592160", "name": "Kosovo"},
    "PS": {"id": "5222370620628546719", "name": "Palestine"},
    "BF": {"id": "5294153164960848949", "name": "Burkina Faso"},
    "BI": {"id": "5294051631933967760", "name": "Burundi"},
    "MM": {"id": "5294254478944393569", "name": "Myanmar"},
    "KH": {"id": "5294225191562400452", "name": "Cambodia"},
    "MA": {"id": "5911482111633658301", "name": "Morocco"},
    "TD": {"id": "5913299849167507310", "name": "Chad"},
}
COUNTRY_NAME_TO_CODE = {
    "afghanistan": "AF", "albania": "AL", "algeria": "DZ", "andorra": "AD",
    "antigua and barbuda": "AG", "argentina": "AR", "armenia": "AM", "australia": "AU",
    "austria": "AT", "azerbaijan": "AZ", "bahamas": "BS", "bahrain": "BH",
    "bangladesh": "BD", "barbados": "BB", "belarus": "BY", "belgium": "BE",
    "bermuda": "BM", "bosnia and herzegovina": "BA", "botswana": "BW", "brazil": "BR",
    "brunei": "BN", "bulgaria": "BG", "canada": "CA", "Chad": "CH", "chile": "CL", "china": "CN",
    "germany": "DE", "estonia": "EE", "egypt": "EG", "el salvador": "SV",
    "equatorial guinea": "GQ", "spain": "ES", "ethiopia": "ET", "fiji": "FJ",
    "finland": "FI", "france": "FR", "gabon": "GA", "gambia": "GM", "georgia": "GE",
    "ghana": "GH", "greece": "GR", "grenada": "GD", "guatemala": "GT", "guinea": "GN",
    "guinea-bissau": "GW", "guyana": "GY", "haiti": "HT", "honduras": "HN",
    "hungary": "HU", "iceland": "IS", "india": "IN", "indonesia": "ID", "iran": "IR",
    "ivory coast": "CI",
    "iraq": "IQ", "ireland": "IE", "israel": "IL", "jamaica": "JM", "japan": "JP",
    "jordan": "JO", "kazakhstan": "KZ", "kenya": "KE", "kiribati": "KI", "kuwait": "KW",
    "kyrgyzstan": "KG", "laos": "LA", "latvia": "LV", "lebanon": "LB", "lesotho": "LS",
    "liberia": "LR", "libya": "LY", "lithuania": "LT", "luxembourg": "LU",
    "madagascar": "MG", "malaysia": "MY", "maldives": "MV", "mali": "ML", "malta": "MT",
    "marshall islands": "MH", "mauritius": "MU", "mexico": "MX", "micronesia": "FM",
    "moldova": "MD", "monaco": "MC", "mongolia": "MN", "montenegro": "ME",
    "mozambique": "MZ", "namibia": "NA", "nepal": "NP", "netherlands": "NL",
    "new zealand": "NZ", "niger": "NE", "nigeria": "NG", "norway": "NO", "oman": "OM",
    "pakistan": "PK", "panama": "PA", "papua new guinea": "PG", "paraguay": "PY",
    "peru": "PE",
    "philippines": "PH", "poland": "PL", "portugal": "PT", "qatar": "QA", "romania": "RO",
    "russia": "RU", "rwanda": "RW", "saint vincent and the grenadines": "VC",
    "samoa": "WS", "sao tome and principe": "ST", "saudi arabia": "SA", "senegal": "SN",
    "serbia": "RS", "seychelles": "SC", "sierra leone": "SL", "singapore": "SG",
    "slovakia": "SK", "slovenia": "SI", "solomon islands": "SB", "somalia": "SO",
    "south africa": "ZA", "south korea": "KR", "south sudan": "SS", "sri lanka": "LK",
    "sudan": "SD", "suriname": "SR", "sweden": "SE", "switzerland": "CH",
    "tajikistan": "TJ", "tanzania": "TZ", "thailand": "TH", "togo": "TG",
    "trinidad and tobago": "TT", "tunisia": "TN", "turkey": "TR", "turkmenistan": "TM",
    "uganda": "UG", "ukraine": "UA", "uae": "AE", "united kingdom": "GB",
    "united states": "US", "uruguay": "UY", "uzbekistan": "UZ", "vanuatu": "VU",
    "venezuela": "VE", "vatican city": "VA", "vietnam": "VN", "yemen": "YE",
    "zambia": "ZM", "zimbabwe": "ZW", "kosovo": "XK", "palestine": "PS",
    "burkina faso": "BF", "burundi": "BI", "myanmar": "MM",
    "bolivia": "BO",
    "cambodia": "KH",
    "morocco": "MA",
    "chad": "TD",
}

# ===== MSI LOGIN PANEL CONFIG =====
MSI_PANEL = {
    'name': 'MSI SMS',
    'url': 'http://145.239.130.45',
    'username': 'wajahatshah',
    'password': 'wajahatshah',
    'use_sesskey': True
}

panel_sessions = {}

# ===== GROUP FORWARD DEDUP =====
_seen_otps_lock = threading.Lock()
_seen_otps = set()

# ===== USER OTP DEDUP (cross-source) =====
_user_otp_lock = threading.Lock()
_user_otp_sent = set()

def _notify_assigned_user(matched_num, matched_data, msg, source=""):
    """Send OTP notification to the assigned user with cross-source dedup."""
    uid_user = matched_data["user_id"]
    svc_name = matched_data["service"]
    country_code = matched_data["country"]
    otp = extract_otp(msg)

    dedup_key = f"{uid_user}_{matched_num}_{otp}"
    with _user_otp_lock:
        if dedup_key in _user_otp_sent:
            return False
        _user_otp_sent.add(dedup_key)
        if len(_user_otp_sent) > 5000:
            _user_otp_sent.clear()

    price_usd = db.get("service_countries", {}).get(svc_name, {}).get(country_code, {}).get("price", 0)
    price_rs = price_usd * RS_PER_USD

    if str(uid_user) in db.get("users", {}):
        db["users"][str(uid_user)]["balance"] = db["users"][str(uid_user)].get("balance", 0) + price_usd
        db["users"][str(uid_user)]["total_earned"] = db["users"][str(uid_user)].get("total_earned", 0) + price_usd
        db["users"][str(uid_user)]["otp_count"] = db["users"][str(uid_user)].get("otp_count", 0) + 1

    # ===== OTP REWARDS MILESTONE CHECK =====
    total_otp_done = db["users"][str(uid_user)].get("otp_count", 0)
    rewards_claimed = db["users"][str(uid_user)].get("otp_rewards_claimed", 0)
    current_milestones = total_otp_done // OTP_REWARD_MILESTONE
    if current_milestones > rewards_claimed:
        new_rewards = current_milestones - rewards_claimed
        reward_usd = (OTP_REWARD_RS * new_rewards) / RS_PER_USD
        db["users"][str(uid_user)]["balance"] = db["users"][str(uid_user)].get("balance", 0) + reward_usd
        db["users"][str(uid_user)]["total_earned"] = db["users"][str(uid_user)].get("total_earned", 0) + reward_usd
        db["users"][str(uid_user)]["otp_rewards_claimed"] = current_milestones
        save_db(db)
        reward_notify = (
            f"{ce('gift','🎁')} <b>OTP Milestone Reward Unlocked!</b>\n\n"
            f"{ce('otpkey','🔐')} <b>{total_otp_done}</b> OTPs Completed!\n"
            f"{ce('moneybag','💰')} <b>+{OTP_REWARD_RS * new_rewards} Rs</b> added to your balance!\n\n"
            f"{ce('rocket','⚡')} Keep going for the next reward!"
        )
        send_message(int(uid_user), reward_notify)
    # ===== END OTP REWARDS =====

    db["stats"]["total_otps"] = db["stats"].get("total_otps", 0) + 1
    add_otp_history(uid_user, matched_num, svc_name, otp, country_code)
    db.setdefault("otp_counts", {}).setdefault(svc_name, {})[country_code] = db["otp_counts"].get(svc_name, {}).get(country_code, 0) + 1

    assignments = db.get("number_assignments", {})
    current_count = matched_data.get("otp_count", 0) + 1
    matched_data["otp_count"] = current_count

    total_otp_done = db["users"][str(uid_user)].get("otp_count", 0)
    total_earned_usd = db["users"][str(uid_user)].get("total_earned", 0)
    total_earned_rs = total_earned_usd * RS_PER_USD

    if current_count >= MAX_OTP_PER_NUMBER:
        assignments.pop(matched_num, None)
    else:
        assignments[matched_num] = matched_data

    save_db(db)

    # Referral unlock check
    referred_by = db["users"].get(str(uid_user), {}).get("referred_by")
    if referred_by and referred_by in db.get("users", {}):
        ref_track = db.get("referral_tracking", {}).get(referred_by, {}).get(str(uid_user))
        if ref_track and not ref_track.get("reward_unlocked", False):
            ref_track["otp_count"] = ref_track.get("otp_count", 0) + 1
            if ref_track["otp_count"] >= 10:
                ref_track["reward_unlocked"] = True
                db["users"][referred_by]["balance"] = db["users"][referred_by].get("balance", 0) + 0.073
                db["users"][referred_by]["total_earned"] = db["users"][referred_by].get("total_earned", 0) + 0.073
                save_db(db)
                unlock_text = (
                    f"{ce('first','🏆')} <b>Invite Reward Unlocked!</b>\n\n"
                    f"Your referral became active after receiving <b>10 OTPs</b>.\n"
                    f"{ce('gift','🎁')} <b>Invite Reward:</b> <code>$0.070</code>\n"
                    f"{ce('star','⭐')} <b>Active Bonus:</b> <code>$0.0003</code>\n"
                    f"{ce('moneybag','💰')} <b>Total Earned:</b> <code>$0.073</code>"
                )
                send_message(int(referred_by), unlock_text)

    country = db.get("countries", {}).get(country_code, {}).get("name", country_code)
    flag = flag_emoji(country_code, "🏳️")
    masked = mask_number(matched_num)
    svc_logo = svc_emoji(svc_name, "📱")

    user_text = (
        f"{svc_logo} <b>{svc_name}</b>\n"
        f"{flag} <b>{country}</b>\n"
        f"{ce('phone','📞')} <code>{masked}</code>\n"
        f"{ce('otpkey','🔐')} <b>OTP Count:</b> <code>{current_count}/{MAX_OTP_PER_NUMBER}</code>\n"
        f"{ce('moneybag','💰')} <b>+{fmt_num(price_rs)} Rs</b> / <b>+{fmt_num(price_usd)} $</b>\n"
        f"{ce('money','💵')} <b>{fmt_num(total_earned_rs)} Rs</b> / <b>{fmt_num(total_earned_usd)} $</b>"
    )

    check_restock_alert(svc_name, country_code)

    otp_markup = build_inline([
        [btn(f"{otp}", copy_text=otp, style="success", emoji_tag="otpkey")]
    ])

    send_message(int(uid_user), user_text, otp_markup)

    # OTP reward summary message
    total_nums = sum(len(v) for v in db.get("numbers", {}).get(svc_name, {}).values())
    avail_display = total_nums * 4
    reward_text = (
        f"{ce('gift','🎁')} <b>{html.escape(svc_name)} Reward!</b>\n\n"
        f"{flag} <b>{html.escape(country)}</b> {ce('msg','💭')} <b>{html.escape(svc_name)}</b>\n"
        f"» {ce('gift','🎁')} <b>Reward:</b> <code>${fmt_num(price_usd)}</code> / <code>{fmt_num(price_rs)} Rs</code>\n"
        f"» {ce('broadcast','👥')} <b>Available Numbers:</b> <code>{avail_display}</code>\n\n"
        f"You earned this amount for the received OTP ({html.escape(country)} price).\n"
        f"{ce('channel','📢')} <b>Total OTPs:</b> <code>{total_otp_done}</code>"
    )
    send_message(int(uid_user), reward_text)

    print(f"[{source}] Forwarded OTP to user {uid_user} for {mask_number(matched_num)} (count {current_count}/{MAX_OTP_PER_NUMBER})")
    return True


# ===== DATABASE =====
def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            try:
                os.rename(DB_FILE, DB_FILE + ".corrupt")
            except:
                os.remove(DB_FILE)
    return {
        "users": {},
        "services": {},
        "countries": {},
        "numbers": {},
        "withdrawals": [],
        "stats": {"total_otps": 0, "total_users": 0},
        "user_states": {},
        "admin_states": {},
        "banned_users": [],
        "number_assignments": {},
        "otp_history": {},
        "restock_alerted": {},
        "otp_counts": {},
        "change_cooldown": {},
        "panel_otps": {},
        "processed_panel_otps": [],
        "panel_last_fetch": "",
        "service_countries": {},
        "forward_groups": [{"name": "Main Group", "group_id": -1003769079833}],
        "withdrawals_enabled": True,
    }

def save_db(data):
    with _db_lock:
        tmp_file = DB_FILE + ".tmp"
        with open(tmp_file, "w") as f:
            json.dump(data, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_file, DB_FILE)

db = load_db()

def is_banned(uid):
    return str(uid) in [str(x) for x in db.get("banned_users", [])]

def ban_user(uid):
    uid = str(uid)
    if uid not in [str(x) for x in db.get("banned_users", [])]:
        db.setdefault("banned_users", []).append(uid)
        save_db(db)

def unban_user(uid):
    uid = str(uid)
    banned = db.get("banned_users", [])
    db["banned_users"] = [x for x in banned if str(x) != uid]
    save_db(db)

def add_otp_history(uid, number, service, otp, country):
    db.setdefault("otp_history", {}).setdefault(str(uid), []).append({
        "number": number, "service": service, "otp": otp, "country": country,
        "time": datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
    })
    if len(db["otp_history"][str(uid)]) > 50:
        db["otp_history"][str(uid)] = db["otp_history"][str(uid)][-50:]
    save_db(db)


def check_restock_alert(svc_name, ccode):
    count = len(db.get("numbers", {}).get(svc_name, {}).get(ccode, []))
    key = f"{svc_name}_{ccode}"
    alerted = db.get("restock_alerted", {})
    if count < 10 and not alerted.get(key):
        country = db.get("countries", {}).get(ccode, {}).get("name", ccode)
        flag = flag_emoji(ccode, "🏳️")
        for admin in ADMIN_IDS:
            send_message(admin, f"{ce('warn','🚨')} <b>Restock Alert!</b>\n\n{svc_emoji(svc_name, '📱')} <b>{svc_name}</b>\n{flag} <b>{country}</b>\n{ce('phone','📞')} Only <code>{count}</code> numbers left!")
        db.setdefault("restock_alerted", {})[key] = True
        save_db(db)
    elif count >= 10 and db.get("restock_alerted", {}).get(key):
        db["restock_alerted"].pop(key, None)
        save_db(db)

# ===== EMOJI HELPERS =====
def ce(tag, fallback):
    eid = CE.get(tag, "")
    if not eid:
        return fallback
    return f'<tg-emoji emoji-id="{eid}">{fallback}</tg-emoji>'

def svc_emoji(service, fallback):
    eid = SERVICE_LOGOS.get(service, "")
    if not eid:
        # Case-insensitive fallback
        for k, v in SERVICE_LOGOS.items():
            if k.lower() == str(service).lower():
                eid = v
                break
    if not eid:
        eid = SERVICE_LOGOS.get("Unknown", "")
    if not eid:
        return fallback
    return f'<tg-emoji emoji-id="{eid}">{fallback}</tg-emoji>'

def flag_emoji(region, fallback):
    # Handle custom country keys (e.g. "Togo 2") by looking up real_code
    real_region = region
    for svc, countries in db.get("service_countries", {}).items():
        if region in countries:
            rc = countries[region].get("real_code", "")
            if rc and rc in COUNTRY_FLAGS:
                real_region = rc
                break
    data = COUNTRY_FLAGS.get(real_region)
    if not data or not data.get("id"):
        return fallback
    return f'<tg-emoji emoji-id="{data["id"]}">{fallback}</tg-emoji>'

# ===== NUMBER HELPERS =====
def get_country_info(number):
    try:
        clean = re.sub(r"[^0-9+]", "", str(number))
        if not clean.startswith("+"):
            clean = "+" + clean
        parsed = phonenumbers.parse(clean)
        region = phonenumbers.region_code_for_number(parsed)
        country = geocoder.description_for_number(parsed, "en")
        if not country:
            country = region
        if not country:
            country = "Unknown"
        unicode_flag = "".join(chr(127397 + ord(c)) for c in region) if region else "🏳️"
        animated_flag = flag_emoji(region, unicode_flag)
        return country, animated_flag, region
    except:
        return "Unknown", "🏳️", ""

def mask_number(number, last_digits=5, mark="***"):
    if not number:
        return None
    if "*" in number:
        return number
    try:
        if not number.startswith("+"):
            number = "+" + number
        parsed = phonenumbers.parse(number)
        country_code = str(parsed.country_code)
        national_number = str(parsed.national_number)
        if len(national_number) > last_digits:
            masked = mark + national_number[-last_digits:]
        else:
            masked = national_number
        return f"+{country_code}{masked}"
    except Exception:
        if len(number) > last_digits + 3:
            return number[0:3] + mark + number[-last_digits:]
        else:
            return number

def normalize_number(num):
    if not num:
        return ""
    num = str(num).strip()
    has_plus = num.startswith("+")
    digits = re.sub(r"[^0-9]", "", num)
    return ("+" + digits) if has_plus else digits

def extract_numbers_from_text(text):
    if not text:
        return []
    clean = re.sub(r"<[^>]+>", "", text)
    raw_matches = re.findall(r'[+]?[0-9*][0-9\s\-*]{5,}[0-9*]', clean)
    results = []
    for raw in raw_matches:
        raw = raw.strip()
        digits_only = re.sub(r"[^0-9]", "", raw)
        if len(digits_only) >= 7:
            results.append(raw)
    return results

def match_assigned_number(raw_num, assignments):
    norm_raw = normalize_number(raw_num)
    if not norm_raw:
        return None, None
    for num, data in list(assignments.items()):
        if normalize_number(num) == norm_raw:
            return num, data
    for num, data in list(assignments.items()):
        norm_assigned = normalize_number(num)
        if "***" in raw_num:
            parts = raw_num.split("***")
            if len(parts) == 2:
                suffix = re.sub(r"[^0-9]", "", parts[1])
                if suffix and norm_assigned.endswith(suffix):
                    return num, data
        if len(norm_raw) >= 5 and len(norm_assigned) >= 5:
            if norm_assigned.endswith(norm_raw[-5:]) or norm_raw.endswith(norm_assigned[-5:]):
                return num, data
    return None, None

def is_member(chat_id, user_id):
    try:
        r = api("getChatMember", {"chat_id": chat_id, "user_id": int(user_id)})
        if r.get("ok"):
            status = r["result"].get("status", "left")
            return status in ("member", "administrator", "creator")
    except:
        pass
    return False

def check_force_join(uid):
    missing = []
    for ch in FORCE_CHANNELS:
        username = _extract_username(ch["link"])
        if not is_member(username, uid):
            missing.append({"type": "channel", **ch})
    group_user = _extract_username(FORCE_GROUP["link"])
    if not is_member(group_user, uid):
        missing.append({"type": "group", **FORCE_GROUP})
    return missing

def force_join_markup(missing):
    rows = []
    for item in missing:
        if item["type"] == "channel":
            rows.append([btn(f"Join {item['name']}", url=item["link"], style="primary", emoji_tag="channel")])
        else:
            rows.append([btn(f"Join {item['name']}", url=item["link"], style="success", emoji_tag="broadcast")])
    rows.append([btn("I Have Joined", "check_join", style="danger", emoji_tag="check")])
    return build_inline(rows)

def detect_service(message, cli_hint=""):
    # First check CLI hint from panel if available
    if cli_hint:
        cli_lower = str(cli_hint).lower().strip()
        for svc_name in SERVICE_LOGOS.keys():
            if svc_name.lower() == cli_lower:
                return svc_name
        cli_map = {
            "whatsapp business": "WhatsApp Business",
            "whatsapp": "WhatsApp",
            "telegram": "Telegram",
            "google": "Google",
            "facebook": "Facebook",
            "fb": "Facebook",
            "instagram": "Instagram",
            "imo": "IMO",
            "youtube": "YouTube",
            "paypal": "PayPal",
            "pay pal": "PayPal",
            "apple": "Apple",
            "ios": "Apple",
            "binance": "Binance",
            "tiktok": "TikTok",
            "qsms": "Qsms",
            "slack": "SLACK",
            "sinchverify": "SinchVerify",
            "sumsub": "Sumsub",
            "weltrade": "WELTRADE",
            "x app": "X App",
            "yango": "Yango",
            "appointfix": "Appointfix",
            "premierbet": "PremierBet",
            "red note": "Red Note",
        }
        for key, val in cli_map.items():
            if key in cli_lower:
                return val
    # Fallback to message content detection (avoid short substrings in encrypted data)
    msg = message.lower()
    if "whatsapp business" in msg:
        return "WhatsApp Business"
    elif "whatsapp" in msg:
        return "WhatsApp"
    elif "telegram" in msg:
        return "Telegram"
    elif "google" in msg:
        return "Google"
    elif "facebook" in msg:
        return "Facebook"
    elif "instagram" in msg:
        return "Instagram"
    elif "imo" in msg:
        return "IMO"
    elif "youtube" in msg:
        return "YouTube"
    elif "pay pal" in msg or "paypal" in msg:
        return "PayPal"
    elif "apple" in msg or "ios" in msg or "iphone" in msg:
        return "Apple"
    elif "binance" in msg:
        return "Binance"
    elif "tiktok" in msg or "tik tok" in msg:
        return "TikTok"
    elif "qsms" in msg:
        return "Qsms"
    elif "microsoft" in msg:
        return "Microsoft"
    elif "meta" in msg:
        return "Meta"
    elif "viber" in msg:
        return "Viber"
    else:
        return "SMS"

def extract_otp(message):
    msg = message or ""

    # Pattern 1: "code/otp/pin/verification code is [=:] 123456"
    m = re.search(r"(?:code|otp|pin|verification code|security code|auth code|passcode|one.time password|confirmation code|access code|login code)\s*[:=]?\s*[:=]\s*([\d\- ]{3,15})", msg, re.IGNORECASE)
    if m:
        return re.sub(r"[^\d]", "", m.group(1))

    # Pattern 2: "code/otp/pin/verification code: 123456"
    m = re.search(r"(?:code|otp|pin|verification code|security code|auth code|passcode|one.time password|confirmation code|access code|login code)\s*[:=]\s*([\d\- ]{3,15})", msg, re.IGNORECASE)
    if m:
        return re.sub(r"[^\d]", "", m.group(1))

    # Pattern 3: "Your code/otp/pin is 123456"
    m = re.search(r"(?:your|the)\s+(?:code|otp|pin|verification code|security code|auth code|passcode|one.time password|confirmation code|access code|login code)\s+is\s+[:=]?\s*([\d\- ]{3,15})", msg, re.IGNORECASE)
    if m:
        return re.sub(r"[^\d]", "", m.group(1))

    # Pattern 4: "123456 is your code/otp/pin"
    m = re.search(r"([\d\- ]{3,15})\s+is\s+(?:your|the)\s+(?:code|otp|pin|verification code|security code|auth code|passcode|one.time password|confirmation code|access code|login code)", msg, re.IGNORECASE)
    if m:
        return re.sub(r"[^\d]", "", m.group(1))

    # Pattern 5: "Use 123456 to verify" / "Enter 123456" / "Reply with 123456"
    m = re.search(r"(?:use|enter|reply with|type|input)\s+[:=]?\s*([\d\- ]{3,15})\s+(?:to|for|as)\s+(?:verify|verification|login|auth|confirm)", msg, re.IGNORECASE)
    if m:
        return re.sub(r"[^\d]", "", m.group(1))

    # Pattern 6: "Enter code 123456" / "Use OTP 123456"
    m = re.search(r"(?:enter|use|type|input)\s+(?:the\s+)?(?:code|otp|pin|verification code|security code|auth code|passcode|one.time password|confirmation code|access code|login code)\s+[:=]?\s*([\d\- ]{3,15})", msg, re.IGNORECASE)
    if m:
        return re.sub(r"[^\d]", "", m.group(1))

    # Pattern 7: "OTP for login is 123456" / "Code for verification: 123456"
    m = re.search(r"(?:code|otp|pin|verification code|security code|auth code|passcode|one.time password|confirmation code|access code|login code)\s+for\s+\w+\s+[:=]?\s*([\d\- ]{3,15})", msg, re.IGNORECASE)
    if m:
        return re.sub(r"[^\d]", "", m.group(1))

    # Pattern 8: "Your 6-digit code: 123456" / "Your 4-digit PIN: 1234"
    m = re.search(r"(?:your|the)\s+\d{1,2}[\- ]?digit\s+(?:code|otp|pin|verification code|security code|auth code|passcode|one.time password|confirmation code|access code|login code)\s*[:=]?\s*([\d\- ]{3,15})", msg, re.IGNORECASE)
    if m:
        return re.sub(r"[^\d]", "", m.group(1))

    # Pattern 9: "123456 - your verification code" / "123456: your code"
    m = re.search(r"([\d\- ]{3,15})\s*[-:]\s*(?:your|the)\s+(?:code|otp|pin|verification code|security code|auth code|passcode|one.time password|confirmation code|access code|login code)", msg, re.IGNORECASE)
    if m:
        return re.sub(r"[^\d]", "", m.group(1))

    # Pattern 10: "Code 123456 expires" / "OTP 123456 valid"
    m = re.search(r"(?:code|otp|pin|verification code|security code|auth code|passcode|one.time password|confirmation code|access code|login code)\s+[:=]?\s*([\d\- ]{3,15})\s+(?:expires|valid|will|is)", msg, re.IGNORECASE)
    if m:
        return re.sub(r"[^\d]", "", m.group(1))

    # Pattern 11: 3-3 format like 123-456 or 123 456
    m = re.search(r"\b(\d{3}[- ]\d{3})\b", msg)
    if m:
        return re.sub(r"[^\d]", "", m.group(1))

    # Pattern 12: 3-4 format like 123-4567 or 123 4567
    m = re.search(r"\b(\d{3}[- ]\d{4})\b", msg)
    if m:
        return re.sub(r"[^\d]", "", m.group(1))

    # Pattern 13: Strict 6-digit boundary
    m = re.search(r"\b(\d{6})\b", msg)
    if m:
        return m.group(1)

    # Pattern 14: Any 4-8 digit number (fallback)
    m = re.search(r"(?<!\d)(\d{4,8})(?!\d)", msg)
    if m:
        return m.group(1)

    # Pattern 15: Numbers in bold/markdown **123456** or `123456`
    m = re.search(r"(?:\*\*|`|\*\*\*|__)([\d\- ]{3,15})(?:\*\*|`|\*\*\*|__)", msg)
    if m:
        return re.sub(r"[^\d]", "", m.group(1))

    # Pattern 16: "Verify with 123456" / "Authenticate using 123456"
    m = re.search(r"(?:verify|authenticate|confirm|login|signin)\s+(?:with|using|by|via)\s+[:=]?\s*([\d\- ]{3,15})", msg, re.IGNORECASE)
    if m:
        return re.sub(r"[^\d]", "", m.group(1))

    # Pattern 17: "Token: 123456" / "Key: 123456"
    m = re.search(r"(?:token|key|secret|password|passwd|pwd)\s*[:=]?\s*([\d\- ]{3,15})", msg, re.IGNORECASE)
    if m:
        return re.sub(r"[^\d]", "", m.group(1))

    # Pattern 18: "123456" alone on a line
    m = re.search(r"(?:^|\n)\s*([\d\- ]{3,15})\s*(?:$|\n)", msg)
    if m:
        return re.sub(r"[^\d]", "", m.group(1))

    return "N/A"

# ===== API FETCHERS (from Script 1) =====

def fetch_api_main():
    try:
        resp = requests.get(API_URL_MAIN, timeout=15)
        data = resp.json()
        print(f"[DEBUG] Main API status: {resp.status_code}, type: {type(data)}")
        results = []
        items = []
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            for key in ["data", "otps", "results", "messages", "aaData"]:
                if key in data and isinstance(data[key], list):
                    items = data[key]
                    print(f"[DEBUG] Extracted {len(items)} from '{key}'")
                    break
        for item in items:
            try:
                if isinstance(item, list) and len(item) >= 4:
                    service = detect_service(item[2] if len(item) > 2 else "")
                    num = str(item[1]) if len(item) > 1 else ""
                    msg = str(item[2]) if len(item) > 2 else ""
                    dt = str(item[3]) if len(item) > 3 else ""
                elif isinstance(item, dict):
                    msg_text = str(item.get("message", item.get("msg", "")))
                    api_svc = str(item.get("service", item.get("app", item.get("cli", "")))).strip()
                    if api_svc and api_svc.lower() != "unknown":
                        service = api_svc
                    else:
                        service = detect_service(msg_text, cli_hint=api_svc)
                    num = str(item.get("num", item.get("number", "")))
                    msg = msg_text
                    dt = str(item.get("dt", item.get("date", item.get("time", ""))))
                else:
                    continue
                if msg and num:
                    results.append([service, num, msg, dt])
            except Exception as e:
                print(f"[DEBUG] Main API item error: {e}")
                continue
        print(f"[DEBUG] Main API parsed: {len(results)} entries")
        return results
    except Exception as e:
        print(f"[DEBUG] Main API error: {e}")
    return []

def fetch_api_original():
    try:
        params = {"token": TOKEN, "records": 5}
        response = requests.get(API_URL, params=params, timeout=5)
        data = response.json()
        print(f"[DEBUG] Original API status: {data.get('status')}, records: {len(data.get('data', []))}")
        if data.get("status") == "success":
            results = []
            for sms in data.get("data", []):
                api_svc = str(sms.get("service", sms.get("app", sms.get("cli", "")))).strip()
                if api_svc and api_svc.lower() != "unknown":
                    service = api_svc
                else:
                    service = detect_service(sms.get("message", ""), cli_hint=api_svc)
                results.append([
                    service,
                    sms.get("num", ""),
                    sms.get("message", ""),
                    sms.get("dt", "")
                ])
            return results
    except Exception as e:
        print(f"[DEBUG] Original API error: {e}")
    return []

def fetch_api_railway(api_url):
    try:
        response = requests.get(api_url, timeout=10)
        data = response.json()
        records = data.get("aaData", [])
        print(f"[DEBUG] Railway API ({api_url}): {len(records)} records")
        valid = [r for r in records if isinstance(r[0], str) and ":" in r[0]]
        results = []
        for r in valid:
            msg = r[4] if len(r) > 4 else ""
            api_svc = str(r[3]).strip() if len(r) > 3 and r[3] else ""
            if api_svc and api_svc.lower() != "unknown":
                service = api_svc
            else:
                service = detect_service(msg, cli_hint=api_svc)
            results.append([
                service,
                r[2] if len(r) > 2 else "",
                msg,
                r[0]
            ])
        return results
    except Exception as e:
        print(f"[DEBUG] Railway API error ({api_url}): {e}")
    return []

def panel_login(panel):
    try:
        session = requests.Session()
        base_url = panel['url']
        username = panel['username']
        password = panel['password']
        login_path = panel.get('login_path', '/ints/login')
        signin_path = panel.get('signin_path', '/ints/signin')
        has_crlf = panel.get('has_crlf', False)
        login_url = base_url + login_path
        signin_url = base_url + signin_path
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive'
        }
        response = session.get(login_url, headers=headers, timeout=10)
        captcha_match = re.search(r'What is (\d+) \+ (\d+) = \?', response.text)
        if not captcha_match:
            return None
        n1 = int(captcha_match.group(1))
        n2 = int(captcha_match.group(2))
        captcha_answer = str(n1 + n2)
        data = {
            'username': username,
            'password': password,
            'capt': captcha_answer
        }
        if has_crlf:
            crlf_match = re.search(r'''name=["']crlf["']\s+value=["']([^"']+)["']''', response.text)
            if crlf_match:
                data['crlf'] = crlf_match.group(1)
        login_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': login_url,
            'Origin': base_url
        }
        login_response = session.post(signin_url, data=data, headers=login_headers, timeout=10)
        if 'login' in login_response.url.lower():
            return None
        return session
    except Exception as e:
        print(f"❌ Login {panel['name']} error: {e}")
        return None

def get_sesskey(session, base_url, panel_name):
    try:
        reports_page = base_url + '/ints/agent/SMSCDRReports'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
        response = session.get(reports_page, headers=headers, timeout=10)
        sesskey_match = re.search(r'sesskey=([a-zA-Z0-9%=]+)', response.text)
        if sesskey_match:
            return sesskey_match.group(1)
        for cookie in session.cookies:
            if 'sesskey' in cookie.name.lower():
                return cookie.value
        return None
    except:
        return None

def fetch_login_panel(panel, session):
    try:
        base_url = panel['url']
        sms_api = base_url + '/ints/agent/res/data_smscdr.php'
        use_sesskey = panel.get('use_sesskey', True)
        now = datetime.now()
        date1 = (now - timedelta(days=2)).strftime('%Y-%m-%d')
        date2 = now.strftime('%Y-%m-%d')
        params = {
            'fdate1': f'{date1} 00:00:00',
            'fdate2': f'{date2} 23:59:59',
            'frange': '',
            'fclient': '',
            'fnum': '',
            'fcli': '',
            'fgdate': '',
            'fgmonth': '',
            'fgrange': '',
            'fgclient': '',
            'fgnumber': '',
            'fgcli': '',
            'fg': '0',
            'sEcho': '1',
            'iColumns': '9',
            'sColumns': ',,,,,,,,',
            'iDisplayStart': '0',
            'iDisplayLength': '200',
            'mDataProp_0': '0',
            'sSearch_0': '',
            'bRegex_0': 'false',
            'bSearchable_0': 'true',
            'bSortable_0': 'true',
            'mDataProp_1': '1',
            'sSearch_1': '',
            'bRegex_1': 'false',
            'bSearchable_1': 'true',
            'bSortable_1': 'true',
            'mDataProp_2': '2',
            'sSearch_2': '',
            'bRegex_2': 'false',
            'bSearchable_2': 'true',
            'bSortable_2': 'true',
            'mDataProp_3': '3',
            'sSearch_3': '',
            'bRegex_3': 'false',
            'bSearchable_3': 'true',
            'bSortable_3': 'true',
            'mDataProp_4': '4',
            'sSearch_4': '',
            'bRegex_4': 'false',
            'bSearchable_4': 'true',
            'bSortable_4': 'true',
            'mDataProp_5': '5',
            'sSearch_5': '',
            'bRegex_5': 'false',
            'bSearchable_5': 'true',
            'bSortable_5': 'true',
            'mDataProp_6': '6',
            'sSearch_6': '',
            'bRegex_6': 'false',
            'bSearchable_6': 'true',
            'bSortable_6': 'true',
            'mDataProp_7': '7',
            'sSearch_7': '',
            'bRegex_7': 'false',
            'bSearchable_7': 'true',
            'bSortable_7': 'true',
            'mDataProp_8': '8',
            'sSearch_8': '',
            'bRegex_8': 'false',
            'bSearchable_8': 'true',
            'bSortable_8': 'false',
            'sSearch': '',
            'bRegex': 'false',
            'iSortCol_0': '0',
            'sSortDir_0': 'desc',
            'iSortingCols': '1',
            '_': str(int(time.time() * 1000))
        }
        if use_sesskey:
            sesskey = get_sesskey(session, base_url, panel['name'])
            if sesskey:
                params['sesskey'] = sesskey
        url = sms_api + '?' + urlencode(params)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': base_url + '/ints/agent/SMSCDRStats',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }
        response = session.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('aaData'):
                sms_list = []
                for row in data['aaData']:
                    if len(row) > 0 and isinstance(row[0], str):
                        if row[0].startswith('0.') or row[0].startswith('0,') or 'NAN%' in str(row[0]):
                            continue
                        if len(row) > 2 and (str(row[2]) == '0' or str(row[2]) == ''):
                            continue
                        sms_list.append({
                            'num': row[2] if len(row) > 2 else '',
                            'message': row[5] if len(row) > 5 else '',
                            'cli': row[3] if len(row) > 3 else '',
                            'dt': row[0] if len(row) > 0 else ''
                        })
                return sms_list
        return []
    except Exception as e:
        print(f"❌ Login Panel {panel['name']} fetch error: {e}")
        return []

def fetch_msi_panel():
    session = panel_sessions.get('MSI SMS')
    if not session:
        session = panel_login(MSI_PANEL)
        if session:
            panel_sessions['MSI SMS'] = session
            print("✅ MSI SMS Logged in")
        else:
            print("❌ MSI SMS Login failed")
            return []
    sms_list = fetch_login_panel(MSI_PANEL, session)
    results = []
    for sms in sms_list:
        phone = sms.get('num', '')
        msg = sms.get('message', '')
        cli = sms.get('cli', '')
        dt = sms.get('dt', '')
        if not phone or not str(phone).strip():
            continue
        if not msg or len(str(msg).strip()) < 3:
            continue
        msg = html.unescape(str(msg))
        msg = msg.replace('null', '').strip()
        if cli and 'Unknown' not in str(cli):
            msg = f"[{cli}] {msg}"
        service = detect_service(msg, cli_hint=cli)
        results.append([service, phone, msg, dt])
    print(f"[DEBUG] MSI Panel: {len(results)} records")
    return results

# ===== TELEGRAM API HELPERS =====
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def api(method, payload=None):
    url = f"{BASE_URL}/{method}"
    try:
        if payload:
            r = requests.post(url, json=payload, timeout=10)
        else:
            r = requests.get(url, timeout=10)
        return r.json()
    except:
        return {}

_edit_context = threading.local()

def send_message(chat_id, text, reply_markup=None, parse_mode="HTML"):
    edit_msg_id = getattr(_edit_context, 'msg_id', None)
    if edit_msg_id:
        return edit_message_text(chat_id, edit_msg_id, text, reply_markup, parse_mode)
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    return api("sendMessage", payload)

def edit_message_text(chat_id, message_id, text, reply_markup=None, parse_mode="HTML"):
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": parse_mode,
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    return api("editMessageText", payload)

def copy_message(chat_id, from_chat_id, message_id, reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "from_chat_id": from_chat_id,
        "message_id": message_id,
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    return api("copyMessage", payload)

def answer_callback_query(callback_query_id, text=None):
    payload = {"callback_query_id": callback_query_id}
    if text:
        payload["text"] = text
        payload["show_alert"] = True
    return api("answerCallbackQuery", payload)

# ===== INLINE BUTTON BUILDERS =====
def btn(text, callback_data=None, url=None, style="primary", emoji_tag=None, copy_text=None, custom_emoji_id=None):
    text = text.strip()
    b = {"text": text, "style": style}
    eid = custom_emoji_id or (CE.get(emoji_tag) if emoji_tag else None)
    if eid:
        b["icon_custom_emoji_id"] = eid
    if emoji_tag and CE.get(emoji_tag):
        b["icon_custom_emoji_id"] = CE[emoji_tag]
    if callback_data:
        b["callback_data"] = callback_data
    if url:
        b["url"] = url
    if copy_text:
        b["copy_text"] = {"text": copy_text}
    return b

def build_inline(rows):
    return {"inline_keyboard": rows}

def reply_btn(text, style="primary", emoji_tag=None, custom_emoji_id=None):
    b = {"text": text, "style": style}
    eid = custom_emoji_id or (CE.get(emoji_tag) if emoji_tag else None)
    if eid:
        b["icon_custom_emoji_id"] = eid
    return b

STYLE_CYCLE = ["primary", "success", "danger"]

def cycle_style(index, offset=0):
    return STYLE_CYCLE[(index + offset) % len(STYLE_CYCLE)]

def fmt_num(val):
    s = f"{val:.12f}".rstrip('0').rstrip('.')
    return s if s else "0"



def detect_services_in_text(text):
    """Detect service names mentioned in text using SERVICE_LOGOS and db services"""
    found = []
    text_lower = text.lower()
    for svc_name in db.get("services", {}):
        if svc_name.lower() in text_lower and svc_name not in found:
            found.append(svc_name)
    for svc_name in SERVICE_LOGOS.keys():
        if svc_name.lower() in text_lower and svc_name not in found:
            found.append(svc_name)
    return found

def detect_countries_in_text(text):
    """Detect country names/codes mentioned in text, returns list of (code, name)"""
    found = []
    text_lower = text.lower()
    for name, code in COUNTRY_NAME_TO_CODE.items():
        if name.lower() in text_lower:
            if code not in [c for c, n in found]:
                cname = COUNTRY_FLAGS.get(code, {}).get("name", name.title())
                found.append((code, cname))
    words = re.findall(r'\b[A-Za-z]{2}\b', text)
    for word in words:
        word_upper = word.upper()
        if word_upper in COUNTRY_FLAGS and word_upper not in [c for c, n in found]:
            found.append((word_upper, COUNTRY_FLAGS[word_upper]["name"]))
    return found

def enhance_broadcast_with_emojis(text):
    """Replace normal emojis with premium ones, add premium service/country emojis inline"""
    result = text

    # 1. Replace normal Unicode emojis with premium <tg-emoji> versions from CE
    _emoji_map = {
        '🔥': 'fire', '🚀': 'rocket', '💯': 'check', '✅': 'check', '✔️': 'check',
        '☑️': 'check', '⚠️': 'warn', '❌': 'no', '❎': 'no', '✨': 'star', '⭐': 'star',
        '💰': 'moneybag', '💵': 'money', '📱': 'phone', '👑': 'crown', '🎁': 'gift',
        '📢': 'broadcast', '🔗': 'link', '⏰': 'clock', '⏳': 'time', '👤': 'user',
        '🌍': 'globe', '📞': 'phone', '📋': 'clipboard', '📊': 'graph', '🔐': 'otpkey',
        '💳': 'money', '💸': 'money', '🏳️': 'globe', '🏴': 'globe', '🚫': 'ban',
        '👥': 'broadcast', '📲': 'phone', '📳': 'phone', '📴': 'phone', '📵': 'no',
        '🆓': 'free', '🆕': 'new', '💎': 'vip', '🔒': 'lock', '🔓': 'lock', '📝': 'pencil',
        '🗑️': 'trash', '↗️': 'rightarrow', '➡️': 'rightarrow', '⬇️': 'downarrow',
        '🔽': 'downarrow2', '🥇': 'first', '🥈': 'second', '🥉': 'third', '🏆': 'first',
        '🎖️': 'first', '💻': 'hacker', '🖥️': 'hacker', '⚡': 'electric', '🔋': 'electric',
        '🔌': 'electric', '📶': 'stats', '📡': 'stats', '📠': 'stats', '💹': 'graph',
        '📈': 'graph', '📉': 'graph', '🔔': 'warn', '🔕': 'no', '📣': 'broadcast',
        '📯': 'broadcast', '🔊': 'broadcast', '🔉': 'broadcast', '🔈': 'broadcast',
        '📍': 'pin', '📌': 'pin2', '✂️': 'scissors', '📎': 'link', '🔗': 'chain',
        '📏': 'stats', '📐': 'stats', '🧮': 'stats', '🔢': 'number', '🔟': 'number',
        '🔠': 'broadcast', '🔡': 'broadcast', '🔤': 'broadcast', '🅰️': 'broadcast',
        '🆎': 'broadcast', '🅱️': 'broadcast', '🆑': 'check', '🆒': 'check', '🆓': 'free',
        '🆔': 'id', 'Ⓜ️': 'broadcast', '🆖': 'no', '🅾️': 'ok', '🆗': 'ok', '🅿️': 'ok',
        '🆘': 'warn', '🆙': 'uparrow', '🆚': 'versus', '🈁': 'ok', '🈂️': 'ok',
        '🈷️': 'ok', '🈶': 'ok', '🈯': 'ok', '🉐': 'ok', '🈹': 'ok', '🈚': 'no',
        '🈲': 'no', '🉑': 'check', '🈸': 'ok', '🈴': 'check', '🈳': 'ok', '㊗️': 'ok',
        '㊙️': 'lock', '🈺': 'ok', '🈵': 'ok',
    }
    for normal_emoji, ce_tag in _emoji_map.items():
        eid = CE.get(ce_tag, "")
        if eid and normal_emoji in result:
            premium = f'<tg-emoji emoji-id="{eid}">{normal_emoji}</tg-emoji>'
            result = result.replace(normal_emoji, premium)

    # 2. Add premium service emoji BEFORE first occurrence only (track seen)
    text_lower = result.lower()
    seen_services = set()
    all_services = set(list(SERVICE_LOGOS.keys()) + list(db.get("services", {}).keys()))
    for svc_name in all_services:
        svc_lower = svc_name.lower()
        if svc_lower in text_lower and svc_lower not in seen_services:
            seen_services.add(svc_lower)
            eid = SERVICE_LOGOS.get(svc_name, "")
            if not eid:
                for k, v in SERVICE_LOGOS.items():
                    if k.lower() == svc_lower:
                        eid = v
                        break
            if eid:
                emoji_tag = f'<tg-emoji emoji-id="{eid}">📱</tg-emoji>'
                pattern = re.compile(r'\b' + re.escape(svc_name) + r'\b', re.IGNORECASE)
                result = pattern.sub(lambda m: emoji_tag + " " + m.group(0), result, count=1)

    # 3. Add premium country flag BEFORE first occurrence only (track seen by country code)
    seen_countries = set()
    for name, code in COUNTRY_NAME_TO_CODE.items():
        if name.lower() in text_lower and code not in seen_countries:
            seen_countries.add(code)
            flag_data = COUNTRY_FLAGS.get(code)
            if flag_data and flag_data.get("id"):
                emoji_tag = f'<tg-emoji emoji-id="{flag_data["id"]}">🏳️</tg-emoji>'
                pattern = re.compile(r'\b' + re.escape(name) + r'\b', re.IGNORECASE)
                result = pattern.sub(lambda m: emoji_tag + " " + m.group(0), result, count=1)

        return result

def build_reply(rows):
    return {"keyboard": rows, "resize_keyboard": True, "one_time_keyboard": False}

# ===== MENUS =====
def main_menu_markup(uid=None):
    rows = [
        [btn("𝗚𝗘𝗧 𝗡𝗨𝗠𝗕𝗘𝗥", "menu_getnumber", style="primary", emoji_tag="phone"),
         btn("𝗠𝗬 𝗔𝗖𝗖𝗢𝗨𝗡𝗧", "menu_account", style="success", emoji_tag="newking")],
        [btn("𝗕𝗔𝗟𝗔𝗡𝗖𝗘", "menu_balance", style="success", emoji_tag="moneybag"),
         btn("𝗪𝗜𝗧𝗛𝗗𝗥𝗔𝗪", "menu_withdraw", style="danger", emoji_tag="money")],
        [btn("𝗧𝗢𝗣 𝗨𝗦𝗘𝗥𝗦", "menu_topusers", style="success", emoji_tag="king2"),
         btn("𝗗𝗘𝗩𝗘𝗟𝗢𝗣𝗘𝗥", "menu_developer", style="primary", emoji_tag="hacker")],
        [btn("𝗥𝗘𝗙𝗘𝗥𝗥𝗔𝗟", "menu_referral", style="success", emoji_tag="gift"),
         btn("𝗔𝗖𝗖𝗘𝗦𝗦 𝗟𝗜𝗦𝗧", "menu_accesslist", style="primary", emoji_tag="graph")],
        [btn("𝗢𝗧𝗣 𝗛𝗜𝗦𝗧𝗢𝗥𝗬", "menu_otphistory", style="success", emoji_tag="otpkey")],
        [btn("𝗢𝗧𝗣 𝗥𝗘𝗪𝗔𝗥𝗗𝗦", "menu_otprewards", style="success", emoji_tag="gift")],
        [btn("𝗝𝗢𝗜𝗡 𝗢𝗨𝗥 𝗖𝗛𝗔𝗡𝗡𝗘𝗟𝗦", "menu_channels", style="primary", emoji_tag="broadcast")],
    ]
    if str(uid) in [str(a) for a in ADMIN_IDS]:
        rows.append([btn("𝗔𝗗𝗠𝗜𝗡 𝗣𝗔𝗡𝗘𝗟", "menu_admin", style="danger", emoji_tag="admin")])
    return build_inline(rows)

def main_menu_reply_markup(uid=None):
    rows = [
        [reply_btn("𝗚𝗘𝗧 𝗡𝗨𝗠𝗕𝗘𝗥", style="primary", emoji_tag="phone"),
         reply_btn("𝗠𝗬 𝗔𝗖𝗖𝗢𝗨𝗡𝗧", style="success", emoji_tag="newking")],
        [reply_btn("𝗕𝗔𝗟𝗔𝗡𝗖𝗘", style="success", emoji_tag="moneybag"),
         reply_btn("𝗪𝗜𝗧𝗛𝗗𝗥𝗔𝗪", style="danger", emoji_tag="money")],
        [reply_btn("𝗧𝗢𝗣 𝗨𝗦𝗘𝗥𝗦", style="success", emoji_tag="king2"),
         reply_btn("𝗗𝗘𝗩𝗘𝗟𝗢𝗣𝗘𝗥", style="primary", emoji_tag="hacker")],
        [reply_btn("𝗥𝗘𝗙𝗘𝗥𝗥𝗔𝗟", style="success", emoji_tag="gift"),
         reply_btn("𝗔𝗖𝗖𝗘𝗦𝗦 𝗟𝗜𝗦𝗧", style="primary", emoji_tag="graph")],
        [reply_btn("𝗢𝗧𝗣 𝗥𝗘𝗪𝗔𝗥𝗗𝗦", style="success", emoji_tag="gift")],
        [reply_btn("𝗝𝗢𝗜𝗡 𝗢𝗨𝗥 𝗖𝗛𝗔𝗡𝗡𝗘𝗟𝗦", style="primary", emoji_tag="broadcast")],
    ]
    if str(uid) in [str(a) for a in ADMIN_IDS]:
        rows.append([reply_btn("𝗔𝗗𝗠𝗜𝗡 𝗣𝗔𝗡𝗘𝗟", style="danger", emoji_tag="admin")])
    return build_reply(rows)

def admin_menu_markup():
    return build_inline([
        [btn("Add Service", "admin_addservice", style="success", emoji_tag="plus"),
         btn("View Services", "admin_viewservices", style="primary", emoji_tag="clipboard")],
        [btn("Remove Service", "admin_removeservice", style="danger", emoji_tag="no"),
         btn("Ban User", "admin_banuser", style="danger", emoji_tag="ban")],
        [btn("Unban User", "admin_unbanuser", style="success", emoji_tag="ntick"),
         btn("Add Country", "admin_addcountry", style="success", emoji_tag="plus")],
        [btn("View Countries", "admin_viewcountries", style="primary", emoji_tag="clipboard"),
         btn("Remove Country", "admin_removecountry", style="danger", emoji_tag="no")],
        [btn("Remove Number", "admin_removenumber", style="danger", emoji_tag="no"),
         btn("Add Numbers", "admin_addnumbers", style="success", emoji_tag="plus")],
        [btn("Stats", "admin_stats", style="primary", emoji_tag="stats"),
         btn("Broadcast", "admin_broadcast", style="danger", emoji_tag="broadcast")],
        [btn("Manage Withdrawals", "admin_withdrawals", style="danger", emoji_tag="money"),
         btn("Check Balance", "admin_checkbalance", style="primary", emoji_tag="moneybag")],
        [btn("Remove Balance", "admin_removebalance", style="danger", emoji_tag="no"),
         btn("Remove All Balances", "admin_removeallbalance", style="danger", emoji_tag="no")],
        [btn("Enable Withdrawals", "admin_enablewithdraw", style="success", emoji_tag="ntick"),
         btn("Disable Withdrawals", "admin_disablewithdraw", style="danger", emoji_tag="no")],
        [btn("Add Admin", "admin_addadmin", style="success", emoji_tag="ntick"),
         btn("Remove Admin", "admin_removeadmin", style="danger", emoji_tag="no")],
        [btn("View Admins", "admin_viewadmins", style="primary", emoji_tag="clipboard"),
         btn("Add IvaSMS", "admin_addivasms", style="success", emoji_tag="plus")],
        [btn("My IvaSMS", "admin_myivasms", style="primary", emoji_tag="clipboard"),
         btn("Add Group", "admin_addgroup", style="success", emoji_tag="plus")],
        [btn("View Groups", "admin_viewgroups", style="primary", emoji_tag="clipboard"),
         btn("Remove Group", "admin_removegroup", style="danger", emoji_tag="no")],
        [btn("Back to Main Menu", "menu_main", style="primary", emoji_tag="back")],
    ])

def back_markup(callback, text="Back"):
    return build_inline([
        [btn(text, callback, style="primary", emoji_tag="back")]
    ])

def back_to_main_markup():
    return build_inline([
        [btn("Back to Main Menu", "menu_main", style="primary", emoji_tag="back")]
    ])

# ===== USER HANDLERS =====
def handle_start(chat_id, user):
    uid = str(user.get("id", chat_id))
    uname = user.get("username", "User")
    fname = user.get("first_name", "User")
    if is_banned(uid):
        send_message(chat_id, f"{ce('no','🚫')} <b>You are banned from using this bot.</b>")
        return
    if uid not in db["users"]:
        db["users"][uid] = {
            "id": uid,
            "username": uname,
            "first_name": fname,
            "balance": 0.0,
            "total_earned": 0.0,
            "referrals": 0,
            "referral_code": uid,
            "joined": datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S"),
            "otp_count": 0,
            "otp_rewards_claimed": 0,
        }
        db["stats"]["total_users"] = len(db["users"])
        save_db(db)
    missing = check_force_join(uid)
    if missing:
        text = (
            f"{ce('warn','⚠️')} <b>Join Required!</b>\n\n"
            f"{ce('hi','👋')} Hello <code>{fname}</code>!\n"
            f"{ce('broadcast','📢')} You must join all channels and group to use this bot."
        )
        send_message(chat_id, text, force_join_markup(missing))
        return
    welcome = (
        f"{ce('electric','⚡')} <b>Welcome to Syed OTP Work Bot!</b>\n\n"
        f"{ce('moneybag','💰')} <b>Do OTPs and Earn a lot of money!</b>\n\n"
    )
    send_message(chat_id, welcome, main_menu_reply_markup(uid))

def handle_get_number(chat_id, uid):
    services = db.get("services", {})
    if not services:
        send_message(chat_id, f"{ce('warn','⚠️')} <b>No services available yet.</b>")
        return
    offset = db.get("user_states", {}).get(uid, {}).get("style_offset", 0)
    rows = []
    svc_items = list(services.items())
    idx = 0
    for i in range(0, len(svc_items), 2):
        row = []
        for j in range(2):
            if i + j < len(svc_items):
                svc_name, svc_data = svc_items[i + j]
                eid = SERVICE_LOGOS.get(svc_name, SERVICE_LOGOS.get("Unknown", ""))
                row.append(btn(f"{svc_name}", f"svc_{svc_name}", style=cycle_style(idx, offset), custom_emoji_id=eid))
                idx += 1
        rows.append(row)
    rows.append([btn("Refresh", "refresh_services", style=cycle_style(idx, offset), emoji_tag="rocket")])
    idx += 1
    send_message(chat_id, f"{ce('downarrow','📱')} <b>Select a Service</b>\n\n{ce('downarrow2','🔽')} Choose below:{ce('free','🆓')}", build_inline(rows))

def handle_service_selected(chat_id, uid, svc_name):
    service_countries = db.get("service_countries", {}).get(svc_name, {})
    countries = service_countries
    if not countries:
        text = f"{ce('warn','⚠️')} <b>No countries available for {svc_name}.</b>\nAdd countries from ADMIN PANEL > Add Country."
        send_message(chat_id, text)
        return
    offset = db.get("user_states", {}).get(uid, {}).get("style_offset", 0)
    rows = []
    ctry_items = list(countries.items())
    idx = 0
    for i in range(0, len(ctry_items), 2):
        row = []
        for j in range(2):
            if i + j < len(ctry_items):
                code, cdata = ctry_items[i + j]
                real_code = cdata.get("real_code", code)
                flag_id = COUNTRY_FLAGS.get(real_code, {}).get("id", "")
                price_display = cdata.get("price_display", str(cdata.get("price", 0)))
                display_name = cdata.get("name", code)
                row.append(btn(f"{display_name} {price_display} $", f"ctry_{svc_name}_{code}", style=cycle_style(idx, offset), custom_emoji_id=flag_id))
                idx += 1
        rows.append(row)
    rows.append([btn("Refresh", f"refresh_svc_{svc_name}", style=cycle_style(idx, offset), emoji_tag="rocket")])
    idx += 1
    text = f"{svc_emoji(svc_name, '📱')} <b>{svc_name}</b>\n{ce('globe','🌍')} <b>Select Country:</b>"
    send_message(chat_id, text, build_inline(rows))

def show_assigned_numbers(chat_id, uid, svc_name, ccode, user_nums, show_cc=True):
    cdata = db.get("service_countries", {}).get(svc_name, {}).get(ccode, {})
    country = cdata.get("name", db.get("countries", {}).get(ccode, {}).get("name", ccode))
    real_code = cdata.get("real_code", ccode)
    flag = flag_emoji(real_code, "🏳️")
    text = (
        f"{flag} <b>{country} Numbers Assigned</b> {ce('check','✅')}\n"
        f"{ce('warn','🔔')} <b>Waiting for OTP…….</b>"
    )
    rows = []
    for num in user_nums:
        display_num = num
        if not show_cc:
            try:
                if not display_num.startswith("+"):
                    parsed = phonenumbers.parse("+" + display_num)
                else:
                    parsed = phonenumbers.parse(display_num)
                display_num = str(parsed.national_number)
            except:
                pass
        rows.append([btn(f"{display_num}", copy_text=display_num, style="primary", emoji_tag="copy")])
    cc_btn_text = "E Without CC" if show_cc else "D Without CC"
    cc_emoji = "plus" if show_cc else "no"
    rows.append([btn(cc_btn_text, f"toggle_cc_{svc_name}_{ccode}", style="primary", emoji_tag=cc_emoji)])
    rows.append([btn("Change Country", f"changectry_{svc_name}", style="success", emoji_tag="world")])
    rows.append([btn("Refresh Numbers", f"changenum_{svc_name}_{ccode}", style="success", emoji_tag="rocket")])
    rows.append([btn("OTP Group", url="https://t.me/TNLOTPZONE", style="danger", emoji_tag="broadcast")])
    send_message(chat_id, text, build_inline(rows))

def handle_service_selected_no_back(chat_id, uid, svc_name):
    service_countries = db.get("service_countries", {}).get(svc_name, {})
    countries = service_countries
    if not countries:
        text = f"{ce('warn','⚠️')} <b>No countries available for {svc_name}.</b>" + chr(10) + "Add countries from ADMIN PANEL > Add Country."
        r = send_message(chat_id, text)
        return r.get("result", {}).get("message_id") if isinstance(r, dict) and r.get("ok") else None
    offset = db.get("user_states", {}).get(uid, {}).get("style_offset", 0)
    rows = []
    ctry_items = list(countries.items())
    idx = 0
    for i in range(0, len(ctry_items), 2):
        row = []
        for j in range(2):
            if i + j < len(ctry_items):
                code, cdata = ctry_items[i + j]
                real_code = cdata.get("real_code", code)
                flag_id = COUNTRY_FLAGS.get(real_code, {}).get("id", "")
                price_display = cdata.get("price_display", str(cdata.get("price", 0)))
                display_name = cdata.get("name", code)
                row.append(btn(f"{display_name} {price_display} $", f"ctry_{svc_name}_{code}", style=cycle_style(idx, offset), custom_emoji_id=flag_id))
                idx += 1
        rows.append(row)
    rows.append([btn("Refresh", f"refresh_svc_{svc_name}", style=cycle_style(idx, offset), emoji_tag="rocket")])
    # NO BACK BUTTON for broadcast flow
    text = f"{svc_emoji(svc_name, '📱')} <b>{svc_name}</b>" + chr(10) + f"{ce('globe','🌍')} <b>Select Country:</b>"
    r = send_message(chat_id, text, build_inline(rows))
    return r.get("result", {}).get("message_id") if isinstance(r, dict) and r.get("ok") else None

def handle_country_selected(chat_id, uid, svc_name, ccode):
    numbers = db.get("numbers", {}).get(svc_name, {}).get(ccode, [])
    # For custom countries, get name from service_countries
    cdata = db.get("service_countries", {}).get(svc_name, {}).get(ccode, {})
    country = cdata.get("name", db.get("countries", {}).get(ccode, {}).get("name", ccode))
    real_code = cdata.get("real_code", ccode)
    flag = flag_emoji(real_code, "🏳️")
    if not numbers:
        send_message(chat_id, f"{ce('warn','⚠️')} <b>No numbers available for {country}.</b>")
        return
    old_state = db.get("user_states", {}).get(uid, {})
    if old_state.get("svc_name") == svc_name and old_state.get("ccode") == ccode:
        old_nums = old_state.get("numbers", [])
        for num in old_nums:
            db["number_assignments"].pop(num, None)
    user_nums = random.sample(numbers, min(5, len(numbers))) if numbers else []
    # Ensure all numbers have + prefix
    user_nums = [n if str(n).startswith("+") else "+" + str(n) for n in user_nums]
    db.setdefault("number_assignments", {})
    for num in user_nums:
        db["number_assignments"][num] = {
            "user_id": uid,
            "service": svc_name,
            "country": ccode,
            "assigned_at": datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S"),
            "otp_count": 0
        }
    db["user_states"][uid] = {
        "state": "numbers_assigned",
        "svc_name": svc_name,
        "ccode": ccode,
        "numbers": user_nums,
        "show_cc": True,
        "refresh_cooldown": time.time()
    }
    save_db(db)
    show_assigned_numbers(chat_id, uid, svc_name, ccode, user_nums, show_cc=True)

def handle_account(chat_id, uid):
    user = db["users"].get(uid, {})
    text = (
        f"{ce('newking','👑')} <b>MY ACCOUNT</b>\n\n"
        f"{ce('user','👤')} <b>Name:</b> <code>{user.get('first_name', 'N/A')}</code>\n"
        f"{ce('moneybag','💰')} <b>Balance:</b> <code>{fmt_num(user.get('balance', 0))}</code> $\n"
        f"{ce('money','💵')} <b>Total Earned:</b> <code>{fmt_num(user.get('total_earned', 0))}</code> $\n"
        f"{ce('otpkey','⭐')} <b>OTPs Done:</b> <code>{user.get('otp_count', 0)}</code>\n"
        f"{ce('gift','🎁')} <b>Referrals:</b> <code>{user.get('referrals', 0)}</code>\n"
        f"{ce('link','🔗')} <b>Referral Code:</b> <code>{user.get('referral_code', uid)}</code>"
    )
    send_message(chat_id, text)

def handle_balance(chat_id, uid):
    bal = db["users"].get(uid, {}).get("balance", 0)
    text = (
        f"{ce('moneybag','💰')} <b>Your Balance</b>\n\n"
        f"{ce('money','💵')} <b>Current Balance:</b> <code>{fmt_num(bal)}</code> $\n\n"
        f"{ce('rocket','⚡')} Do more OTPs to earn more!"
    )
    rows = [
        [btn("WITHDRAW", "menu_withdraw", style="danger", emoji_tag="money")],
    ]
    send_message(chat_id, text, build_inline(rows))

def handle_withdraw(chat_id, uid):
    if not db.get("withdrawals_enabled", True):
        send_message(
            chat_id,
            f"{ce('no','❌')} <b>Withdrawals Disabled</b>\n\n"
            f"{ce('warn','🔔')} Withdrawal requests are currently disabled by the admin.\n"
            f"Please check back later.",
            None
        )
        return
    bal = db["users"].get(uid, {}).get("balance", 0)
    if bal < 1:
        send_message(
            chat_id,
            f"{ce('warn','⚠️')} <b>Minimum withdrawal is 1$.</b>\n"
            f"{ce('moneybag','💰')} Your balance: <code>{fmt_num(bal)}</code> $",
            None
        )
        return
    db["user_states"][uid] = {"state": "awaiting_withdraw_amount"}
    save_db(db)
    text = (
        f"{ce('withdraw','💵')} <b>Withdrawal Request</b>\n\n"
        f"{ce('moneybag','💰')} Available: <code>{fmt_num(bal)}</code> $\n"
        f"{ce('warn','⚠️')} Send the amount you want to withdraw:"
    )
    send_message(chat_id, text)

def handle_withdraw_amount(chat_id, uid, amount_text):
    try:
        amount = float(amount_text)
    except:
        send_message(chat_id, f"{ce('no','❌')} Invalid amount. Send a number.")
        db["user_states"].pop(uid, None)
        save_db(db)
        return
    bal = db["users"].get(uid, {}).get("balance", 0)
    if amount > bal:
        send_message(chat_id, f"{ce('no','❌')} Insufficient balance. You have <code>{fmt_num(bal)}</code> $.")
        db["user_states"].pop(uid, None)
        save_db(db)
        return
    if amount < 1:
        send_message(chat_id, f"{ce('no','❌')} Minimum withdrawal is 1$.")
        db["user_states"].pop(uid, None)
        save_db(db)
        return
    db["user_states"][uid] = {"state": "awaiting_withdraw_method", "amount": amount}
    save_db(db)
    text = (
        f"{ce('withdraw','💵')} <b>Amount: {fmt_num(amount)} $</b>\n\n"
        f"{ce('link','🔗')} <b>Select Payment Method:</b>"
    )
    rows = [
        [btn("𝗕𝗶𝗻𝗮𝗻𝗰𝗲 𝗜𝗗", "wd_method_binanceid", style="primary", emoji_tag="link")],
        [btn("𝗧𝗥𝗖𝟮𝟬 (𝗨𝗦𝗗𝗧)", "wd_method_trc20", style="success", emoji_tag="money")],
        [btn("𝗖𝗿𝘆𝗽𝘁𝗼 (𝗔𝗻𝘆)", "wd_method_crypto", style="success", emoji_tag="coin")],
        [btn("𝗕𝟮𝗣 / 𝗣𝟮𝗣", "wd_method_b2p", style="primary", emoji_tag="moneybag")],
        [btn("𝗝𝗮𝘇𝘇𝗖𝗮𝘀𝗵", "wd_method_jazzcash", style="danger", emoji_tag="phone")],
        [btn("𝗘𝗮𝘀𝘆𝗽𝗮𝗶𝘀𝗮", "wd_method_easypaisa", style="danger", emoji_tag="phone")],
        [btn("𝗖𝗮𝗻𝗰𝗲𝗹", "menu_main", style="danger", emoji_tag="back")]
    ]
    send_message(chat_id, text, build_inline(rows))

def handle_withdraw_method(chat_id, uid, method_text):
    state = db["user_states"].get(uid, {})
    amount = state.get("amount", 0)
    user = db["users"].get(uid, {})
    db["withdrawals"].append({
        "user_id": uid,
        "username": user.get("username", "N/A"),
        "first_name": user.get("first_name", "N/A"),
        "amount": amount,
        "method": "Binance",
        "binance_id": method_text,
        "status": "pending",
        "date": datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S"),
    })
    db["users"][uid]["balance"] -= amount
    db["user_states"].pop(uid, None)
    save_db(db)
    idx = len(db["withdrawals"]) - 1
    admin_text = (
        f"{ce('warn','🚨')} <b>New Withdrawal Request!</b>\n\n"
        f"{ce('user','👤')} User: @{user.get('username', 'N/A')}\n"
        f"{ce('money','💵')} Amount: <code>{fmt_num(amount)}</code> $\n"
        f"{ce('link','🔗')} Binance ID: <code>{method_text}</code>\n"
        f"{ce('time','⏰')} Date: <code>{db['withdrawals'][idx]['date']}</code>"
    )
    admin_rows = build_inline([
        [btn("✅ Approve & Paid", f"wd_approve_{idx}", style="success", emoji_tag="check"),
         btn("❌ Reject", f"wd_reject_{idx}", style="danger", emoji_tag="no")],
    ])
    for admin_id in ADMIN_IDS:
        send_message(admin_id, admin_text, admin_rows)
    text = (
        f"{ce('check','✅')} <b>Withdrawal Request Submitted!</b>\n\n"
        f"{ce('money','💵')} Amount: <code>{fmt_num(amount)}</code> $\n"
        f"{ce('link','🔗')} Binance ID: <code>{method_text}</code>\n"
        f"{ce('time','⏰')} Status: <code>Pending</code>\n\n"
        f"{ce('warn','⚠️')} Admin will review and send payment soon!"
    )
    send_message(chat_id, text)

def handle_top_users(chat_id):
    users = sorted(db["users"].values(), key=lambda x: x.get("otp_count", 0), reverse=True)[:10]
    text = f"{ce('top','🔝')} <b>TOP USERS</b>\n\n"
    for i, u in enumerate(users, 1):
        if i == 1:
            medal = ce("first", "🥇")
        elif i == 2:
            medal = ce("second", "🥈")
        elif i == 3:
            medal = ce("third", "🥉")
        else:
            medal = f"{i}."
        text += f"{medal} <code>{u.get('first_name', 'User')}</code> — <code>{u.get('otp_count', 0)}</code> OTPs\n"
    if not users:
        text += "No users yet."
    send_message(chat_id, text)


def handle_developer(chat_id):
    text = (
        f"{ce('verified','👨‍💻')} <b>Developer Info</b>\n\n"
        f"{ce('hacker','🚀')} <b>Bot Made By:</b> <code>FLEX SAMAY </code>\n"
        f"{ce('crown','👑')} <b>Owner:</b> <a href=\"t.me/FLEXSAMAY\">𝐅𝐋𝐄𝐗 𝐒𝐀𝐌𝐀𝐘</a>\n\n"
        f"{ce('channel','📢')} <b>Channel:</b> <a href=\"{CHANNEL_LINK}\">𝗠𝗔𝗜𝗡 𝗖𝗛𝗔𝗡𝗡𝗘𝗟</a>\n"
        f"{ce('link','🔗')} <b>Chat:</b> <a href=\"{CHAT_LINK}\">𝗡𝗨𝗠𝗕𝗘𝗥 𝗖𝗛𝗔𝗡𝗡𝗘𝗟</a>"
    )
    send_message(chat_id, text)

def handle_referral(chat_id, uid):
    code = db["users"].get(uid, {}).get("referral_code", uid)
    link = f"https://t.me/OTP_WORKBOT?start={code}"
    count = db["users"].get(uid, {}).get("referrals", 0)
    text = (
        f"{ce('gift','🎁')} <b>Referral Program</b>\n\n"
        f"{ce('link','🔗')} <b>Your Link:</b>\n<code>{link}</code>\n\n"
        f"{ce('user','👤')} <b>Total Referrals:</b> <code>{count}</code>\n"
        f"{ce('money','💵')} Earn 10% from each referral!"
    )
    rows = [[btn("Copy Link", copy_text=link, style="success", emoji_tag="clipboard")]]
    send_message(chat_id, text, build_inline(rows))

def handle_channels(chat_id):
    text = (
        f"{ce('broadcast','📢')} <b>JOIN OUR CHANNELS</b>\n\n"
        f"{ce('channel','📢')} Stay updated with latest OTPs and news!"
    )
    rows = [
        [btn("𝗠𝗔𝗜𝗡 𝗖𝗛𝗔𝗡𝗡𝗘𝗟", url=CHANNEL_LINK, style="primary", emoji_tag="channel")],
        [btn("𝗡𝗨𝗠𝗕𝗘𝗥 𝗖𝗛𝗔𝗡𝗡𝗘𝗟", url=CHAT_LINK, style="success", emoji_tag="call")],
        [btn("𝗠𝗘𝗧𝗛𝗢𝗗𝗦 𝗖𝗛𝗔𝗡𝗡𝗘𝗟", url="https://t.me/TNLMETHODS", style="success", emoji_tag="channel")],
    ]
    send_message(chat_id, text, build_inline(rows))

def handle_access_list(chat_id, uid):
    services = db.get("services", {})
    numbers = db.get("numbers", {})
    countries = db.get("countries", {})
    service_countries = db.get("service_countries", {})
    otp_counts = db.get("otp_counts", {})
    if not services:
        send_message(chat_id, f"{ce('warn','⚠️')} <b>No services added yet.</b>")
        return
    text = f"{ce('live','📡')} <b>LIVE TRAFFIC</b> {ce('clock','⏰')}\n\n"
    all_otps = []
    for svc, ctry_data in otp_counts.items():
        for ccode, count in ctry_data.items():
            all_otps.append((count, svc, ccode))
    all_otps.sort(reverse=True)
    if all_otps:
        for count, svc, ccode in all_otps[:5]:
            cname = countries.get(ccode, {}).get("name", ccode)
            flag = flag_emoji(ccode, "🏳️")
            text += f"{ce('top','🔝')} {svc_emoji(svc, '📱')} <code>{svc}</code> | {flag} <code>{cname}</code> | <b>{count}</b> OTPs\n"
    else:
        text += f"{ce('warn','⚠️')} No OTP data yet.\n"
    text += f"\n{ce('graph','📊')} <b>ACCESS LIST</b> {ce('fire','🔥')}\n\n"
    for svc_name in sorted(services.keys()):
        svc_data = services.get(svc_name, {})
        svc_nums = numbers.get(svc_name, {})
        total_nums = sum(len(v) for v in svc_nums.values())
        text += f"{svc_emoji(svc_name, '📱')} <b>{svc_name}</b>"
        text += f" | {ce('phone','📞')} <b>{total_nums}</b>\n"
        if svc_nums:
            for ccode in sorted(svc_nums.keys()):
                cdata = service_countries.get(ccode, {})
                cname = cdata.get("name", countries.get(ccode, {}).get("name", ccode))
                real_code = cdata.get("real_code", ccode)
                flag = flag_emoji(real_code, "🏳️")
                num_count = len(svc_nums.get(ccode, []))
                c_otp_count = otp_counts.get(svc_name, {}).get(ccode, 0)
                nums_preview = ", ".join(svc_nums[ccode][:3])
                if len(svc_nums[ccode]) > 3:
                    nums_preview += f" ... (+{len(svc_nums[ccode]) - 3} more)"
                text += f"  {flag} <code>{cname}</code> {ce('phone','📞')} <b>{num_count}</b>"
                if c_otp_count > 0:
                    text += f" {ce('top','🔝')} <b>{c_otp_count}</b> OTPs"
                text += "\n"
                text += f"   └ <code>{nums_preview}</code>\n"
        else:
            text += f"  {ce('no','❌')} No numbers added\n"
        text += "\n"
    send_message(chat_id, text)


def handle_otp_history(chat_id, uid):
    history = db.get("otp_history", {}).get(str(uid), [])
    if not history:
        send_message(chat_id, f"{ce('warn','⚠️')} <b>No OTP history yet.</b>")
        return
    text = f"{ce('otpkey','🔐')} <b>Your OTP History</b> {ce('fire','🔥')}\n\n"
    for i, h in enumerate(history[-10:], 1):
        svc = h.get("service", "N/A")
        otp = h.get("otp", "N/A")
        num = h.get("number", "N/A")
        text += f"{i}. {svc_emoji(svc, '📱')} <code>{svc}</code> | {ce('otpkey','🔐')} <code>{otp}</code> | {ce('phone','📞')} <code>{num}</code>\n"
    send_message(chat_id, text)

def handle_otp_rewards(chat_id, uid):
    user = db["users"].get(uid, {})
    total_otps = user.get("otp_count", 0)
    rewards_claimed = user.get("otp_rewards_claimed", 0)
    milestone = OTP_REWARD_MILESTONE
    reward_rs = OTP_REWARD_RS
    next_milestone = ((total_otps // milestone) + 1) * milestone
    remaining = next_milestone - total_otps
    unclaimed = (total_otps // milestone) - rewards_claimed
    text = (
        f"{ce('gift','🎁')} <b>OTP Rewards</b>\n\n"
        f"{ce('key','🔑')} Your total OTPs counted: <code>{total_otps}</code>\n"
        f"{ce('moneybag','💰')} Reward {milestone} OTPs → <b>+{reward_rs} Rs</b>\n"
        f"{ce('graph','📊')} <code>{remaining}</code> more OTPs to unlock\n"
        f"{ce('vip','💎')} <code>{rewards_claimed}</code> claimed, <code>{max(0, unclaimed)}</code> remaining"
    )
    send_message(chat_id, text)

# ===== ADMIN HANDLERS =====
def handle_admin_panel(chat_id, uid):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        send_message(chat_id, f"{ce('no','❌')} <b>Access Denied!</b>", back_to_main_markup())
        return
    text = f"{ce('admin','🔐')} <b>ADMIN PANEL</b>\n\nWelcome Boss!"
    send_message(chat_id, text, admin_menu_markup())

def handle_add_service(chat_id, uid):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    db["admin_states"][uid] = {"state": "awaiting_service_name"}
    save_db(db)
    text = f"{ce('plus','➕')} <b>Add Service</b>\n\nSend service name (e.g. Facebook, WhatsApp):"
    rows = [[btn("Cancel", "menu_admin", style="danger", emoji_tag="back")]]
    send_message(chat_id, text, build_inline(rows))

def handle_service_name(chat_id, uid, name):
    db["services"][name] = {"added": datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")}
    db["admin_states"].pop(uid, None)
    save_db(db)
    text = (
        f"{ce('check','✅')} <b>Service Added!</b>\n\n"
        f"{svc_emoji(name, '📱')} <b>Name:</b> <code>{name}</code>\n\n"
        f"{ce('warn','⚠️')} Now add countries with prices from ADMIN PANEL > Add Country."
    )
    send_message(chat_id, text, admin_menu_markup())


def handle_service_price(chat_id, uid, price_text):
    state = db["admin_states"].get(uid, {})
    name = state.get("name", "Unknown")
    try:
        price = float(price_text)
    except:
        send_message(chat_id, f"{ce('no','❌')} Invalid price.", admin_menu_markup())
        db["admin_states"].pop(uid, None)
        save_db(db)
        return
    db["services"][name] = {"price": price, "added": datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")}
    db["admin_states"].pop(uid, None)
    save_db(db)
    text = (
        f"{ce('check','✅')} <b>Service Added!</b>\n\n"
        f"{svc_emoji(name, '📱')} <b>Name:</b> <code>{name}</code>\n"
        f"{ce('money','💵')} <b>Price:</b> <code>{price}</code> $ per OTP"
    )
    send_message(chat_id, text, admin_menu_markup())

def handle_view_services(chat_id, uid):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    services = db.get("services", {})
    if not services:
        send_message(chat_id, f"{ce('warn','⚠️')} No services added yet.", admin_menu_markup())
        return
    text = f"{ce('clipboard','📋')} <b>All Services</b>\n\n"
    for name, data in services.items():
        text += f"{svc_emoji(name, '📱')} <code>{name}</code> — <code>{data.get('price', 0)}</code> $\n"
    send_message(chat_id, text, admin_menu_markup())

def handle_remove_service(chat_id, uid):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    services = db.get("services", {})
    if not services:
        send_message(chat_id, f"{ce('warn','⚠️')} No services to remove.", admin_menu_markup())
        return
    offset = db.get("user_states", {}).get(uid, {}).get("style_offset", 0)
    rows = []
    idx = 0
    for svc_name in services:
        eid = SERVICE_LOGOS.get(svc_name, SERVICE_LOGOS.get("Unknown", ""))
        rows.append([btn(f"Remove {svc_name}", f"rmsvc_{svc_name}", style=cycle_style(idx, offset), custom_emoji_id=eid)])
        idx += 1
    rows.append([btn("Back", "menu_admin", style=cycle_style(idx, offset), emoji_tag="back")])
    send_message(chat_id, f"{ce('no','❌')} <b>Select Service to Remove:</b>", build_inline(rows))

def handle_remove_service_selected(chat_id, uid, svc_name):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    services = db.get("services", {})
    if svc_name not in services:
        send_message(chat_id, f"{ce('warn','⚠️')} Service not found.", admin_menu_markup())
        return
    db["services"].pop(svc_name, None)
    if svc_name in db.get("numbers", {}):
        db["numbers"].pop(svc_name, None)
    save_db(db)
    text = (
        f"{ce('check','✅')} <b>Service Removed!</b>\n\n"
        f"{svc_emoji(svc_name, '📱')} <b>Name:</b> <code>{svc_name}</code>\n"
        f"{ce('warn','⚠️')} All countries and numbers for this service have been deleted."
    )
    send_message(chat_id, text, admin_menu_markup())

def handle_add_country(chat_id, uid):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    services = db.get("services", {})
    if not services:
        send_message(chat_id, f"{ce('warn','⚠️')} Add a service first!", admin_menu_markup())
        return
    db["admin_states"][uid] = {"state": "awaiting_country_service"}
    save_db(db)
    rows = []
    for svc_name in services:
        eid = SERVICE_LOGOS.get(svc_name, SERVICE_LOGOS.get("Unknown", ""))
        rows.append([btn(f"{svc_name}", f"ctrysvc_{svc_name}", style="primary", custom_emoji_id=eid)])
    rows.append([btn("Cancel", "menu_admin", style="danger", emoji_tag="back")])
    send_message(chat_id, f"{ce('plus','➕')} <b>Add Country</b>\n\nSelect a service:", build_inline(rows))

def handle_country_service(chat_id, uid, svc_name):
    db["admin_states"][uid] = {"state": "awaiting_country_code", "service": svc_name}
    save_db(db)
    text = (
        f"{ce('plus','➕')} <b>Add Country to {svc_name}</b>\n\n"
        f"{ce('warn','⚠️')} Send country code or name:\n"
        f"<code>EG</code> or <code>EGYPT</code>\n"
        f"<code>DZ</code> or <code>ALGERIA</code>"
    )
    rows = [[btn("Cancel", "menu_admin", style="danger", emoji_tag="back")]]
    send_message(chat_id, text, build_inline(rows))

def handle_country_code(chat_id, uid, text_input):
    state = db["admin_states"].get(uid, {})
    svc_name = state.get("service", "")
    name_input = text_input.lower().strip()

    # Try 1: Exact match
    code = COUNTRY_NAME_TO_CODE.get(name_input)
    custom_name = None

    # Try 2: If no exact match, find real country name inside the input
    if not code:
        for cname, ccode in COUNTRY_NAME_TO_CODE.items():
            if cname in name_input:
                code = ccode
                # Use the full input as custom name, real country as base
                custom_name = text_input.strip()
                break

    if code and code in COUNTRY_FLAGS:
        real_name = COUNTRY_FLAGS[code]["name"]

        # If user sent just the real country name (e.g. "Togo")
        if custom_name is None:
            custom_name = real_name

        existing = db.get("service_countries", {}).get(svc_name, {}).get(custom_name)

        # If exact same name already exists
        if existing:
            db["admin_states"][uid] = {
                "state": "awaiting_country_custom_name",
                "service": svc_name,
                "country_code": code,
                "country_name": real_name
            }
            save_db(db)
            flag = flag_emoji(code, "🏳️")
            text = (
                f"{ce('warn','⚠️')} <b>{flag} {custom_name}</b> already exists in {svc_name}!\n\n"
                f"{ce('plus','➕')} Send a different custom name (e.g. <code>{real_name} 2</code>, <code>{real_name} VIP</code>)\n"
                f"Or send <code>same</code> to overwrite existing."
            )
            rows = [[btn("Cancel", "menu_admin", style="danger", emoji_tag="back")]]
            send_message(chat_id, text, build_inline(rows))
            return

        # If real country exists but under different custom name, allow it directly
        real_exists = db.get("service_countries", {}).get(svc_name, {}).get(real_name)
        if real_exists and custom_name == real_name:
            # Same real country name exists, ask for custom
            db["admin_states"][uid] = {
                "state": "awaiting_country_custom_name",
                "service": svc_name,
                "country_code": code,
                "country_name": real_name
            }
            save_db(db)
            flag = flag_emoji(code, "🏳️")
            text = (
                f"{ce('warn','⚠️')} <b>{flag} {real_name}</b> already exists in {svc_name}!\n\n"
                f"{ce('plus','➕')} Send a custom name (e.g. <code>{real_name} 2</code>, <code>{real_name} VIP</code>)\n"
                f"Or send <code>same</code> to overwrite existing."
            )
            rows = [[btn("Cancel", "menu_admin", style="danger", emoji_tag="back")]]
            send_message(chat_id, text, build_inline(rows))
            return

        # New country (either real name first time, or custom name like "Togo 2")
        db["countries"][custom_name] = {"name": custom_name, "code": code}
        db.setdefault("service_countries", {}).setdefault(svc_name, {})[custom_name] = {
            "name": custom_name,
            "code": code,
            "real_code": code
        }
        db["admin_states"][uid] = {
            "state": "awaiting_country_price",
            "service": svc_name,
            "country_code": custom_name,
            "country_name": custom_name,
            "real_code": code
        }
        save_db(db)
        flag = flag_emoji(code, "🏳️")
        text = (
            f"{ce('plus','➕')} <b>Add Country to {svc_name}</b>\n\n"
            f"{flag} <b>{custom_name}</b>\n\n"
            f"{ce('warn','⚠️')} Send price per OTP for this country (e.g. 0.00239):"
        )
        rows = [[btn("Cancel", "menu_admin", style="danger", emoji_tag="back")]]
        send_message(chat_id, text, build_inline(rows))
    else:
        text = f"{ce('warn','⚠️')} Country <code>{text_input}</code> not found.\nSend a valid full country name like <code>EGYPT</code> / <code>ALGERIA</code> / <code>IVORY COAST</code> or <code>Togo 2</code>."
        db["admin_states"].pop(uid, None)
        save_db(db)
        send_message(chat_id, text, admin_menu_markup())


def handle_country_custom_name(chat_id, uid, custom_name):
    state = db["admin_states"].get(uid, {})
    svc_name = state.get("service", "")
    code = state.get("country_code", "")
    name = state.get("country_name", "")
    custom_name = custom_name.strip()
    if custom_name.lower() == "same":
        # Overwrite existing
        db["countries"][code] = {"name": name, "code": code}
        db.setdefault("service_countries", {}).setdefault(svc_name, {})[code] = {"name": name, "code": code, "real_code": code}
        db["admin_states"][uid] = {"state": "awaiting_country_price", "service": svc_name, "country_code": code, "country_name": name}
        save_db(db)
        flag = flag_emoji(code, "🏳️")
        text = (
            f"{ce('plus','➕')} <b>Overwrite Country in {svc_name}</b>\n\n"
            f"{flag} <b>{name}</b>\n\n"
            f"{ce('warn','⚠️')} Send price per OTP for this country:"
        )
        rows = [[btn("Cancel", "menu_admin", style="danger", emoji_tag="back")]]
        send_message(chat_id, text, build_inline(rows))
        return
    # Custom name - use it as the key
    custom_key = custom_name
    db["countries"][custom_key] = {"name": custom_name, "code": code}
    db.setdefault("service_countries", {}).setdefault(svc_name, {})[custom_key] = {
        "name": custom_name,
        "code": code,
        "real_code": code,
        "is_custom": True
    }
    db["admin_states"][uid] = {
        "state": "awaiting_country_price",
        "service": svc_name,
        "country_code": custom_key,
        "country_name": custom_name,
        "real_code": code
    }
    save_db(db)
    flag = flag_emoji(code, "🏳️")
    text = (
        f"{ce('plus','➕')} <b>Add Custom Country to {svc_name}</b>\n\n"
        f"{flag} <b>{custom_name}</b> (based on {name})\n\n"
        f"{ce('warn','⚠️')} Send price per OTP for this country:"
    )
    rows = [[btn("Cancel", "menu_admin", style="danger", emoji_tag="back")]]
    send_message(chat_id, text, build_inline(rows))

def handle_country_price(chat_id, uid, price_text):
    state = db["admin_states"].get(uid, {})
    svc_name = state.get("service", "")
    code = state.get("country_code", "")
    name = state.get("country_name", "")
    real_code = state.get("real_code", code)
    try:
        price = float(price_text)
    except:
        send_message(chat_id, f"{ce('no','❌')} Invalid price.", admin_menu_markup())
        db["admin_states"].pop(uid, None)
        save_db(db)
        return
    db.setdefault("service_countries", {}).setdefault(svc_name, {}).setdefault(code, {})["price"] = price
    db["service_countries"][svc_name][code]["price_display"] = price_text.strip()
    db["admin_states"].pop(uid, None)
    save_db(db)
    flag = flag_emoji(real_code, "🏳️")
    text = (
        f"{ce('check','✅')} <b>Country Added with Price!</b>\n\n"
        f"{svc_emoji(svc_name, '📱')} Service: <code>{svc_name}</code>\n"
        f"{flag} <b>{name}</b>\n"
        f"{ce('money','💵')} Price: <code>{price_text.strip()}</code> $ per OTP"
    )
    send_message(chat_id, text, admin_menu_markup())


def handle_view_countries(chat_id, uid):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    countries = db.get("countries", {})
    if not countries:
        send_message(chat_id, f"{ce('warn','⚠️')} No countries added yet.", admin_menu_markup())
        return
    text = f"{ce('clipboard','📋')} <b>All Countries</b>\n\n"
    for code, data in countries.items():
        flag = flag_emoji(code, "🏳️")
        text += f"{flag} <code>{data.get('name', code)}</code> (<code>{code}</code>)\n"
    send_message(chat_id, text, admin_menu_markup())

def handle_remove_country(chat_id, uid):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    services = db.get("services", {})
    if not services:
        send_message(chat_id, f"{ce('warn','⚠️')} No services added yet.", admin_menu_markup())
        return
    rows = []
    for svc_name in services:
        eid = SERVICE_LOGOS.get(svc_name, SERVICE_LOGOS.get("Unknown", ""))
        rows.append([btn(f"{svc_name}", f"rmctrysvc_{svc_name}", style="danger", custom_emoji_id=eid)])
    rows.append([btn("Back", "menu_admin", style="primary", emoji_tag="back")])
    send_message(chat_id, f"{ce('no','❌')} <b>Select Service to Remove Country From:</b>", build_inline(rows))

def handle_remove_country_service(chat_id, uid, svc_name):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    countries = db.get("service_countries", {}).get(svc_name, {})
    if not countries:
        send_message(chat_id, f"{ce('warn','⚠️')} No countries added for {svc_name}.", admin_menu_markup())
        return
    offset = db.get("user_states", {}).get(uid, {}).get("style_offset", 0)
    rows = []
    idx = 0
    for code in countries:
        cdata = countries.get(code, {})
        real_code = cdata.get("real_code", code)
        flag_id = COUNTRY_FLAGS.get(real_code, {}).get("id", "")
        cname = cdata.get("name", db.get("countries", {}).get(code, {}).get("name", code))
        rows.append([btn(cname, f"rmctry_{svc_name}_{code}", style=cycle_style(idx, offset), custom_emoji_id=flag_id)])
        idx += 1
    rows.append([btn("Back", "admin_removecountry", style=cycle_style(idx, offset), emoji_tag="back")])
    send_message(chat_id, f"{ce('no','❌')} <b>Select Country to Remove from {svc_name}:</b>", build_inline(rows))

def handle_remove_country_selected(chat_id, uid, svc_name, ccode):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    if svc_name in db.get("numbers", {}) and ccode in db["numbers"][svc_name]:
        db["numbers"][svc_name].pop(ccode, None)
        if not db["numbers"][svc_name]:
            db["numbers"].pop(svc_name, None)
    if svc_name in db.get("service_countries", {}) and ccode in db["service_countries"][svc_name]:
        db["service_countries"][svc_name].pop(ccode, None)
        if not db["service_countries"][svc_name]:
            db["service_countries"].pop(svc_name, None)
    if ccode in db.get("countries", {}):
        db["countries"].pop(ccode, None)
    save_db(db)
    country_name = COUNTRY_FLAGS.get(ccode, {}).get("name", ccode)
    flag = flag_emoji(ccode, "🏳️")
    send_message(chat_id, f"{ce('check','✅')} <b>Removed {flag} {country_name} from {svc_name}!</b>", admin_menu_markup())

def handle_remove_number(chat_id, uid):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    services = db.get("services", {})
    if not services:
        send_message(chat_id, f"{ce('warn','⚠️')} No services added yet.", admin_menu_markup())
        return
    rows = []
    for svc_name in services:
        eid = SERVICE_LOGOS.get(svc_name, SERVICE_LOGOS.get("Unknown", ""))
        rows.append([btn(f"{svc_name}", f"rmnumsvc_{svc_name}", style="danger", custom_emoji_id=eid)])
    rows.append([btn("Back", "menu_admin", style="primary", emoji_tag="back")])
    send_message(chat_id, f"{ce('no','❌')} <b>Select Service to Remove Number From:</b>", build_inline(rows))

def handle_remove_number_service(chat_id, uid, svc_name):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    countries = db.get("numbers", {}).get(svc_name, {})
    if not countries:
        send_message(chat_id, f"{ce('warn','⚠️')} No countries with numbers for {svc_name}.", admin_menu_markup())
        return
    service_countries = db.get("service_countries", {}).get(svc_name, {})
    offset = db.get("user_states", {}).get(uid, {}).get("style_offset", 0)
    rows = []
    idx = 0
    for code in countries:
        cdata = service_countries.get(code, {})
        real_code = cdata.get("real_code", code)
        flag_id = COUNTRY_FLAGS.get(real_code, {}).get("id", "")
        cname = cdata.get("name", db.get("countries", {}).get(code, {}).get("name", code))
        count = len(db["numbers"][svc_name][code])
        rows.append([btn(f"{cname} ({count})", f"rmnumctry_{svc_name}_{code}", style=cycle_style(idx, offset), custom_emoji_id=flag_id)])
        idx += 1
    rows.append([btn("Back", "admin_removenumber", style=cycle_style(idx, offset), emoji_tag="back")])
    send_message(chat_id, f"{ce('no','❌')} <b>Select Country in {svc_name}:</b>", build_inline(rows))

def handle_remove_number_country(chat_id, uid, svc_name, ccode):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    country = db.get("countries", {}).get(ccode, {}).get("name", ccode)
    flag = flag_emoji(ccode, "🏳️")
    removed_count = 0
    if svc_name in db.get("numbers", {}) and ccode in db["numbers"].get(svc_name, {}):
        removed_count = len(db["numbers"][svc_name][ccode])
        db["numbers"][svc_name][ccode] = []
        save_db(db)
    if removed_count > 0:
        text = (
            f"{ce('check','✅')} <b>All Numbers Removed!</b>\n\n"
            f"{svc_emoji(svc_name, '📱')} Service: <code>{svc_name}</code>\n"
            f"{flag} Country: <code>{country}</code>\n"
            f"{ce('phone','📞')} Removed: <code>{removed_count}</code> numbers\n\n"
            f"Country entry preserved. Use <b>Remove Country</b> to delete the country itself."
        )
    else:
        text = (
            f"{ce('warn','⚠️')} <b>No numbers found!</b>\n\n"
            f"{svc_emoji(svc_name, '📱')} Service: <code>{svc_name}</code>\n"
            f"{flag} Country: <code>{country}</code>\n"
            f"Numbers list was already empty."
        )
    send_message(chat_id, text, admin_menu_markup())

def handle_add_numbers(chat_id, uid):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    db["admin_states"][uid] = {"state": "awaiting_numbers_service"}
    save_db(db)
    services = db.get("services", {})
    if not services:
        send_message(chat_id, f"{ce('warn','⚠️')} Add a service first!", admin_menu_markup())
        db["admin_states"].pop(uid, None)
        save_db(db)
        return
    offset = db.get("user_states", {}).get(uid, {}).get("style_offset", 0)
    rows = []
    svc_items = list(services.items())
    idx = 0
    for i in range(0, len(svc_items), 2):
        row = []
        for j in range(2):
            if i + j < len(svc_items):
                svc_name = svc_items[i + j][0]
                eid = SERVICE_LOGOS.get(svc_name, SERVICE_LOGOS.get("Unknown", ""))
                row.append(btn(f"{svc_name}", f"numsvc_{svc_name}", style=cycle_style(idx, offset), custom_emoji_id=eid))
                idx += 1
        rows.append(row)
    rows.append([btn("Cancel", "menu_admin", style=cycle_style(idx, offset), emoji_tag="back")])
    send_message(chat_id, f"{ce('plus','➕')} <b>Select Service:</b>", build_inline(rows))

def handle_numbers_service(chat_id, uid, svc_name):
    db["admin_states"][uid] = {"state": "awaiting_numbers_country", "service": svc_name}
    save_db(db)
    countries = db.get("service_countries", {}).get(svc_name, {})
    if not countries:
        send_message(chat_id, f"{ce('warn','⚠️')} No countries added for {svc_name}! Add countries first from ADMIN PANEL > Add Country.", admin_menu_markup())
        db["admin_states"].pop(uid, None)
        save_db(db)
        return
    offset = db.get("user_states", {}).get(uid, {}).get("style_offset", 0)
    rows = []
    ctry_items = list(countries.items())
    idx = 0
    for i in range(0, len(ctry_items), 2):
        row = []
        for j in range(2):
            if i + j < len(ctry_items):
                code, cdata = ctry_items[i + j]
                real_code = cdata.get("real_code", code)
                flag_id = COUNTRY_FLAGS.get(real_code, {}).get("id", "")
                display_name = cdata.get("name", code)
                row.append(btn(f"{display_name}", f"numctry_{code}", style=cycle_style(idx, offset), custom_emoji_id=flag_id))
                idx += 1
        rows.append(row)
    rows.append([btn("Cancel", "menu_admin", style=cycle_style(idx, offset), emoji_tag="back")])
    send_message(chat_id, f"{ce('plus','➕')} <b>Select Country for {svc_name}:</b>", build_inline(rows))

def handle_numbers_country(chat_id, uid, ccode):
    state = db["admin_states"].get(uid, {})
    svc_name = state.get("service", "")
    db["admin_states"][uid] = {"state": "awaiting_numbers_list", "service": svc_name, "country": ccode}
    save_db(db)
    country = db.get("countries", {}).get(ccode, {}).get("name", ccode)
    flag = flag_emoji(ccode, "🏳️")
    text = (
        f"{ce('plus','➕')} <b>Add Numbers</b>\n"
        f"{svc_emoji(svc_name, '📱')} Service: <code>{svc_name}</code>\n"
        f"{flag} Country: <code>{country}</code>\n\n"
        f"{ce('warn','⚠️')} Send numbers separated by commas or new lines, OR upload a .txt file with numbers:"
    )
    rows = [[btn("Cancel", "menu_admin", style="danger", emoji_tag="back")]]
    send_message(chat_id, text, build_inline(rows))

def handle_numbers_list(chat_id, uid, numbers_text):
    state = db["admin_states"].get(uid, {})
    svc_name = state.get("service", "")
    ccode = state.get("country", "")
    numbers = [n.strip() for n in re.split(r"[,\n]", numbers_text) if n.strip()]
    if svc_name not in db["numbers"]:
        db["numbers"][svc_name] = {}
    if ccode not in db["numbers"][svc_name]:
        db["numbers"][svc_name][ccode] = []
    old_count = len(db["numbers"][svc_name][ccode])
    db["numbers"][svc_name][ccode] = numbers  # OVERWRITE: old removed, new added
    db["admin_states"].pop(uid, None)
    save_db(db)
    country = db.get("countries", {}).get(ccode, {}).get("name", ccode)
    flag = flag_emoji(ccode, "🏳️")
    text = (
        f"{ce('check','✅')} <b>Numbers Overwritten!</b>\n\n"
        f"{svc_emoji(svc_name, '📱')} Service: <code>{svc_name}</code>\n"
        f"{flag} Country: <code>{country}</code>\n"
        f"{ce('trash','🗑️')} Old Removed: <code>{old_count}</code>\n"
        f"{ce('phone','📞')} New Added: <code>{len(numbers)}</code>\n"
        f"{ce('graph','📊')} Total Now: <code>{len(numbers)}</code>"
    )
    send_message(chat_id, text, admin_menu_markup())

def handle_stats(chat_id, uid):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    total_users = len(db.get("users", {}))
    total_services = len(db.get("services", {}))
    total_countries = len(db.get("countries", {}))
    total_otps = db.get("stats", {}).get("total_otps", 0)
    total_withdrawals = len([w for w in db.get("withdrawals", []) if w.get("status") == "pending"])
    text = (
        f"{ce('stats','📊')} <b>Bot Statistics</b>\n\n"
        f"{ce('user','👤')} Total Users: <code>{total_users}</code>\n"
        f"{ce('phone','📞')} Total Services: <code>{total_services}</code>\n"
        f"{ce('globe','🌍')} Total Countries: <code>{total_countries}</code>\n"
        f"{ce('msg','💬')} Total OTPs Sent: <code>{total_otps}</code>\n"
        f"{ce('withdraw','💵')} Pending Withdrawals: <code>{total_withdrawals}</code>"
    )
    send_message(chat_id, text, admin_menu_markup())

def handle_broadcast(chat_id, uid):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    db["admin_states"][uid] = {"state": "awaiting_broadcast"}
    save_db(db)
    text = (
        f"{ce('broadcast','📢')} <b>Broadcast</b>\n\n"
        f"{ce('warn','⚠️')} Send the message to broadcast to all users:"
    )
    rows = [[btn("Cancel", "menu_admin", style="danger", emoji_tag="back")]]
    send_message(chat_id, text, build_inline(rows))

def handle_broadcast_message(chat_id, uid, message_text, message_id=None):
    users = db.get("users", {})
    count = 0
    broadcast_services = detect_services_in_text(message_text)
    broadcast_service = broadcast_services[0] if broadcast_services else None
    broadcast_countries = detect_countries_in_text(message_text)
    broadcast_country = broadcast_countries[0][0] if broadcast_countries else None
    enhanced_text = enhance_broadcast_with_emojis(message_text)
    bc_markup = None
    if broadcast_service and broadcast_country:
        getnum_callback = f"bc_getnum_{broadcast_service}_{broadcast_country}"
        bc_markup = build_inline([
            [btn("👉 Get Number", getnum_callback, style="success", emoji_tag="getnum")]
        ])
    for uid_str, udata in users.items():
        try:
            send_message(int(uid_str), enhanced_text, bc_markup)
            count += 1
            time.sleep(0.1)
        except:
            pass
    db["admin_states"].pop(uid, None)
    save_db(db)
    text = f"{ce('check','✅')} <b>Broadcast sent to {count} users!</b>"
    send_message(chat_id, text, admin_menu_markup())
def handle_ban_user(chat_id, uid):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    db["admin_states"][uid] = {"state": "awaiting_ban_uid"}
    save_db(db)
    text = f"{ce('ban','🚫')} <b>Ban User</b>\n\nSend the User ID to ban:"
    rows = [[btn("Cancel", "menu_admin", style="danger", emoji_tag="back")]]
    send_message(chat_id, text, build_inline(rows))

def handle_unban_user(chat_id, uid):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    banned = db.get("banned_users", [])
    if not banned:
        send_message(chat_id, f"{ce('check','✅')} No banned users.", admin_menu_markup())
        return
    offset = db.get("user_states", {}).get(uid, {}).get("style_offset", 0)
    rows = []
    idx = 0
    for b in banned:
        u = db.get("users", {}).get(str(b), {})
        name = u.get("first_name", b)
        rows.append([btn(f"Unban {name} ({b})", f"unban_{b}", style=cycle_style(idx, offset), emoji_tag="ntick")])
        idx += 1
    rows.append([btn("Back", "menu_admin", style=cycle_style(idx, offset), emoji_tag="back")])
    send_message(chat_id, f"{ce('no','🚫')} <b>Banned Users:</b>", build_inline(rows))

def handle_manage_withdrawals(chat_id, uid):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    withdrawals = db.get("withdrawals", [])
    pending = [w for w in withdrawals if w.get("status") == "pending"]
    if not pending:
        send_message(chat_id, f"{ce('check','✅')} No pending withdrawals.", admin_menu_markup())
        return
    text = f"{ce('money','💳')} <b>Pending Withdrawals</b>\n\n"
    for i, w in enumerate(pending[:5], 1):
        text += (
            f"{i}. @{w.get('username', 'N/A')} — <code>{fmt_num(w.get('amount', 0))}</code> $\n"
            f"   Method: <code>{w.get('method', 'N/A')}</code>\n\n"
        )
    send_message(chat_id, text, admin_menu_markup())

def handle_check_balance(chat_id, uid):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    db["admin_states"][uid] = {"state": "awaiting_checkbalance_uid"}
    save_db(db)
    text = f"{ce('moneybag','💰')} <b>Check Balance</b>\n\nSend the User ID to check balance:"
    rows = [[btn("Cancel", "menu_admin", style="danger", emoji_tag="back")]]
    send_message(chat_id, text, build_inline(rows))

def handle_remove_balance(chat_id, uid):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    db["admin_states"][uid] = {"state": "awaiting_removebalance_uid"}
    save_db(db)
    text = f"{ce('no','🚫')} <b>Remove Balance</b>\n\nSend the User ID:"
    rows = [[btn("Cancel", "menu_admin", style="danger", emoji_tag="back")]]
    send_message(chat_id, text, build_inline(rows))


def handle_checkbalance_uid(chat_id, uid, target_uid):
    target = str(target_uid).strip()
    user = db["users"].get(target)
    if not user:
        send_message(chat_id, f"{ce('warn','⚠️')} User <code>{target}</code> not found.", admin_menu_markup())
        db["admin_states"].pop(uid, None)
        save_db(db)
        return
    bal = user.get("balance", 0)
    total = user.get("total_earned", 0)
    name = user.get("first_name", "N/A")
    uname = user.get("username", "N/A")
    text = (
        f"{ce('moneybag','💰')} <b>User Balance</b>\n\n"
        f"{ce('user','👤')} Name: <code>{html.escape(name)}</code>\n"
        f"{ce('user','👤')} Username: @{html.escape(uname)}\n"
        f"{ce('money','💵')} Balance: <code>{fmt_num(bal)}</code> $\n"
        f"{ce('moneybag','💰')} Total Earned: <code>{fmt_num(total)}</code> $"
    )
    send_message(chat_id, text, admin_menu_markup())
    db["admin_states"].pop(uid, None)
    save_db(db)

def handle_removebalance_uid(chat_id, uid, target_uid):
    target = str(target_uid).strip()
    if target not in db.get("users", {}):
        send_message(chat_id, f"{ce('warn','⚠️')} User <code>{target}</code> not found.", admin_menu_markup())
        db["admin_states"].pop(uid, None)
        save_db(db)
        return
    db["admin_states"][uid] = {"state": "awaiting_removebalance_amount", "target_uid": target}
    save_db(db)
    user = db["users"][target]
    text = (
        f"{ce('no','🚫')} <b>Remove Balance</b>\n\n"
        f"{ce('user','👤')} User: <code>{html.escape(user.get('first_name', 'N/A'))}</code>\n"
        f"{ce('moneybag','💰')} Current Balance: <code>{fmt_num(user.get('balance', 0))}</code> $\n\n"
        f"{ce('warn','⚠️')} Send amount to remove:"
    )
    rows = [[btn("Cancel", "menu_admin", style="danger", emoji_tag="back")]]
    send_message(chat_id, text, build_inline(rows))

def handle_removebalance_amount(chat_id, uid, amount_text):
    state = db["admin_states"].get(uid, {})
    target = state.get("target_uid")
    try:
        amount = float(amount_text)
    except:
        send_message(chat_id, f"{ce('no','❌')} Invalid amount.", admin_menu_markup())
        db["admin_states"].pop(uid, None)
        save_db(db)
        return
    if target and target in db.get("users", {}):
        old_bal = db["users"][target].get("balance", 0)
        new_bal = max(0, old_bal - amount)
        db["users"][target]["balance"] = new_bal
        save_db(db)
        send_message(chat_id, f"{ce('check','✅')} Removed <code>{fmt_num(amount)}</code> $ from user <code>{target}</code>.\nOld: <code>{fmt_num(old_bal)}</code> $\nNew: <code>{fmt_num(new_bal)}</code> $", admin_menu_markup())
    else:
        send_message(chat_id, f"{ce('warn','⚠️')} User not found.", admin_menu_markup())
    db["admin_states"].pop(uid, None)
    save_db(db)
def handle_withdrawal_action(chat_id, uid, action, idx):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    withdrawals = db.get("withdrawals", [])
    if idx < 0 or idx >= len(withdrawals):
        return
    w = withdrawals[idx]
    w["status"] = action
    save_db(db)
    user_id = w.get("user_id")
    amount = w.get("amount", 0)
    binance_id = w.get("binance_id", "N/A")
    if action == "approved":
        user_text = (
            f"{ce('check','✅')} <b>Payment Received!</b>\n\n"
            f"{ce('money','💵')} Amount: <code>{fmt_num(amount)}</code> $\n"
            f"{ce('link','🔗')} Binance ID: <code>{binance_id}</code>\n"
            f"{ce('time','⏰')} Status: <code>Payment Sent ✅</code>\n\n"
            f"{ce('rocket','⚡')} Thank you for using our bot!"
        )
        admin_text = (
            f"{ce('check','✅')} <b>Withdrawal #{idx} Approved & Paid!</b>\n"
            f"{ce('money','💵')} Amount: <code>{fmt_num(amount)}</code> $\n"
            f"{ce('user','👤')} User: @{w.get('username', 'N/A')}"
        )
    else:
        if user_id and user_id in db["users"]:
            db["users"][user_id]["balance"] += amount
        user_text = (
            f"{ce('no','❌')} <b>Withdrawal Rejected!</b>\n\n"
            f"{ce('money','💵')} Amount: <code>{fmt_num(amount)}</code> $ refunded.\n"
            f"{ce('warn','⚠️')} Contact admin for details."
        )
        admin_text = f"{ce('no','❌')} Withdrawal #{idx} rejected."
    save_db(db)
    if user_id:
        send_message(int(user_id), user_text)
    send_message(chat_id, admin_text, admin_menu_markup())

def handle_remove_all_balances(chat_id, uid):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    users = db.get("users", {})
    count = 0
    for u in users:
        if users[u].get("balance", 0) > 0:
            users[u]["balance"] = 0.0
            count += 1
    save_db(db)
    text = (
        f"{ce('check','✅')} <b>All Balances Reset!</b>\n\n"
        f"{ce('user','👤')} Users affected: <code>{count}</code>\n"
        f"{ce('moneybag','💰')} All balances set to <code>0.00</code> $"
    )
    send_message(chat_id, text, admin_menu_markup())

# ===== NEW: GROUP MANAGEMENT HANDLERS =====


def handle_add_admin(chat_id, uid):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    db["admin_states"][uid] = {"state": "awaiting_admin_id"}
    save_db(db)
    text = f"{ce('ntick','🔐')} <b>Add Admin</b>\n\nSend the User ID of the new admin:"
    rows = [[btn("Cancel", "menu_admin", style="danger", emoji_tag="back")]]
    send_message(chat_id, text, build_inline(rows))

def handle_view_admins(chat_id, uid):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    admins = [str(a) for a in ADMIN_IDS]
    text = f"{ce('admin','🔐')} <b>Admin List</b>\n\n"
    for i, a in enumerate(admins, 1):
        u = db.get("users", {}).get(a, {})
        name = u.get("first_name", "Unknown")
        uname = u.get("username", "N/A")
        text += f"{i}. <code>{a}</code> — <code>{name}</code> (@{uname})\n"
    send_message(chat_id, text, admin_menu_markup())



def handle_remove_admin(chat_id, uid):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    admins = [str(a) for a in ADMIN_IDS]
    if len(admins) <= 1:
        send_message(chat_id, f"{ce('warn','⚠️')} <b>Cannot remove!</b>\n\nAt least one admin must remain.", admin_menu_markup())
        return
    rows = []
    for a in admins:
        if str(a) != str(uid):
            u = db.get("users", {}).get(str(a), {})
            name = u.get("first_name", "Unknown")
            rows.append([btn(f"Remove {name} ({a})", f"rmadmin_{a}", style="danger", emoji_tag="no")])
    rows.append([btn("Back", "menu_admin", style="primary", emoji_tag="back")])
    send_message(chat_id, f"{ce('no','🚫')} <b>Select Admin to Remove:</b>", build_inline(rows))

def handle_remove_admin_selected(chat_id, uid, target):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    target = str(target)
    if target == str(uid):
        send_message(chat_id, f"{ce('warn','⚠️')} You cannot remove yourself!", admin_menu_markup())
        return
    if int(target) in ADMIN_IDS:
        ADMIN_IDS.remove(int(target))
        db["admins"] = [a for a in db.get("admins", []) if str(a) != target]
        save_db(db)
        send_message(chat_id, f"{ce('check','✅')} Admin <code>{target}</code> removed successfully!", admin_menu_markup())
    else:
        send_message(chat_id, f"{ce('warn','⚠️')} Admin not found.", admin_menu_markup())

# ===== IVASMS MANAGEMENT =====

def handle_add_ivasms(chat_id, uid):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    db["admin_states"][uid] = {"state": "awaiting_ivasms_name"}
    save_db(db)
    text = (
        f"{ce('plus','➕')} <b>Add IvaSMS</b>\n\n"
        f"Send a name for this IvaSMS config (e.g. IvaSMS 1, IvaSMS 2):"
    )
    rows = [[btn("Cancel", "menu_admin", style="danger", emoji_tag="back")]]
    send_message(chat_id, text, build_inline(rows))

def handle_ivasms_name(chat_id, uid, name):
    db["admin_states"][uid] = {"state": "awaiting_ivasms_token", "ivasms_name": name.strip()}
    save_db(db)
    text = (
        f"{ce('plus','➕')} <b>IvaSMS Name: {html.escape(name.strip())}</b>\n\n"
        f"{ce('warn','⚠️')} Now send the WebSocket token (full token string):"
    )
    rows = [[btn("Cancel", "menu_admin", style="danger", emoji_tag="back")]]
    send_message(chat_id, text, build_inline(rows))

def handle_ivasms_token(chat_id, uid, token):
    state = db["admin_states"].get(uid, {})
    name = state.get("ivasms_name", "Unknown")
    db["admin_states"][uid] = {"state": "awaiting_ivasms_user", "ivasms_name": name, "ivasms_token": token.strip()}
    save_db(db)
    text = (
        f"{ce('plus','➕')} <b>IvaSMS: {html.escape(name)}</b>\n\n"
        f"{ce('warn','⚠️')} Now send the User ID for this IvaSMS:"
    )
    rows = [[btn("Cancel", "menu_admin", style="danger", emoji_tag="back")]]
    send_message(chat_id, text, build_inline(rows))

def handle_ivasms_user(chat_id, uid, user_id_text):
    state = db["admin_states"].get(uid, {})
    name = state.get("ivasms_name", "Unknown")
    token = state.get("ivasms_token", "")
    user_id = user_id_text.strip()
    configs = db.get("ivasms_configs", [])
    configs.append({
        "name": name,
        "token": token,
        "user": user_id,
        "status": "inactive",
        "added_at": datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
    })
    db["ivasms_configs"] = configs
    db["admin_states"].pop(uid, None)
    save_db(db)
    text = (
        f"{ce('check','✅')} <b>IvaSMS Added!</b>\n\n"
        f"{ce('hacker','💻')} Name: <code>{html.escape(name)}</code>\n"
        f"{ce('link','🔗')} Token: <code>{token[:20]}...</code>\n"
        f"{ce('user','👤')} User ID: <code>{user_id}</code>\n\n"
        f"Go to <b>My IvaSMS</b> to connect and check logs."
    )
    send_message(chat_id, text, admin_menu_markup())

def handle_my_ivasms(chat_id, uid):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    configs = db.get("ivasms_configs", [])
    if not configs:
        send_message(chat_id, f"{ce('warn','⚠️')} No IvaSMS configs added yet.", admin_menu_markup())
        return
    text = f"{ce('clipboard','📋')} <b>My IvaSMS Configs</b>\n\n"
    rows = []
    for i, cfg in enumerate(configs):
        status_emoji = "🟢" if cfg.get("status") == "active" else "🔴"
        name = cfg.get("name", f"Config {i+1}")
        token_preview = cfg.get("token", "")[:15] + "..."
        text += f"{status_emoji} <b>{html.escape(name)}</b>\nToken: <code>{token_preview}</code>\nStatus: <code>{cfg.get('status', 'inactive')}</code>\n\n"
        rows.append([btn(f"Check {name}", f"checkivasms_{i}", style="primary", emoji_tag="stats")])
    rows.append([btn("Back", "menu_admin", style="primary", emoji_tag="back")])
    send_message(chat_id, text, build_inline(rows))

async def _test_ivasms_connection(token, user_id):
    """Test IvaSMS WebSocket connection"""
    if websockets is None:
        return False, "websockets library not installed"
    uri = f"wss://ivasms.qzz.io:2087/socket.io/?token={token}&user={user_id}&EIO=4&transport=websocket"
    ssl_context = ssl._create_unverified_context()
    try:
        async with websockets.connect(uri, ssl=ssl_context, timeout=10) as websocket:
            initial = await asyncio.wait_for(websocket.recv(), timeout=5)
            if initial.startswith("0{"):
                return True, f"Connected! Server response: {initial[:50]}..."
            return True, f"Connected! Response: {initial[:50]}"
    except Exception as e:
        return False, f"Connection failed: {str(e)}"

def handle_check_ivasms(chat_id, uid, idx):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    configs = db.get("ivasms_configs", [])
    idx = int(idx)
    if idx < 0 or idx >= len(configs):
        send_message(chat_id, f"{ce('warn','⚠️')} Invalid config.", admin_menu_markup())
        return
    cfg = configs[idx]
    name = cfg.get("name", f"Config {idx+1}")
    token = cfg.get("token", "")
    user_id = cfg.get("user", "")
    send_message(chat_id, f"{ce('time','⏳')} <b>Testing {html.escape(name)}...</b>\nPlease wait...")
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        success, msg = loop.run_until_complete(_test_ivasms_connection(token, user_id))
        loop.close()
        cfg["status"] = "active" if success else "error"
        cfg["last_check"] = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
        cfg["last_log"] = msg
        save_db(db)
        status_emoji = ce("check", "✅") if success else ce("no", "❌")
        text = (
            f"{status_emoji} <b>IvaSMS Check: {html.escape(name)}</b>\n\n"
            f"{ce('stats','📊')} Status: <code>{cfg['status']}</code>\n"
            f"{ce('time','⏰')} Last Check: <code>{cfg['last_check']}</code>\n"
            f"{ce('msg','💬')} Log: <code>{html.escape(msg)}</code>"
        )
    except Exception as e:
        cfg["status"] = "error"
        cfg["last_log"] = str(e)
        save_db(db)
        text = (
            f"{ce('no','❌')} <b>IvaSMS Check Failed: {html.escape(name)}</b>\n\n"
            f"Error: <code>{html.escape(str(e))}</code>"
        )
    rows = [[btn("Back to My IvaSMS", "admin_myivasms", style="primary", emoji_tag="back")]]
    send_message(chat_id, text, build_inline(rows))
def handle_add_group(chat_id, uid):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    db["admin_states"][uid] = {"state": "awaiting_group_name"}
    save_db(db)
    text = f"{ce('plus','➕')} <b>Add Group</b>\n\nSend the name for this group:"
    rows = [[btn("Cancel", "menu_admin", style="danger", emoji_tag="back")]]
    send_message(chat_id, text, build_inline(rows))

def handle_group_name(chat_id, uid, name):
    db["admin_states"][uid] = {"state": "awaiting_group_id", "group_name": name}
    save_db(db)
    text = (
        f"{ce('plus','➕')} <b>Group Name: {name}</b>\n\n"
        f"{ce('warn','⚠️')} Now send the Group ID (e.g., -1001234567890):\n"
        f"Bot must be admin in that group!"
    )
    rows = [[btn("Cancel", "menu_admin", style="danger", emoji_tag="back")]]
    send_message(chat_id, text, build_inline(rows))

def handle_group_id(chat_id, uid, gid_text):
    state = db["admin_states"].get(uid, {})
    name = state.get("group_name", "Unknown")
    try:
        gid = int(gid_text.strip())
    except:
        send_message(chat_id, f"{ce('no','❌')} Invalid Group ID. Must be a number.", admin_menu_markup())
        db["admin_states"].pop(uid, None)
        save_db(db)
        return
    groups = db.get("forward_groups", [])
    if any(g.get("group_id") == gid for g in groups):
        send_message(chat_id, f"{ce('warn','⚠️')} This group is already added.", admin_menu_markup())
        db["admin_states"].pop(uid, None)
        save_db(db)
        return
    groups.append({"name": name, "group_id": gid})
    db["forward_groups"] = groups
    db["admin_states"].pop(uid, None)
    save_db(db)
    text = (
        f"{ce('check','✅')} <b>Group Added!</b>\n\n"
        f"{ce('broadcast','📢')} Name: <code>{name}</code>\n"
        f"{ce('link','🔗')} Group ID: <code>{gid}</code>\n\n"
        f"{ce('rocket','⚡')} OTPs will now forward to this group too!"
    )
    send_message(chat_id, text, admin_menu_markup())

def handle_view_groups(chat_id, uid):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    groups = db.get("forward_groups", [])
    if not groups:
        send_message(chat_id, f"{ce('warn','⚠️')} No groups added yet.", admin_menu_markup())
        return
    text = f"{ce('clipboard','📋')} <b>Forward Groups</b>\n\n"
    for i, g in enumerate(groups, 1):
        text += f"{i}. {ce('broadcast','📢')} <code>{g.get('name', 'N/A')}</code> — <code>{g.get('group_id', 'N/A')}</code>\n"
    send_message(chat_id, text, admin_menu_markup())

def handle_remove_group(chat_id, uid):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    groups = db.get("forward_groups", [])
    if not groups:
        send_message(chat_id, f"{ce('warn','⚠️')} No groups to remove.", admin_menu_markup())
        return
    rows = []
    for i, g in enumerate(groups):
        rows.append([btn(f"Remove {g.get('name', 'Group')}", f"rmgroup_{i}", style="danger", emoji_tag="no")])
    rows.append([btn("Back", "menu_admin", style="primary", emoji_tag="back")])
    send_message(chat_id, f"{ce('no','❌')} <b>Select Group to Remove:</b>", build_inline(rows))

def handle_remove_group_selected(chat_id, uid, idx):
    if str(uid) not in [str(a) for a in ADMIN_IDS]:
        return
    groups = db.get("forward_groups", [])
    idx = int(idx)
    if idx < 0 or idx >= len(groups):
        send_message(chat_id, f"{ce('warn','⚠️')} Invalid group.", admin_menu_markup())
        return
    removed = groups.pop(idx)
    db["forward_groups"] = groups
    save_db(db)
    text = (
        f"{ce('check','✅')} <b>Group Removed!</b>\n\n"
        f"{ce('broadcast','📢')} Name: <code>{removed.get('name', 'N/A')}</code>\n"
        f"{ce('link','🔗')} Group ID: <code>{removed.get('group_id', 'N/A')}</code>"
    )
    send_message(chat_id, text, admin_menu_markup())

# ===== GROUP FORWARDING (from Script 1) =====

def send_to_groups(entry, forced_service=None, price=None):
    """Forward OTP entry to all configured groups with block quote style"""
    service = forced_service or entry[0]
    num = entry[1]
    msg = entry[2]
    groups = db.get("forward_groups", [])
    if not groups:
        return
    country_name, flag, iso = get_country_info(num)
    if not iso:
        iso = "XX"
    if not country_name or country_name == "Unknown":
        country_name = iso
    masked = mask_number(num)
    if not masked:
        return
    otp = extract_otp(msg)

    # Determine reward price
    if price is not None:
        reward = price
    else:
        reward = db.get("service_countries", {}).get(service, {}).get(iso, {}).get("price", 0)

    svc_logo = svc_emoji(service, "📱")
    crown = ce("crown", "👑")
    moneybag = ce("moneybag", "💰")

    # Block quote style message
    text = (
        f"<blockquote>{crown} <b>Syed OTP</b>\n"
        f"{flag} <code>{masked}</code>\n"
        f"{svc_logo} <b>{html.escape(str(service))}</b>\n"
        f"{moneybag} <b>Reward: ${fmt_num(reward)}</b></blockquote>"
    )

    # Case-insensitive service logo lookup for button
    service_logo_id = ""
    for k, v in SERVICE_LOGOS.items():
        if k.lower() == str(service).lower():
            service_logo_id = v
            break
    if not service_logo_id:
        service_logo_id = SERVICE_LOGOS.get("Unknown", CE.get("otpkey", ""))

    row1 = [btn(f"{otp}", copy_text=otp, style="success", custom_emoji_id=service_logo_id)]
    row2 = [
        btn("𝗖𝗛𝗔𝗡𝗡𝗘𝗟", url="https://t.me/syedtechteam", style="danger", emoji_tag="channel"),
        btn("𝗡𝗨𝗠𝗕𝗘𝗥", url=PANEL_LINK, style="primary", emoji_tag="money")
    ]
    markup = build_inline([row1, row2])

    for grp in groups:
        gid = grp.get("group_id")
        if not gid:
            continue
        try:
            payload = {
                "chat_id": gid,
                "text": text,
                "parse_mode": "HTML",
                "reply_markup": markup,
                "disable_web_page_preview": True
            }
            api("sendMessage", payload)
            print(f"Sent OTP for {num} - {service} to group {gid}")
        except Exception as e:
            print(f"Failed to send to group {gid}: {e}")

def otp_forward_poller():
    """Poll APIs for group forwarding (Script 1's fetchers)"""
    try:
        railway_entries = []
        railway_entries.extend(fetch_api_main())
        for url in API_URLS_NEW:
            railway_entries.extend(fetch_api_railway(url))
        other_entries = []
        other_entries.extend(fetch_api_original())
        other_entries.extend(fetch_msi_panel())
        all_entries = railway_entries + other_entries
        for item in all_entries:
            uid = f"{item[0]}_{item[1]}_{item[3]}"
            with _seen_otps_lock:
                _seen_otps.add(uid)
        print(f"Group forwarder initialized with {len(_seen_otps)} existing OTPs.")
    except Exception as e:
        print(f"Initial group forwarder fetch failed: {e}")
    while True:
        try:
            railway_entries = []
            railway_entries.extend(fetch_api_main())
            for url in API_URLS_NEW:
                railway_entries.extend(fetch_api_railway(url))
            other_entries = []
            other_entries.extend(fetch_api_original())
            other_entries.extend(fetch_msi_panel())
            new_count = 0
            # Process railway entries with fixed $0.080 price
            for item in reversed(railway_entries):
                uid = f"{item[0]}_{item[1]}_{item[3]}"
                with _seen_otps_lock:
                    if uid not in _seen_otps:
                        _seen_otps.add(uid)
                        assignments = db.get("number_assignments", {})
                        matched_num, matched_data = None, None
                        if assignments:
                            variants = [item[1], item[1].lstrip('+'), re.sub(r"^\+?\d{1,3}", "", item[1])]
                            for variant in variants:
                                matched_num, matched_data = match_assigned_number(variant, assignments)
                                if matched_num and matched_data:
                                    break
                        if matched_num and matched_data:
                            _notify_assigned_user(matched_num, matched_data, item[2], "GROUP_FWD")
                            send_to_groups(item, forced_service=matched_data["service"], price=0.80)
                        else:
                            send_to_groups(item, price=0.80)
                        new_count += 1
            # Process other entries with bot-configured price
            for item in reversed(other_entries):
                uid = f"{item[0]}_{item[1]}_{item[3]}"
                with _seen_otps_lock:
                    if uid not in _seen_otps:
                        _seen_otps.add(uid)
                        assignments = db.get("number_assignments", {})
                        matched_num, matched_data = None, None
                        if assignments:
                            variants = [item[1], item[1].lstrip('+'), re.sub(r"^\+?\d{1,3}", "", item[1])]
                            for variant in variants:
                                matched_num, matched_data = match_assigned_number(variant, assignments)
                                if matched_num and matched_data:
                                    break
                        if matched_num and matched_data:
                            _notify_assigned_user(matched_num, matched_data, item[2], "GROUP_FWD")
                            send_to_groups(item, forced_service=matched_data["service"])
                        else:
                            send_to_groups(item)
                        new_count += 1
            if new_count > 0:
                print(f"[DEBUG] Sent {new_count} new OTPs to groups this cycle.")
            with _seen_otps_lock:
                if len(_seen_otps) > 10000:
                    _seen_otps.clear()
        except Exception as e:
            print(f"Group forward poller error: {e}")
        time.sleep(POLL_INTERVAL)


# ===== IVASMS WEBSOCKET SYSTEM =====
async def send_ping(websocket, ping_interval, ping_msg="3"):
    while True:
        await asyncio.sleep(ping_interval / 1000)
        try:
            await websocket.send(ping_msg)
        except Exception as e:
            print(f"[{datetime.now(ZoneInfo('Asia/Kolkata'))}] Ping failed: {e}")
            break

async def ivasms():
    uri = "wss://ivasms.qzz.io:2087/socket.io/?token=eyJpdiI6IlIzRzJFemVkQk9nYmVxVXFnM3BSY1E9PSIsInZhbHVlIjoiNHY2cUxwZ0ZLN0xDZkRXQ24zbGovYUNsTU5sM1RrZnRWWnNPUlU5UCtZNVhlc005YmJEZ2VOTzhMcXJVQTZyVDlCYjU2KzRxUnErRkVBVjJpdmtWQS9MZnB2OEdMS1pqM1hPYzFjY2JYR0hQZHVFVHRTK1Jpdk15OFR1SDZUTnQ5aVhYdWk1RTVMMUtNL09xSm1RL1V0M0xXWlAwOXpJTzVGbElyRVV4d2JaaGRyNWVqOUJkOVFkZUJtU0NLbUNjTGJRMnhkQndVM0ZkRkpQekJWSmo0dXdoeTB1VG82aXM4OU1zTGdvY0M4Y0ZURDN3MUwyNGwybzIwOWZQTFp4dXM0cHlkRjAxZXhldmxxa3JKcHBjTGIrK084Zng1V0UwSnlPdXZkMUtvQjFib2VNWTVLcERVV2tlZVNuMUxGb2JBY3B3RHRSczJoMEk5WlZJR1hCSW0xUkwxK1FPZjdHRTJnZ1hoYTFqaWNhMTkwYzRLVkpKeUh2dFdDT2xaRWl2dmxtTnlsdHZPQ0Q1eUloQ1hubmJhY2lQWDdLakxYaXVNSERVeGdOcjZ4K21xMlhmT1RISmJPekZzVTZyMEhycUdzRWlCc2VrK2psem1wWHlRSDFzNmQ4cVd6TlJra3hERUpGN2pLWTRmOTdDWnM5bmFEUXZtbzFTTk8vL0gyZVJDSDBaeEhxUWNVUDA2RWFpdU5zeFNRPT0iLCJtYWMiOiIzM2EwOGVlOTFiNTdmODg3YWQ4ZGE0YjY5NjAyNWI3NjAyZDc0MzgzMzZjNzA0Y2QwZmY4NjJkZmZkNDU4Y2MyIiwidGFnIjoiIn0%3D&user=2066ec6ed4fa33468c75e1782a4a0970&EIO=4&transport=websocket"
    ssl_context = ssl._create_unverified_context()
    while True:
        try:
            async with websockets.connect(uri, ssl=ssl_context) as websocket:
                print(f"[{datetime.now(ZoneInfo('Asia/Kolkata'))}] Connected to Ivasms WebSocket.")
                initial_message = await websocket.recv()
                ping_interval = 25000
                try:
                    if initial_message.startswith("0{") and initial_message.endswith("}"):
                        data = json.loads(initial_message[1:])
                        ping_interval = data.get("pingInterval", 25000)
                except Exception:
                    pass
                await websocket.send("40/livesms,")
                ping_task = asyncio.create_task(send_ping(websocket, ping_interval, "3"))
                while True:
                    message = await websocket.recv()
                    if message.startswith("42/livesms,"):
                        try:
                            json_str = message[message.find("["):]
                            data = json.loads(json_str)
                            if isinstance(data, list) and len(data) > 1 and isinstance(data[1], dict):
                                sms = data[1]
                                ws_sender = str(sms.get("sender", sms.get("from", sms.get("cli", sms.get("service", sms.get("app", "")))))).strip()
                                if not ws_sender:
                                    ws_sender = str(sms.get("source", "")).strip()
                                msg_text = str(sms.get("message", ""))
                                detected_svc = detect_service(msg_text)
                                if detected_svc and detected_svc != "SMS":
                                    service = detected_svc
                                elif ws_sender and str(ws_sender).lower() not in ("", "sms", "unknown", "null"):
                                    service = ws_sender
                                else:
                                    service = detected_svc if detected_svc else "SMS"
                                num = str(sms.get("recipient", ""))
                                msg = str(sms.get("message", ""))
                                dt = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
                                process_ivasms_entry(service, num, msg, dt)
                        except Exception as e:
                            print(f"Error parsing WebSocket SMS: {e}")
        except Exception as e:
            print(f"[{datetime.now(ZoneInfo('Asia/Kolkata'))}] IvaSMS Connection error: {e}. Retrying in 5s...")
            await asyncio.sleep(5)

async def ivasms2():
    uri = "wss://ivasms.qzz.io:2087/socket.io/?token=eyJpdiI6IjA4NEN3SFdjdmtsdUp2cDFJNkllZ2c9PSIsInZhbHVlIjoiTG14OVR5RU9oSk5kVTZBa3Nkb2h0YjNuZGQwVE04ZGZIWmFSOUtmalBnL3YreGl6clJDaXB2WTdSRDUvbStaTTNVdFdFTTVTYTdON0xKTzZlUVEvRDUxdkFHbXdKVU9kalFIeHhNREhxUCtxbEszZVVKeVNSWXJhTUEzTjZjQ1hzVmRmb1Z4bzFaNDJ5S1Z6VTlsNmZrV0NtZ2liQXpuakllandMYXA1NUNQcmQ5SEVzRjlOSDZmZG51YlFHT2M2UGpTNldXVURVallPUHR0S1M2dTBoZUp4RE5DOG5ROG5aT0t0T1VNN01BSFBZSGxCZUdaZEU5WHdqdVowV0Z6Qld1M0NiMlRSd1gyZlgzSkhTS0d6V09IUG1YWFp6QS9SbU5Lc0RVSzdUMThYcG1qTjZnNVBQOTkyLzhTdlZBUk1KbVd4NlBpSVFqSmJYbUs2czRHdzFOTzlSb0RLWGx3dUkzbkFxRHZPTmdHY1dIZkZZVEVmZ2tYQlY5amRWMFRabEx6Q0kxOXdkT21sTENuclRtMyszVjlka2svQk96Uzk3L25UTTM3RUUxMXVhTGVzVXFza3dsTHlZZDJ0RE5RRXZML3VSV24wTHdPbE5oMCt3WWtIS1ZEQXZnL1VpTFczWk1tbk5HWklZNFhjbTBRaHUrSGxnVmRHUFhPbUVxSnlRZHNJbWprdWVMeEE3cW9VYkpwSTdOdW5lcEs0YmxWWkI4V0tNZmRZK3BZPSIsIm1hYyI6ImM3NjBkNjUyODUyZTA1ZTkwMjk5NjRhYTZkNjA1MDhlMDM1MWJkZWNjMDA4M2ZhODlmMGVlMGJiOGNhMGRmMGYiLCJ0YWciOiIifQ%3D%3D&user=7acd83b9f99cc4a87306026289f35895&EIO=4&transport=websocket"
    ssl_context = ssl._create_unverified_context()
    while True:
        try:
            async with websockets.connect(uri, ssl=ssl_context) as websocket:
                print(f"[{datetime.now(ZoneInfo('Asia/Kolkata'))}] Connected to Ivasms 2 WebSocket.")
                initial_message = await websocket.recv()
                ping_interval = 25000
                try:
                    if initial_message.startswith("0{") and initial_message.endswith("}"):
                        data = json.loads(initial_message[1:])
                        ping_interval = data.get("pingInterval", 25000)
                except Exception:
                    pass
                await websocket.send("40/livesms,")
                ping_task = asyncio.create_task(send_ping(websocket, ping_interval, "3"))
                while True:
                    message = await websocket.recv()
                    if message.startswith("42/livesms,"):
                        try:
                            json_str = message[message.find("["):]
                            data = json.loads(json_str)
                            if isinstance(data, list) and len(data) > 1 and isinstance(data[1], dict):
                                sms = data[1]
                                ws_sender = str(sms.get("sender", sms.get("from", sms.get("cli", sms.get("service", sms.get("app", "")))))).strip()
                                if not ws_sender:
                                    ws_sender = str(sms.get("source", "")).strip()
                                msg_text = str(sms.get("message", ""))
                                detected_svc = detect_service(msg_text)
                                if detected_svc and detected_svc != "SMS":
                                    service = detected_svc
                                elif ws_sender and str(ws_sender).lower() not in ("", "sms", "unknown", "null"):
                                    service = ws_sender
                                else:
                                    service = detected_svc if detected_svc else "SMS"
                                num = str(sms.get("recipient", ""))
                                msg = str(sms.get("message", ""))
                                dt = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
                                process_ivasms_entry(service, num, msg, dt)
                        except Exception as e:
                            print(f"Error parsing WebSocket SMS: {e}")
        except Exception as e:
            print(f"[{datetime.now(ZoneInfo('Asia/Kolkata'))}] IvaSMS 2 Connection error: {e}. Retrying in 5s...")
            await asyncio.sleep(5)

async def ivasms3():
    uri = "wss://ivasms.qzz.io:2087/socket.io/?token=eyJpdiI6InlxNWNnanh0ZUwreVlQYytEelJoamc9PSIsInZhbHVlIjoiemV5YnJCV0pEUytzZEhKV0dyUUxuaFFacXl0NTlmQ0lwcVV3Z0g3cCs1ZHJpNWk2c01xZzNibElQanVEemlKbGZ4d0lLRmlaN3NMZTdTVUJzMWJON0dnWXQ4dlRTbGExTURoVEhWSlo1aFI2ajRqMDk2K25RVk1MZUdkSjM3TjkvcjlYdStRN1p3L05sYVdjbDJLTWNuTFBEVDBRcDF4Rk5lTFd1UGhncVZhUUVRam1jbFNHV3Y1NUVOendOdkFUZWV5VGNYUk84S1BFZTZkV25tWU1oR0VHZklJZzNGdUJwLzUvajFRVkpjeHdlYnlMM0ptZFBOeGFVcTIyRUhWVytxVGtjN2RlMkJYYnZZRlhVdkZzY0xhc2syYi81UUxFNmIxZHVnV0MrbTdnYS9tQytVSFBuNXk2M1MyT1NzR3hteUExaThIU2wxb20wK3g2NktSL1NOWWZPdytsMXcxRzJKcE9XeTgwMGRMNG9yTmdTbW10NTQ5OFpNSzRSeWJsWm1lNFVReVZhdjJaSTEzSHVuOG5VZyswTFNtZCsrT2V2YVVnZjZhemw2YzJJVGZOZ0ZUeTFjTFMrNFNSL0wyWHFvd0FzR3NwdWdvTXp5djVyYVFnNlJsVzM3aWF6K2tvWEMzTGxXS1pQT3RCTE1VT3hoZWhTeDFxMlNPZVJXTUtXWmxrTDROaFpJSzZGYlJjcXJpZGFpOFlPYkdKS1RNeVZITXU3S051VExNPSIsIm1hYyI6IjJjNmM2MGFjZmQyZTBmYmMwMWM2MWFiM2Q2MWNmZmZlYTczMTUzZDE2MzFlMDliYzBmYzY3MDczMWQ0YTEyZDMiLCJ0YWciOiIifQ%3D%3D&user=98fbd6a8ecd465bec072d02058829a74&EIO=4&transport=websocket"
    ssl_context = ssl._create_unverified_context()
    while True:
        try:
            async with websockets.connect(uri, ssl=ssl_context) as websocket:
                print(f"[{datetime.now(ZoneInfo('Asia/Kolkata'))}] Connected to Ivasms 3 WebSocket.")
                initial_message = await websocket.recv()
                ping_interval = 25000
                try:
                    if initial_message.startswith("0{") and initial_message.endswith("}"):
                        data = json.loads(initial_message[1:])
                        ping_interval = data.get("pingInterval", 25000)
                except Exception:
                    pass
                await websocket.send("40/livesms,")
                ping_task = asyncio.create_task(send_ping(websocket, ping_interval, "3"))
                while True:
                    message = await websocket.recv()
                    if message.startswith("42/livesms,"):
                        try:
                            json_str = message[message.find("["):]
                            data = json.loads(json_str)
                            if isinstance(data, list) and len(data) > 1 and isinstance(data[1], dict):
                                sms = data[1]
                                ws_sender = str(sms.get("sender", sms.get("from", sms.get("cli", sms.get("service", sms.get("app", "")))))).strip()
                                if not ws_sender:
                                    ws_sender = str(sms.get("source", "")).strip()
                                msg_text = str(sms.get("message", ""))
                                detected_svc = detect_service(msg_text)
                                if detected_svc and detected_svc != "SMS":
                                    service = detected_svc
                                elif ws_sender and str(ws_sender).lower() not in ("", "sms", "unknown", "null"):
                                    service = ws_sender
                                else:
                                    service = detected_svc if detected_svc else "SMS"
                                num = str(sms.get("recipient", ""))
                                msg = str(sms.get("message", ""))
                                dt = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
                                process_ivasms_entry(service, num, msg, dt)
                        except Exception as e:
                            print(f"Error parsing WebSocket SMS: {e}")
        except Exception as e:
            print(f"[{datetime.now(ZoneInfo('Asia/Kolkata'))}] IvaSMS 3 Connection error: {e}. Retrying in 5s...")
            await asyncio.sleep(5)


async def ivasms4():
    # TODO: Add your IvaSMS token 4 here
    uri = "wss://ivasms.qzz.io:2087/socket.io/?token=YOUR_TOKEN_4&user=YOUR_USER_4&EIO=4&transport=websocket"
    ssl_context = ssl._create_unverified_context()
    while True:
        try:
            async with websockets.connect(uri, ssl=ssl_context) as websocket:
                print(f"[{datetime.now(ZoneInfo('Asia/Kolkata'))}] Connected to Ivasms 4 WebSocket.")
                initial_message = await websocket.recv()
                ping_interval = 25000
                try:
                    if initial_message.startswith("0{") and initial_message.endswith("}"):
                        data = json.loads(initial_message[1:])
                        ping_interval = data.get("pingInterval", 25000)
                except Exception:
                    pass
                await websocket.send("40/livesms,")
                ping_task = asyncio.create_task(send_ping(websocket, ping_interval, "3"))
                while True:
                    message = await websocket.recv()
                    if message.startswith("42/livesms,"):
                        try:
                            json_str = message[message.find("["):]
                            data = json.loads(json_str)
                            if isinstance(data, list) and len(data) > 1 and isinstance(data[1], dict):
                                sms = data[1]
                                ws_sender = str(sms.get("sender", sms.get("from", sms.get("cli", sms.get("service", sms.get("app", "")))))).strip()
                                if not ws_sender:
                                    ws_sender = str(sms.get("source", "")).strip()
                                msg_text = str(sms.get("message", ""))
                                detected_svc = detect_service(msg_text)
                                if detected_svc and detected_svc != "SMS":
                                    service = detected_svc
                                elif ws_sender and str(ws_sender).lower() not in ("", "sms", "unknown", "null"):
                                    service = ws_sender
                                else:
                                    service = detected_svc if detected_svc else "SMS"
                                num = str(sms.get("recipient", ""))
                                msg = str(sms.get("message", ""))
                                dt = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
                                process_ivasms_entry(service, num, msg, dt)
                        except Exception as e:
                            print(f"Error parsing WebSocket SMS: {e}")
        except Exception as e:
            print(f"[{datetime.now(ZoneInfo('Asia/Kolkata'))}] IvaSMS 4 Connection error: {e}. Retrying in 5s...")
            await asyncio.sleep(5)

async def ivasms5():
    # TODO: Add your IvaSMS token 5 here
    uri = "wss://ivasms.qzz.io:2087/socket.io/?token=YOUR_TOKEN_5&user=YOUR_USER_5&EIO=4&transport=websocket"
    ssl_context = ssl._create_unverified_context()
    while True:
        try:
            async with websockets.connect(uri, ssl=ssl_context) as websocket:
                print(f"[{datetime.now(ZoneInfo('Asia/Kolkata'))}] Connected to Ivasms 5 WebSocket.")
                initial_message = await websocket.recv()
                ping_interval = 25000
                try:
                    if initial_message.startswith("0{") and initial_message.endswith("}"):
                        data = json.loads(initial_message[1:])
                        ping_interval = data.get("pingInterval", 25000)
                except Exception:
                    pass
                await websocket.send("40/livesms,")
                ping_task = asyncio.create_task(send_ping(websocket, ping_interval, "3"))
                while True:
                    message = await websocket.recv()
                    if message.startswith("42/livesms,"):
                        try:
                            json_str = message[message.find("["):]
                            data = json.loads(json_str)
                            if isinstance(data, list) and len(data) > 1 and isinstance(data[1], dict):
                                sms = data[1]
                                ws_sender = str(sms.get("sender", sms.get("from", sms.get("cli", sms.get("service", sms.get("app", "")))))).strip()
                                if not ws_sender:
                                    ws_sender = str(sms.get("source", "")).strip()
                                msg_text = str(sms.get("message", ""))
                                detected_svc = detect_service(msg_text)
                                if detected_svc and detected_svc != "SMS":
                                    service = detected_svc
                                elif ws_sender and str(ws_sender).lower() not in ("", "sms", "unknown", "null"):
                                    service = ws_sender
                                else:
                                    service = detected_svc if detected_svc else "SMS"
                                num = str(sms.get("recipient", ""))
                                msg = str(sms.get("message", ""))
                                dt = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
                                process_ivasms_entry(service, num, msg, dt)
                        except Exception as e:
                            print(f"Error parsing WebSocket SMS: {e}")
        except Exception as e:
            print(f"[{datetime.now(ZoneInfo('Asia/Kolkata'))}] IvaSMS 5 Connection error: {e}. Retrying in 5s...")
            await asyncio.sleep(5)

async def ivasms6():
    # TODO: Add your IvaSMS token 6 here
    uri = "wss://ivasms.qzz.io:2087/socket.io/?token=YOUR_TOKEN_6&user=YOUR_USER_6&EIO=4&transport=websocket"
    ssl_context = ssl._create_unverified_context()
    while True:
        try:
            async with websockets.connect(uri, ssl=ssl_context) as websocket:
                print(f"[{datetime.now(ZoneInfo('Asia/Kolkata'))}] Connected to Ivasms 6 WebSocket.")
                initial_message = await websocket.recv()
                ping_interval = 25000
                try:
                    if initial_message.startswith("0{") and initial_message.endswith("}"):
                        data = json.loads(initial_message[1:])
                        ping_interval = data.get("pingInterval", 25000)
                except Exception:
                    pass
                await websocket.send("40/livesms,")
                ping_task = asyncio.create_task(send_ping(websocket, ping_interval, "3"))
                while True:
                    message = await websocket.recv()
                    if message.startswith("42/livesms,"):
                        try:
                            json_str = message[message.find("["):]
                            data = json.loads(json_str)
                            if isinstance(data, list) and len(data) > 1 and isinstance(data[1], dict):
                                sms = data[1]
                                ws_sender = str(sms.get("sender", sms.get("from", sms.get("cli", sms.get("service", sms.get("app", "")))))).strip()
                                if not ws_sender:
                                    ws_sender = str(sms.get("source", "")).strip()
                                msg_text = str(sms.get("message", ""))
                                detected_svc = detect_service(msg_text)
                                if detected_svc and detected_svc != "SMS":
                                    service = detected_svc
                                elif ws_sender and str(ws_sender).lower() not in ("", "sms", "unknown", "null"):
                                    service = ws_sender
                                else:
                                    service = detected_svc if detected_svc else "SMS"
                                num = str(sms.get("recipient", ""))
                                msg = str(sms.get("message", ""))
                                dt = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
                                process_ivasms_entry(service, num, msg, dt)
                        except Exception as e:
                            print(f"Error parsing WebSocket SMS: {e}")
        except Exception as e:
            print(f"[{datetime.now(ZoneInfo('Asia/Kolkata'))}] IvaSMS 6 Connection error: {e}. Retrying in 5s...")
            await asyncio.sleep(5)

async def ivasms7():
    # TODO: Add your IvaSMS token 7 here
    uri = "wss://ivasms.qzz.io:2087/socket.io/?token=YOUR_TOKEN_7&user=YOUR_USER_7&EIO=4&transport=websocket"
    ssl_context = ssl._create_unverified_context()
    while True:
        try:
            async with websockets.connect(uri, ssl=ssl_context) as websocket:
                print(f"[{datetime.now(ZoneInfo('Asia/Kolkata'))}] Connected to Ivasms 7 WebSocket.")
                initial_message = await websocket.recv()
                ping_interval = 25000
                try:
                    if initial_message.startswith("0{") and initial_message.endswith("}"):
                        data = json.loads(initial_message[1:])
                        ping_interval = data.get("pingInterval", 25000)
                except Exception:
                    pass
                await websocket.send("40/livesms,")
                ping_task = asyncio.create_task(send_ping(websocket, ping_interval, "3"))
                while True:
                    message = await websocket.recv()
                    if message.startswith("42/livesms,"):
                        try:
                            json_str = message[message.find("["):]
                            data = json.loads(json_str)
                            if isinstance(data, list) and len(data) > 1 and isinstance(data[1], dict):
                                sms = data[1]
                                ws_sender = str(sms.get("sender", sms.get("from", sms.get("cli", sms.get("service", sms.get("app", "")))))).strip()
                                if not ws_sender:
                                    ws_sender = str(sms.get("source", "")).strip()
                                msg_text = str(sms.get("message", ""))
                                detected_svc = detect_service(msg_text)
                                if detected_svc and detected_svc != "SMS":
                                    service = detected_svc
                                elif ws_sender and str(ws_sender).lower() not in ("", "sms", "unknown", "null"):
                                    service = ws_sender
                                else:
                                    service = detected_svc if detected_svc else "SMS"
                                num = str(sms.get("recipient", ""))
                                msg = str(sms.get("message", ""))
                                dt = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
                                process_ivasms_entry(service, num, msg, dt)
                        except Exception as e:
                            print(f"Error parsing WebSocket SMS: {e}")
        except Exception as e:
            print(f"[{datetime.now(ZoneInfo('Asia/Kolkata'))}] IvaSMS 7 Connection error: {e}. Retrying in 5s...")
            await asyncio.sleep(5)

async def ivasms8():
    # TODO: Add your IvaSMS token 8 here
    uri = "wss://ivasms.qzz.io:2087/socket.io/?token=YOUR_TOKEN_8&user=YOUR_USER_8&EIO=4&transport=websocket"
    ssl_context = ssl._create_unverified_context()
    while True:
        try:
            async with websockets.connect(uri, ssl=ssl_context) as websocket:
                print(f"[{datetime.now(ZoneInfo('Asia/Kolkata'))}] Connected to Ivasms 8 WebSocket.")
                initial_message = await websocket.recv()
                ping_interval = 25000
                try:
                    if initial_message.startswith("0{") and initial_message.endswith("}"):
                        data = json.loads(initial_message[1:])
                        ping_interval = data.get("pingInterval", 25000)
                except Exception:
                    pass
                await websocket.send("40/livesms,")
                ping_task = asyncio.create_task(send_ping(websocket, ping_interval, "3"))
                while True:
                    message = await websocket.recv()
                    if message.startswith("42/livesms,"):
                        try:
                            json_str = message[message.find("["):]
                            data = json.loads(json_str)
                            if isinstance(data, list) and len(data) > 1 and isinstance(data[1], dict):
                                sms = data[1]
                                ws_sender = str(sms.get("sender", sms.get("from", sms.get("cli", sms.get("service", sms.get("app", "")))))).strip()
                                if not ws_sender:
                                    ws_sender = str(sms.get("source", "")).strip()
                                msg_text = str(sms.get("message", ""))
                                detected_svc = detect_service(msg_text)
                                if detected_svc and detected_svc != "SMS":
                                    service = detected_svc
                                elif ws_sender and str(ws_sender).lower() not in ("", "sms", "unknown", "null"):
                                    service = ws_sender
                                else:
                                    service = detected_svc if detected_svc else "SMS"
                                num = str(sms.get("recipient", ""))
                                msg = str(sms.get("message", ""))
                                dt = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
                                process_ivasms_entry(service, num, msg, dt)
                        except Exception as e:
                            print(f"Error parsing WebSocket SMS: {e}")
        except Exception as e:
            print(f"[{datetime.now(ZoneInfo('Asia/Kolkata'))}] IvaSMS 8 Connection error: {e}. Retrying in 5s...")
            await asyncio.sleep(5)

def process_ivasms_entry(service, num, msg, dt):
    """Process IvaSMS OTP - match against assigned numbers and send to user, also forward to groups"""
    # If IvaSMS sends generic service name, try to detect from message
    detected = detect_service(msg)
    if detected and detected != "SMS":
        service = detected
    elif not service or str(service).lower() in ("", "sms", "unknown", "null"):
        service = detected if detected else "SMS"
    entry = [service, num, msg, dt]
    uid = f"{service}_{num}_{dt}"
    assignments = db.get("number_assignments", {})
    matched_num, matched_data = None, None
    if assignments:
        variants = [num, num.lstrip('+'), re.sub(r"^\+?\d{1,3}", "", num)]
        for variant in variants:
            matched_num, matched_data = match_assigned_number(variant, assignments)
            if matched_num and matched_data:
                break
    with _seen_otps_lock:
        if uid not in _seen_otps:
            _seen_otps.add(uid)
            if matched_num and matched_data:
                send_to_groups(entry, forced_service=matched_data["service"])
            else:
                send_to_groups(entry)
    if not matched_num or not matched_data:
        print(f"[IVASMS] No match for number {num}")
        return
    _notify_assigned_user(matched_num, matched_data, msg, "IVASMS")
def start_ivasms():
    if websockets is None:
        print("websockets not installed, IvaSMS disabled")
        return
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(asyncio.gather(ivasms(), ivasms2(), ivasms3(), ivasms4(), ivasms5(), ivasms6(), ivasms7(), ivasms8()))

# ===== PANEL POLLER =====
def fetch_panel_otps():
    all_otps = []
    try:
        r = requests.get(f"{API_URL}?token={TOKEN}", timeout=15)
        if r.status_code == 200:
            data = r.json()
            if data.get("status") == "success":
                for item in data.get("data", []):
                    num = item.get("num", "")
                    svc = item.get("cli", "SMS")
                    msg = item.get("message", "")
                    country = "Unknown"
                    ccode = ""
                    try:
                        num_parsed = "+" + num if not num.startswith("+") else num
                        parsed = phonenumbers.parse(num_parsed)
                        ccode = phonenumbers.region_code_for_number(parsed)
                        country = geocoder.description_for_number(parsed, "en")
                    except:
                        pass
                    all_otps.append({"number": num, "service": svc, "country_name": country, "country_code": ccode, "message": msg, "source": "viewstats"})
    except Exception as e:
        print(f"Panel fetch viewstats error: {e}")
    try:
        r = requests.get(API_URLS_NEW[0], timeout=15)
        if r.status_code == 200:
            data = r.json()
            for item in data.get("aaData", []):
                if len(item) >= 5:
                    dt, country_name, num, svc, msg = item[0], item[1], item[2], item[3], item[4]
                    ccode = COUNTRY_NAME_TO_CODE.get(country_name.lower(), "")
                    if not ccode and num:
                        try:
                            num_parsed = "+" + str(num) if not str(num).startswith("+") else str(num)
                            parsed = phonenumbers.parse(num_parsed)
                            ccode = phonenumbers.region_code_for_number(parsed)
                        except:
                            pass
                    all_otps.append({"number": str(num), "service": svc, "country_name": country_name, "country_code": ccode, "message": msg, "source": "ps"})
    except Exception as e:
        print(f"Panel fetch ps error: {e}")
    try:
        r = requests.get(API_URLS_NEW[1], timeout=15)
        if r.status_code == 200:
            data = r.json()
            for item in data.get("aaData", []):
                if len(item) >= 5:
                    dt, country_name, num, svc, msg = item[0], item[1], item[2], item[3], item[4]
                    ccode = COUNTRY_NAME_TO_CODE.get(country_name.lower(), "")
                    if not ccode and num:
                        try:
                            num_parsed = "+" + str(num) if not str(num).startswith("+") else str(num)
                            parsed = phonenumbers.parse(num_parsed)
                            ccode = phonenumbers.region_code_for_number(parsed)
                        except:
                            pass
                    all_otps.append({"number": str(num), "service": svc, "country_name": country_name, "country_code": ccode, "message": msg, "source": "np"})
    except Exception as e:
        print(f"Panel fetch np error: {e}")
    panel_otps = {}
    panel_counts = {}
    for otp in all_otps:
        svc = otp["service"]
        ccode = otp["country_code"] or "XX"
        if svc not in panel_otps:
            panel_otps[svc] = {}
        if ccode not in panel_otps[svc]:
            panel_otps[svc][ccode] = []
        panel_otps[svc][ccode].append(otp)
        if svc not in panel_counts:
            panel_counts[svc] = {}
        panel_counts[svc][ccode] = panel_counts[svc].get(ccode, 0) + 1
    db["panel_otps"] = panel_otps
    db["panel_counts"] = panel_counts
    db["panel_last_fetch"] = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
    save_db(db)
    process_panel_otps()

def process_panel_otps():
    panel_otps = db.get("panel_otps", {})
    assignments = db.get("number_assignments", {})
    processed = set(db.get("processed_panel_otps", []))
    if not panel_otps or not assignments:
        return
    matched_any = False
    for svc, countries in list(panel_otps.items()):
        for ccode, otps in list(countries.items()):
            for otp_data in list(otps):
                num = str(otp_data.get("number", ""))
                msg = otp_data.get("message", "")
                otp_id = f"{num}_{msg}"
                if otp_id in processed:
                    continue
                if not num:
                    processed.add(otp_id)
                    continue
                matched_num, matched_data = match_assigned_number(num, assignments)
                if matched_num and matched_data:
                    if _notify_assigned_user(matched_num, matched_data, msg, "PANEL"):
                        matched_any = True
                        send_to_groups([matched_data["service"], num, msg, ""], forced_service=matched_data["service"])
                processed.add(otp_id)
    if len(processed) > 5000:
        processed = set(list(processed)[-2500:])
    db["processed_panel_otps"] = list(processed)
    if matched_any:
        save_db(db)

def panel_poller():
    while True:
        try:
            fetch_panel_otps()
        except Exception as e:
            print(f"Panel poller error: {e}")
        time.sleep(60)

# ===== CALLBACK ROUTER =====
def process_callback(chat_id, uid, data, message_id, cid):
    _edit_context.msg_id = message_id
    try:
        if data == "menu_main":
            _edit_context.msg_id = None
            handle_start(chat_id, {"id": uid, "username": db["users"].get(uid, {}).get("username", ""), "first_name": db["users"].get(uid, {}).get("first_name", "User")})
        elif data == "menu_getnumber":
            handle_get_number(chat_id, uid)
        elif data == "menu_account":
            handle_account(chat_id, uid)
        elif data == "menu_balance":
            handle_balance(chat_id, uid)
        elif data == "menu_withdraw":
            handle_withdraw(chat_id, uid)
        elif data == "menu_topusers":
            handle_top_users(chat_id)
        elif data == "menu_developer":
            handle_developer(chat_id)
        elif data == "menu_referral":
            handle_referral(chat_id, uid)
        elif data == "menu_channels":
            handle_channels(chat_id)
        elif data == "menu_accesslist":
            handle_access_list(chat_id, uid)
        elif data == "menu_otphistory":
            handle_otp_history(chat_id, uid)
        elif data == "menu_otprewards":
            handle_otp_rewards(chat_id, uid)
        elif data.startswith("bc_getnum"):
            old_msg_id = db.get("user_states", {}).get(uid, {}).get("bc_getnum_msg_id")
            if old_msg_id:
                api("deleteMessage", {"chat_id": chat_id, "message_id": old_msg_id})
            broadcast_service = None
            broadcast_country = None
            if data.startswith("bc_getnum_"):
                rest = data[10:]
                if "_" in rest:
                    last_underscore = rest.rfind("_")
                    possible_service = rest[:last_underscore]
                    possible_country = rest[last_underscore+1:]
                    if possible_country.upper() in COUNTRY_FLAGS:
                        broadcast_service = possible_service
                        broadcast_country = possible_country.upper()
                    elif possible_country in COUNTRY_NAME_TO_CODE.values():
                        broadcast_service = possible_service
                        broadcast_country = possible_country
                    else:
                        broadcast_service = rest
                else:
                    broadcast_service = rest
            if broadcast_service and broadcast_country:
                if broadcast_service in db.get("services", {}) and broadcast_country in db.get("service_countries", {}).get(broadcast_service, {}):
                    handle_country_selected(chat_id, uid, broadcast_service, broadcast_country)
                elif broadcast_service in db.get("services", {}):
                    handle_service_selected(chat_id, uid, broadcast_service)
                else:
                    handle_get_number(chat_id, uid)
            elif broadcast_service and broadcast_service in db.get("services", {}):
                msg_id = handle_service_selected_no_back(chat_id, uid, broadcast_service)
                if msg_id:
                    db.setdefault("user_states", {}).setdefault(uid, {})["bc_getnum_msg_id"] = msg_id
                    save_db(db)
            else:
                handle_get_number(chat_id, uid)
        elif data == "menu_admin":
            handle_admin_panel(chat_id, uid)
        elif data == "admin_addservice":
            handle_add_service(chat_id, uid)
        elif data == "admin_viewservices":
            handle_view_services(chat_id, uid)
        elif data == "admin_removeservice":
            handle_remove_service(chat_id, uid)
        elif data == "admin_addcountry":
            handle_add_country(chat_id, uid)
        elif data.startswith("ctrysvc_"):
            handle_country_service(chat_id, uid, data[8:])
        elif data == "admin_viewcountries":
            handle_view_countries(chat_id, uid)
        elif data == "admin_addnumbers":
            handle_add_numbers(chat_id, uid)
        elif data == "admin_stats":
            handle_stats(chat_id, uid)
        elif data == "admin_broadcast":
            handle_broadcast(chat_id, uid)
        elif data == "refresh_services":
            db.setdefault("user_states", {}).setdefault(uid, {})["style_offset"] = db.get("user_states", {}).get(uid, {}).get("style_offset", 0) + 1
            save_db(db)
            handle_get_number(chat_id, uid)
        elif data.startswith("refresh_svc_"):
            db.setdefault("user_states", {}).setdefault(uid, {})["style_offset"] = db.get("user_states", {}).get(uid, {}).get("style_offset", 0) + 1
            save_db(db)
            handle_service_selected(chat_id, uid, data[12:])
        elif data == "admin_withdrawals":
            handle_manage_withdrawals(chat_id, uid)
        elif data == "admin_checkbalance":
            handle_check_balance(chat_id, uid)
        elif data == "admin_removebalance":
            handle_remove_balance(chat_id, uid)
        elif data == "admin_removeallbalance":
            handle_remove_all_balances(chat_id, uid)
        elif data == "admin_enablewithdraw":
            db["withdrawals_enabled"] = True
            save_db(db)
            send_message(chat_id, f"{ce('check','✅')} <b>Withdrawals Enabled!</b>\n\nUsers can now request withdrawals.", admin_menu_markup())
        elif data == "admin_disablewithdraw":
            db["withdrawals_enabled"] = False
            save_db(db)
            send_message(chat_id, f"{ce('no','❌')} <b>Withdrawals Disabled!</b>\n\nUsers cannot request withdrawals until enabled.", admin_menu_markup())
        elif data == "admin_addadmin":
            handle_add_admin(chat_id, uid)
        elif data == "admin_removeadmin":
            handle_remove_admin(chat_id, uid)
        elif data == "admin_viewadmins":
            handle_view_admins(chat_id, uid)
        elif data == "admin_addivasms":
            handle_add_ivasms(chat_id, uid)
        elif data == "admin_myivasms":
            handle_my_ivasms(chat_id, uid)
        elif data.startswith("rmadmin_"):
            handle_remove_admin_selected(chat_id, uid, data[8:])
        elif data.startswith("checkivasms_"):
            handle_check_ivasms(chat_id, uid, data[12:])
        elif data == "admin_banuser":
            handle_ban_user(chat_id, uid)
        elif data == "admin_unbanuser":
            handle_unban_user(chat_id, uid)
        elif data == "admin_removecountry":
            handle_remove_country(chat_id, uid)
        elif data == "admin_removenumber":
            handle_remove_number(chat_id, uid)
        elif data == "admin_addgroup":
            handle_add_group(chat_id, uid)
        elif data == "admin_viewgroups":
            handle_view_groups(chat_id, uid)
        elif data == "admin_removegroup":
            handle_remove_group(chat_id, uid)
        elif data.startswith("rmgroup_"):
            handle_remove_group_selected(chat_id, uid, data[8:])
        elif data.startswith("rmctrysvc_"):
            handle_remove_country_service(chat_id, uid, data[10:])
        elif data.startswith("rmctry_"):
            parts = data.split("_")
            if len(parts) >= 3:
                handle_remove_country_selected(chat_id, uid, parts[1], parts[2])
        elif data.startswith("rmnumsvc_"):
            handle_remove_number_service(chat_id, uid, data[9:])
        elif data.startswith("rmnumctry_"):
            parts = data.split("_")
            if len(parts) >= 3:
                handle_remove_number_country(chat_id, uid, parts[1], parts[2])
        elif data.startswith("unban_"):
            target = data[6:]
            unban_user(target)
            send_message(chat_id, f"{ce('check','✅')} User <code>{target}</code> unbanned!", admin_menu_markup())
        elif data.startswith("svc_"):
            handle_service_selected(chat_id, uid, data[4:])
        elif data.startswith("ctry_"):
            parts = data.split("_")
            if len(parts) >= 3:
                handle_country_selected(chat_id, uid, parts[1], parts[2])
        elif data.startswith("numsvc_"):
            handle_numbers_service(chat_id, uid, data[7:])
        elif data.startswith("numctry_"):
            handle_numbers_country(chat_id, uid, data[8:])
        elif data.startswith("wd_approve_"):
            try:
                idx = int(data.split("_")[2])
                handle_withdrawal_action(chat_id, uid, "approved", idx)
            except:
                pass
        elif data.startswith("wd_reject_"):
            try:
                idx = int(data.split("_")[2])
                handle_withdrawal_action(chat_id, uid, "rejected", idx)
            except:
                pass
        elif data.startswith("rmsvc_"):
            handle_remove_service_selected(chat_id, uid, data[6:])
        elif data.startswith("toggle_cc_"):
            parts = data.split("_")
            if len(parts) >= 4:
                state = db.get("user_states", {}).get(uid, {})
                nums = state.get("numbers", [])
                current = state.get("show_cc", True)
                db["user_states"][uid]["show_cc"] = not current
                save_db(db)
                show_assigned_numbers(chat_id, uid, parts[2], parts[3], nums, show_cc=not current)
        elif data.startswith("changenum_"):
            parts = data.split("_")
            if len(parts) >= 3:
                svc_name = parts[1]
                ccode = parts[2]
                now = time.time()
                last_refresh = db.get("user_states", {}).get(uid, {}).get("refresh_cooldown", 0)
                elapsed = now - last_refresh
                if elapsed < 3:
                    remaining = 3 - int(elapsed)
                    answer_callback_query(cid, f"Too many requests. Wait {remaining} second{'s' if remaining != 1 else ''}...")
                    cid = None
                    return
                db["user_states"][uid]["refresh_cooldown"] = now
                db["user_states"][uid]["style_offset"] = db.get("user_states", {}).get(uid, {}).get("style_offset", 0) + 1
                save_db(db)
                state = db.get("user_states", {}).get(uid, {})
                old_nums = state.get("numbers", [])
                for num in old_nums:
                    db["number_assignments"].pop(num, None)
                save_db(db)
                handle_country_selected(chat_id, uid, svc_name, ccode)
        elif data.startswith("changectry_"):
            handle_service_selected(chat_id, uid, data[11:])
        elif data.startswith("refresh_"):
            parts = data.split("_")
            if len(parts) >= 3:
                handle_country_selected(chat_id, uid, parts[1], "_".join(parts[2:]))
    finally:
        if cid:
            answer_callback_query(cid)
        _edit_context.msg_id = None

# ===== MESSAGE ROUTER =====
def process_message(chat_id, uid, text, user, message_id=None):
    user_state = db.get("user_states", {}).get(uid, {})
    admin_state = db.get("admin_states", {}).get(uid, {})
    if text.startswith("/start"):
        parts = text.split()
        if len(parts) > 1:
            ref_code = parts[1]
            if ref_code != uid and ref_code in db.get("users", {}):
                is_new_user = uid not in db["users"]
                if is_new_user:
                    db["users"][uid] = {
                        "id": uid,
                        "username": user.get("username", "User"),
                        "first_name": user.get("first_name", "User"),
                        "balance": 0.0,
                        "total_earned": 0.0,
                        "referrals": 0,
                        "referral_code": uid,
                        "joined": datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S"),
                        "otp_count": 0,
                        "referred_by": ref_code,
                    }
                    db["stats"]["total_users"] = len(db["users"])
                else:
                    if not db["users"][uid].get("referred_by"):
                        db["users"][uid]["referred_by"] = ref_code
                already_referred = False
                if ref_code in db.get("referral_tracking", {}) and uid in db["referral_tracking"][ref_code]:
                    already_referred = True
                if not already_referred:
                    db.setdefault("referral_tracking", {}).setdefault(ref_code, {})[uid] = {
                        "joined_at": datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S"),
                        "otp_count": 0,
                        "reward_unlocked": False,
                    }
                    db["users"][ref_code]["referrals"] = db["users"][ref_code].get("referrals", 0) + 1
                    save_db(db)
                    referred_name = user.get("first_name", "User")
                    ref_notify = (
                        f"{ce('user','👤')} <b>{html.escape(referred_name)}</b> joined using your referral link!\n\n"
                        f"{ce('time','⏳')} The reward will be unlocked after they receive <b>10 OTPs</b>.\n"
                        f"{ce('gift','🎁')} <b>Invite:</b> <code>$0.070</code> + {ce('star','⭐')} <b>Bonus:</b> <code>$0.0003</code>"
                    )
                    send_message(int(ref_code), ref_notify)
                else:
                    if is_new_user:
                        save_db(db)
        handle_start(chat_id, user)
        return
    menu_routes = {
        "𝗚𝗘𝗧 𝗡𝗨𝗠𝗕𝗘𝗥": lambda c, u: handle_get_number(c, u),
        "𝗠𝗬 𝗔𝗖𝗖𝗢𝗨𝗡𝗧": lambda c, u: handle_account(c, u),
        "𝗕𝗔𝗟𝗔𝗡𝗖𝗘": lambda c, u: handle_balance(c, u),
        "𝗪𝗜𝗧𝗛𝗗𝗥𝗔𝗪": lambda c, u: handle_withdraw(c, u),
        "𝗧𝗢𝗣 𝗨𝗦𝗘𝗥𝗦": lambda c, u: handle_top_users(c),
        "𝗗𝗘𝗩𝗘𝗟𝗢𝗣𝗘𝗥": lambda c, u: handle_developer(c),
        "𝗥𝗘𝗙𝗘𝗥𝗥𝗔𝗟": lambda c, u: handle_referral(c, u),
        "𝗔𝗖𝗖𝗘𝗦𝗦 𝗟𝗜𝗦𝗧": lambda c, u: handle_access_list(c, u),
        "𝗢𝗧𝗣 𝗥𝗘𝗪𝗔𝗥𝗗𝗦": lambda c, u: handle_otp_rewards(c, u),
        "𝗝𝗢𝗜𝗡 𝗢𝗨𝗥 𝗖𝗛𝗔𝗡𝗡𝗘𝗟𝗦": lambda c, u: handle_channels(c),
        "𝗔𝗗𝗠𝗜𝗡 𝗣𝗔𝗡𝗘𝗟": lambda c, u: handle_admin_panel(c, u),
    }
    if text.strip() in menu_routes:
        db["user_states"].pop(uid, None)
        db["admin_states"].pop(uid, None)
        save_db(db)
        menu_routes[text.strip()](chat_id, uid)
        return
    if user_state.get("state") == "awaiting_withdraw_amount":
        handle_withdraw_amount(chat_id, uid, text)
        return
    if user_state.get("state") == "awaiting_withdraw_method":
        handle_withdraw_method(chat_id, uid, text)
        return
    if admin_state.get("state") == "awaiting_service_name":
        handle_service_name(chat_id, uid, text)
        return
    if admin_state.get("state") == "awaiting_country_code":
        handle_country_code(chat_id, uid, text)
        return
    if admin_state.get("state") == "awaiting_numbers_list":
        handle_numbers_list(chat_id, uid, text)
        return
    if admin_state.get("state") == "awaiting_country_custom_name":
        handle_country_custom_name(chat_id, uid, text)
        return
    if admin_state.get("state") == "awaiting_country_price":
        handle_country_price(chat_id, uid, text)
        return
    if admin_state.get("state") == "awaiting_broadcast":
        handle_broadcast_message(chat_id, uid, text, message_id)
        return
    if admin_state.get("state") == "awaiting_ban_uid":
        target = text.strip()
        ban_user(target)
        db["admin_states"].pop(uid, None)
        save_db(db)
        send_message(chat_id, f"{ce('no','🚫')} User <code>{target}</code> banned!", admin_menu_markup())
        return
    if admin_state.get("state") == "awaiting_country_service":
        send_message(chat_id, f"{ce('warn','⚠️')} Please select a service from the buttons above.")
        return
    if admin_state.get("state") == "awaiting_group_name":
        handle_group_name(chat_id, uid, text)
        return
    if admin_state.get("state") == "awaiting_group_id":
        handle_group_id(chat_id, uid, text)
        return
    if admin_state.get("state") == "awaiting_checkbalance_uid":
        handle_checkbalance_uid(chat_id, uid, text)
        return
    if admin_state.get("state") == "awaiting_removebalance_uid":
        handle_removebalance_uid(chat_id, uid, text)
        return
    if admin_state.get("state") == "awaiting_removebalance_amount":
        handle_removebalance_amount(chat_id, uid, text)
        return
    if admin_state.get("state") == "awaiting_ivasms_name":
        handle_ivasms_name(chat_id, uid, text)
        return
    if admin_state.get("state") == "awaiting_ivasms_token":
        handle_ivasms_token(chat_id, uid, text)
        return
    if admin_state.get("state") == "awaiting_ivasms_user":
        handle_ivasms_user(chat_id, uid, text)
        return
    if admin_state.get("state") == "awaiting_admin_id":
        target = text.strip()
        if target and target.isdigit():
            if int(target) not in ADMIN_IDS:
                ADMIN_IDS.append(int(target))
                db.setdefault("admins", []).append(int(target))
                save_db(db)
                send_message(chat_id, f"{ce('check','✅')} <b>Admin Added!</b>\n\nUser ID: <code>{target}</code> can now use admin panel.", admin_menu_markup())
            else:
                send_message(chat_id, f"{ce('warn','⚠️')} User <code>{target}</code> is already an admin.", admin_menu_markup())
        else:
            send_message(chat_id, f"{ce('no','❌')} Invalid User ID.", admin_menu_markup())
        db["admin_states"].pop(uid, None)
        save_db(db)
        return
    handle_start(chat_id, user)

# ===== DOCUMENT HANDLER =====
def process_document(chat_id, uid, document, user):
    admin_state = db.get("admin_states", {}).get(uid, {})
    if admin_state.get("state") != "awaiting_numbers_list":
        send_message(chat_id, f"{ce('warn','⚠️')} No pending number addition request. Upload file from ADMIN PANEL > Add Numbers.")
        return
    file_id = document.get("file_id")
    if not file_id:
        send_message(chat_id, f"{ce('no','❌')} Could not get file ID.")
        return
    try:
        file_info = api("getFile", {"file_id": file_id})
        if not file_info.get("ok"):
            send_message(chat_id, f"{ce('no','❌')} Failed to get file info.")
            return
        file_path = file_info["result"]["file_path"]
        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
        r = requests.get(file_url, timeout=30)
        if r.status_code != 200:
            send_message(chat_id, f"{ce('no','❌')} Failed to download file.")
            return
        file_content = r.text
    except Exception as e:
        send_message(chat_id, f"{ce('no','❌')} Error downloading file: {e}")
        return
    numbers = [n.strip() for line in file_content.splitlines() for n in line.split(",") if n.strip()]
    if not numbers:
        send_message(chat_id, f"{ce('warn','⚠️')} No numbers found in file.")
        return
    state = db["admin_states"].get(uid, {})
    svc_name = state.get("service", "")
    ccode = state.get("country", "")
    if svc_name not in db["numbers"]:
        db["numbers"][svc_name] = {}
    if ccode not in db["numbers"][svc_name]:
        db["numbers"][svc_name][ccode] = []
    old_count = len(db["numbers"][svc_name][ccode])
    db["numbers"][svc_name][ccode] = numbers  # OVERWRITE: old removed, new added
    db["admin_states"].pop(uid, None)
    save_db(db)
    country = db.get("countries", {}).get(ccode, {}).get("name", ccode)
    flag = flag_emoji(ccode, "🏳️")
    text = (
        f"{ce('check','✅')} <b>Numbers Overwritten from File!</b>\n\n"
        f"{svc_emoji(svc_name, '📱')} Service: <code>{svc_name}</code>\n"
        f"{flag} Country: <code>{country}</code>\n"
        f"{ce('trash','🗑️')} Old Removed: <code>{old_count}</code>\n"
        f"{ce('phone','📞')} New Added: <code>{len(numbers)}</code>\n"
        f"{ce('graph','📊')} Total Now: <code>{len(numbers)}</code>"
    )
    send_message(chat_id, text, admin_menu_markup())

# ===== GROUP MESSAGE HANDLER =====
def handle_group_message(msg):
    text = msg.get("text", "") or msg.get("caption", "")
    if not text:
        return
    clean_text = re.sub(r"<[^>]+>", "", text)
    number_matches = re.findall(r'\+?\d[\d\s\-\*]{5,}', clean_text)
    if not number_matches:
        return
    assignments = db.get("number_assignments", {})
    if not assignments:
        return
    for raw_num in number_matches:
        raw_num = raw_num.replace(" ", "").replace("-", "")
        if not raw_num.startswith("+"):
            raw_num = "+" + raw_num
        matched_num = None
        matched_data = None
        for num, data in list(assignments.items()):
            n1 = num.replace("+", "").replace(" ", "")
            n2 = raw_num.replace("+", "").replace(" ", "")
            if n1 == n2 or n1 in n2 or n2 in n1:
                matched_num = num
                matched_data = data
                break
            if "***" in n2:
                suffix = n2.split("***")[-1]
                if suffix and n1.endswith(suffix):
                    matched_num = num
                    matched_data = data
                    break
            if len(n2) >= 5 and len(n1) >= 5:
                if n1.endswith(n2[-5:]) or n2.endswith(n1[-5:]):
                    matched_num = num
                    matched_data = data
                    break
        if matched_num and matched_data:
            _notify_assigned_user(matched_num, matched_data, clean_text, "GROUP_MSG")
            send_to_groups([matched_data["service"], matched_num, clean_text, ""], forced_service=matched_data["service"])
            check_restock_alert(matched_data["service"], matched_data["country"])
            break

# ===== POLLING LOOP =====
last_update_id = 0

def get_updates():
    global last_update_id
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    try:
        r = requests.get(url, params={"offset": last_update_id + 1, "limit": 100}, timeout=30)
        data = r.json()
        if data.get("ok"):
            return data.get("result", [])
    except:
        pass
    return []

def handle_update(update):
    global last_update_id
    last_update_id = update.get("update_id", last_update_id)
    if "message" in update:
        msg = update["message"]
        chat_id = msg["chat"]["id"]
        uid = str(msg["from"]["id"])
        text = msg.get("text", "")
        user = msg["from"]
        if is_banned(uid):
            return
        chat_type = msg["chat"].get("type", "private")
        if chat_type in ("group", "supergroup", "channel"):
            handle_group_message(msg)
        else:
            if "document" in msg:
                process_document(chat_id, uid, msg["document"], user)
            else:
                process_message(chat_id, uid, text, user, msg.get("message_id"))
    elif "callback_query" in update:
        cq = update["callback_query"]
        chat_id = cq["message"]["chat"]["id"]
        uid = str(cq["from"]["id"])
        data = cq["data"]
        message_id = cq["message"]["message_id"]
        cq_id = cq["id"]
        process_callback(chat_id, uid, data, message_id, cq_id)

# ===== MAIN =====
def main():
    print("=" * 50)
    print("Syed OTP Bot Started!")
    print(f"Admin IDs: {ADMIN_IDS}")
    print("=" * 50)
    t1 = threading.Thread(target=panel_poller, daemon=True)
    t1.start()
    t2 = threading.Thread(target=otp_forward_poller, daemon=True)
    t2.start()
    threading.Thread(target=fetch_panel_otps, daemon=True).start()
    t3 = threading.Thread(target=start_ivasms, daemon=True)
    t3.start()
    # Use ThreadPoolExecutor to limit concurrent update handlers
    from concurrent.futures import ThreadPoolExecutor
    executor = ThreadPoolExecutor(max_workers=10)
    while True:
        try:
            updates = get_updates()
            if updates:
                for update in updates:
                    executor.submit(handle_update, update)
            time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nShutting down...")
            executor.shutdown(wait=False)
            break
        except Exception as e:
            print(f"Main loop error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
