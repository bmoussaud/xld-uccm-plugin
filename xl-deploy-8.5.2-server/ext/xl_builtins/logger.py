from org.slf4j import LoggerFactory
from uccm.dynamic.planner.dynamic_deployed_rule_selector import DynamicDeployedSelector
import __builtin__

__builtin__.logger = LoggerFactory.getLogger("com.xebialabs.platform.script.Logging")
__builtin__.uccm_utils = DynamicDeployedSelector()