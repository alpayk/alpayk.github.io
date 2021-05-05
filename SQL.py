import hazelcast
import time
import json
#import pyodbc
import jaydebeapi
import jpype
import jpype.imports
from datetime import datetime
from hazelcast.config import NearCacheConfig, IN_MEMORY_FORMAT, EVICTION_POLICY

BULK_SIZE = 1000
STRUCTURE_MAP_NAME = 'coolgenlookup'
ATTRIBUTE_MAP_NAME = 'desiredlogfieldslookup'

config = hazelcast.ClientConfig()

config.network_config.addresses.append('10.151.160.77:5701')
config.network_config.addresses.append('10.151.161.87:5701')
config.network_config.addresses.append('10.151.161.94:5701')
config.network_config.smart_routing = True

client = hazelcast.HazelcastClient(config)

structure_map = client.get_map(STRUCTURE_MAP_NAME).blocking()
attribute_map = client.get_map(ATTRIBUTE_MAP_NAME).blocking()

#item = attribute_map.get('ZJP5:JP1FP51I')
#print(item)
#exit(1)

#structure_map.destroy()
#attribute_map.destroy()
#exit()

conn = jaydebeapi.connect('com.microsoft.sqlserver.jdbc.SQLServerDriver', 'jdbc:sqlserver://RHYSALS:1663;user=SurecWebUser;password=Ko4g}Hj+', [], 'C:\\Users\\AlpayKa\\Desktop\\sqljdbc_9.2\\enu\\mssql-jdbc-9.2.1.jre8.jar')
cursor = conn.cursor()
cursor.execute('''
SELECT load_module_name_text, procedure_step_name_text, entity_text, variable_text, variable_type, sequence_num, firm_code
FROM [SURECWEBDB].[dbo].[T_source_structure_info] WITH(NOLOCK)
WHERE variable_type = 'Input'
AND status = 1
AND environment_code = 'PROD'
ORDER BY load_module_name_text, procedure_step_name_text, firm_code, sequence_num ASC
''')

key = None
value = {}
items = {}

start_time = time.time()

row = cursor.fetchone()
while row is not None:
    temp_key = f'{row[0]}:{row[1]}:{row[6]}'

    if key != temp_key:
        if key != None:
            items[key] = json.dumps(value)
            if len(items) == BULK_SIZE:
                structure_map.put_all(items)
                print(f'[{datetime.now().strftime("%H:%M:%S")}] - {BULK_SIZE} items was added')
                items = {}

        value = {'load_module_name_text': row[0], 'procedure_step_name_text': row[1], 'firm_code': row[6], f'_p{row[5]}': row[3] }
        key = temp_key
    else:
        value[f'_p{row[5]}'] = row[3]
    row = cursor.fetchone()

items[key] = json.dumps(value)
structure_map.put_all(items)
print(f'[{datetime.now().strftime("%H:%M:%S")}] - {len(items)} items was added')
print('T_source_structure_info loaded in  %s seconds\n' % (time.time() - start_time))

cursor.execute('''
SELECT transaction_name_text ,load_module_name_text, attribute_text, domain_text
FROM [SURECWEBDB].[dbo].[T_txn_entity_attribute_relation]
WHERE status = 1
ORDER BY transaction_name_text, load_module_name_text, attribute_text ASC
''')

key = None
value = {}
items = {}
p_count = 1

start_time = time.time()

row = cursor.fetchone()
while row is not None:
    temp_key = f'{row[0]}:{row[1]}'

    if key != temp_key:
        if key != None:
            items[key] = json.dumps(value)
            if len(items) == BULK_SIZE:
                attribute_map.put_all(items)
                print(f'[{datetime.now().strftime("%H:%M:%S")}] - {BULK_SIZE} items was added')
                items = {}

        p_count = 1
        value = {'transaction_name_text': row[0], 'load_module_name_text': row[1], f'_p{p_count}': {'attribute_text': row[2], 'domain_text': row[3]} }
        key = temp_key
    else:
        value[f'_p{p_count}'] = {'attribute_text': row[2], 'domain_text': row[3]}
    p_count = p_count + 1
    row = cursor.fetchone()

items[key] = json.dumps(value)
attribute_map.put_all(items)
print(f'[{datetime.now().strftime("%H:%M:%S")}] - {len(items)} items was added')
print('T_txn_entity_attribute_relation loaded in  %s seconds\n' % (time.time() - start_time))
