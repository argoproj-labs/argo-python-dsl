for f in tests/workflows/*.py
do
    workflow=$(basename ${f%%.*})
    echo "Testing $workflow workflow ..."
    PYTHONPATH=. python $f
    argo submit -n argo tests/workflows/$workflow.yaml --name $workflow
    bash scripts/validate_workflow.sh $workflow
    echo "Testing $workflow workflow ... done!\n"
done
