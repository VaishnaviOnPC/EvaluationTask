## Write up
To avoid redundant CI executions, generated test scenarios can be filtered so that only configurations representing different dependency combinations are executed.

Each test scenario is generated via 'spack install' command. AI can use Spack's metadata for packages and versions to generate the scenarios. We can find similarity between two scenarios by comparing the top-level package, package version, dependency name, and dependency version. And then use a simple distance metric that assigns a certain reward value when the components differ. If the distance between two configurations is below a threshold, they are considered equivalent and only one is executed in CI. Before executing a test scenario, it is compared against previous run configurations. If it is similar to an existing test, it can also be skipped.

Since Spack specs internally represent builds as dependency graphs, similarity detection can operate on the full dependency DAG. This can be done by comparing dependency DAGs to detect overlaps between configurations. This can form a system that can compare similarities across the graphs to catch overlaps.

After filtering, the remaining scenarios can be passed to the CI orchestration layer, which schedules the most informative builds for execution.

To support stacks of 100+ packages, the system:
1. Compresses metadata into a minimal JSON representation
2. Limits the prompt to essential fields (versions, dependencies, unbounded constraints)
3. Generates test scenarios heuristically
4. Filters redundant scenarios using a similarity metric before CI execution

## Concepts used: 
Dependency DAG, Heuristic scenario generation, Distance-based similarity metric, Redundant scenario pruning, CI test scheduling.

## Pipeline Explanation:
Spack metadata -> compressed summary -> AI generates risky configs (done via prompting in this task) -> valid versions enforced from metadata -> similarity filtering -> CI execution