###############################
# ### LOGGING CONFIGURATION ###
###############################
import logging
logging.basicConfig(level=logging.ERROR)
logging.getLogger("BaseHandlers").setLevel(logging.DEBUG)
logging.getLogger("ngsild").setLevel(logging.INFO)
logging.getLogger("ngsildclient").setLevel(logging.INFO)
log = logging.getLogger(__name__)

#########################################
# ### Various configuration variables ###
#########################################
SDEVICE = "/dev/ttyUSB0"
sensor_entity_format = "urn:ngsi-ld:Device:TETRIS:D{id}"

#####################################
# ### DATA HANDLING CONFIGURATION ###
#####################################
from BaseHandlers import DebugHandler, ListOfHandlers
from ngsild import NgsildHandler
from bearer_auth import BearerAuth
from ngsildclient import Client

handler = ListOfHandlers()
handler.append(DebugHandler())

client_id="your-client-id"
client_secret="your_client-secret"
url_keycloak = "the_kc_url"

authentifier = BearerAuth(client_id, client_secret, url_keycloak)

url_graced_int = "graced-broker-url"
port_graced_int = 443
context = 'https://easy-global-market.github.io/ngsild-api-data-models/projects/jsonld-contexts/graced.jsonld'


stellio = NgsildHandler(Client(url_graced_int, port_graced_int, secure=True, custom_auth=authentifier), sensor_entity_format, context)
handler.append(stellio)

#######################################
# ### DATA CONVERSION CONFIGURATION ###
#######################################

# Data conversion functions
def f100(i):
    return float(i)/100

def i1(i):
    return i

def NotUsed(i):
    return None

# Codec triplets (function, name, unit)
not_used = (NotUsed,"","")
temperature = (f100,"temperature","CEL")
h_ext = (f100,"humidity","P1")
pm25 = (f100,"pm25","GQ")
pm1 = (f100,"pm1","GQ")
t_voc = (i1,"tVoc","61")
v_co2 = (i1,"co2","59")
h2 = (i1,"h2","")
eth = (i1,"eth","")
ldr = (i1,"ldr","")
storm_nb = (i1,"stormNb","")
storm_distance = (i1,"stormDistance","MTR")
atm_pressure = (f100,"pressure","A97")
altitude = (i1,"altitude","MTR")
tds = (f100, "totalDissolvedSolids", "H29")
vol = (f100, 'volume', "MLT")
pH = (f100, "pH", "Q30")
tdy = (i1, "tdy", "NTU")
conduct = (f100, "conductivity", "H61")
txox = (f100, "dissolvedOxygen", "M1")

# Devices declarations
devices = {
    10 : ([
        not_used,not_used, temperature, h_ext, not_used, not_used, not_used,
        not_used, not_used,not_used, ldr, not_used, not_used, not_used, 
        atm_pressure, altitude
    ],"GtwFablab","Gateway Fablab"),
    11 : ([
        not_used,not_used, temperature, h_ext, pm25, pm1, t_voc,
        v_co2, h2,eth, ldr, not_used, not_used, not_used, 
        atm_pressure, altitude
    ],"Roof","Environmental sensor - Roof canteen"),
    12 : ([
        not_used,not_used, temperature, h_ext, pm25, pm1, t_voc,
        v_co2, h2,eth, ldr, not_used, not_used, not_used, 
        atm_pressure, altitude
    ],"ReseachCntr","Environmental sensor - Research Centre"),
    20 : ([
        not_used,not_used, tds, vol, txox, pH, temperature, tdy, conduct,
        not_used,not_used,not_used,not_used,not_used,not_used,not_used
    ],"Tank01","Water sensors - Tank01"),
    21 : ([
        not_used,not_used, tds, vol, not_used, pH, temperature, tdy, conduct,
        not_used,not_used,not_used,not_used,not_used,not_used,not_used
    ],"Tank02","Water sensors - Tank02"),
    22 : ([
        not_used,not_used, tds, vol, not_used, pH, temperature, tdy, conduct,
        not_used,not_used,not_used,not_used,not_used,not_used,not_used
    ],"Tank03","Water sensors - Tank03"),
}

################################
# ### Config related actions ###
################################

def create_entities():
    stellio.ensure_entities_for_devices(devices)
