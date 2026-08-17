# RepoPilot

RepoPilot is a multi-agent AI system powered by [crewAI](https://crewai.com) that analyzes GitHub repositories and recommends potential contributions and pull requests.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

```bash
crewai install
```

## Configuration

Add your API key to the `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

The default configuration uses OpenAI's **nano model**.

If you are using a provider other than OpenAI, or a different model, update your `.env` file with the appropriate API key and configuration. Then update the `llm` field in:

```text
src/repopilot/config/agents.yaml
```

Make sure the `llm` configuration matches the provider and model you are using.

Once your API key and model configuration are set, **you're good to go.**

## Customizing

* Modify `src/repopilot/config/agents.yaml` to define your agents
* Modify `src/repopilot/config/tasks.yaml` to define your tasks
* Modify `src/repopilot/crew.py` to add your own logic, tools, and specific arguments
* Modify `src/repopilot/main.py` to add custom inputs for your agents and tasks

## Running the Project

To start RepoPilot, run this from the root folder of your project:

```bash
crewai run
```

This launches the RepoPilot Gradio interface. Enter a GitHub repository URL and RepoPilot will analyze the repository and generate contribution recommendations.

## Understanding Your Crew

RepoPilot is composed of multiple AI agents, each with a specific role, goal, and set of tools.

The agents collaborate through a series of tasks:

1. **Cloner** — Creates a sandbox environment and clones the GitHub repository.
2. **Analyzer** — Reads through the codebase, connects files and components, and analyzes the architecture and dependencies.
3. **Reporter** — Reviews the analysis and produces the top three recommended contribution opportunities, ranked by impact, difficulty, and estimated effort.

Agent configurations are defined in:

```text
src/repopilot/config/agents.yaml
```

Task configurations are defined in:

```text
src/repopilot/config/tasks.yaml
```

## Support

For support, questions, or feedback regarding RepoPilot or crewAI:

* Visit the [crewAI documentation](https://docs.crewai.com)
* Visit the [RepoPilot GitHub repository](https://github.com/hoodadfarhad/repopilot)

Let's build better open-source contributions with AI. 🚀
