from math import log

import construct
from Protocol.enums import ChatNoteTypes, ColorId, RPCAction
from construct import Struct, Byte
from construct.core import Array, Enum, GreedyRange, Int32ul, PascalString, Switch, VarInt

from .enums import ColorId
from .player_data import player_data


def _get_length_of_rpc_data(this):
    '''
        Gets the construct.this and calculates the VarInt length of
        the rpc_target_id and adds it to the rest of the header
    '''
    num = this._.rpc_target_id
    if num == 0:
        return 1
    return this._._.content_size - (int(log(num, 128)) + 1 + 1)


set_tasks = Struct(
    'tasks_data' / Array(_get_length_of_rpc_data, Byte)
)


send_chat = Struct(
    'message' / PascalString(Int32ul, 'ascii')
)


set_start_counter = Struct(
    'unknown1' / Byte,
    'unknown2' / Byte,
)

set_color = Struct(
    'color_id' / Enum(VarInt, ColorId)
)


set_hat = Struct(
    'hat_id' / VarInt
)


set_skin = Struct(
    'skin_id' / VarInt
)

set_pet = Struct(
    'pet_id' / VarInt
)

set_name = Struct(
    'name' / PascalString(VarInt, 'ascii')
)

check_name = Struct(
    'name' / PascalString(VarInt, 'ascii')
)

start_meeting = Struct(
    'player_id' / Byte
)

voting_complete = Struct(
    'unknown' / Array(11, Byte),
    'player_id?' / Byte,
    'unknown2' / Byte
)

send_chat_note = Struct(
    'player_id' / Byte,
    'chat_note_type' / Enum(Byte, ChatNoteTypes)
)

report_dead_body = Struct(
    'player_id' / Byte
)

update_game_data = Struct(
    'players' / GreedyRange(player_data)
)

complete_task = Struct(
    'task_id' / VarInt
)


murder_player = Struct(
    'rpc_player_id' / Byte
)


set_infected = Struct(
    'number_of_infected' / Byte,
    'infected_ids' / Array(construct.this.number_of_infected, Byte)
)


sync_settings = Struct(
    'settings' / Array(_get_length_of_rpc_data, Byte)
)


add_vote = Struct(
    'vote_data' / Array(_get_length_of_rpc_data, Byte)
)


snap_to = Struct(
    'snap_to_data' / Array(_get_length_of_rpc_data, Byte)
)


exiled = Struct(
    'rpc_player_id' / Byte
)


cast_vote = Struct(
    'player_id' / Byte,
    'vote_to' / Byte
)


enter_vent = Struct(
    'vent_id' / Byte
)


rpc = Struct(
    'rpc_target_id' / VarInt,
    'rpc_action' / Enum(Byte, RPCAction),
    'data' / Switch(lambda this: int(this.rpc_action),
        {
            RPCAction.SENDCHAT: send_chat,
            RPCAction.SETSTARTCOUNTER: set_start_counter,
            RPCAction.SETCOLOR: set_color,
            RPCAction.SETHAT: set_hat,
            RPCAction.SETSKIN: set_skin,
            RPCAction.SETPET: set_pet,
            RPCAction.SETNAME: set_name,
            RPCAction.STARTMEETING: start_meeting,
            RPCAction.VOTINGCOMPLETE: voting_complete,
            RPCAction.SENDCHATNOTE: send_chat_note,
            RPCAction.REPORTDEADBODY: report_dead_body,
            RPCAction.UPDATEGAMEDATA: update_game_data,
            RPCAction.COMPLETETASK: complete_task,
            RPCAction.MURDERPLAYER: murder_player,
            RPCAction.SETINFECTED: set_infected,
            RPCAction.SETTASKS: set_tasks,
            RPCAction.CHECKNAME: check_name,
            RPCAction.SYNCSETTINGS: sync_settings,
            RPCAction.EXILED: exiled,
            RPCAction.CASTVOTE: cast_vote,
            RPCAction.ADDVOTE: add_vote,
            RPCAction.SNAPTO: snap_to,
            RPCAction.ENTERVENT: enter_vent,
        }
    )
)
