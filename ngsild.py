from datetime import datetime
from ngsildclient import Client, Entity
from ngsildclient.utils import iso8601

from bearer_auth import BearerAuth
from packet import DecodedDataHandler

import logging
log = logging.getLogger(__name__)


class NgsildHandler(DecodedDataHandler):
    "Update the decoded packet to a NGSI-LD broker"

    def __init__(self, broker : Client, sensor_entity_format : str, context) -> None:
        self.broker = broker
        self.context = context
        self.sensor_entity_format = sensor_entity_format
        self.cur_entity = None
        self.cur_ts = None
        super().__init__()


    def begin(self, id, timestamp):
        self.cur_entity = self.entity_from_id(id)
        self.cur_ts,x1,x2 = iso8601.parse(timestamp)


    def handle_property(self, name, value, unit):
        self.cur_entity.prop(name,value,observedat=self.cur_ts, userdata={"unitCode":unit})


    def end(self):
        self.broker.update(self.cur_entity)


    def entity_from_id(self, id):
        "Given the id in a packet, returns the entity object"

        return Entity("Device", self.sensor_entity_format.format(id=id), ctx=self.context)


    def ensure_entities_for_devices(self, devices:dict):
        "Ensure that all the entities related to the declared devices do exist in the context broker"
        
        log.info("Updating device entities")
        entities = [self.entity_from_id(id) for id in devices.keys()]
        self.broker.batch.upsert(entities)

        for id in devices.keys() :
            if (self.broker.exists(self.entity_from_id(id))):
                log.info(f"Entity for device {id} : OK")
            else:
                log.error(f"Entity for device {id} is not created in the context broker")

