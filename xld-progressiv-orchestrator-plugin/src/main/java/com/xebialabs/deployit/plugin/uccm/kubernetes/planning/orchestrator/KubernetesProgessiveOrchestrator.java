package com.xebialabs.deployit.plugin.uccm.kubernetes.planning.orchestrator;

import com.google.common.base.Predicates;
import com.rits.cloning.Cloner;
import com.xebialabs.deployit.engine.spi.orchestration.InterleavedOrchestration;
import com.xebialabs.deployit.engine.spi.orchestration.Orchestrator;
import com.xebialabs.deployit.engine.spi.orchestration.Orchestration;
import com.xebialabs.deployit.engine.spi.orchestration.Orchestrations;

import com.xebialabs.deployit.plugin.api.deployment.specification.Operation;
import com.xebialabs.deployit.plugin.api.udm.Container;
import com.xebialabs.deployit.plugin.api.udm.Deployable;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import com.google.common.base.Predicate;
import com.google.common.collect.Collections2;
import com.google.common.collect.Lists;
import com.xebialabs.deployit.plugin.api.deployment.specification.Delta;
import com.xebialabs.deployit.plugin.api.deployment.specification.DeltaSpecification;
import com.xebialabs.deployit.plugin.api.udm.Deployed;
import com.xebialabs.deployit.plugin.api.udm.DeployedApplication;


import java.util.Collection;
import java.util.List;

import static com.google.common.collect.Collections2.filter;


@Orchestrator.Metadata(
        name = "k8s-progressive-group",
        description = "a progressive group orchestrator ")
public class KubernetesProgessiveOrchestrator implements Orchestrator {

    private static final Logger logger = LoggerFactory.getLogger(KubernetesProgessiveOrchestrator.class);

    @Override
    public Orchestration orchestrate(DeltaSpecification specification) {
        if (specification.getOperation() != Operation.MODIFY) {
            return Orchestrations.interleaved(this.descForAppDeployment(specification.getDeployedApplication()), specification.getDeltas());
        }

        Cloner cloner = new Cloner();
        List<Orchestration> orchestrationList = Lists.newArrayList();

        Collection<Delta> uccmContainerDeltas = filter(specification.getDeltas(), new IsTypeOf("uccm.Container"));
        Collection<Delta> smokeTestDeltas = filter(specification.getDeltas(), new IsTypeOf("smoketest.ExecutedHttpRequestTest"));

        Collection<Delta> uccmProgressiveContainerDeltas = filter(uccmContainerDeltas, new IsPropertyTrue("progressive"));
        Collection<Delta> uccmNonProgressiveContainerDeltas = filter(uccmContainerDeltas, Predicates.not(new IsPropertyTrue("progressive")));
        for (Delta delta : uccmProgressiveContainerDeltas) {

            if (delta.getOperation() != Operation.MODIFY) {
                continue;
            }

            Deployed deployed = delta.getDeployed() == null ? delta.getPrevious() : delta.getDeployed();
            String replicasPropertyName = "replicas";

            int replicas = deployed.getProperty(replicasPropertyName);
            for (int i = 0; i < replicas; i++) {
                Delta current_delta = cloner.deepClone(delta);
                Deployed current_deployed = current_delta.getDeployed() == null ? current_delta.getPrevious() : current_delta.getDeployed();
                current_deployed.setProperty(replicasPropertyName, (i + 1));

                if (current_delta.getOperation() == Operation.MODIFY) {
                    Deployed<? extends Deployable, ? extends Container> current_previousDeployed = current_delta.getPrevious();
                    current_previousDeployed.setProperty(replicasPropertyName, (replicas - (i + 1)));
                }

                List<Delta> current_deltas = Lists.newArrayList(current_delta);
                current_deltas.addAll(uccmNonProgressiveContainerDeltas);
                current_deltas.addAll(smokeTestDeltas);

                InterleavedOrchestration interleaved = Orchestrations.interleaved("Rollout Deployment " + deployed.getName() + " #" + (i + 1), current_deltas);
                orchestrationList.add(interleaved);
            }


        }
        return Orchestrations.serial(this.descForAppDeployment(specification.getDeployedApplication()), orchestrationList);

    }

    private String descForAppDeployment(DeployedApplication deployedApplication) {
        return deployedApplication.getVersion().getApplication().getName();
    }


    private class IsTypeOf implements Predicate<Delta> {
        private final String typeName;

        private IsTypeOf(String typeName) {
            this.typeName = typeName;
        }

        public boolean apply(Delta delta) {
            Deployed deployed = delta.getDeployed() == null ? delta.getPrevious() : delta.getDeployed();
            Boolean is = deployed.getType().toString().equals(typeName);
            return is;
        }
    }

    private class IsPropertyTrue implements Predicate<Delta> {
        private final String propertyName;

        private IsPropertyTrue(String propertyName) {
            this.propertyName = propertyName;
        }

        public boolean apply(Delta delta) {
            Deployed deployed = delta.getDeployed() == null ? delta.getPrevious() : delta.getDeployed();
            if (!deployed.hasProperty(propertyName))
                return false;
            Boolean v = deployed.getProperty(propertyName);
            return v;
        }
    }


}
