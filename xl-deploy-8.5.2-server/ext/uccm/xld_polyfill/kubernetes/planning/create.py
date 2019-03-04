#
# Copyright (c) 2018. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries, and licensors.
#
import uccm.xld_polyfill.kubernetes.planning.preview_aware_generators
reload(uccm.xld_polyfill.kubernetes.planning.preview_aware_generators)
from uccm.xld_polyfill.kubernetes.planning.preview_aware_generators import PreviewAwareStepsGenerator, ProfileResourceHelper
from xld.kubernetes.resource.planningScripts.generator import CreatePlanGenerator

if deployed.type != 'openshift.TemplateResources':
    steps_generator = PreviewAwareStepsGenerator(context=context, steps=steps, delta=delta)
    plan_generator = CreatePlanGenerator(deployed, steps_generator)
    plan_generator.__resource_helper = ProfileResourceHelper(deployed, deployedApplication.environment)
    plan_generator.generate()
