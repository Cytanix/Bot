# Copyright (c) 2025 SpiritTheWalf and Cytanix
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/ or see the LICENSE file.
"""This file contains the enums needed"""
from enum import Enum

class Dms(Enum):
    """Dms Enum"""
    ALLOWED = "allowed"
    NOT_ALLOWED = "not_allowed"
    ASK = "ask"

class Gender(Enum):
    """Gender Enum"""
    MALE = "male"
    FEMALE = "female"
    GENDERFLUID = "genderfluid"
    AGENDER = "agender"
    NON_BINARY = "non-binary"
    TRANSGENDER = "transgender"
    TRANS_MALE = "trans-male"
    TRANS_FEMALE = "trans-female"

class Relationship(Enum):
    """Relationship Enum"""
    TAKEN = "taken"
    SINGLE = "single"
    SINGLE_SEEKING = "single-seeking"
    SINGLE_NOT = "single-not"
    RATHER_NOT = "rather_not"

class Sexuality(Enum):
    """Sexuality Enum"""
    ASEXUAL = "asexual"
    BISEXUAL = "bisexual"
    GAY = "gay"
    STRAIGHT = "straight"
    LESBIAN = "lesbian"
    PANSEXUAL = "pansexual"
    AROMANTIC = "aromantic"
    RATHER_NOT = "rather_not"

class Position(Enum):
    """Position Enum"""
    DOMINANT = "dominant"
    SUBMISSIVE = "submissive"
    SWITCH = "switch"
    RATHER_NOT = "rather_not"
    NEITHER = "neither"
