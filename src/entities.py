from typing import Sequence


class DocumentObject:
    __slots__ = ('name', )

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self):
        return f'{self.__class__.__name__}(name={repr(self.name)})'

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class Document:
    __slots__ = ('id', 'level', 'objects')

    def __init__(
        self, id_: str, level: int, objects: Sequence[DocumentObject],
    ):
        self.id = id_
        self.level = level
        self.objects = objects

    def __repr__(self):
        return (
            f'{self.__class__.__name__}'
            f'('
            f'id_={repr(self.id)}, '
            f'level={repr(self.level)}, '
            f'objects={repr(self.objects)}'
            f')'
        )

    def __eq__(self, other):
        return (
            self.id == other.id
            and self.level == other.level
            and self.objects == other.objects
        )

    def __hash__(self):
        return hash(self.id)
