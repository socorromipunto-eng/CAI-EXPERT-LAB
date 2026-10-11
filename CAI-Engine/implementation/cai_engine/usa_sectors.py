"""U.S. critical infrastructure sectors (NSM-22, 2024).

The 16 critical infrastructure sectors and their Sector Risk Management
Agencies (SRMAs), per National Security Memorandum NSM-22 (April 2024, which
superseded PPD-21). Each sector carries a consequence level and whether it is
OT/ICS-intensive, so the USA governance profile can treat each sector on its
own terms rather than applying one blanket rule.

consequence:  CATASTROPHIC > HIGH > MODERATE   (drives assurance strictness)
ot_intensive: sector where cyber-physical / OT safety gating applies
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Sector:
    key: str
    name: str
    srma: str            # Sector Risk Management Agency
    consequence: str     # CATASTROPHIC | HIGH | MODERATE
    ot_intensive: bool


SECTORS: dict[str, Sector] = {
    "chemical":              Sector("chemical", "Chemical", "CISA (DHS)", "CATASTROPHIC", True),
    "commercial_facilities": Sector("commercial_facilities", "Commercial Facilities", "CISA (DHS)", "MODERATE", False),
    "communications":        Sector("communications", "Communications", "CISA (DHS)", "HIGH", True),
    "critical_manufacturing":Sector("critical_manufacturing", "Critical Manufacturing", "CISA (DHS)", "HIGH", True),
    "dams":                  Sector("dams", "Dams", "CISA (DHS)", "CATASTROPHIC", True),
    "defense_industrial_base":Sector("defense_industrial_base", "Defense Industrial Base", "Department of Defense", "HIGH", True),
    "emergency_services":    Sector("emergency_services", "Emergency Services", "CISA (DHS)", "HIGH", False),
    "energy":                Sector("energy", "Energy", "Department of Energy", "CATASTROPHIC", True),
    "financial_services":    Sector("financial_services", "Financial Services", "Department of the Treasury", "HIGH", False),
    "food_agriculture":      Sector("food_agriculture", "Food and Agriculture", "USDA and HHS (FDA)", "HIGH", True),
    "government_facilities":  Sector("government_facilities", "Government Facilities", "CISA (DHS) and GSA", "HIGH", False),
    "healthcare":            Sector("healthcare", "Healthcare and Public Health", "Department of Health and Human Services", "HIGH", False),
    "information_technology":Sector("information_technology", "Information Technology", "CISA (DHS)", "HIGH", False),
    "nuclear":               Sector("nuclear", "Nuclear Reactors, Materials, and Waste", "CISA (DHS)", "CATASTROPHIC", True),
    "transportation":        Sector("transportation", "Transportation Systems", "TSA and U.S. Coast Guard (DHS)", "CATASTROPHIC", True),
    "water":                 Sector("water", "Water and Wastewater Systems", "Environmental Protection Agency", "CATASTROPHIC", True),
}

# Aliases so inputs like "electricity" or "aviation" resolve to a sector.
ALIASES = {
    "electricity": "energy", "power": "energy", "gas": "energy", "oil": "energy",
    "aviation": "transportation", "rail": "transportation", "maritime": "transportation",
    "road_traffic": "transportation", "transit": "transportation",
    "wastewater": "water", "drinking_water": "water",
    "it": "information_technology", "telecom": "communications",
    "bank": "financial_services", "banking": "financial_services",
    "hospital": "healthcare", "public_health": "healthcare",
    "manufacturing": "critical_manufacturing",
}


def resolve(sector_key: str) -> Sector | None:
    if not sector_key:
        return None
    k = sector_key.strip().lower().replace(" ", "_").replace("-", "_")
    k = ALIASES.get(k, k)
    return SECTORS.get(k)
