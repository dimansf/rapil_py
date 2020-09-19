from raspil_rt.data_structs.StoreBoard import StoreBoard
from typing import Callable, Tuple, List


class Board:
    '''
    Абстракция доски в распиле пришедшей в заказ
    '''

    def __init__(self, id, len, amount) -> None:
        self.id = id
        self.len = len
        self.amount = amount

    @staticmethod
    def copy(dup: 'Board', amount=False):
        return Board(dup.id, dup.len, amount if amount is not False else dup.amount)

    def __len__(self):
        self.amount * self.len

    def __sub__(self, other):
        if self == other:
            self.amount -= other.amount
            if self.amount < 0:
                raise Exception('Negative amount of Boards')
        return self

    def __add__(self, other):
        if self == other:
            self.amount += other.amount
        return self

    def __eq__(self, o: object) -> bool:
        return (self.id, self.len) == (o.id, o.len)  # type: ignore

    def __hash__(self) -> int:
        return hash(str(self))

    def __str__(self) -> str:
        return f'( {self.id}, {self.len}, {self.amount} )'


class BoardCollection(List[Board]):
    '''
    Список Досок из заказа. Имеют несколько полезных методов
    '''

    def __init__(self, seq: List[Board] = []) -> None:
        super().__init__()
        for el in seq:
            self.append(el)

    @staticmethod
    def copy(bc: 'BoardCollection'):
        bcn = BoardCollection()
        for el in bc:
            bcn.append(Board.copy(el))
        return bcn

    def append(self, el):
        for x in self:
            if el == x:
                x.amount += el.amount
                return
        super().append(el)

    def total_amount(self):
        return sum([x.amount for x in self])

    def __sub__(self, other):
        for board in other:
            for b in range(self.count()):
                if self[b] == board:
                    self[b] -= board
                if self[b] == 0:
                    del self[b]
    
    def count(self):
        return super().__len__()
    def __len__(self) -> int:
        return sum([x.amount*x.len for x in self])

    def __str__(self):
        s = 'Collection: (\n'
        for b in self:
            s += f'{b},'
        return s + '\n\t)'


class BoardCombinations(List[BoardCollection]):
    '''
    Список комбинаций для одной доски на складе
    '''

    def __init__(self, sb: StoreBoard, seq: List[BoardCollection] = []) -> None:
        super().__init__()
        self.store_board = sb
        self.best_coll = BoardCollection()
        for el in seq:
            self.append(el)

    def zip(self, cond: Callable[[BoardCollection, BoardCollection, StoreBoard], bool]):
        for bcol in self:
            if cond(self.best_coll, bcol, self.store_board):
                self.best_coll = bcol

    def __str__(self) -> str:
        s = 'Board Combinations: { \n'
        for x in self:
            s += f'\t{x}\n'
        return s + '\n \t}'


class OneIterationResult(List[BoardCombinations]):
    def __init__(self):
        super().__init__()
