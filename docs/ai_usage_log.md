# AI Usage Log

This log records our team's collaborative development process with artificial intelligence tools. The purpose of this log is to be transparent about the use of artificial intelligence in the design and construction of our project throughout different stages, such as planning, brainstorming, making architectural decisions following best practices, and streamlining repetitive tasks where AI can reduce execution times and improve efficiency.

## AI Tools Used

- **Tools:** Claude Code, Google Gemini
- **Primary Tasks:** AI agents acted as our consultants to create a robust execution plan, evaluate different modeling options, propose adequate tests for both our model and our pipeline, and implement a compelling and seamless interface for our web application. Additionally, throughout this project, AI agents helped clarify questions regarding how to collaborate between team members on GitHub, ensuring a clear and structured collaboration process.

In the following section, we outline in detail the contributions and outcomes of the tasks assigned to our AI agents.

## Task Breakdown

| Task | AI Contribution | Outcome |
|---|---|---|
| **Project Execution Plan** | Evaluated gaps in the initial execution plan proposed by our team, highlighting possible issues and providing recommendations on best practices for architecture, modeling, evaluation, and application deployment. | Successfully built a robust execution plan before the creation of the model and the pipeline, ensuring an effective workflow for our team and the AI agents. |
| **Model Optimization** | Suggested alternatives to our team's initial proposal of building linear and logistic regressions by recommending the implementation of a LightGBM model with Optuna hyperparameter tuning. | Successfully guided our team to implement a LightGBM model with Optuna hyperparameter tuning in Python. |
| **API Debugging** | Diagnosed 401/429 errors and identified the need for SimFin v3 mapping (GOOGL -> GOOG). | Resolved authentication issues and implemented robust error handling. |
| **UI/UX Design** | Injected custom CSS to implement a minimal aesthetic. | Created a professional dashboard without standard Streamlit defaults. |
| **Trading Strategy** | Developed the backtesting simulation logic and equity curve visualization. | Provided a functional comparison between AI signals and Benchmark returns. |

## Reflections

- **What worked well:** Working with AI agents throughout all phases of this project proved to be highly efficient. We recognize the value in leveraging AI agents for filling knowledge gaps, researching best practices, debugging the first iterations of our pipeline, and highlighting possible issues.

- **Challenges:** Although AI agents proved to be highly efficient for specific tasks in this project, it is necessary to highlight the limitations of their capabilities and the importance of remaining involved in all decisions throughout the project. Having a clear understanding of the project's requirements and expected outcomes is key to delivering the best possible results and improving our collaboration with AI agents.

- **Learning:** For many of us, this was our first experience in building a machine learning pipeline applied to financial markets. Therefore, using AI agents to inform our team about the best possible practices, both for planning and execution, was of great value to all of us. A clear example of this was the proposal by one of our AI agents to implement a battery of indicators alongside our model to achieve the best possible results for our predictions.
