"""Constants for Coopernico GO 2.0 integration."""

from typing import Final

DOMAIN: Final = "coopernico_go"
DEFAULT_NAME: Final = "Coopernico GO"

# Coopernico GO 2.0 formula constants
# Formula: ((OMIE + K) * (1 + FP)) + GO
K: Final = 0.009
FP: Final = 0.16
GO: Final = 0.001

# Regulated costs
CS: Final = 0.003
CR: Final = 0.006
TSE: Final = 0.0020666
IEC: Final = 0.001

REGULATED_COSTS: Final = CS + CR + TSE + IEC

# TAR values (BTN 2026) - split by semester
# S1: January-May, S2: June-December
TAR: Final = {
    "simples": {
        "s1": {"flat": 0.0365},
        "s2": {"flat": 0.0625},
    },
    "bi": {
        "s1": {"fora_de_vazio": 0.0502, "vazio": 0.0092},
        "s2": {"fora_de_vazio": 0.0860, "vazio": 0.0157},
    },
    "tri": {
        "s1": {"ponta": 0.1511, "cheias": 0.0237, "vazio": 0.0092},
        "s2": {"ponta": 0.0259, "cheias": 0.0406, "vazio": 0.0157},
    },
}

# Tariff types
TARIFF_SIMPLES: Final = "simples"
TARIFF_BI: Final = "bi"
TARIFF_TRI: Final = "tri"

TARIFF_OPTIONS: Final = {
    TARIFF_SIMPLES: "Simples",
    TARIFF_BI: "Bi-Horária",
    TARIFF_TRI: "Tri-Horária",
}

# Config keys
CONF_OMIE_ENTITY: Final = "omie_entity"
CONF_TARIFF: Final = "tariff"
