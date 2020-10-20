echo "Workflow Tests ... \n"

for f in tests/workflows/*.py
do
    workflow=$(basename ${f%%.*})
    echo "Testing $workflow workflow ..."
    PYTHONPATH=. python $f
    argo submit -n argo tests/workflows/$workflow.yaml --name $workflow
    bash scripts/validate_workflow.sh $workflow
    echo "Testing $workflow workflow ... done!\n"
done


echo "CronWorkflow Tests ... \n"
for f in tests/cronworkflows/*.py
do
    workflow=$(basename ${f%%.*})
    echo "Testing $workflow workflow ..."
    PYTHONPATH=. python $f
    argo cron create -n argo tests/cronworkflows/$workflow.yaml
    argo submit -n argo --from=cronwf/$workflow --name $workflow
    bash scripts/validate_workflow.sh $workflow
    echo "Testing $workflow workflow ... done!\n"
done
