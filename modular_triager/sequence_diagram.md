sequenceDiagram
    actor User as Support Developer
    participant UI as UI/Chatbot
    participant Agent as Trigger Agent
    participant LLM as Bedrock LLM
    participant OS as AWS Open Search
    participant CW as AWS Cloudwatch
    participant KB as Configuration<br/>Knowledge Base
    participant Output as Response to User

    User->>UI: Step 1: Request to Trigger a Race
    activate UI
    UI->>Agent: Send Request
    deactivate UI

    activate Agent
    Agent->>KB: Fetch Configuration
    KB-->>Agent: Return Config Details
    
    Agent->>LLM: Step 2: Create execution plan<br/>(System Prompt, tools, User Input)
    activate LLM
    LLM-->>Agent: Return Execution Plan
    deactivate LLM

    Agent->>OS: Step 3: Search Indexed S3 vectors<br/>to retrieve Race Data
    activate OS
    OS-->>Agent: Return Race Data
    deactivate OS

    Agent->>CW: Step 5: Send CW logs to LLM<br/>for summarizing & highlighting issues
    activate CW
    CW-->>Agent: Return Log Summary
    deactivate CW

    Agent->>LLM: Process Log Summary
    activate LLM
    LLM-->>Agent: Return Analysis
    deactivate LLM

    Agent->>Agent: Step 6: Return Summary of<br/>Race Updates across platform

    Agent->>Output: Step 7: Formatted Agent Response<br/>with timeline view of Race Updates/Issues
    deactivate Agent

    Output-->>UI: Display Results
    activate UI
    UI-->>User: Show Timeline View & Issues
    deactivate UI