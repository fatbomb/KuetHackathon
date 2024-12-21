from models import db, IngredientsForRecipe


class IngredientsForRecipeService:
    def add_ingredient_to_recipe(self, recipe_id, data):
        ingredient_for_recipe = IngredientsForRecipe(
            recipe_id=recipe_id,
            ingredient_id=data['ingredient_id'],
            quantity=data['quantity'],
            unit=data['unit']
        )
        db.session.add(ingredient_for_recipe)
        db.session.commit()
        return ingredient_for_recipe

    def get_ingredients_for_recipe(self, recipe_id):
        return IngredientsForRecipe.query.filter_by(recipe_id=recipe_id).all()
