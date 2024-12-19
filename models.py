from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Buyer(Base):
    __tablename__ = "buyers"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    items = relationship("Item", back_populates="buyer", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Buyer(id={self.id}, name='{self.name}', email='{self.email}')"


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    buyer_id = Column(Integer, ForeignKey("buyers.id"))

    buyer = relationship("Buyer", back_populates="items")

    def __repr__(self):
        return f"Item(id={self.id}, name='{self.name}', price={self.price}, buyer_id={self.buyer_id})"

# Example functions for CRUD operations and relationships
def create_buyer(session, name, email):
    new_buyer = Buyer(name=name, email=email)
    session.add(new_buyer)
    session.commit()
    return new_buyer

def update_buyer(session, buyer_id, name=None, email=None):
    buyer = session.query(Buyer).filter_by(id=buyer_id).first()
    if buyer:
        if name:
            buyer.name = name
        if email:
            buyer.email = email
        session.commit()
    return buyer

def delete_buyer(session, buyer_id):
    buyer = session.query(Buyer).filter_by(id=buyer_id).first()
    if buyer:
        session.delete(buyer)
        session.commit()


def list_all_buyers(session):
    return session.query(Buyer).all()

def view_items_for_buyer(session, buyer_id):
    buyer = session.query(Buyer).filter_by(id=buyer_id).first()
    if buyer:
        return buyer.items
    return []
