import asyncio
from bleak import BleakScanner, BleakClient
import xml.etree.ElementTree as ET
import queue
import threading
import time

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
    def __init__(self, q_from_ble, dev_name = 'Arduino_Nano_33_iot'):
        self.parseXML('./Game/references/Server_'+dev_name+'.xml')

        self.q_from_ble = q_from_ble

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
            print('Succesfully Connected to Arduino')
        except Exception as e:
            print(e)
    
    async def GATT_disconnect(self, *args):
        try:
            await self.disconnect()
        except Exception as e:
            print(e+'\nCould Not Disconnect From Arduino')
    
    async def GATT_write(self, service:str, char:str, val:int):
        try:
            print('writting')
            await self.write_gatt_char(self.profile.services[service].char[char].uuid, bytearray(val))
            print('finished writting')
        except Exception as e:
            pass

    async def GATT_read(self, service:str, char:str, val):
        if self.is_connected:
            result = await self.read_gatt_char(self.profile.services[service].char[char].uuid)
            result=int.from_bytes(result, 'little')
            self.q_from_ble.put(result)
    
    def GSR_callback(self, sender:int, data:bytearray):
        print(data)
        self.q_from_ble.put(data)

    async def GATT_start_notify(self, service:str, char:str, val):
        print('notify_started')
        await self.start_notify(self.profile.services[service].char[char].uuid, self.GSR_callback)
    
    async def GATT_stop_notify(self, service:str, char:str, val):
        print('notify_ended')
        await self.stop_notify(self.profile.services[service].char[char].uuid)
    
    async def execute_queue(self, q1:queue.Queue):
        while(not q1.empty()):
            task = q1.get()
            func = getattr(self, 'GATT_'+task['Command'])
            await func(task['Service'], task['Characteristic'], task['Value'])

async def ble_main(q_to_ble, q_from_ble):
    client = GATT_Client(q_from_ble)
    await client.GATT_connect()

    while(1):
        if client.is_connected:
            await client.execute_queue(q_to_ble)
            await asyncio.sleep(0.001)
        else:
            break



