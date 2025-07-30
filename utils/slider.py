from typing import Iterable


class SliderState:
    obj: Iterable | None
    length: int | None
    current_page: int

    def __init__(self, obj: Iterable | None = None, length: int | None = None):
        self.obj = obj
        if self.obj is not None:
            _l = len(self.obj)
            if _l < 1:
                raise ValueError(f"`obj` length must be at least 1, found: {_l}")
            self.length = _l
        else:
            if length is None or length < 1:
                raise ValueError(
                    f"If `obj` is None, you must specify a `length > 0`; found: {length}"
                )
            self.length = length

        self.current_page = 0

    def prev_page(self, return_element=False):
        self.current_page = max(0, self.current_page - 1)
        if return_element and self.obj is not None:
            return self.obj[self.current_page]
        return self.current_page

    def next_page(self, return_element=False):
        self.current_page = min(self.length, self.current_page + 1)
        if return_element and self.obj is not None:
            return self.obj[self.current_page]
        return self.current_page

    def go_to_page(self, page: int, return_element=False):
        self.current_page = min(max(0, self.page), self.length)
        if return_element and self.obj is not None:
            return self.obj[self.current_page]
        return self.current_page
