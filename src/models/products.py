from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import ImageType
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

# from fastapi_storages.
from src.models.base import Base, BaseModel

product_type_association = Table(
    'product_type_association',
    Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('type_id', Integer, ForeignKey('type.id'))
)


class Products(BaseModel):
    __tablename__ = 'products'
    subcategory_id = Column(Integer, ForeignKey(
        "subcategory.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255))
    image = Column(ImageType(
        storage=FileSystemStorage(path="tmp")), nullable=True)

    tg_message_id = Column(String(25), nullable=True)
    subcategory = relationship("SubCategory")
    types = relationship(
        "Type", secondary=product_type_association, back_populates="products", lazy="selectin")

    def __str__(self):
        return self.name


class Type(Base):
    __tablename__ = 'type'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Define the many-to-many relationship with Product
    products = relationship(
        "Products", secondary=product_type_association, back_populates="types")

    def __str__(self):
        return self.name
