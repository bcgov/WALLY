# This script cleans up dev environments (pull request environments) after
# the pull request is merged or closed.
#
# Usage: Add the script to a Jenkins event/pipeline that gets triggered
# by a webhook.  It requires parameters pull_request and action. Register the
# webhook in the GitHub repo's settings.
#
# This script is currently run by Jenkins > Events > ON_PR_CLOSED.
#
# The webhook payload contains the pull request number and action.
# A "closed" action indicates that the pull request was either 
# merged or closed (there is no separate "merged" status).

if [[ ! -z $pull_request && $action == 'closed' ]]
then
	# delete resources created for this pull request
	oc delete all,sa,role,rolebinding -n bfpeyx-dev -l app=wally-pr-$pull_request
	oc delete all -n bfpeyx-tools -l app=wally-pr-$pull_request
    oc delete all,pvc,cm -n bfpeyx-dev -l statefulset=wally-psql-pr-$pull_request
    
    # remove image tags in dev and tools
    oc tag -d -n bfpeyx-dev wally-web:pr-$pull_request
    oc tag -d -n bfpeyx-tools wally-web:pr-$pull_request
    oc tag -d -n bfpeyx-dev wally-api:pr-$pull_request
    oc tag -d -n bfpeyx-tools wally-api:pr-$pull_request
    
fi
