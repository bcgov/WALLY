if [[ ! -z $pull_request && $action == 'closed' ]]
then
	# delete resources created for this pull request
	oc delete all,sa,role,rolebinding -n d1b5d2-dev -l app=wally-pr-$pull_request
	oc delete all -n d1b5d2-tools -l app=wally-pr-$pull_request
    oc delete all,pvc,cm -n d1b5d2-dev -l statefulset=wally-psql-pr-$pull_request
    oc delete all,pvc,cm -n d1b5d2-dev -l cluster-name=wally-psql-pr-$pull_request
    
    # remove image tags in dev and tools
    oc tag -d -n d1b5d2-dev wally-web:pr-$pull_request
    oc tag -d -n d1b5d2-tools wally-web:pr-$pull_request
    oc tag -d -n d1b5d2-dev wally-api:pr-$pull_request
    oc tag -d -n d1b5d2-tools wally-api:pr-$pull_request
    oc tag -d -n d1b5d2-dev wally-reporting:pr-$pull_request
    oc tag -d -n d1b5d2-tools wally-reporting:pr-$pull_request
    
fi
