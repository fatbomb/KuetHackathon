from models import db, Ingredient


class IngredientService:
    def add_ingredient(self, data):
        ingredient = Ingredient(
            name=data['name'],
            quantity=data['quantity'],
            unit=data['unit'],
            category=data.get('category')
        )
        db.session.add(ingredient)
        db.session.commit()
        return ingredient

    def get_all_ingredients(self):
        return Ingredient.query.all()

    def update_ingredient(self, ingredient_id, data):
        ingredient = Ingredient.query.get(ingredient_id)
        if not ingredient:
            return None
        ingredient.name = data.get('name', ingredient.name)
        ingredient.quantity = data.get('quantity', ingredient.quantity)
        ingredient.unit = data.get('unit', ingredient.unit)
        ingredient.category = data.get('category', ingredient.category)
        db.session.commit()
        return ingredient

    def delete_ingredient(self, ingredient_id):
        ingredient = Ingredient.query.get(ingredient_id)
        if not ingredient:
            return False
        db.session.delete(ingredient)
        db.session.commit()
        return True