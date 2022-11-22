import asyncio
from bleak import BleakScanner, BleakClient
import xml.etree.ElementTree as ET
import queue

#EXAMPLE profile.service['TENS'].char['left'].uuid

class GATT_Char():
    def __init__(self, char_uuid, char_permission):
        self.uuid = char_uuid
        self.value = None
        self.permission = char_permission

class GATT_Service():
    def __init__(self, serv_uuid, char_dict:dict):
        self.uuid = serv_uuid
        self.char = char_dict

class GATT_Profile():
    def __init__(self, services_dict:dict):
        self.services = services_dict


class GATT_Client(BleakClient):
    def __init__(self, dev_name = 'Arduino_Nano_33_iot'):
        self.parseXML('./Game/references/Server_'+dev_name+'.xml')

        super().__init__(self.client_uuid)

    def parseXML(self, xmlfile):
        tree = ET.parse(xmlfile)
        self.root = tree.getroot()
        self.name = self.root.attrib['name']
        self.client_uuid = self.root.attrib['uuid']

        characteristics = {}
        services = {}

        for parent in self.root:
            for child in parent:
                for child_child in child:
                    characteristics[child.attrib['name']] = GATT_Char(child.attrib['uuid'], child_child.attrib)
            services[parent.attrib['name']] = GATT_Service(parent.attrib['uuid'], characteristics)

        self.profile = GATT_Profile(services)

    async def GATT_connect(self):
        try:
            await self.connect()
        except Exception as e:
            print(e)
    
    async def GATT_disconnect(self, *args):
        try:
            await self.disconnect()
        except Exception as e:
            print(e+'\nCould Not Disconnect From Arduino')
    
    async def GATT_write(self, service:str, char:str, val:int):
        try:
            await self.write_gatt_char(self.profile.service[service].char[char].uuid, bytearray(val))
        except Exception as e:
            pass

    async def GATT_read(self):
        pass

    async def GATT_notify(self):
        pass
    
    async def execute_queue(self, q1:queue.Queue):
        while(not q1.empty()):
            task = q1.get()
            func = getattr(self, 'GATT_'+task['Command'])
            await func(task['Service'], task['Characteristic'], task['Value'])


async def ble_main(q_to_ble, q_from_ble):
    client = GATT_Client()
    await client.GATT_connect()

    #Setup

    while(1):
        if client.is_connected:
            await client.execute_queue(q_to_ble)
        else:
            break



