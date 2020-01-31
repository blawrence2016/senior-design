from typing import List

from app.exceptions.InvalidInputsException import InvalidInputsError
from app.models.model_manager import ModelManager
from flask import Blueprint, request

models = Blueprint(
    "models", __name__, template_folder="templates", static_folder="static"
)

MODEL_MANAGER = ModelManager()


@models.route("/models/test", methods=["GET"])
def test():
    """ route to test model endpoints """
    return "test"


@models.route("/models/create", methods=["POST"])
def create():
    """ Route for creating models """

    global MODEL_MANAGER
    returnJSON = createJSON()

    try:
        model_data = request.get_json()
        MODEL_MANAGER.create_model(model_data)
        return addMessageToJSON(returnJSON, "success")
    except InvalidInputsError:
        return addMessageToJSON(returnJSON, "failure")


@models.route("/models/delete", methods=["POST"])
def delete():
    """ Route for deleting models """

    global MODEL_MANAGER
    returnJSON = createJSON()

    try:
        model_data = request.get_json()
        MODEL_MANAGER.delete_model(model_data)
        return addMessageToJSON(returnJSON, "success")
    except InvalidInputsError:
        return addMessageToJSON(returnJSON, "failure")


@models.route("/models/search/", methods=["POST"])
def search():
    """ Route for searching models """

    global MODEL_MANAGER
    global modelsArr
    returnJSON = createJSON()

    filter = request.json["filter"]
    try:
        limit = int(request.json["limit"])
    except:
        limit = 1000

    try:
        model_list = MODEL_MANAGER.get_models(filter, limit)
        returnJSON = addModelsTOJSON(
            addMessageToJSON(returnJSON, "success"), [model_list]
        )
        return returnJSON
    except:
        return addMessageToJSON(returnJSON, "failure")


@models.route("/models/edit", methods=["POST"])
def edit():
    """ Route for editing models """

    global MODEL_MANAGER
    returnJSON = createJSON()

    try:
        model_data = request.get_json()
        MODEL_MANAGER.edit_model(model_data)
        return addMessageToJSON(returnJSON, "success")
    except:
        return addMessageToJSON(returnJSON, "failure")

    return addMessageToJSON(returnJSON, "success")


@models.route("/models/detailview", methods=["POST"])
def detail_view():
    """ Route for table view of models """

    global MODEL_MANAGER
    global modelsArr

    model_data = request.get_json()
    model = MODEL_MANAGER.detail_view(model_data)

    returnJSON = createJSON()
    returnJSON = addModelsTOJSON(addMessageToJSON(returnJSON, "success"), [model])

    return returnJSON


def createJSON() -> dict:
    return {"metadata": "none"}


def addMessageToJSON(json, message) -> dict:
    json["message"] = message
    return json


def addModelsTOJSON(json, modelsArr: List[str]) -> dict:
    json["models"] = modelsArr
    return json
