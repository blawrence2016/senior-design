from app.dal.instance_table import InstanceTable
from app.dal.model_table import ModelTable
from app.data_models.instance import Instance
from app.exceptions.InvalidInputsException import InvalidInputsError
from app.instances.instance_validator import InstanceValidator


class InstanceManager:
    def __init__(self):
        self.table = InstanceTable()
        self.model_table = ModelTable()
        self.validate = InstanceValidator()

    def create_instance(self, instance_data):
        # try:
        # try:
        new_instance = self.make_instance(instance_data)
        if type(new_instance) is InvalidInputsError:
            return new_instance
        print(new_instance)
        # except InvalidInputsError as e:
        #     return e.message
        create_validation_result = "success"
        print(create_validation_result)
        # try:
        create_validation_result = self.validate.create_instance_validation(
            new_instance
        )
        # except InvalidInputsError as e:
        #     return e.message
        if create_validation_result == "success":
            self.table.add_instance(new_instance)
        else:
            return InvalidInputsError(create_validation_result)
        # except:
        #     raise InvalidInputsError(
        #         "An error occurred when attempting to create the instance."
        #     )

    def delete_instance(self, instance_data):
        rack = self.check_null(instance_data["rack"])
        rack_u = self.check_null(instance_data["rack_u"])

        if rack == "":
            raise InvalidInputsError("Must provide a vendor")
        if rack_u == "":
            raise InvalidInputsError("Must provide a model number")

        try:
            self.table.delete_instance_by_rack_location(rack, rack_u)
        except:
            raise InvalidInputsError(
                "An error occurred when trying to delete the specified instance."
            )

    def detail_view(self, instance_data):
        print(instance_data)
        rack = self.check_null(instance_data["rack"])
        rack_u = self.check_null(instance_data["rack_u"])

        # try:
        print("Get these things")
        print(rack)
        print(rack_u)
        instance = self.table.get_instance_by_rack_location(rack, rack_u)
        return instance
        # except:
        #     raise InvalidInputsError(
        #         "An error occured while retrieving data for this instance."
        #     )

    def edit_instance(self, instance_data):
        original_rack = instance_data.get("rackOriginal")
        original_rack_u = instance_data.get("rack_uOriginal")
        if original_rack is None or original_rack_u is None:
            raise InvalidInputsError("Unable to find the instance to edit.")

        new_instance = self.make_instance(instance_data)
        if type(new_instance) is InvalidInputsError:
            return new_instance
        self.table.edit_instance(new_instance, original_rack, original_rack_u)

    def get_instances(self, filter, limit: int):
        model_name = filter.get("model")

        try:
            if model_name is not None:
                model_id = self.get_model_id_from_name(model_name)
            else:
                model_id = None
        except:
            raise InvalidInputsError(
                "An error occurred while trying to filter by model name. Please input a different model name"
            )

        hostname = filter.get("hostname")
        rack_label = filter.get("rack")
        rack_u = filter.get("rack_u")

        try:
            instance_list = self.table.get_instances_with_filters(
                model_id=model_id,
                hostname=hostname,
                rack_label=rack_label,
                rack_u=rack_u,
                limit=limit,
            )
            return instance_list
        except:
            raise InvalidInputsError(
                "An error occurred while trying to retrieve instance data."
            )

    def get_possible_models_with_filters(self, prefix_json):
        try:
            return_list = []
            # prefix = prefix_json.get("input")
            # if prefix is None:
            #     prefix = ""

            model_list = self.model_table.get_all_models()
            for model in model_list:
                model_name = model.vendor + " " + model.model_number
                # if model_name.startswith(prefix):
                return_list.append(model_name)

            return return_list
        except:
            raise InvalidInputsError(
                "An error occurred while trying to retrieve model options."
            )

    def make_instance(self, instance_data):
        print("instance data")
        print(instance_data)
        model_name = self.check_null(instance_data["model"])
        model_id = self.get_model_id_from_name(model_name)

        try:
            hostname = self.check_null(instance_data["hostname"])
            rack = self.check_null(instance_data["rack"])
            rack_u = self.check_null(instance_data["rack_u"])
            owner = self.check_null(instance_data["owner"])
            comment = self.check_null(instance_data["comment"])
        except:
            raise InvalidInputsError(
                "Could not read data fields correctly. Client-server error occurred."
            )

        if hostname == "":
            return InvalidInputsError("Must provide a hostname")
        if rack == "":
            return InvalidInputsError("Must provide a rack location")
        if rack_u == "":
            return InvalidInputsError("Must provide a rack location")

        print("about to make instance")
        return Instance(model_id, hostname, rack, rack_u, owner, comment)

    def get_model_id_from_name(self, model_name):
        data = model_name.split(" ")
        print(data)
        if len(data) == 0:
            return None
        if len(data) != 2:
            return -1

        vendor = data[0]
        model_number = data[1]
        # if len(data) > 2:
        #     raise InvalidInputsError("Invalid model name.")
        # vendor = data[0]
        # model_number = ""
        # if len(data) > 1:
        #     model_number = data[1]

        try:
            model_id = self.model_table.get_model_id_by_vendor_number(
                vendor, model_number
            )
            if model_id is None:
                # raise InvalidInputsError("Invalid model name.")
                model_id = -1

            return model_id
        except:
            raise InvalidInputsError(
                "An error occurred while trying to retrieve model info corresponding to the instance."
            )

    def get_model_name_from_id(self, model_id):
        model = self.model_table.get_model(model_id)
        if model is None:
            raise InvalidInputsError(
                "An error occurred while trying to retrieve model info corresponding to the instance."
            )

        return model.vendor + " " + model.model_number

    def check_null(self, val):
        if val is None:
            return ""
        else:
            return val
