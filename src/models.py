from typing import Sequence


class DocumentObject:
    __slots__ = ('name', )

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self):
        return f'{self.__class__.__name__}(name={repr(self.name)})'


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
