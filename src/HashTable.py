from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")

class hashtable(Generic[T, U]):
    data: list[dict[T,U]]
    size: int
    
    def __init__(self, table_size: int) -> None:
        super().__init__()
        self.data = [{} for _ in range(table_size)]
        self.size = table_size
        
    def add(self, key: T, input: U):
        hashKey = hash(key) % self.size
        self.data[hashKey][key] = input
        
    def get(self, key: T) -> U:
        hashKey = hash(key) % self.size
        if not key in self.data[hashKey]:
            return None
        return self.data[hashKey][key]
    
    def remove(self, key: T) -> U:
        hashKey = hash(key) % self.size
        if not key in self.data[hashKey]:
            return None
        return self.data[hashKey].pop(key)
    
    def haskey(self, key: T) -> bool:
        hashKey = hash(key) % self.size
        return key in self.data[hashKey]
    
    def clone(self) -> hashtable[T, U]:
        newHastTable = hashtable(self.size)
        newHastTable.data = [dict.copy() for dict in self.data]
        return newHastTable
    
    def keys(self) -> list[T]:
        keys = []
        for dict in self.data:
            keys.extend(list(dict.keys()))
        return keys
    
    def tostring(self) -> str:
        text = ""
        for index, dict in enumerate(self.data):
            text += f"Index {index}\n"
            for key in list(dict.keys()):
                text += f"\t{key}:\t{dict[key]}\n"
        return text
        
