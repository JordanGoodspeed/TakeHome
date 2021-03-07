from enum import IntEnum

class StatusTypes(IntEnum):
  NEW = 1
  TURNED_IN = 2
  
  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]