from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from database.database import Base

class RecipeItem(Base):
    __tablename__ = "Recipe_Item"

    recipe_id = Column(
        Integer,
        ForeignKey("Recipe.id"),
        primary_key=True
    )
    item_id = Column(
        Integer,
        ForeignKey("Item.id"),
        primary_key=True
    )

    amount = Column(Numeric, nullable=False)

    recipe = relationship("Recipe", back_populates="recipe_itens")
    item = relationship("Item", back_populates="recipe_itens")
