#!/usr/bin/env bash
# @name compose-updater
# @brief Script to update image version tags in your Compose file.

set -euo pipefail


################################################################################
# @section Help message

HELP () {
    >&2 cat << EOF
Update image version tags in your Compose/Stack file.

Syntax: $0
        [-t|--tag BASE_TAG]
        [-r|--rule RULE]
        [-f|--file COMPOSE_FILENAME]
        [-v|--verbose]
        IMAGE_NAME

Arguments:
    IMAGE_NAME:       The name of the container image.

Options:
    BASE_TAG:           The image tag to compare against, e.g., latest, develop,
                        edge, etc. (default: latest)"
    RULE:               The regex rule to parse the version tags. Supports
                        default, lscr. (default: default)
    COMPOSE_FILENAME:   The filename of the Compose/Stack file.
                        (default: compose.yaml)

Flags:
    VERBOSE: Add verbosity.
EOF
    exit 1
}

IMAGE_NAME=""
BASE_TAG="latest"
RULE="default"
VERBOSE=false
COMPOSE_FILENAME="compose.yaml"


VALID_ARGS=$(getopt -o ht:r:f:v -l help,tag:,rule:,file:,verbose -- "$@" || HELP)

eval set -- ${VALID_ARGS}
while :; do
    case $1 in
        -h | --help) HELP ;;
        -t | --tag) BASE_TAG=$2; shift 2 ;;
        -r | --rule) RULE=$2; shift 2 ;;
        -f | --file) COMPOSE_FILENAME=$2; shift 2 ;;
        -v | --verbose) VERBOSE=true; shift ;;
        --) shift; break ;;
        *) >&2 echo Unsupported option: $1; HELP ;;
    esac
done

if [[ $# -eq 0 ]]; then
    >&2 echo "Error: An image name is required!"
    >&2 echo
    HELP
fi

IMAGE_NAME=$1

################################################################################
# @section Global variables
# @description This section sets the default global variables that are expected
# by the functions to follow. The names are descriptive.

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
# @internal
verbose-log () {
    if $VERBOSE; then
        echo "$@"
    fi
}

# @descrition Print out the necessary variables used to construct a Git commit
# message.
output () {
    echo "commit-message=${GIT_MSG}" >> $OUTPUT
    echo "commit-description=${GIT_DESC}" >> $OUTPUT
    echo "git-branch=${GIT_BRANCH}" >> $OUTPUT
    exit 0
}

################################################################################
# @section Compose file
# @description Update the Compose file with the most up-to-date version tag. If
# this script is run as an action, i.e., the variable GITHUB_WORKSPACE is set,
# the default workspace will first be changed to that. After which, all
# instances of the image in the Compose file will be updated.

# If run as an Action, change to the appropriate workspace.
cd $WORKSPACE


if $(! grep -q $IMAGE_NAME $COMPOSE_FILENAME); then
    echo $IMAGE_NAME cannot be found in $COMPOSE_FILENAME
    exit 2
fi

IMAGE_VERSIONS="$(
    grep "image:.*${IMAGE_NAME}" $COMPOSE_FILENAME | \
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
        sed -i "s|${IMAGE}|${NEW_IMAGE}|" $COMPOSE_FILENAME
        UPDATED_VERSIONS+=("$(echo $IMAGE | cut -d ':' -f 2)")
    else
        verbose-log "${IMAGE} needs not be updated."
    fi
done <<< $IMAGE_VERSIONS

NEW_IMAGE_VERSION=$(echo $NEW_IMAGE | cut -d ':' -f 2)

################################################################################
# @section Git outputs
# @description Prepare the output variables for a Git message. If there is
# nothing updated, the output will be empty. Otherwise, the output will be three
# variables detailing a standard Git commit message, description, and the name
# of a new branch for the changes.


if [[ ${#UPDATED_VERSIONS[@]} -eq 0 ]]; then
    output
fi

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

output
