from typing import List, Optional

from app.dal.database import db
from app.dal.exceptions.ChangeModelDBException import ChangeModelDBException
from app.data_models.model import Model


class ModelEntry(db.Model):
    __tablename__ = "models"

    identifier = db.Column(db.Integer, primary_key=True, unique=True)

    vendor = db.Column(db.String(80))
    model_number = db.Column(db.String(80))
    height = db.Column(db.Integer)
    eth_ports = db.Column(db.Integer)
    power_ports = db.Column(db.Integer)
    cpu = db.Column(db.String(80))
    memory = db.Column(db.Integer)
    storage = db.Column(db.String(80))
    comment = db.Column(db.String(80))
    display_color = db.Column(db.String(80))

    def __init__(self, model: Model):
        self.vendor = model.vendor
        self.model_number = model.model_number
        self.height = model.height
        self.eth_ports = model.eth_ports
        self.power_ports = model.power_ports
        self.cpu = model.cpu
        self.memory = model.memory
        self.storage = model.storage
        self.comment = model.comment
        self.display_color = model.display_color


class ModelTable:
    def get_model(self, identifier: int) -> Optional[Model]:
        """ Get the model for the given id """
        model: ModelEntry = ModelEntry.query.filter_by(identifier=identifier).model()
        if model is None:
            return None

        return Model(
            vendor=model.vendor,
            model_number=model.model_number,
            height=model.height,
            eth_ports=model.eth_ports,
            power_ports=model.power_ports,
            cpu=model.cpu,
            memory=model.memory,
            storage=model.storage,
            comment=model.comment,
            display_color=model.display_color,
        )

    def get_model_by_vendor_number(self, vendor, modelNumber):
        model: ModelEntry.query.filter_by(vendor=vendor, model_number=modelNumber)
        if model is None:
            return None

        return Model(
            vendor=model.vendor,
            model_number=model.model_number,
            height=model.height,
            eth_ports=model.eth_ports,
            power_ports=model.power_ports,
            cpu=model.cpu,
            memory=model.memory,
            storage=model.storage,
            comment=model.comment,
            display_color=model.display_color,
        )

    def get_model_id_by_vendor_number(self, vendor, modelNumber):
        model: ModelEntry.query.filter_by(vendor=vendor, model_number=modelNumber)
        if model is None:
            return None

        return model.identifier

    def edit_model(self, model: Model) -> None:
        """ Updates a model to the database """

        model_entry: ModelEntry = ModelEntry(model=model)

        try:
            # TODO: make this edit not add
            # db.session.add(model_entry)
            db.session.commit()
        except:
            raise ChangeModelDBException(
                "Failed to udpate model {model.vendor} {model.model_number}"
            )

    def add_model(self, model: Model) -> None:
        """ Adds a model to the database """
        model_entry: ModelEntry = ModelEntry(model=model)

        try:
            db.session.add(model_entry)
            db.session.commit()
        except:
            raise ChangeModelDBException(
                "Failed to add model {model.vendor} {model.model_number}"
            )

    @DeprecationWarning
    def delete_model(self, model: Model) -> None:
        """ Removes a model from the database """
        try:
            ModelEntry.query.filter_by(
                vendor=model.vendor, model_number=model.model_number
            ).delete()
            db.session.commit()
        except:
            raise ChangeModelDBException(
                "Failed to add model {model.vendor} {model.model_number}"
            )

    def delete_model_str(self, vendor: str, model_num: str) -> None:
        """ Removes a model from the database """
        try:
            ModelEntry.query.filter_by(vendor=vendor, model_number=model_num).delete()
            db.session.commit()
        except:
            raise ChangeModelDBException("Failed to add model {vendor} {model_number}")

    def get_all_models(self) -> List[Model]:
        """ Get a list of all models """
        all_models: List[ModelEntry] = ModelEntry.query.all()

        return [
            Model(
                vendor=model.vendor,
                model_number=model.model_number,
                height=model.height,
                eth_ports=model.eth_ports,
                power_ports=model.power_ports,
                cpu=model.cpu,
                memory=model.memory,
                storage=model.storage,
                comment=model.comment,
                display_color=model.display_color,
            )
            for model in all_models
        ]

    def get_models_with_filter(self, filter: str, limit: int) -> List[Model]:
        """ Get a list of all models containing the given filter """

        # filtered_models: List[ModelEntry] = ModelEntry.query.filter_by(or_(filter)).limit(limit)
        filtered_models: List[Model] = []

        return [
            Model(
                vendor=model.vendor,
                model_number=model.model_number,
                height=model.height,
                eth_ports=model.eth_ports,
                power_ports=model.power_ports,
                cpu=model.cpu,
                memory=model.memory,
                storage=model.storage,
                comment=model.comment,
                display_color=model.display_color,
            )
            for model in filtered_models
        ]
