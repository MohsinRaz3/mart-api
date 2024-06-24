from sqlmodel import SQLModel, Field
    
class BaseProduct(SQLModel):
    name: str
    description: str
    price: float
    brand: str | None = None
    category: str 
    sku: str | None = None
    
class Product(BaseProduct, table=True):
    id: int | None = Field(default=None, primary_key=True)

class GetProducts(SQLModel):
    id: int
    name: str
    description: str
    price: float
    brand: str | None = None
    category: str 
    sku: str | None = None
    
class UpdateProduct(BaseProduct):
    pass

    