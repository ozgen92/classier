import classier.decorators.has_state_decorator.options.ATTRIBUTE_OPTIONS as ATTRIBUTE_OPTIONS
import classier.decorators.has_state_decorator.options.METHOD_OPTIONS as METHOD_OPTIONS
from classier.objects import ClassMarker
from classier.decorators import _MARK_ATTRIBUTE_NAME
from classier.decorators.has_state_decorator import _MARK_TYPE_NAME
import classier.utils as utils
import os

def add_does_state_exist(some_class, options):
	get_id = METHOD_OPTIONS.METHOD_GET_ID.get_option(options)

	def does_state_exist(self, file_path=None):
		state_id = None if get_id is None else str(get_id(self))
		if file_path is None:
			get_path = METHOD_OPTIONS.METHOD_GET_PATH.get_option(options)
			path = get_path(self)
			assert state_id is not None
			file_path = os.path.join(path, state_id)
		return os.path.exists(file_path)

	method_name_does_state_exist = METHOD_OPTIONS.METHOD_NAME_DOES_STATE_EXIST.get_option(options)
	if not ClassMarker.does_mark_exist(some_class, _MARK_ATTRIBUTE_NAME, _MARK_TYPE_NAME, method_name_does_state_exist):
		ClassMarker.add_mark_to_class(some_class, _MARK_ATTRIBUTE_NAME, _MARK_TYPE_NAME, method_name_does_state_exist)
		some_class = utils.convenience.add_mixin(some_class, does_state_exist, method_name_does_state_exist)
	return some_class
