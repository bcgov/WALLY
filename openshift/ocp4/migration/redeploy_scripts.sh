#!/bin/bash
oc -n $1 delete configmap migration-scripts
oc -n $1 create configmap migration-scripts --from-file=scripts/
oc -n $1 rollout latest dc/migrator-cli
oc -n $1 rollout status dc/migrator-cli
