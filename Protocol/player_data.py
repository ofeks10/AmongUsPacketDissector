import construct
from construct import Struct, Byte, Enum
from construct.core import Array, Flag, Int16ul, PascalString, VarInt

from Protocol.enums import ColorId


task_data = Struct(
    'task_id' / VarInt,
    'completed' / Flag,
)


player_data = Struct(
    'player_data_len' / Int16ul,
    'player_id' / Byte,
    'player_name' / PascalString(Byte, 'ascii'),
    'color_id' / Enum(Byte, ColorId),
    'hat_id' / VarInt,
    'pet_id' / VarInt,
    'skin_id' / VarInt,
    'status_bit_field' / Byte,
    'task_count' / Byte,
    'tasks' / Array(construct.this.task_count, task_data),
)
