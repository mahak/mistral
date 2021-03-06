# -*- coding: utf-8 -*-
#
# Copyright 2013 - Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""Valid task and workflow states."""

IDLE = 'IDLE'
RUNNING = 'RUNNING'
PAUSED = 'PAUSED'
DELAYED = 'DELAYED'
SUCCESS = 'SUCCESS'
ERROR = 'ERROR'

_ALL = [IDLE, RUNNING, SUCCESS, ERROR, PAUSED, DELAYED]

_VALID_TRANSITIONS = {
    IDLE: [RUNNING, ERROR],
    RUNNING: [PAUSED, DELAYED, SUCCESS, ERROR],
    PAUSED: [RUNNING, ERROR],
    DELAYED: [RUNNING, ERROR],
    SUCCESS: [],
    ERROR: []
}


def is_valid(state):
    return state in _ALL


def is_invalid(state):
    return not is_valid(state)


def is_completed(state):
    return state in [SUCCESS, ERROR]


def is_idle(state):
    return state == IDLE


def is_paused_or_completed(state):
    return state == PAUSED or is_completed(state)


def is_valid_transition(from_state, to_state):
    if is_invalid(from_state) or is_invalid(to_state):
        return False

    if from_state == to_state:
        return True

    return to_state in _VALID_TRANSITIONS[from_state]
