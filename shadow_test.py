import json
from google import genai

client = genai.Client(api_key="API_KEY")

with open("summary.json") as f:
    summary = json.load(f)

with open("prompt_logic.md") as f:
    prompt_logic = f.read()

prompt = f"""
{prompt_logic}

Important rules:

1. Every output line MUST contain:
   spack install <package>@<version> ^<dependency>@<new_version>

2. The dependency MUST come from the "unbounded" list.

3. The dependency version MUST be newer than those implied by the metadata
   (for example increase the major or minor version).

4. Do NOT output build variants such as build_system or %cmake.

Return exactly 3 lines.

Metadata:
{json.dumps(summary)}
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

text = response.text.strip()

commands = []
for line in text.splitlines():
    line = line.strip()
    if line.startswith("spack install"):
        commands.append(line)

commands = commands[:3]

with open("spack_spec.md", "w") as f:
    f.write("# Potential Off-Leading-Edge Scenarios\n\n")
    for c in commands:
        f.write(c + "\n")

for c in commands:
    print(c)