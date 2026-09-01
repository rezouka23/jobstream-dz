"""Source adapter registry."""

from .emploitic import EmploiticAdapter
from .jobindz import JobindzAdapter
from .linkedin import LinkedInAdapter
from .naukrigulf import NaukriGulfAdapter
from .ouedkniss import OuedknissAdapter

__all__ = [
    "EmploiticAdapter", "JobindzAdapter", "LinkedInAdapter",
    "NaukriGulfAdapter", "OuedknissAdapter",
]
