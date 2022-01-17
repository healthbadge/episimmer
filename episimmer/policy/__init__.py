from .base import AgentPolicy
from .lockdown_policy import (AgentLockdown, AgentPolicyBasedLockdown,
                              FullLockdown)
from .testing_policy import Machine, TestPolicy, TestResult, TestTube
from .vaccination_policy import VaccinationPolicy, VaccineResult, VaccineType

lockdown_classes = [
    'AgentPolicy', 'FullLockdown', 'AgentLockdown', 'AgentPolicyBasedLockdown'
]
test_classes = ['TestPolicy', 'TestTube', 'Machine', 'TestResult']
vaccine_classes = ['VaccinationPolicy', 'VaccineType', 'VaccineResult']
__all__ = lockdown_classes + test_classes + vaccine_classes
classes = __all__
