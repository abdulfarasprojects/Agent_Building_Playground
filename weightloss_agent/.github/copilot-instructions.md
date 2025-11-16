# Weight Loss Chat Agent - Copilot Instructions

## Project Overview
You are helping build a **Weight Loss Chat Agent** - a Telegram-based AI coaching system that helps users track 6 health metrics (calories, protein, water, sleep, steps, workouts) with personalized nudges and weekly synthesis.

## Core Principles (NON-NEGOTIABLE)
- **User-Centric Design**: All features prioritize user experience and mental health
- **Data Minimization**: Only essential data, stored locally (MVP), no cloud sync
- **Transparency**: Clear confidence levels, no false claims, disclose limitations
- **Recommendation-Only**: Agent never executes autonomously, only suggests
- **Emotional Intelligence**: Detect mental health risks, escalate appropriately, never shame
- **Cost Effectiveness**: MVP uses free APIs only, no paid services

## Technology Stack (MANDATORY)
- **Platform**: Telegram ONLY
- **AI Framework**: Google ADK (Agent Development Kit)
- **LLM**: Gemini 2.5 Flash
- **Orchestration**: LangGraph (not LangChain)
- **Database**: SQLite (device-local only)
- **Python**: 3.12+ (required)
- **Scheduler**: APScheduler (asyncio-based)

## Architecture (REQUIRED)
- **Multi-Agent Pattern**: Root agent + 4 specialized sub-agents (Nutrition, Fitness, Wellness, Nudge)
- **Batch Processing**: Collect all items, ask confirmation, process together
- **Delegation**: LLM-driven (not if-then logic)
- **Session State**: Persistent per user, accessible to all agents

## Code Quality Standards
- **Type Hints**: 100% coverage on all function signatures
- **Testing**: 80%+ coverage for agents, 70%+ for tools
- **Style**: Black formatter, ruff linter, Google-style docstrings
- **Error Handling**: Specific exceptions, always log, user-friendly messages
- **Function Size**: Max 50 lines (excluding docstring)

## Development Workflow
1. **Constitution First**: Reference `.specify/memory/constitution.md` for all decisions
2. **Specification**: Use `/speckit.specify` to define features with user stories
3. **Planning**: Use `/speckit.plan` to create technical design
4. **Tasks**: Use `/speckit.tasks` to generate actionable tasks
5. **Implementation**: Use `/speckit.implement` to generate code from tasks

## Guardrails (MANDATORY)
1. **Input Validation**: Reject impossible values (negative calories, >500 reps)
2. **Confidence Thresholding**: Show ranges for <0.75 confidence
3. **Hallucination Prevention**: RAG with USDA DB (no unsourced claims)
4. **Task Looping Prevention**: Max 3 retries, exponential backoff
5. **Emotional Safety**: Multi-factor crisis detection, human escalation
6. **Rate Limiting**: Max 20 logs/day per user (eating disorder prevention)

## File Organization
```
weightloss_agent/
├── agents/
│   ├── root/
│   ├── nutrition/
│   ├── fitness/
│   ├── wellness/
│   └── nudge/
├── tools/
│   ├── intent_classifier.py
│   ├── sentiment_detector.py
│   ├── batch_state_manager.py
│   ├── nutrition/
│   ├── fitness/
│   └── wellness/
├── scheduler/
├── telegram_bot/
├── guardrails/
├── evals/
├── tests/
├── config.py
└── main.py
```

## Implementation Guidelines

### Agent Development
- **Clear Descriptions**: Every agent needs specific, guardrailed descriptions
- **Single Responsibility**: Each agent handles one domain only
- **Tool Integration**: All tools must be async functions with proper error handling
- **Session Awareness**: All agents access shared session state

### Tool Development
- **Async Functions**: All tools must be async, even without I/O
- **Timeout Handling**: Max 5 sec timeout on all external calls
- **Consistent Returns**: `{"status": "success|error", "data": ..., "error_message": ...}`
- **Idempotency**: Tools safe to call multiple times with same input

### Error Handling
- **Never Crash**: All exceptions must be caught and handled gracefully
- **User Messages**: Always provide non-technical error messages
- **Logging**: Log errors before returning user-friendly messages
- **Fallbacks**: Implement fallback chains (e.g., USDA → Nutritionix)

### Testing Requirements
- **Unit Tests**: 80%+ coverage for agents, 70%+ for tools
- **Integration Tests**: Multi-agent interactions, end-to-end flows
- **Golden Test Sets**: Documented user stories in `evals/`
- **CI/CD**: All tests must pass before merge

## Success Metrics
- **70%+ daily active logging** in first 30 days
- **50%+ 30-day retention**
- **<1% message delivery failures**
- **Zero false crisis escalations**
- **NPS >40** by end of Q1

## Privacy & Security
- **GDPR Compliant**: Data minimization, explicit consent, right to deletion
- **Device-Local**: All data stored in SQLite locally (MVP)
- **No Cloud Sync**: Zero data transmission to cloud in MVP
- **No Tracking**: No third-party analytics or monitoring

## Development Commands
- `/speckit.specify` - Define features with user stories
- `/speckit.plan` - Create technical design
- `/speckit.tasks` - Generate actionable tasks
- `/speckit.implement` - Generate code from tasks

## Quality Gates
Every PR must pass:
- [ ] Constitution compliance verified
- [ ] 80%+ test coverage (agents/tools)
- [ ] Type hints: pyright passes
- [ ] Linting: ruff passes (strict mode)
- [ ] Documentation updated
- [ ] No new warnings/TODOs
- [ ] Guardrails reviewed (if safety logic changes)
- [ ] User stories updated (if spec changes)

**Remember**: Constitution supersedes all other guidance. When in doubt, reference `.specify/memory/constitution.md`.