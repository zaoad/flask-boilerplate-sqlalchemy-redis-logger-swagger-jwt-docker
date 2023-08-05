from my_api.security.helpers import get_session_data

# from flask_jwt_extended import get_jwt_identity
from my_api.sql_alchemy.enums import StatusType
from flask_jwt_extended.exceptions import InvalidHeaderError


from my_api.security.token_type import TokenType


class BaseManager(object):
    def __init__(self, model):
        self.model = model

    def _fetch_user_id_from_session(self):
        try:
            auth_data = get_session_data()
            current_user_id = None
            if auth_data:
                current_user_id = auth_data.user_identity
            return current_user_id
        except InvalidHeaderError:
            current_user_id = None
            return current_user_id
        except Exception as e:
            raise e

    def add(self, session, **kwargs):
        try:
            # current_user_id = get_jwt_identity()
            current_user_id = self._fetch_user_id_from_session()

            if current_user_id:
                kwargs["created_by"] = current_user_id

            model_object = self.model(**kwargs)
            session.add(model_object)
            return model_object, None
        except Exception as e:
            raise e

    def add_list(self, session, kwargs_list):
        try:
            if not kwargs_list:
                return kwargs_list, None
            # current_user_id = get_jwt_identity()
            current_user_id = self._fetch_user_id_from_session()

            model_object_list = []
            for kwargs in kwargs_list:
                if not kwargs:
                    continue
                if current_user_id:
                    kwargs["created_by"] = current_user_id
                model_object = self.model(**kwargs)
                model_object_list.append(model_object)

            if not model_object_list:
                return model_object_list, None

            session.add_all(model_object_list)
            return model_object_list, None
        except Exception as e:
            raise e

    def get_by_id(self, session, **kwargs):
        """Id will be provided by kwargs as filter_by(**kwargs)"""

        try:
            if not kwargs.get("status", None):
                kwargs["status"] = StatusType.ACTIVE.name.lower()
            model_object = self.model.query.filter_by(**kwargs).first()
            return model_object, None
        except Exception as e:
            raise e

    def get_all_by_id(self, session, **kwargs):
        """Id will be provided by kwargs as filter_by(**kwargs)"""

        try:
            if not kwargs.get("status", None):
                kwargs["status"] = StatusType.ACTIVE.name.lower()
            model_object_list = self.model.query.filter_by(**kwargs).all()
            return model_object_list, None
        except Exception as e:
            raise e

    def update(self, session, **kwargs):
        if not kwargs:
            raise Exception("kwargs for filter_by must not be empty")
        try:
            filter_args_dict = kwargs.get("filter_args_dict", None)
            update_args_dict = kwargs.get("update_args_dict", None)
            # assert filter_args_dict is not None, "Must provide filter_args_dict"
            if filter_args_dict is None:
                raise Exception("Must provide filter_args_dict")
            # assert update_args_dict is not None, "Must provide update_args_dict"
            if update_args_dict is None:
                raise Exception("Must provide update_args_dict")

            # current_user_id = get_jwt_identity()
            current_user_id = self._fetch_user_id_from_session()
            if current_user_id:
                update_args_dict["updated_by"] = current_user_id

            model_object = self.model.query.filter_by(**filter_args_dict).first()
            for key, value in update_args_dict.items():
                setattr(model_object, key, value)
            return model_object
        except Exception as e:
            raise e

    def delete(self, session, **kwargs):
        if not kwargs:
            raise Exception("kwargs for filter_by must not be empty")
        try:
            model_object = self.model.query.filter_by(**kwargs).first()
            model_object.status = StatusType.DELETED.name.lower()

            # current_user_id = get_jwt_identity()
            current_user_id = self._fetch_user_id_from_session()
            if current_user_id:
                model_object.updated_by = current_user_id
        except Exception as e:
            raise e

    def delete_all(self, session, **kwargs):
        if not kwargs:
            raise Exception("kwargs for filter_by must not be empty")
        current_user_id = self._fetch_user_id_from_session()
        self.model.query.filter_by(**kwargs).update(
            {"status": StatusType.DELETED.name.lower(), "updated_by": current_user_id}
        )

    def hard_delete(self, session, **kwargs):
        if not kwargs:
            raise Exception("kwargs for filter_by must not be empty")
        try:
            return self.model.query.filter_by(**kwargs).delete()
            # model_object = self.model.query.filter_by(**kwargs).first()
            # session.delete(model_object)
        except Exception as e:
            raise e

    def activate(self, **kwargs):
        if not kwargs:
            raise Exception("kwargs for filter_by must not be empty")
        model_object = self.model.query.filter_by(**kwargs).first()
        if model_object:
            setattr(model_object, "status", StatusType.ACTIVE.name.lower())

    def filter_by(self, **kwargs):
        return self.model.query.filter_by(**kwargs).first()
