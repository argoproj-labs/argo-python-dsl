Changelog
=========


0.4.0
-----
- [release-0.4.0] update tests to be compatibel with argo-sdk. [Yudi
  Xue]

  - compatible with argo-client-python 4.0.1
- [release-0.4.0] make argo-python-dsl compatible with latest sdk. [Yudi
  Xue]

  - align with argo-python-client 4.0.1
- :tada: Release 0.4.0. [Yudi Xue]
- Update README.md. [Yudi Xue]

  remove contributors since github provides that info
- :tada: Release 0.3.0 (#15) [Yudi Xue]


v0.3.0 (2020-11-17)
-------------------
- :tada: Release 0.3.0. [Yudi Xue]
- [master] fix CI. [Yudi Xue]
- Release 0.2.0 (#14) [Yudi Xue]

  * [release-0.2.0] use argo-workflows 3.6

  * :tada: Release 0.2.0


v0.2.0 (2020-11-17)
-------------------

Changes
~~~~~~~
- Updated README due to migration to argoproj-labs. [Marek Cermak]
- Return workflow result on submit. [asavpatel92]

  modified:   argo/workflows/dsl/_workflow.py
  modified:   tests/test_workflow.py

Fix
~~~
- Make sure both, swagger and openapi code works. [Marek Cermak]
- :pushpin: Lock dependencies. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  modified:   Pipfile
  modified:   Pipfile.lock
- Fixed compilation issue with multiple instances. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  modified:   argo/workflows/dsl/_base.py
  modified:   argo/workflows/dsl/_workflow.py
  modified:   tests/test_workflow.py
- Updated return type and doc strings, improve test. [asavpatel92]

  modified:   argo/workflows/dsl/_workflow.py
  modified:   tests/test_workflow.py

Other
~~~~~
- :tada: Release 0.2.0. [Yudi Xue]
- [release-0.2.0] use argo-workflows 3.6. [Yudi Xue]
- Feat: Add (Cluster)WorkflowTemplate DSL (#13) [Pablo Osinaga]

  * feat: Add WorkflowTempate DSL

  * feat: Add ClusterWorkflowTempate DSL

  * fix: update argo workflow client version to 3.5
- Feat: Add CronWorkflow DSL (#12) [Pablo Osinaga]
- Ci: add integration tests workflows (#11) [Pablo Osinaga]

  * ci(integration):  add artifacts workflow

  * ci(integration): add script workflow

  * ci(integration): add loop workflow

  * docs: integration tests
- Ci: add integration tests (#9) [Pablo Osinaga]
- Use argo workflows v3.5 (#8) [binarycrayon]

  * [argo-workflows-3.5] set argo-workflows 3.5 as dep

  Signed-off-by: Yudi Xue <10211+binarycrayon@users.noreply.github.com>

  * [arge-workflows-v3.5] fix a bug

  - image kwarg for Template should not be None

  Signed-off-by: Yudi Xue <10211+binarycrayon@users.noreply.github.com>

  * [argo-workflows-v3.5] update readme and github worklow

  - update workflow to test python 3.6, 3.7, 3.8
  - show CI badge

  Signed-off-by: Yudi Xue <10211+binarycrayon@users.noreply.github.com>

  * [argo-workflows-v3.5] only submit wf with generate_name

  - when both 'name' and 'generate_name' present in metadata, name is prefered
  - change design to use generate_name only
- Bad model ref (#1) [Ross Crawford-d'Heureuse, Ross
  Crawford-d'Heureuse]


v0.1.0-rc (2020-03-08)
----------------------

New
~~~
- Added `Workflow.to_file` method. [Marek Cermak]
- :clipboard: Document closures and scopes. [Marek Cermak]
- Organize closure imports. [Marek Cermak]
- Multi-line strings are represented as blocks. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  modified:   argo/workflows/sdk/_utils.py
  modified:   argo/workflows/sdk/_workflow.py
- Implemented scoped closures. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  modified:   argo/workflows/sdk/_base.py
  modified:   argo/workflows/sdk/_workflow.py
  modified:   argo/workflows/sdk/templates.py
- Added `submit` function to submit a Workflow. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  modified:   argo/workflows/sdk/_base.py
  modified:   argo/workflows/sdk/_workflow.py
- Closure accepts V1alpha1ScriptTemplate attributes. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  modified:   argo/workflows/sdk/_base.py
  modified:   argo/workflows/sdk/templates.py
- Added Workflow utility methods. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  modified:   Pipfile
  modified:   Pipfile.lock
  modified:   argo/workflows/sdk/_workflow.py
  modified:   argo/workflows/sdk/templates.py
  new file:   tests/__init__.py
  new file:   tests/_base.py
  new file:   tests/data/workflows/hello-world.yaml
  new file:   tests/test_workflow.py
- Workflow spec can be configured with class properties. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  modified:   argo/workflows/sdk/_workflow.py
  modified:   argo/workflows/sdk/templates.py
- Added scripts and closure examples. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  new file:   examples/scripts.ipynb
  new file:   examples/scripts.yaml
- Added `closure` Prop. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  modified:   argo/workflows/sdk/tasks.py
  modified:   argo/workflows/sdk/templates.py
  modified:   examples/resource.ipynb
- Added resource example. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  modified:   argo/workflows/sdk/templates.py
  new file:   examples/resource.ipynb
  new file:   examples/resource.yaml

Changes
~~~~~~~
- Do not truncate version in the commit message. [Marek Cermak]
- Argo Workflows SDK -> Argo Workflows DSL. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  modified:   README.md
  renamed:    argo/workflows/sdk/__about__.py -> argo/workflows/dsl/__about__.py
  renamed:    argo/workflows/sdk/__init__.py -> argo/workflows/dsl/__init__.py
  renamed:    argo/workflows/sdk/_arguments.py -> argo/workflows/dsl/_arguments.py
  renamed:    argo/workflows/sdk/_base.py -> argo/workflows/dsl/_base.py
  renamed:    argo/workflows/sdk/_inputs.py -> argo/workflows/dsl/_inputs.py
  renamed:    argo/workflows/sdk/_outputs.py -> argo/workflows/dsl/_outputs.py
  renamed:    argo/workflows/sdk/_utils.py -> argo/workflows/dsl/_utils.py
  renamed:    argo/workflows/sdk/_workflow.py -> argo/workflows/dsl/_workflow.py
  renamed:    argo/workflows/sdk/tasks.py -> argo/workflows/dsl/tasks.py
  renamed:    argo/workflows/sdk/templates.py -> argo/workflows/dsl/templates.py

  modified:   Makefile
  modified:   argo/workflows/dsl/__about__.py
  modified:   argo/workflows/dsl/__init__.py
  modified:   argo/workflows/dsl/_utils.py
  modified:   examples/artifacts.ipynb
  modified:   examples/dag-diamond.ipynb
  modified:   examples/hello-world-single-task.ipynb
  modified:   examples/hello-world.ipynb
  modified:   examples/resource.ipynb
  modified:   examples/scripts.ipynb
  modified:   setup.py
  modified:   tests/__init__.py
  modified:   tests/test-notebooks.sh
  modified:   tests/test_workflow.py
- Arguments.artifact -> artifact. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  modified:   argo/workflows/sdk/_arguments.py
  modified:   argo/workflows/sdk/_inputs.py
  modified:   argo/workflows/sdk/_outputs.py
  modified:   argo/workflows/sdk/_workflow.py
  modified:   argo/workflows/sdk/tasks.py
  modified:   argo/workflows/sdk/templates.py
- Allow to disable `omitempty` in `to_yaml` [Marek Cermak]
- Added skip CI flags. [Marek Cermak]

Fix
~~~
- Fixed invalid Makefile variable. [Marek Cermak]
- Fixed missing target in the Makefile. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  modified:   .gitchangelog.rc
  modified:   Makefile
- Fixed Workflow.submit parameter handling. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  modified:   argo/workflows/dsl/_base.py
  modified:   argo/workflows/dsl/_workflow.py
  modified:   tests/test_workflow.py
- Fix Workflow.from_url. [Yudi Xue - binarycrayon]

  Workflow.from_url should be using url argument to fetch yaml
- Change __extra__ to __origin__ in python >=3.7. [Marek Cermak]
- Fill missing parameter value. [Marek Cermak]
- Fixed multiple inputs/outputs being discarded. [Marek Cermak]
- Omitempty should only discard None. [Marek Cermak]
- Fixed newlines being removed with trailing spaces. [Marek Cermak]
- Fixed closures with undefined scope. [Marek Cermak]
- Closures should not be called. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  modified:   argo/workflows/sdk/_base.py
  modified:   argo/workflows/sdk/templates.py

Other
~~~~~
- :tada: Release 0.1.0-rc. [Marek Cermak]


v0.1.0-dev (2019-12-19)
-----------------------

New
~~~
- Added badges to the README. [Marek Cermak]
- Added issue templates and CI workflow. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  new file:   .github/ISSUE_TEMPLATE/bug_report.md
  new file:   .github/ISSUE_TEMPLATE/feature_request.md
  new file:   .github/ISSUE_TEMPLATE/minor-release.md
  new file:   .github/ISSUE_TEMPLATE/patch-release.md
  new file:   .github/ISSUE_TEMPLATE/pre-release.md
  new file:   .github/ISSUE_TEMPLATE/question.md
  new file:   .github/ISSUE_TEMPLATE/task.md
  new file:   .github/workflows/ci.yml
  new file:   .github/workflows/package-release.yml
- Added notebook tests. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  modified:   Pipfile.lock
  modified:   examples/artifacts.ipynb
  modified:   examples/dag-diamond.ipynb
  modified:   examples/hello-world-single-task.ipynb
  modified:   examples/hello-world.ipynb
  new file:   tests/test-notebooks.sh
- Updated README with the Artifact example. [Marek Cermak]
- Updated README with Dag Diamond example. [Marek Cermak]
- Artifact passing. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  modified:   Pipfile
  modified:   Pipfile.lock
  modified:   argo/workflows/sdk/_arguments.py
  modified:   argo/workflows/sdk/_inputs.py
  new file:   argo/workflows/sdk/_outputs.py
  modified:   argo/workflows/sdk/_workflow.py
  modified:   argo/workflows/sdk/tasks.py
  modified:   argo/workflows/sdk/templates.py
  new file:   examples/artifacts.ipynb
  new file:   examples/artifacts.yaml
  modified:   examples/dag-diamond.ipynb
  modified:   examples/dag-diamond.yaml
- Updated README with Hello World example. [Marek Cermak]
- Added possibility to pass parameters to tasks. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  modified:   argo/workflows/sdk/_arguments.py
  modified:   argo/workflows/sdk/_base.py
  modified:   argo/workflows/sdk/_workflow.py
  modified:   argo/workflows/sdk/tasks.py
  modified:   argo/workflows/sdk/templates.py
  new file:   examples/dag-diamond.ipynb
  new file:   examples/dag-diamond.yaml
- Allow input parameters to the template spec. [Marek Cermak]
- Added hello-world example. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  new file:   ../../examples/hello-world.ipynb
  new file:   ../../examples/hello-world.yaml
- New: usr: Initial implementation of @template. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  modified:   sdk/__init__.py
  modified:   sdk/_workflow.py
  new file:   sdk/_utils.py
  new file:   sdk/templates.py
  renamed:    sdk/task.py -> sdk/tasks.py
- Initial implementation of the Workflow class. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  modified:   sdk/__init__.py
  modified:   sdk/_workflow.py
- New: dev: Initial implementation of a @task. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  new file:   argo/workflows/__init__.py
  new file:   argo/workflows/sdk/__init__.py
  new file:   argo/workflows/sdk/_base.py
  new file:   argo/workflows/sdk/_task.py
- Added .gitignore. [Marek Cermak]

Changes
~~~~~~~
- Use pure pip instead of pipenv for the CI. [Marek Cermak]
- Input parameters have to be provided explicitly. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  new file:   argo/workflows/sdk/_inputs.py
  modified:   argo/workflows/sdk/_arguments.py
  modified:   argo/workflows/sdk/_base.py
  modified:   argo/workflows/sdk/_workflow.py
  modified:   argo/workflows/sdk/tasks.py
  modified:   argo/workflows/sdk/templates.py
  modified:   examples/dag-diamond.ipynb
- Refactor template specification and compilation. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  modified:   argo/workflows/sdk/_base.py
  modified:   argo/workflows/sdk/_workflow.py
  modified:   argo/workflows/sdk/tasks.py
  modified:   argo/workflows/sdk/templates.py
  modified:   examples/hello-world.ipynb
- Compile a Workflow on instance initialization. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  modified:   Pipfile
  modified:   Pipfile.lock
  modified:   argo/workflows/sdk/_workflow.py
  modified:   argo/workflows/sdk/tasks.py
  modified:   argo/workflows/sdk/templates.py
  modified:   examples/hello-world.yaml
- Excluded some of the props from the task spec. [Marek Cermak]

Fix
~~~
- Fixed TTY issue with the CI. [Marek Cermak]
- Fixed CI python permission issue. [Marek Cermak]
- Fixed CI permission issues. [Marek Cermak]
- Fixed missing s2i binary in the CI. [Marek Cermak]
- Fixed misplaced result of compilation hook. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  modified:   argo/workflows/sdk/_base.py
  modified:   argo/workflows/sdk/tasks.py
  modified:   examples/hello-world-single-task.yaml
- Fixed invalid task template reference. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  modified:   argo/workflows/sdk/_base.py
  modified:   argo/workflows/sdk/_workflow.py
  modified:   argo/workflows/sdk/tasks.py
  new file:   examples/hello-world-single-task.ipynb
  new file:   examples/hello-world-single-task.yaml
- Fixed spec return annotation. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  modified:   argo/workflows/sdk/_base.py
  modified:   argo/workflows/sdk/_workflow.py
- Fixed issue with argument passing. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  modified:   argo/workflows/sdk/_base.py
  modified:   argo/workflows/sdk/_workflow.py
  modified:   examples/hello-world.ipynb
- Allow a Spec to be called as a function. [Marek Cermak]

  Signed-off-by: Marek Cermak <macermak@redhat.com>

  new file:   argo/workflows/sdk/__about__.py
  modified:   argo/workflows/sdk/_base.py
  modified:   argo/workflows/sdk/_workflow.py
  modified:   argo/workflows/sdk/tasks.py


