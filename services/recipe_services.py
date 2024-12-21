from models import db, Recipe


class RecipeService:
    def add_recipe(self, data):
        recipe = Recipe(
            name=data['name'],
            taste=data['taste'],
            cuisine_type=data['cuisine_type'],
            preparation_time=data['preparation_time'],
            reviews=data.get('reviews'),
            instructions=data['instructions'],
            image_path=data.get('image_path')
        )
        db.session.add(recipe)
        db.session.commit()
        return recipe

    def get_all_recipes(self):
        return Recipe.query.all()

    def update_recipe(self, recipe_id, data):
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            return None
        recipe.name = data.get('name', recipe.name)
        recipe.taste = data.get('taste', recipe.taste)
        recipe.cuisine_type = data.get('cuisine_type', recipe.cuisine_type)
        recipe.preparation_time = data.get('preparation_time',
                                           recipe.preparation_time)
        recipe.reviews = data.get('reviews', recipe.reviews)
        recipe.instructions = data.get('instructions', recipe.instructions)
        recipe.image_path = data.get('image_path', recipe.image_path)
        db.session.commit()
        return recipe

    def delete_recipe(self, recipe_id):
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            return False
        db.session.delete(recipe)
        db.session.commit()
        return True
