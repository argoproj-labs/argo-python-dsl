#!/bin/bash
set -x

for nb_path in $(ls examples/*.ipynb); do
{
    notebook="$(basename ${nb_path})"

    echo "---"
    echo "--- Test: ${notebook}"
    echo "---"

    {
        set -euo pipefail
        set +x

        IMAGE_NAME="s2i-test-${notebook%%.*}"

        s2i build \
        --rm \
        --env JUPYTER_NOTEBOOK_PATH="$notebook" \
        'examples/' quay.io/cermakm/jupyter-notebook-s2i ${IMAGE_NAME} \
        > "/tmp/test-${notebook}-build.stdout"

        docker run \
        -v $(pwd)/argo/workflows/sdk/:/opt/app-root/lib/python3.6/site-packages/argo/workflows/sdk/:ro,z \
        -v $(pwd)/examples/:/opt/app-root/src/examples/:ro,z \
        --env JUPYTER_NOTEBOOK_PATH="examples/$notebook" \
        --name "test-${notebook}" \
        --rm -it \
        --user $(id -u) \
        ${IMAGE_NAME}:latest
    }

    res=$?

    # cleanup
    docker rmi ${IMAGE_NAME} || true

    if [ $res -ne 0 ]; then
      echo "--- Test: ${notebook} ... FAILED\n" ; exit 1  # fail fast
    else
      echo "--- Test: ${notebook} ... PASSED\n"
    fi
}
done

exit 0
