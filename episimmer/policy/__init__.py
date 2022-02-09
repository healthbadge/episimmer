from .base import AgentPolicy, EventPolicy, Policy
from .contact_tracing_policy import CTPolicy
from .lockdown_policy import (AgentLockdown, AgentLockdownPolicy,
                              EventLockdown, EventLockdownPolicy, FullLockdown,
                              TestingBasedLockdown)
from .testing_policy import Machine, TestPolicy, TestResult, TestTube
from .vaccination_policy import VaccinationPolicy, VaccineResult, VaccineType

lockdown_classes = [
    'AgentLockdownPolicy', 'FullLockdown', 'AgentLockdown',
    'TestingBasedLockdown', 'EventLockdownPolicy', 'EventLockdown'
]
test_classes = ['TestPolicy', 'TestTube', 'Machine', 'TestResult']
vaccine_classes = ['VaccinationPolicy', 'VaccineType', 'VaccineResult']
contact_tracing_classes = ['CTPolicy']
__all__ = [
    'Policy', 'AgentPolicy', 'EventPolicy'
] + lockdown_classes + test_classes + vaccine_classes + contact_tracing_classes
classes = __all__
