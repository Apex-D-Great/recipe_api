from flask_restx import Namespace, Resource, fields
from ..models import Recipe
from flask_jwt_extended import jwt_required
from flask import request, jsonify

authorizations = {
    "apikey":{
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}
recipe_ns = Namespace("recipe", 
                      description="a simple recipe blog endpoint which contains just title and description",
                      authorizations=authorizations)

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
    # @jwt_required()
    @recipe_ns.doc(security="apikey")
    def get(self):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            error_message = 'Authorization header is missing.'
            return jsonify({'error': error_message}), 401
        """get all recipes"""
        recipes = Recipe.query.all()
        return recipes
    
    
    @recipe_ns.marshal_with(recipe_model)
    @recipe_ns.expect(recipe_model)
    # @jwt_required()
    @recipe_ns.doc(security="apikey")
    def post(self):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            error_message = 'Authorization header is missing.'
            return jsonify({'error': error_message}), 401
        """this method helps in creating a post"""
        data = request.get_json()
        new_recipe = Recipe(title=data.get("title"), description=data.get("description"))
        new_recipe.save()
        return new_recipe,201