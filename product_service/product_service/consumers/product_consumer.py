from aiokafka import AIOKafkaConsumer
from product_service import settings
import json
from product_service.deps import get_session
from product_service.crud.product_crud import add_new_product
from product_service.models.product_models import Product

async def consume_product(topic, bootstrap_server):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_server,
        group_id=settings.KAFKA_CONSUMER_GROUP_ID_FOR_PRODUCT
    )
    
    await consumer.start()
    try:
        async for msg in consumer:
            product_data = json.loads(msg.value.decode())            
            with next(get_session()) as session:
                db_insert_product = add_new_product(
                    product_data=Product(**product_data), session=session
                )
                print("DB_INSERT_PRODUCT", db_insert_product)
    finally:
        await consumer.stop()