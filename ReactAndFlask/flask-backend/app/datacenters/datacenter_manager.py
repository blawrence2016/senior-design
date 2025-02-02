from app.constants import Constants
from app.dal.datacenter_table import DatacenterTable
from app.data_models.datacenter import Datacenter
from app.datacenters.datacenter_validator import DatacenterValidator
from app.exceptions.InvalidInputsException import InvalidInputsError


class DatacenterManager:
    def __init__(self):
        self.dc_table = DatacenterTable()
        self.validate = DatacenterValidator()

    def get_all_datacenters(self):
        try:
            dc_list = self.dc_table.get_all_datacenters()
            return dc_list
        except:
            raise InvalidInputsError(
                "A failure occured while retrieving datacenter information."
            )

    def create_datacenter(self, dc_data):
        try:
            try:
                new_datacenter = self.make_datacenter(dc_data)
                if type(new_datacenter) is InvalidInputsError:
                    return new_datacenter
            except InvalidInputsError as e:
                return e.message

            try:
                create_validation_result = self.validate.create_dc_validation(
                    new_datacenter
                )
            except InvalidInputsError as e:
                return e.message
            if create_validation_result == Constants.API_SUCCESS:
                self.dc_table.add_datacenter(new_datacenter)
            else:
                return InvalidInputsError(create_validation_result)

        except:
            raise InvalidInputsError(
                "An error occurred when attempting to create the datacenter."
            )

    def edit_datacenter(self, dc_data):
        try:
            print("here1")
            try:
                original_name = self.check_null(dc_data[Constants.NAME_ORIG_KEY])
                print("here2")
                updated_datacenter = self.make_datacenter(dc_data)
                print("here3")
                if type(updated_datacenter) is InvalidInputsError:
                    return updated_datacenter
                print("here4")
            except InvalidInputsError as e:
                return e.message

            try:
                print("here5")
                edit_validation_result = self.validate.edit_dc_validation(
                    updated_datacenter, original_name
                )
            except InvalidInputsError as e:
                return e.message
            print("here6")
            if edit_validation_result == Constants.API_SUCCESS:
                self.dc_table.edit_datacenter(updated_datacenter, original_name)
            else:
                return InvalidInputsError(edit_validation_result)
            print("here7")
        except:
            raise InvalidInputsError(
                "An error occurred when attempting to edit the datacenter."
            )

    def delete_datacenter(self, dc_data):
        try:
            dc_name = self.check_null(dc_data[Constants.DC_NAME_KEY])

            if dc_name == "":
                raise InvalidInputsError("Must provide a datacenter name to delete")

            try:
                delete_validation_result = self.validate.delete_dc_validation(dc_name)
            except InvalidInputsError as e:
                return e.message
            if delete_validation_result == Constants.API_SUCCESS:
                self.dc_table.delete_datacenter_by_name(dc_name)
            else:
                return InvalidInputsError(delete_validation_result)
        except:
            raise InvalidInputsError(
                "An error occurred when trying to delete the specified asset."
            )

    def make_datacenter(self, dc_data):
        try:
            print("were1")
            abbreviation = self.check_null(dc_data[Constants.DC_ABRV_KEY]).upper()
            print("were2")
            name = self.check_null(dc_data[Constants.DC_NAME_KEY])
            print("were3")
            is_offline_storage = dc_data[Constants.DC_IS_OFFLINE_KEY]
            print("were4")
        except:
            raise InvalidInputsError(
                "Could not read data fields correctly. Client-server error occurred."
            )

        print("were5")
        if abbreviation == "":
            raise InvalidInputsError("Must provide an abbreviation for the datacenter")
        print("were6")
        if name == "":
            raise InvalidInputsError("Must provide a datacenter name")
        print("were7")
        if type(is_offline_storage) != bool:
            raise InvalidInputsError(
                "Must provide a boolean value specifying whether or not the datacenter is an offline storage location"
            )

        return Datacenter(abbreviation, name, is_offline_storage)

    def check_null(self, val):
        if val is None:
            return ""
        else:
            return val
