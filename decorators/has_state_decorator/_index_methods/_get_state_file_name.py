
def get_state_file_name(self, id_getter):
    state_file_name = "state"
    if id_getter is not None:
        self_id = id_getter(self)
        state_file_name = f"{state_file_name}_{self_id}"
    return state_file_name
