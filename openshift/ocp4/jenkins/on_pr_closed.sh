if [[ ! -z $pull_request && $action == 'closed' ]]
then
	# delete resources created for this pull request
	oc delete all,sa,role,rolebinding -n bfpeyx-dev -l app=wally-pr-$pull_request
	oc delete all -n bfpeyx-tools -l app=wally-pr-$pull_request
    oc delete all,pvc,cm -n bfpeyx-dev -l statefulset=wally-psql-pr-$pull_request
    oc delete all,pvc,cm -n bfpeyx-dev -l cluster-name=wally-psql-pr-$pull_request
    
    # remove image tags in dev and tools
    oc tag -d -n bfpeyx-dev wally-web:pr-$pull_request
    oc tag -d -n bfpeyx-tools wally-web:pr-$pull_request
    oc tag -d -n bfpeyx-dev wally-api:pr-$pull_request
    oc tag -d -n bfpeyx-tools wally-api:pr-$pull_request
    oc tag -d -n bfpeyx-dev wally-reporting:pr-$pull_request
    oc tag -d -n bfpeyx-tools wally-reporting:pr-$pull_request
    
fi
