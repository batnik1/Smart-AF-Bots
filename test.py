import logging

#Creating Log File
logging.basicConfig(filename="Warehouse.log",format='%(asctime)s %(message)s',filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)
for i in range(10):
    logger.info('Hello')