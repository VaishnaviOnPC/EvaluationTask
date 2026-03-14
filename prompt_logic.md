# AI Prompt Logic for Off-Leading-Edge Risk Detection

# System Prompt

You are a developer familiar with Spack package specifications and dependency compatibility issues.

Context  
You are given a compressed JSON summary of package metadata extracted from Spack.  
The metadata contains the following fields:

1. `pkg` - package name  
2. `v` - a list of recent package versions  
3. `deps` - direct dependencies  
4. `unbounded` - dependencies that do not have an upper version constraint  

This summary is designed to be compact so that it can be processed efficiently by an LLM.

Definition of Off-Leading-Edge Risk  
An off-leading-edge compatibility risk occurs when:

1. Package **A** depends on package **B**
2. The dependency **B** has no upper version bound
3. A **newer version of B** may introduce breaking changes
4. Continuous Integration (CI) pipelines usually test only versions available at the time of release

As a result, CI may miss configurations where an older version of a package is paired with a much newer version of one of its dependencies.

# Task Prompt

Using the provided metadata:

1. Examine the `unbounded` dependencies for each package.
2. Select a **middle version** from the package's "v" list. The list is ordered newest to oldest. Choose the SECOND version in the list.
3. Pair the package with a **hypothetical newer version** of one of its unbounded dependencies.
4. Construct a Spack installation specification that represents this potentially risky configuration.

# Constraints

1. Only use dependency names that appear in the metadata.
2. Assume the dependency has a **newer version than those historically tested**.
3. Avoid repeating the same package–dependency pair.
4. Generate **three unique configurations**.

# Output Format  

Return **only valid Spack commands** using the format:

spack install <package>@<version> ^<dependency>@<new_version>

Example: spack install root@6.36.04 ^arrow@13.0.0

# Output Rules

1. Output exactly **three commands**.
2. Do **not include explanations or additional text**.
3. Each line must contain a single valid Spack command.