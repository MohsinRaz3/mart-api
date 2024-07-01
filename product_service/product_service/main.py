import asyncio
import json
from product_service import settings 
from fastapi import FastAPI, HTTPException,Depends
from sqlmodel import SQLModel, Session
from typing import Annotated,AsyncGenerator
from contextlib import asynccontextmanager
from product_service.database_engine import engine
from product_service.models.product_models import Product, GetProducts, UpdateProduct
from product_service.deps import get_session, get_kafka_producer
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from product_service.crud.product_crud import get_all_products, get_product_by_id, update_product_by_id, delete_product_by_id, validate_product_by_id, add_new_product
from product_service.consumers.product_consumer import consume_product

def create_database():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def life_span(app:FastAPI)-> AsyncGenerator[None, None]:
    task = asyncio.create_task(consume_product(
        settings.KAFKA_PRODUCT_TOPIC, 'broker:19092'
    ))
    create_database()
    yield
    

app = FastAPI(title="Product services", 
    version="0.0.1",
    servers=[{"url": "http://127.0.0.1:8003","description": "Development Server" }],
    lifespan=life_span)

@app.get("/root")
async def home_route():
    return {"message":"hello from homie"}



@app.post("/products/", response_model=Product)
async def create_new_product(product: Product, session: Annotated[Session, Depends(get_session)], producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    """ Create a new product and send it to Kafka"""

    product_dict = {field: getattr(product, field) for field in product.dict()}
    product_json = json.dumps(product_dict).encode("utf-8")
    print("product_JSON:", product_json)
    # Produce message
    try:
        await producer.send_and_wait(settings.KAFKA_PRODUCT_TOPIC, product_json)
        # new_product = add_new_product(product, session)
    finally:
        await producer.stop()
        return product


@app.get("/products/all", response_model=list[GetProducts])
def call_all_products(session: Annotated[Session, Depends(get_session)]):
    """ Get all products from the database"""
    return get_all_products(session)


@app.get("/products/{product_id}", response_model=Product)
def get_single_product(product_id: int, session: Annotated[Session, Depends(get_session)]):
    """ Get a single product by ID"""
    try:
        return get_product_by_id(product_id=product_id, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/products/{product_id}", response_model=dict)
def delete_single_product(product_id: int, session: Annotated[Session, Depends(get_session)]):
    """ Delete a single product by ID"""
    try:
        return delete_product_by_id(product_id=product_id, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/products/{product_id}", response_model=Product)
def update_single_product(product_id: int, product: UpdateProduct, session: Annotated[Session, Depends(get_session)]):
    """ Update a single product by ID"""
    try:
        return update_product_by_id(product_id=product_id, to_update_product_data=product, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
