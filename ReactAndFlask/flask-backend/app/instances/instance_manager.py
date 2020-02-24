from app.constants import Constants
from app.dal.datacenter_table import DatacenterTable
from app.dal.instance_table import InstanceTable
from app.dal.model_table import ModelTable
from app.data_models.instance import Instance
from app.exceptions.InvalidInputsException import InvalidInputsError
from app.instances.instance_validator import InstanceValidator


class InstanceManager:
    def __init__(self):
        self.table = InstanceTable()
        self.model_table = ModelTable()
        self.dc_table = DatacenterTable()
        self.validate = InstanceValidator()

    def create_instance(self, instance_data):
        try:
            try:
                new_instance = self.make_instance(instance_data)
                if type(new_instance) is InvalidInputsError:
                    return new_instance
                print(new_instance)
            except InvalidInputsError as e:
                return e.message
            create_validation_result = Constants.API_SUCCESS
            print(create_validation_result)
            try:
                create_validation_result = self.validate.create_instance_validation(
                    new_instance
                )
                if create_validation_result != Constants.API_SUCCESS:
                    raise InvalidInputsError(create_validation_result)
            except InvalidInputsError as e:
                raise InvalidInputsError(e.message)

            try:
                print("Creating instance")
                self.table.add_instance(new_instance)

                print("Attempting to add other connections")
                connect_result = self.make_corresponding_connections(
                    new_instance.network_connections, new_instance.hostname
                )
                print(connect_result)
                if connect_result != Constants.API_SUCCESS:
                    self.table.delete_instance_by_asset_number(
                        new_instance.asset_number
                    )
                    return connect_result
            except:
                raise InvalidInputsError("Unable to create instance")
        except:
            raise InvalidInputsError(
                "An error occurred when attempting to create the instance."
            )

    def delete_instance(self, instance_data):
        asset_number = self.check_null(instance_data[Constants.ASSET_NUMBER_KEY])

        if asset_number == "":
            raise InvalidInputsError("Must provide an asset number")

        try:
            self.table.delete_instance_by_asset_number(asset_number)
        except:
            raise InvalidInputsError(
                "An error occurred when trying to delete the specified asset."
            )

    def detail_view(self, instance_data):
        print(instance_data)
        asset_number = instance_data.get(Constants.ASSET_NUMBER_KEY)

        try:
            print("Get these things")
            print(asset_number)
            instance = self.table.get_instance_by_asset_number(asset_number)
            return instance
        except:
            raise InvalidInputsError(
                "An error occured while retrieving data for this asset."
            )

    def edit_instance(self, instance_data):
        print("INSTANCE DATA")
        print(instance_data)
        try:
            original_asset_number = instance_data.get(Constants.ASSET_NUMBER_ORIG_KEY)
            if original_asset_number is None:
                raise InvalidInputsError("Unable to find the asset to edit.")

            new_instance = self.make_instance(instance_data)
            if type(new_instance) is InvalidInputsError:
                return new_instance
            edit_validation_result = self.validate.edit_instance_validation(
                new_instance, original_asset_number
            )
            if edit_validation_result != Constants.API_SUCCESS:
                return InvalidInputsError(edit_validation_result)
        except InvalidInputsError as e:
            return e.message
        if edit_validation_result == Constants.API_SUCCESS:
            self.table.edit_instance(new_instance, original_asset_number)
        else:
            return InvalidInputsError(edit_validation_result)

        self.table.edit_instance(new_instance, original_asset_number)

    def get_instances(self, filter, dc_name, limit: int):
        model_name = filter.get(Constants.MODEL_KEY)

        try:
            if model_name is not None and model_name != "":
                print("MODEL_NAME")
                print(model_name)
                model_id = self.get_model_id_from_name(model_name)
            else:
                model_id = None
        except:
            raise InvalidInputsError(
                "An error occurred while trying to filter by model name. Please input a different model name"
            )

        try:
            if dc_name is not None:
                dc_id = self.get_datacenter_id_from_name(dc_name)
                if dc_id == -1:
                    dc_id = None
        except:
            raise InvalidInputsError(
                "An error occurred while trying to filter by datacenter name. Please input a different model name"
            )

        hostname = filter.get(Constants.HOSTNAME_KEY)
        rack_label = filter.get(Constants.RACK_KEY)
        rack_position = filter.get(Constants.RACK_POSITION_KEY)

        try:
            instance_list = self.table.get_instances_with_filters(
                model_id=model_id,
                hostname=hostname,
                rack_label=rack_label,
                rack_position=rack_position,
                datacenter_id=dc_id,
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
        model_name = self.check_null(instance_data[Constants.MODEL_KEY])
        model_id = self.get_model_id_from_name(model_name)

        print("1")
        datacenter_name = self.check_null(instance_data[Constants.DC_NAME_KEY])
        print("2")
        datacenter_id = self.get_datacenter_id_from_name(datacenter_name)
        print("3")
        try:
            hostname = self.check_null(instance_data[Constants.HOSTNAME_KEY])
            print("4")
            rack = self.check_null(instance_data[Constants.RACK_KEY].upper())
            print("5")
            rack_position = self.check_null(instance_data[Constants.RACK_POSITION_KEY])
            print("6")
            owner = self.check_null(instance_data[Constants.OWNER_KEY])
            print("7")
            comment = self.check_null(instance_data[Constants.COMMENT_KEY])
            network_connections = self.check_null(
                instance_data[Constants.NETWORK_CONNECTIONS_KEY]
            )
            print("10")
            power_connections = self.check_null(
                instance_data[Constants.POWER_CONNECTIONS_KEY]
            )
            print("11")
            asset_number = self.check_null(instance_data[Constants.ASSET_NUMBER_KEY])
        except:
            raise InvalidInputsError(
                "Could not read data fields correctly. Client-server error occurred."
            )
        print("12")
        if rack == "":
            return InvalidInputsError("Must provide a rack location")
        print("13")
        if rack_position == "":
            return InvalidInputsError("Must provide a rack location")
        print("14")
        if asset_number == "":
            return InvalidInputsError("Must provide an asset number")

        print(network_connections)
        print(type(network_connections))
        print("about to make instance")
        return Instance(
            model_id,
            hostname,
            rack,
            rack_position,
            owner,
            comment,
            datacenter_id,
            network_connections,
            power_connections,
            asset_number,
        )

    def get_model_id_from_name(self, model_name):
        try:
            model_list = self.model_table.get_all_models()
            print("MODEL_LIST")
            print(model_list)
            for model in model_list:
                if model.vendor + " " + model.model_number == model_name:
                    print("FOUND MATCH")
                    model_id = self.model_table.get_model_id_by_vendor_number(
                        model.vendor, model.model_number
                    )
                    if model_id is None:
                        print("MODEL_ID = -1")
                        # raise InvalidInputsError("Invalid model name.")
                        model_id = -1

                    print("MODEL_ID")
                    print(model_id)
                    return model_id
            return -1
        except:
            raise InvalidInputsError(
                "An error occurred while trying to retrieve model info corresponding to the instance."
            )

    def get_datacenter_id_from_name(self, datacenter_name):
        try:
            datacenter_id = self.dc_table.get_datacenter_id_by_name(datacenter_name)
            if datacenter_id is None:
                return -1
            return datacenter_id
        except:
            raise InvalidInputsError(
                "An error occurred while trying to retrieve datacenter info corresponding to the instance."
            )

    def get_model_from_id(self, model_id):
        model = self.model_table.get_model(model_id)
        if model is None:
            raise InvalidInputsError(
                "An error occurred while trying to retrieve model info corresponding to the instance."
            )

        return model

    def get_dc_from_id(self, dc_id):
        datacenter = self.dc_table.get_datacenter(dc_id)
        if datacenter is None:
            raise InvalidInputsError(
                "An error occurred while trying to retrieve datacenter info corresponding to the instance."
            )

        return datacenter

    def make_corresponding_connections(self, network_connections, hostname):
        for port in network_connections:
            connection_hostname = network_connections[port]["connection_hostname"]
            connection_port = network_connections[port]["connection_port"]

            if connection_hostname == "" and connection_port == "":
                continue

            print("SEARCH " + connection_hostname)
            other_instance = self.table.get_instance_by_hostname(connection_hostname)
            print("COMPLETE")
            if other_instance is None:
                return f"An error occurred when attempting to add the network connection. Could not find asset iwht hostname {connection_hostname}."

            other_instance.network_connections[connection_port][
                "connection_hostname"
            ] = hostname
            other_instance.network_connections[connection_port][
                "connection_port"
            ] = port
            print(other_instance.network_connections)

            try:
                print("EDITIG")
                self.table.edit_instance(other_instance, other_instance.asset_number)
                print("EDITED SUCCESS")
            except:
                print("BUMMER")
                return f"Could not add new network connections to asset with hostname {other_instance.hostname}."

        return Constants.API_SUCCESS

    def get_network_neighborhood(self, asset_data):
        asset_number = self.check_null(asset_data[Constants.ASSET_NUMBER_KEY])
        if asset_number is None or asset_number == "":
            raise InvalidInputsError("No asset number found in the request.")

        asset = self.table.get_instance_by_asset_number(asset_number)
        if asset_number is None or asset_number == "":
            raise InvalidInputsError("The asset requested could not be found.")

        connections_dict = {}
        for port in asset.network_connections:
            hostname = asset.network_connections[port]["connection_hostname"]
            connected_asset = self.table.get_instance_by_hostname(hostname)
            if connected_asset is None:
                raise InvalidInputsError(
                    f"Connection to asset with hostname {hostname} was not found."
                )
            two_deep_list = []
            for port2 in connected_asset.network_connections:
                host2 = connected_asset.network_connections[port2][
                    "connection_hostname"
                ]
                two_deep_list.append(host2)

            connections_dict[hostname] = two_deep_list

        return connections_dict

    def check_null(self, val):
        if val is None:
            return ""
        else:
            return val
