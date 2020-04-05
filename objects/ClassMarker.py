class ClassMarker:

    @staticmethod
    def get_marks_from_class(some_class, marks_attribute_name, mark_type) -> list:
        all_marks = getattr(some_class, marks_attribute_name, {})
        return all_marks.get(mark_type, [])

    @staticmethod
    def add_mark_to_class(some_class, marks_attribute_name, mark_type, mark_value) -> None:
        all_marks = getattr(some_class, marks_attribute_name, {})
        marks_of_type = all_marks.get(mark_type, [])
        marks_of_type.append(mark_value)
        all_marks[mark_type] = marks_of_type
        setattr(some_class, marks_attribute_name, all_marks)

    @staticmethod
    def remove_mark_from_class(some_class, marks_attribute_name, mark_type, mark_value) -> None:
        all_marks = getattr(some_class, marks_attribute_name, {})
        marks_of_type = all_marks.get(mark_type, [])
        if mark_value in marks_of_type:
            marks_of_type.remove(mark_value)
        all_marks[mark_type] = marks_of_type
        setattr(some_class, marks_attribute_name, all_marks)

    @staticmethod
    def does_mark_exist(some_class, marks_attribute_name, mark_type, mark_value) -> bool:
        return mark_value in ClassMarker.get_marks_from_class(some_class, marks_attribute_name, mark_type)
