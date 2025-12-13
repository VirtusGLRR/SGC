from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from database.database import Base

class Recipe(Base):
    __tablename__ = "Recipe"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    steps = Column(Text, nullable=False)
    description = Column(Text)

    recipe_itens = relationship(
        "RecipeItem",
        back_populates="recipe",
        cascade="all, delete-orphan"
    )
