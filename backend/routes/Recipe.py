from flask_restx import Namespace, Resource, fields
from ..models import Recipe
from flask_jwt_extended import jwt_required
from flask import request

recipe_ns = Namespace("recipe", description="a namespace for recipe")

recipes_model = recipe_ns.model(
    "Recipe",
    {
        "id":fields.Integer(),
        "title": fields.String(),
        "description": fields.String()
    }
)

recipe_model = recipe_ns.model(
    "Recipe",
    {
        "title": fields.String(),
        "description": fields.String()
    }
)

@recipe_ns.route("/recipes")
class RecipeResources(Resource):
    @recipe_ns.marshal_list_with(recipes_model)
    @jwt_required()
    def get(self):
        """get all recipes"""
        recipes = Recipe.query.all()
        return recipes

    @recipe_ns.marshal_with(recipe_model)
    @recipe_ns.expect(recipe_model)
    # @jwt_required
    def post(self):
        """this method helps in creating a post"""
        data = request.get_json()
        new_recipe = Recipe(title=data.get("title"), description=data.get("description"))
        new_recipe.save()
        return new_recipe,201