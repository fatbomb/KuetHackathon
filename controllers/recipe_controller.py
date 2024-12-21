from flask import Blueprint, request, jsonify
import os
from services import RecipeService
from models import db, Ingredient, IngredientsForRecipe

# Create a Blueprint for the recipe controller
recipe_controller = Blueprint('recipe_controller', __name__)
recipe_service = RecipeService()

# Upload recipe endpoint
@recipe_controller.route('/upload_recipe', methods=['POST'])
def upload_recipe():
    try:
        # Extract data from the request
        file = request.files.get('file')
        recipe_data = {
            "name": request.form.get('name'),
            "taste": request.form.get('taste', 'Unknown'),
            "cuisine_type": request.form.get('cuisine_type', 'Unknown'),
            "preparation_time": int(request.form.get('preparation_time', 0)),
            "reviews": float(request.form.get('reviews', 0.0)),
            "instructions": request.form.get('instructions')
        }
        ingredients = request.form.getlist('ingredients')  # List of ingredients

        # Handle file upload
        if file:
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)
            recipe_data["image_path"] = file_path

        # Validate required fields
        if not recipe_data["name"] or not recipe_data["instructions"] or not ingredients:
            return jsonify({"message": "Recipe details are missing"}), 400

        # Add recipe via service
        recipe = recipe_service.add_recipe(recipe_data)

        # Handle ingredients
        for ingredient_name in ingredients:
            ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
            if not ingredient:
                ingredient = Ingredient(name=ingredient_name, quantity=0.0)
                db.session.add(ingredient)
                db.session.commit()

            ingredients_for_recipe = IngredientsForRecipe(recipe=recipe.id, ingredient=ingredient.id)
            db.session.add(ingredients_for_recipe)

        db.session.commit()

        return jsonify({"message": "Recipe added successfully", "recipe_id": recipe.id}), 201

    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
