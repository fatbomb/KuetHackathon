from flask import Blueprint, jsonify, request
from services import IngredientService


class IngredientController:
    def __init__(self):
        self.ingredient_blueprint = Blueprint('ingredients', __name__)
        self.ingredient_service = IngredientService()
        self.register_routes()

    def register_routes(self):
        self.ingredient_blueprint.add_url_rule('/add_ingredient', view_func=self.add_ingredient, methods=['POST'])
        self.ingredient_blueprint.add_url_rule('/get_all_ingredients', view_func=self.get_all_ingredients, methods=['GET'])
        self.ingredient_blueprint.add_url_rule('/increase_ingredient/<int:ingredient_id>', view_func=self.increase_ingredient_quantity, methods=['PUT'])
        self.ingredient_blueprint.add_url_rule('/decrease_ingredient/<int:ingredient_id>', view_func=self.decrease_ingredient_quantity, methods=['PUT'])
        self.ingredient_blueprint.add_url_rule('/delete_ingredient/<int:ingredient_id>', view_func=self.delete_ingredient, methods=['DELETE'])

    def add_ingredient(self):
        """
        Add a new ingredient.
        Request body: { "name": "Tomato", "quantity": 5, "unit": "kg", 
        "category": "Vegetable" }
        """
        data = request.get_json()
        required_fields = ['name', 'quantity', 'unit']
        if not all(field in data for field in required_fields):
            return jsonify({"error": f"Missing required fields: {', '.join(required_fields)}"}), 400

        try:
            ingredient = self.ingredient_service.add_ingredient(data)
            return jsonify({
                "message": "Ingredient added successfully",
                "ingredient": {
                    "id": ingredient.id,
                    "name": ingredient.name,
                    "quantity": ingredient.quantity,
                    "unit": ingredient.unit,
                    "category": ingredient.category
                }
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_all_ingredients(self):
        """
        Retrieve all ingredients.
        """
        try:
            ingredients = self.ingredient_service.get_all_ingredients()
            data = [{
                "id": ingredient.id,
                "name": ingredient.name,
                "quantity": ingredient.quantity,
                "unit": ingredient.unit,
                "category": ingredient.category
            } for ingredient in ingredients]
            return jsonify(data), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def increase_ingredient_quantity(self, ingredient_id):
        """
        Increase the quantity of an ingredient by ID.
        Request body: { "quantity": 2 }
        """
        data = request.get_json()
        if "quantity" not in data or not isinstance(data["quantity"], (int, float)):
            return jsonify({"error": "A valid 'quantity' field is required."}), 400

        try:
            ingredient = self.ingredient_service.increase_quantity(ingredient_id, data["quantity"])
            if not ingredient:
                return jsonify({"error": "Ingredient not found"}), 404

            return jsonify({
                "message": "Ingredient quantity increased successfully",
                "ingredient": {
                    "id": ingredient.id,
                    "name": ingredient.name,
                    "quantity": ingredient.quantity,
                    "unit": ingredient.unit,
                    "category": ingredient.category
                }
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def decrease_ingredient_quantity(self, ingredient_id):
        """
        Decrease the quantity of an ingredient by ID.
        Request body: { "quantity": 2 }
        """
        data = request.get_json()
        if "quantity" not in data or not isinstance(data["quantity"], (int, float)):
            return jsonify({"error": "A valid 'quantity' field is required."}), 400

        try:
            ingredient = self.ingredient_service.decrease_quantity(ingredient_id, data["quantity"])
            if not ingredient:
                return jsonify({"error": "Ingredient not found"}), 404

            return jsonify({
                "message": "Ingredient quantity decreased successfully",
                "ingredient": {
                    "id": ingredient.id,
                    "name": ingredient.name,
                    "quantity": ingredient.quantity,
                    "unit": ingredient.unit,
                    "category": ingredient.category
                }
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def delete_ingredient(self, ingredient_id):
        """
        Delete an ingredient by ID.
        """
        try:
            success = self.ingredient_service.delete_ingredient(ingredient_id)
            if not success:
                return jsonify({"error": "Ingredient not found"}), 404

            return jsonify({"message": "Ingredient deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


# Initialize the controller and blueprint
ingredient_controller = IngredientController()
ingredient_blueprint = ingredient_controller.ingredient_blueprint
