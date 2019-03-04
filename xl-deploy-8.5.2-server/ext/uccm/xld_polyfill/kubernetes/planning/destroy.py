#
# Copyright (c) 2018. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries, and licensors.
#
from uccm.xld_polyfill.kubernetes.planning.preview_aware_generators import PreviewAwareStepsGenerator, ProfileResourceHelper
from xld.kubernetes.resource.planningScripts.generator import DestroyPlanGenerator

if previousDeployed.type != 'openshift.TemplateResources':
    steps_generator = PreviewAwareStepsGenerator(context=context, steps=steps, delta=delta)
    plan_generator = DestroyPlanGenerator(previousDeployed, steps_generator)
    plan_generator.__resource_helper = ProfileResourceHelper(previousDeployed, previousDeployedApplication.environment)
    plan_generator.generate()
