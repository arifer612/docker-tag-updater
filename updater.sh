#!/bin/bash

set -euo pipefail

################################################################################
# @section Global variables
# @description This section sets the default global variables that are expected
# by the functions to follow. The names are descriptive.

IMAGE_NAME=$1
BASE_TAG=${2:-latest}
RULE=${3:-default}
VERBOSE=${4:-false}
COMPOSE_FILE=${5:-compose.yaml}

WORKSPACE=${GITHUB_WORKSPACE:-$(pwd)}
OUTPUT=${GITHUB_OUTPUT:-/dev/stdout}
NEW_IMAGE=""
GIT_BRANCH=""
GIT_MSG=""
GIT_DESC=""
UPDATED_VERSIONS=()

OPTS="--tag ${BASE_TAG} --rule ${RULE}"
if $VERBOSE; then
    OPTS="$OPTS --verbose"
fi

################################################################################
# @section General functions
# @description This section provides useful functions that can be used
# everywhere.

# @description Log if verbose.
verbose-log () {
    if $VERBOSE; then
        echo "$@"
    fi
}

################################################################################
# @section Compose file
# @description Update the Compose file with the most up-to-date version tag.

# If run as an Action, change to the appropriate workspace.
cd $WORKSPACE

IMAGE_VERSIONS="$(
    grep $IMAGE_NAME $COMPOSE_FILE | \
    cut -d ':' -f 2- | \
    tr -d '[:blank:]' | \
    uniq
)"

verbose-log "Checking ${IMAGE_NAME}"
while read IMAGE; do
    if [[ -z $NEW_IMAGE ]]; then
        verbose-log "Getting new version for ${IMAGE_NAME}"
        NEW_IMAGE=$(image-version-checker $IMAGE $OPTS | tail -n 1)
        verbose-log "The most up-to-date image version is ${NEW_IMAGE}"
    fi
    if [[ "$IMAGE" != "$NEW_IMAGE" ]]; then
        verbose-log "Updating ${IMAGE} with ${NEW_IMAGE}..."
        sed -i "s|${IMAGE}|${NEW_IMAGE}|" $COMPOSE_FILE
        UPDATED_VERSIONS+=("$(echo $IMAGE | cut -d ':' -f 2)")
    else
        verbose-log "${IMAGE} needs not be updated."
    fi
done <<< $IMAGE_VERSIONS

NEW_IMAGE_VERSION=$(echo $NEW_IMAGE | cut -d ':' -f 2)

################################################################################
# @section Git
# @description Prepare the Git message.

if [[ ${#UPDATED_VERSIONS[@]} -eq 0 ]]; then
    echo "commit-message=" >> $OUTPUT
    echo "commit-description=" >> $OUTPUT
    echo "git-branch=" >> $OUTPUT
    exit 0
fi

# @description Get the name of the image without the owner.
PARSED_IMAGE_NAME="$(
    image-version-checker --parse $IMAGE_NAME | \
    awk '{print $2}' | \
    rev | \
    cut -d '/' -f 1 | \
    rev
)"

GIT_MSG="chore: bump"
GIT_BRANCH="bump/${PARSED_IMAGE_NAME}-${NEW_IMAGE_VERSION}"

if [[ ${#UPDATED_VERSIONS[@]} -eq 1 ]]; then
    GIT_MSG="${GIT_MSG} ${PARSED_IMAGE_NAME} from ${UPDATED_VERSIONS[0]} to ${NEW_IMAGE_VERSION}"
else
    GIT_MSG="${GIT_MSG} ${PARSED_IMAGE_NAME} to ${NEW_IMAGE_VERSION}"
    GIT_DESC="The following versions of ${PARSED_IMAGE_NAME} were updated:"
    for UPDATED_VERSION in ${UPDATED_VERSIONS[@]}; do
        GIT_DESC+="\n- ${UPDATED_VERSION}"
    done
fi

echo "commit-message=\"${GIT_MSG}\"" >> $OUTPUT
echo "commit-description=\"${GIT_DESC}\"" >> $OUTPUT
echo "git-branch=\"${GIT_BRANCH}\"$" >> $OUTPUT
