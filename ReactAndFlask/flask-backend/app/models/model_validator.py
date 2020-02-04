import re

from app.dal.instance_table import InstanceTable
from app.dal.model_table import ModelTable


class ModelValidator:
    def __init__(self):
        self.model_table = ModelTable()
        self.instance_table = InstanceTable()

    def create_model_validation(self, model):
        result = self.model_table.get_model_id_by_vendor_number(
            model.vendor, model.model_number
        )
        print("RESULT")
        print(result)
        if result is not None:
            return "This vendor and model number combination already exists."
        pattern = re.compile("[0-9]+")
        if pattern.fullmatch(str(model.height)) is None:
            return "The value for model height must be a positive integer."
        if (
            model.ethernet_ports != ""
            and model.ethernet_ports != None
            and pattern.fullmatch(str(model.ethernet_ports)) is None
        ):
            return "The value for ethernet ports must be a positive integer."
        if (
            model.power_ports != ""
            and model.power_ports != None
            and pattern.fullmatch(str(model.power_ports)) is None
        ):
            return "The value for power ports must be a positive integer."
        if model.memory != "" and pattern.fullmatch(str(model.memory)) is None:
            return "The value for memory must be a positive integer in terms of GB."

        return "success"

    def edit_model_validation(self, model):
        pattern = re.compile("[0-9]+")
        if pattern.fullmatch(str(model.height)) is None:
            return "The value for model height must be a positive integer."
        if (
            model.ethernet_ports != ""
            and pattern.fullmatch(str(model.ethernet_ports)) is None
        ):
            return "The value for ethernet ports must be a positive integer."
        if (
            model.power_ports != ""
            and pattern.fullmatch(str(model.power_ports)) is None
        ):
            return "The value for ethernet ports must be a positive integer."
        if (
            model.memory != ""
            and model.memory != None
            and pattern.fullmatch(str(model.memory)) is None
        ):
            return "The value for memory must be a positive integer in terms of GB."

        return "success"

    def delete_model_validation(self, vendor, model_number):
        model_id = self.model_table.get_model_id_by_vendor_number(vendor, model_number)
        print("MODEL_ID")
        print(model_id)
        if self.instance_table.get_instances_by_model_id(model_id) is None:
            return "success"
        else:
            result = "There are still existing instances for this model. "
            result += "Please delete them before deleting the model."
            return result
