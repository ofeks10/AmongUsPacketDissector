import construct
from construct import Struct, Enum, Byte, If
from construct.core import Array, GreedyRange, Int16ub, Int32ul, Int16ul, Optional, Switch, VarInt

from .enums import GameDataType, HazelType, RoomMessageType
from .rpc import rpc


data = Struct(
    'data' / Array(construct.this._.content_size, Byte)
)


spawn = Struct(
    'spawn_data' / Array(construct.this._.content_size, Byte),
)


despawn = Struct(
    'player_id' / VarInt,
)


scene_change = Struct(
    'scene_data' / Array(construct.this._.content_size, Byte)
)


change_settings = Struct(
    'settings_data' / Array(construct.this._.content_size, Byte)
)


unknown1 = Struct(
    'data' / Array(construct.this._.content_size, Byte)
)


game_data = Struct(
    'content_size' / Int16ul,
    'type' / Enum(Byte, GameDataType),
    'data' / Switch(lambda this: int(this.type),
        {
            GameDataType.DATA.value: data,
            GameDataType.RPC.value: rpc,
            GameDataType.SPAWN.value: spawn,
            GameDataType.DESPAWN.value: despawn,
            GameDataType.SCENE_CHANGE: scene_change,
            GameDataType.CHANGE_SETTINGS: change_settings,
            GameDataType.UNKNOWN1: unknown1,
        }
    ),
)


room_message = Struct(
    'content_size' / Int16ul,
    'type' / Enum(Byte, RoomMessageType),
    'room_code' / Int32ul,
    'messages' / GreedyRange(game_data)
)


base_packet = Struct(
    'type' / Enum(Byte, HazelType),
    'packet_id' / If(lambda this: int(this.type) in HazelType.get_reliable(), Int16ub),
    'content' / Optional(room_message)
)
