import html

import gradio as gr
from .tools.sandbox_tools import reset_sandbox

from repopilot.crew import Repopilot


def _render_recommendation_card(recommendation) -> str:
    return f"""
    <div class="rec-card">
        <div class="rec-rank">#{recommendation.rank}</div>
        <h3 class="rec-title">{html.escape(recommendation.title)}</h3>
        <p class="rec-meta"><strong>Impact:</strong> {html.escape(recommendation.impact)}</p>
        <p class="rec-meta"><strong>Difficulty:</strong> {html.escape(recommendation.difficulty)}</p>
        <p class="rec-meta"><strong>Estimated time:</strong> {html.escape(recommendation.estimated_time)}</p>
        <div class="rec-section">
            <h4>What to change</h4>
            <p class="rec-desc">{html.escape(recommendation.description)}</p>
        </div>
    </div>
    """


def analyze_repository(repo_url: str):
    reset_sandbox()
    if not repo_url.strip():
        return "<p class='rec-message'>⚠️ Please enter a GitHub repository URL.</p>"

    try:
        result = Repopilot().crew().kickoff(
            inputs={"input_url": repo_url.strip()}
        )

        report = result.pydantic

        if report is None:
            return f"<pre class='rec-fallback'>{html.escape(str(result.raw))}</pre>"

        cards = "".join(
            _render_recommendation_card(recommendation)
            for recommendation in report.recommendations
        )

        return f"""
        <div class="report-wrap">
            <h1 class="report-title">🚀 RepoPilot Report</h1>
            <div class="rec-grid">
                {cards}
            </div>
        </div>
        """

    except Exception as e:
        return f"""
        <div class="rec-error">
            <h2>❌ Something went wrong</h2>
            <pre>{html.escape(str(e))}</pre>
        </div>
        """


def run():
    reset_sandbox()
    css = """
    .gradio-container {
        max-width: 1100px !important;
        margin: auto !important;
    }

    .hero {
        text-align: center;
        padding: 35px 20px 20px 20px;
    }

    .hero h1 {
        font-size: 42px;
        margin-bottom: 8px;
    }

    .hero p {
        font-size: 17px;
        opacity: 0.7;
    }

    .report {
        margin-top: 25px;
    }

    .report-wrap {
        margin-top: 10px;
    }

    .report-title {
        font-size: 28px;
        margin: 0 0 20px 0;
        text-align: center;
    }

    .rec-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 20px;
    }

    .rec-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        display: flex;
        flex-direction: column;
        height: 100%;
    }

    .rec-rank {
        font-size: 13px;
        font-weight: 700;
        color: #6366f1;
        margin-bottom: 8px;
    }

    .rec-title {
        font-size: 17px;
        line-height: 1.35;
        margin: 0 0 12px 0;
    }

    .rec-meta {
        font-size: 13px;
        margin: 4px 0;
        line-height: 1.45;
    }

    .rec-section {
        margin-top: auto;
        padding-top: 12px;
    }

    .rec-section h4 {
        font-size: 14px;
        margin: 0 0 8px 0;
    }

    .rec-desc {
        font-size: 13px;
        line-height: 1.5;
        margin: 0;
    }

    .rec-message,
    .rec-error {
        margin-top: 20px;
    }

    .rec-error pre,
    .rec-fallback {
        white-space: pre-wrap;
        word-break: break-word;
    }

    @media (min-width: 800px) {
        .rec-grid {
            grid-template-columns: repeat(3, 1fr);
            align-items: stretch;
        }
    }
    """

    with gr.Blocks(
        title="RepoPilot",
        css=css,
        theme=gr.themes.Soft(),
    ) as app:

        gr.HTML(
            """
            <div class="hero">
                <h1>🚀 RepoPilot</h1>
                <p>
                    Analyze any GitHub repository and discover what to build next.
                </p>
            </div>
            """
        )

        with gr.Row():
            repo_url = gr.Textbox(
                label="GitHub Repository",
                placeholder="https://github.com/user/repository",
                scale=4,
            )

            analyze_button = gr.Button(
                "Analyze Repository",
                variant="primary",
                scale=1,
            )

        gr.Markdown(
            "RepoPilot will inspect the codebase and recommend "
            "the most valuable improvements or features for future PRs."
        )

        output = gr.HTML(
            label="Analysis Report",
            elem_classes=["report"],
        )

        analyze_button.click(
            fn=analyze_repository,
            inputs=repo_url,
            outputs=output,
        )

        repo_url.submit(
            fn=analyze_repository,
            inputs=repo_url,
            outputs=output,
        )

    app.launch()


if __name__ == "__main__":
    run()