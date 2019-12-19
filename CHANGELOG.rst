Changelog
=========


master
------

New
~~~
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


