from pkg_resources import DistributionNotFound, get_distribution

from . import policy, utils, vulnerability_detection
from .agent import Agent
from .location import Location
from .main import main
from .model import ScheduledModel, StochasticModel
from .policy import (AgentLockdown, AgentPolicy, AgentPolicyBasedLockdown,
                     FullLockdown, Machine, TestPolicy, TestResult, TestTube,
                     VaccinationPolicy, VaccineResult, VaccineType)
from .read_file import (ReadAgents, ReadConfiguration, ReadEvents,
                        ReadInteractions, ReadLocations, ReadOneTimeEvents,
                        ReadProbabilisticInteractions, ReadVDConfiguration)
from .simulate import Simulate
from .vulnerability_detection import (VD, AgentVD, AgentVulnerabilities,
                                      AgentVulnerabilitiesMC,
                                      AgentVulnerabilitiesMC2, BanditAlgos,
                                      VulnerableAgentMC1, VulnerableAgentMC2,
                                      VulnerableAgents)
from .world import World

try:
    __version__ = get_distribution('episimmer').version
except DistributionNotFound:
    __version__ = 'Please install this project with setup.py'

__all__ = ['main']
__all__.extend(policy.__all__)
__all__.extend(vulnerability_detection.__all__)
__all__.extend(['utils'])
