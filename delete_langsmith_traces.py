from langsmith import Client

client = Client()
project_name = "Promblem-first-ai-demo"

# Fetch all runs in the project
runs = client.list_runs(project_name=project_name)

# Delete each run
for run in runs:
    print(f"Deleting: {run.name} ({run.id})")
    client.delete_run_from_annotation_queue({'run_id': run.id})

