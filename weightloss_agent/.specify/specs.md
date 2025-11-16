# Weight Loss Chat Agent - Application Specifications

**Project:** Weight Loss Chat Agent (Telegram)  
**Version:** 1.0  
**Created:** November 16, 2025  
**Status:** ACTIVE (Non-negotiable)  
**Framework:** Speckit Constitution-Driven Development

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Project Vision & Success Metrics](#project-vision--success-metrics)
3. [Core User Stories](#core-user-stories)
4. [Nudge Agent Specifications](#nudge-agent-specifications)
5. [Batch Processing Requirements](#batch-processing-requirements)
6. [Technical Architecture](#technical-architecture)
7. [MVP Scope & Constraints](#mvp-scope--constraints)
8. [Edge Cases & Failure Scenarios](#edge-cases--failure-scenarios)
9. [Acceptance Criteria](#acceptance-criteria)
10. [Testing Strategy](#testing-strategy)
11. [Implementation Roadmap](#implementation-roadmap)

---

## Executive Summary

### Project Overview
Build a **privacy-first weight loss coaching agent** accessible via Telegram that helps users track 6 health metrics (calories, protein, water, sleep, steps, workouts) with personalized nudges and weekly synthesis.

### Key Differentiators
- **Batch Processing**: Collect all items, confirm, then process together
- **4-Agent Architecture**: Root orchestrator + 3 specialized sub-agents + autonomous Nudge agent
- **Emotional Intelligence**: Detect mental health risks, provide support
- **Privacy-First**: Device-local storage, no cloud sync in MVP
- **Recommendation-Only**: Agent never executes autonomously

### Technology Foundation
- **Platform**: Telegram ONLY (free, open API)
- **AI Framework**: Google ADK (Agent Development Kit)
- **LLM**: Gemini 2.5 Flash
- **Orchestration**: LangGraph
- **Database**: SQLite (device-local)
- **Python**: 3.12+ (required)

---

## Project Vision & Success Metrics

### Vision Statement
Build a lightweight, privacy-first weight loss coaching agent accessible via Telegram that helps users track 6 health metrics (calories, protein, water, sleep, steps, workouts) with personalized nudges and weekly synthesis.

### Success Definition
- **70%+ daily active logging rate** in first 30 days
- **50%+ 30-day retention**
- **<1% message delivery failures**
- **Zero false crisis escalations**
- **NPS >40** by end of Q1

### Core Principles (Non-Negotiable)
1. **User-Centric Design** - All features prioritize user experience and mental health
2. **Data Minimization** - Only collect essential data, store locally (MVP), no cloud sync
3. **Transparency** - Clear confidence levels, no false claims, always disclose limitations
4. **Recommendation-Only** - Agent never executes actions autonomously, only suggests
5. **Emotional Intelligence** - Detect mental health risks, escalate appropriately, never shame
6. **Cost Effectiveness** - MVP uses free APIs only, no paid services

---

## Core User Stories

### **USER STORY 1: User Onboarding & Profile Setup**

```
As a new user,
I want to set up my profile with my weight, height, age, and weight loss goal,
so that the agent can personalize my recommendations and track my progress accurately.

Acceptance Criteria:
- [ ] User can complete onboarding in <2 minutes
- [ ] Profile fields: age, height, weight, target weight, activity level, goal deficit
- [ ] User sees confirmation of saved profile
- [ ] Bot calculates daily calorie goal from profile data
- [ ] User can edit profile anytime via /profile command
- [ ] System validates inputs (age 18-100, height/weight reasonable ranges)

Priority: MUST HAVE
Story Points: 5
```

### **USER STORY 2: Log Single Meal (Simple)**

```
As a user,
I want to log a meal I just ate by describing it in natural language,
so that I can quickly record my food intake without complex menus.

Acceptance Criteria:
- [ ] User can type "Had 2 eggs and toast"
- [ ] Bot asks "Is that all for this meal?"
- [ ] Bot collects all meal items before processing
- [ ] Bot queries USDA database for nutrition
- [ ] Bot displays: total calories, protein, confidence level
- [ ] Bot shows remaining calorie budget for the day
- [ ] Meal is stored in session memory with timestamp

Priority: MUST HAVE
Story Points: 5
```

### **USER STORY 3: Log Complete Breakfast (Multi-Item Batch)**

```
As a busy user,
I want to log a multi-item breakfast (eggs, toast, juice, coffee),
so that I can capture the full meal without re-entering each item separately.

Acceptance Criteria:
- [ ] User enters first item "2 eggs"
- [ ] Bot asks "Anything else for breakfast?"
- [ ] User adds "toast" → Bot still asks
- [ ] User adds "OJ" → Bot asks again
- [ ] User says "that's all"
- [ ] Bot processes ALL 4 items as single breakfast batch
- [ ] Bot returns: Total 420 cal, 16g protein for breakfast
- [ ] Each item shows individual contribution
- [ ] Confidence score shown per item

Priority: MUST HAVE
Story Points: 8
```

### **USER STORY 4: Log Workout Session (Multi-Exercise Batch)**

```
As a gym user,
I want to log a complete workout session with multiple exercises,
so that the agent can track my volume and suggest progression.

Acceptance Criteria:
- [ ] User enters "10 pull-ups"
- [ ] Bot asks "Any more sets of pull-ups or different exercise?"
- [ ] User adds "3 sets of 8 squats at 185 lbs"
- [ ] User adds "20 push-ups"
- [ ] User says "that's all"
- [ ] Bot calculates total volume:
  - Pull-ups: 10 reps (1 set)
  - Squats: 24 reps total (3 sets × 8)
  - Push-ups: 20 reps (1 set)
- [ ] Bot suggests progression (e.g., "Next week, try 185 lbs × 10 on squats")
- [ ] Includes form tips for compound lifts
- [ ] Workout stored with timestamp and body part focus

Priority: MUST HAVE
Story Points: 8
```

### **USER STORY 5: Log Water Intake**

```
As a user,
I want to log my water intake throughout the day,
so that I can ensure I'm hydrated and meeting my daily goal.

Acceptance Criteria:
- [ ] User can log in multiple units: "2 glasses", "500 ml", "1 liter"
- [ ] Bot converts to ounces for standard measurement
- [ ] Bot shows progress toward daily goal (8-10 glasses)
- [ ] User can log multiple times: morning water, afternoon water, evening water
- [ ] Daily hydration summary shows: logged today, remaining goal
- [ ] Bot suggests hydration nudges if behind schedule

Priority: MUST HAVE
Story Points: 3
```

### **USER STORY 6: Log Sleep**

```
As a user,
I want to log my sleep duration and quality,
so that I can correlate sleep with weight loss and workout performance.

Acceptance Criteria:
- [ ] User enters sleep in hours: "7 hours", "7.5 hours", "7 hours 30 min"
- [ ] User enters sleep quality as 1-10 scale: "quality 8/10"
- [ ] Bot validates: 4-12 hours reasonable range
- [ ] Bot validates: quality 1-10 scale
- [ ] Sleep logged with date (previous night's sleep)
- [ ] Weekly sleep quality trend shown
- [ ] Sleep correlated with workout performance (tired → suggest light workout)
- [ ] Sleep correlated with weight gain (poor sleep linked to plateau)

Priority: MUST HAVE
Story Points: 4
```

### **USER STORY 7: Log Daily Steps**

```
As a user,
I want to log my daily step count,
so that I can track my non-exercise activity and reach my step goal.

Acceptance Criteria:
- [ ] User enters daily steps: "12,500 steps"
- [ ] Bot accepts formats: "12500", "12,500", "12k"
- [ ] Bot shows progress toward goal (default 10,000)
- [ ] Bot shows weekly step trend (trending up/down)
- [ ] User can manually override auto-count if different from wearable

Priority: SHOULD HAVE
Story Points: 3
```

### **USER STORY 8: View Today's Progress**

```
As a user,
I want to see a summary of my progress today across all 6 metrics,
so that I can understand my current status and make decisions for remaining day.

Acceptance Criteria:
- [ ] Command: /stats or "Show today's progress"
- [ ] Summary includes:
  - Calories: logged vs goal, remaining budget
  - Protein: logged vs goal, % of target
  - Water: logged vs goal, glasses remaining
  - Sleep: (from last night) hours and quality
  - Steps: logged today vs goal
  - Workouts: completed sessions, volume
- [ ] Color/emoji indicators: ✅ on track, ⚠️ behind, 🔥 ahead
- [ ] Suggestions based on gaps (e.g., "300 cal remaining, try protein snack")

Priority: MUST HAVE
Story Points: 5
```

### **USER STORY 9: View Weekly Report**

```
As a user,
I want to see a comprehensive weekly summary every Sunday,
so that I can assess my progress and plan for the coming week.

Acceptance Criteria:
- [ ] Automatic report sent Sunday 18:00
- [ ] Report includes:
  - Avg daily calorie deficit
  - Protein consistency (% days meeting target)
  - Water intake trend (↗️↘️→)
  - Sleep quality average
  - Total steps logged
  - Workout frequency
  - Logging streak (consecutive days logged ≥1 metric)
  - Hero stat: 1 thing user crushed this week
- [ ] Trend arrows: ↗️ improved, ↘️ declined, → stable
- [ ] User can request early report: /report command

Priority: SHOULD HAVE
Story Points: 8
```

### **USER STORY 10: Viewing Logging Streak**

```
As a user,
I want to see my logging streak (consecutive days I've logged something),
so that I can stay motivated and see my consistency.

Acceptance Criteria:
- [ ] User can check /streak command
- [ ] Shows: Current streak, longest streak, days since break
- [ ] Definition: Logged at least 1 metric per day (any of 6 areas)
- [ ] Breaks streak if: 0 logs for entire calendar day
- [ ] Streak protects: Nudge at 23:55 if at risk
- [ ] Can resume streak if: Log within 24 hours after break

Priority: SHOULD HAVE
Story Points: 3
```

---

## Nudge Agent Specifications

### **USER STORY 11: Morning Motivational Nudge**

```
As a user,
I want to receive a morning nudge with encouragement,
so that I start my day motivated and reminded to track my progress.

Acceptance Criteria:
- [ ] Nudge arrives at 07:00 (user's preferred time)
- [ ] Personalized based on previous day's performance
- [ ] If yesterday logged: "Great consistency! 5-day streak. Let's extend it 💪"
- [ ] If yesterday skipped: "New day, fresh start! You got this 🚀"
- [ ] Can customize nudge time via /settings
- [ ] User can snooze nudge (15 min, 1 hour, ask later)
- [ ] User can disable morning nudges

Priority: SHOULD HAVE
Story Points: 5
```

### **USER STORY 12: Midday Activity Check**

```
As a user,
I want to receive a midday nudge checking my activity,
so that I can log meals and stay on track.

Acceptance Criteria:
- [ ] Nudge arrives at 12:00 (lunch time)
- [ ] Check: Any meals logged yet today?
- [ ] If YES: "On track! Keep it going 🔥"
- [ ] If NO: "Time for lunch? Ready to log? 🍽️"
- [ ] Shows: Calorie budget remaining so far
- [ ] Can dismiss or snooze

Priority: SHOULD HAVE
Story Points: 4
```

### **USER STORY 13: Evening Nudge with Focus Goal**

```
As a user,
I want to receive an evening nudge highlighting one goal to focus on tomorrow,
so that I don't feel overwhelmed and can prioritize my efforts.

Acceptance Criteria:
- [ ] Nudge arrives at 19:00 (evening)
- [ ] Algorithm selects ONE goal with lowest adherence last 7 days
- [ ] Rotates daily: protein, steps, water, workouts, sleep, calories
- [ ] If all goals equal: Show strongest area
- [ ] Goal changes daily, not mid-day

Priority: SHOULD HAVE
Story Points: 6
```

### **USER STORY 14: Streak Protection Nudge (23:55)**

```
As a user,
I want to receive a gentle nudge at 23:55 if I haven't logged anything today,
so that I can quickly log before midnight to keep my streak alive.

Acceptance Criteria:
- [ ] Triggers at 23:55 only if: 0 logs for entire day
- [ ] Message: "5 min left to keep your 7-day streak alive! Quick log? ⏰"
- [ ] Tone: Gentle, not pushy or shaming
- [ ] One nudge only (not 23:56, 23:57, 23:58)

Priority: SHOULD HAVE
Story Points: 3
```

### **USER STORY 15: Weekly Synthesis Report (Sunday 18:00)**

```
As a user,
I want to receive a comprehensive weekly report every Sunday,
so that I can celebrate wins and plan for the next week.

Acceptance Criteria:
- [ ] Sent automatically Sunday 18:00
- [ ] Includes: calorie deficit avg, protein consistency, water trend, sleep quality, total steps, workout frequency, logging streak, hero stat
- [ ] Personalized section: "You crushed [metric] this week! 🏆"
- [ ] Celebratory tone with emojis

Priority: SHOULD HAVE
Story Points: 8
```

---

## Batch Processing Requirements

### **USER STORY 16: Complete Meal Batch Confirmation**

```
As a user,
I want to confirm when my meal batch is complete,
so that the agent can process all items together accurately.

Acceptance Criteria:
- [ ] User logs "2 eggs"
- [ ] Bot asks "Is that all for this meal?"
- [ ] User can respond: "yes", "that's all", "done", "no more"
- [ ] User can respond: "no" or "more" to add more items
- [ ] User can respond: "cancel" to discard batch
- [ ] Once confirmed, bot shows: All items collected, total calories, total protein, confidence per item, daily budget remaining

Priority: MUST HAVE
Story Points: 4
```

### **USER STORY 17: Workout Session Batch Processing**

```
As a user,
I want to log multiple exercises in one session,
so that the agent can calculate total volume and suggest progression.

Acceptance Criteria:
- [ ] User logs "3 sets of 8 pull-ups"
- [ ] Bot asks "Any more sets of pull-ups or different exercise?"
- [ ] User adds "20 push-ups"
- [ ] Bot processes batch as complete workout
- [ ] Bot calculates: Total pull-ups: 24 reps, total push-ups: 20 reps, volume per muscle group, total session duration estimate, suggests progression

Priority: MUST HAVE
Story Points: 6
```

### **USER STORY 18: Hydration Batch (Multiple Water Logs)**

```
As a user,
I want to log multiple water intake sessions throughout the day,
so that the agent can aggregate total daily hydration.

Acceptance Criteria:
- [ ] Morning: "Drank 2 glasses" → logged
- [ ] Midday: "500ml water" → logged and summed
- [ ] After gym: "1 liter" → logged and summed
- [ ] Evening: "2 more glasses" → logged and summed
- [ ] Bot shows daily total: 8 glasses + 500ml + 1L = 12.5 glasses

Priority: SHOULD HAVE
Story Points: 3
```

---

## Technical Architecture

### 4-Agent System Architecture

```
USER (Telegram)
    ↓
┌─────────────────────────────────────────────────────────┐
│      ROOT AGENT (Orchestrator)                          │
│  - Intent Classification                                │
│  - Emotional Context Detection                          │
│  - Response Synthesis                                   │
│  - Session State Management                             │
│  - Delegates to sub-agents                              │
└─────────────────────────────────────────────────────────┘
    ↓ (on user input)     ↓ (on user input)     ↓ (on user input)     ↓ (scheduled)
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ NUTRITION AGENT  │  │ FITNESS AGENT    │  │ WELLNESS AGENT   │  │ NUDGE AGENT ⭐   │
│ (BATCH MODE)     │  │ (BATCH MODE)     │  │ (BATCH MODE)     │  │ (AUTONOMOUS)     │
│                  │  │                  │  │                  │  │                  │
│ Collects meals:  │  │ Collects workouts:│ │ Collects entries:│  │ Scheduled tasks: │
│ "Is that all?"   │  │ "Any more sets?" │  │ "More water?"    │  │ 1. Daily nudges  │
│ "Anything else?" │  │ "Another exercise?"│ │ "Done sleeping?" │  │ 2. Weekly report │
│                  │  │                  │  │                  │  │ 3. Streak protect│
│ BATCH PROCESS:   │  │ BATCH PROCESS:   │  │ BATCH PROCESS:   │  │ 4. Goal focus    │
│ - Parse all meal │  │ - Aggregate all  │  │ - Sum all water  │  │                  │
│   items together │  │   sets/reps      │  │ - Avg sleep      │  │ RUNS INDEPENDENT-│
│ - Query USDA DB  │  │ - Check form tips│  │ - Total steps    │  │ LY FROM USER     │
│ - Calculate total│  │ - Progression    │  │ - Correlate data │  │ INPUT (ROOT only │
│   cal, protein   │  │   overload       │  │ - Log session    │  │ delivers msgs)   │
│ - Return summary │  │ - Return summary │  │ - Return summary │  │                  │
└──────────────────┘  └──────────────────┘  └──────────────────┘  └──────────────────┘
```

### Key Technical Requirements

#### Agent Design Requirements
- **Multi-Agent Pattern**: Root agent (orchestrator) + 4 specialized sub-agents
- **Delegation Method**: LLM-driven (agent decides which sub-agent, not if-then logic)
- **Autonomy Level**: RECOMMENDATION-ONLY (no action execution)
- **Session State**: Persistent per user, accessible to all agents

#### Batch Processing Requirements
- **NOT Real-time**: Collect all items, ask confirmation, process together
- **Batch Size Limit**: 10 items per meal/workout/session max
- **Timeout**: 30 minutes of inactivity = auto-complete batch
- **All-or-Nothing**: If any item fails, entire batch fails (atomicity)
- **User Confirmation**: Always ask "Is that all?" before processing

#### Tool Development Requirements
- **Tool Definition**: Every tool = Python async function with docstring + type hints
- **Error Handling**: All tools must catch exceptions, never crash agent
- **Timeout**: Every tool has max 5 sec timeout (except USDA API = 5 sec with Nutritionix fallback)
- **Return Format**: Consistent dict with "status", "data", "error" fields
- **Idempotency**: Tools must be safe to call multiple times with same input

#### Nudge Agent Requirements
- **Autonomous Scheduling**: Runs on APScheduler (asyncio-based)
- **Message Delivery**: All nudges delivered by ROOT AGENT for consistency
- **Timezone Support**: User-aware timezones (not UTC-only)
- **Personalization**: Based on user performance and preferences
- **Snooze Support**: 15 min, 1 hour, or ask later options

### Data Architecture

#### Session Management
- **Local Storage**: ADK LocalSessionService (not cloud-based)
- **Persistence**: SQLite database for long-term storage
- **State Management**: All user data stored locally (MVP)
- **Backup**: No cloud sync in MVP

#### Data Minimization
- **Essential Data Only**: age, height, weight, activity level, meal entries, workouts, water, sleep, steps
- **No Medical Data**: Never ask for/store diagnoses, medications, health conditions
- **Retention**: Delete logs >90 days old automatically
- **Right to Deletion**: /delete_my_data command wipes all user data immediately

### API Integration Requirements

#### Free APIs (MVP Only)
- **USDA Food Data Central**: Primary nutrition database (free with API key)
- **Nutritionix API**: Backup nutrition lookup (free, no auth required)
- **Google Gemini**: LLM for agent reasoning (free tier available)
- **Telegram Bot API**: Messaging platform (free, open)

#### API Fallback Strategy
1. **Primary**: USDA FoodData Central (5 sec timeout)
2. **Secondary**: Nutritionix API (3 sec timeout)
3. **Tertiary**: Local food database (instant)
4. **Fallback**: Ask user for manual calorie entry

---

## MVP Scope & Constraints

### ✅ What's Included in MVP

| Feature | Status | Implementation |
|---------|--------|-----------------|
| **Meal Logging** | ✅ | Manual text entry + USDA FDC API (free) |
| **Calorie Calculation** | ✅ | USDA FoodData Central API |
| **Protein Tracking** | ✅ | Included in USDA API data |
| **Workout Logging** | ✅ | Manual reps/weight text entry |
| **Progressive Overload** | ✅ | Simple rules (add 2-5 lbs when 3×8 feels easy) |
| **Water Tracking** | ✅ | Manual entry (cups/liters/oz) |
| **Sleep Logging** | ✅ | Manual hours + quality (1-10) |
| **Steps Tracking** | ✅ | Manual daily count entry |
| **Emotional Awareness** | ✅ | Sentiment analysis (Gemini NLU) |
| **Nudge Agent** | ✅ | Scheduled (APScheduler) + autonomous |
| **Weekly Report** | ✅ | Data aggregation + synthesis |
| **Telegram Bot** | ✅ | python-telegram-bot library |
| **Batch Processing** | ✅ | Confirmation before aggregating |
| **Session Management** | ✅ | ADK LocalSessionService (local DB) |

### ❌ What's NOT in MVP (Future)

| Feature | Timeline | Why Later |
|---------|----------|-----------|
| HealthKit Sync | Q2 | Complex iOS integration |
| Google Fit Sync | Q2 | Android API setup |
| Image Recognition (photos) | Q2 | Requires vision model |
| Advanced NLP | Q2 | Need production data for fine-tuning |
| Cloud Sync | Q2 | GDPR complexity, MVP privacy-first |
| Multi-language | Q3 | Focus on English first |
| Premium Tier | Q4 | Need retention data first |

---

## Edge Cases & Failure Scenarios

### Critical Edge Cases

#### **EDGE CASE 1: USDA API Timeout**
- **Scenario**: User logs "2 eggs", USDA API takes >10 seconds
- **Behavior**: Agent catches timeout after 5 seconds, switches to Nutritionix, if both fail, asks user for manual entry
- **Recovery**: User can always provide manual calorie entry

#### **EDGE CASE 2: Batch Collection Timeout**
- **Scenario**: User starts batch, doesn't respond for 20 minutes
- **Behavior**: If user returns within 30 min: Resume batch; After 30 min: Start fresh batch
- **Recovery**: Clear message about batch expiration, offer to re-add old items

#### **EDGE CASE 3: Negative/Impossible Values**
- **Scenarios**: "-500 calories", "50,000 calories", "-2 liters water", "1000 pull-ups"
- **Behavior**: Guardrail catches immediately, asks for clarification, non-judgmental message
- **Recovery**: Suggest reasonable values, user clarifies

#### **EDGE CASE 4: Emotional Crisis During Logging**
- **Scenario**: User says "Ugh I'm so fat 😞" while logging meal
- **Behavior**: Sentiment detected (-0.8), meal still logged, response includes empathy
- **Recovery**: "I hear you're struggling. Here's what I logged... Want to chat with support?"

#### **EDGE CASE 5: Multi-Timezone User**
- **Scenario**: User travels across timezones mid-day
- **Behavior**: Use user's local timezone consistently, re-calculate all previous logs
- **Recovery**: Clear message: "Detected timezone change. Updated all your data."

#### **EDGE CASE 6: Session Crash & Recovery**
- **Scenario**: User collecting meal batch (3 items), server crashes
- **Behavior**: Session persisted to database, user reconnects, batch recovered
- **Recovery**: "Welcome back! You were collecting a meal. Items so far: [list]"

### Critical Bugs & Agent Failures

#### **BUG 1: Infinite Retry Loop**
- **Root Cause**: Tool throws error, agent retries forever
- **Solution**: Max retries: 3, exponential backoff (1s, 2s, 4s), escalate to user after 3 failures

#### **BUG 2: Data Duplication**
- **Root Cause**: Network delay causes meal logged twice
- **Solution**: Unique batch ID, idempotent processing, deduplication check

#### **BUG 3: Sentiment False Positive**
- **Root Cause**: User joking "I could eat 1000 pizzas!" flagged as binge alert
- **Solution**: Multi-factor analysis, check for hyperbole indicators, require multiple crisis keywords

#### **BUG 4: Batch Processing Fails Mid-Batch**
- **Root Cause**: One item fails lookup, entire batch unclear
- **Solution**: All-or-nothing atomicity, clear error message, option to retry or log individually

#### **BUG 5: Nudge Agent Sends Duplicate Messages**
- **Root Cause**: Scheduler runs multiple times
- **Solution**: Idempotency key, check if already sent, replace_existing=True

---

## Acceptance Criteria

### Feature Acceptance Checklist

Every feature must pass:
- [ ] **Unit Tests**: 80%+ coverage for agents, 70%+ for tools
- [ ] **Integration Tests**: Multi-agent interactions, end-to-end flows
- [ ] **Golden Test Sets**: Documented user stories in `evals/`
- [ ] **Guardrails Not Violated**: Input validation, confidence thresholding, hallucination prevention
- [ ] **Type Checking**: pyright passes (100% type hints)
- [ ] **Linting**: ruff passes (strict mode)
- [ ] **Documentation**: Updated API reference, code comments
- [ ] **No New TODOs**: All implementation complete
- [ ] **Constitution Compliance**: Verified against `.specify/memory/constitution.md`

### Quality Gates

#### Code Quality Standards
- **Type Safety**: 100% type hints on all function signatures
- **Code Style**: Black formatter (88-char line length), ruff linter
- **Function Size**: Max 50 lines (excluding docstring)
- **Error Handling**: Specific exceptions, always log, user-friendly messages
- **Documentation**: Google-style docstrings required

#### Testing Standards
- **Unit Test Coverage**: 80% for agents, 70% for tools
- **Integration Tests**: Multi-agent flows, golden test sets
- **Evaluation Framework**: ADK built-in evaluation with metrics
- **Performance**: Response latency P95 <3 seconds
- **Accuracy**: Task success rate >90% for logging

#### Security & Privacy
- **GDPR Compliance**: Data minimization, consent flows, right to deletion
- **Data Minimization**: Only essential health metrics collected
- **Local Storage**: All data stored in SQLite locally (MVP)
- **No Cloud Sync**: Zero data transmission to cloud in MVP
- **No Third-Party Tracking**: No analytics or monitoring

---

## Testing Strategy

### Test Suite Categories

#### **TEST SUITE 1: Happy Path (Everything Works)**
- Complete morning to evening logging journey
- All APIs responding, all data valid
- Expected: All data logged, streak maintained, user satisfied

#### **TEST SUITE 2: Error Recovery**
- API fails, user recovers via fallback/manual entry
- Expected: Graceful fallback, meal still logged

#### **TEST SUITE 3: Edge Cases**
- Negative values, impossible values, validation triggers
- Expected: Validation caught, user clarified, recovered

#### **TEST SUITE 4: Batch Timeout**
- User starts batch, goes AFK for 20 min, returns
- Expected: Batch recovered despite timeout

#### **TEST SUITE 5: Emotional Crisis Detection**
- User expressing guilt/shame during logging
- Expected: Meal logged, emotional support provided

### Evaluation Metrics (ADK Framework)
- **Task Success Rate (LSR)**: >90% for logging tasks
- **Hallucination Rate**: <5% (no unsourced nutrition claims)
- **Emotional Accuracy**: >80% (correctly identify crisis signals)
- **Response Latency P95**: <3 seconds
- **Confidence Thresholding**: Correctly qualified <75% confidence

---

## Implementation Roadmap

### Phase 1: Core Infrastructure (Week 1-2)
- [ ] Telegram Bot setup and BotFather configuration
- [ ] Google ADK environment setup and API keys
- [ ] SQLite database schema and session management
- [ ] Root Agent creation with basic intent classification
- [ ] Basic message handling and response routing

### Phase 2: Nutrition Agent & Batch Processing (Week 3-4)
- [ ] Nutrition Agent implementation with USDA API integration
- [ ] Batch collection workflow ("Is that all?" confirmation)
- [ ] Meal parsing and calorie calculation
- [ ] Nutritionix API fallback implementation
- [ ] Manual calorie entry fallback

### Phase 3: Fitness & Wellness Agents (Week 5-6)
- [ ] Fitness Agent with workout batch processing
- [ ] Progressive overload suggestions
- [ ] Wellness Agent (water, sleep, steps)
- [ ] Multi-unit support (glasses, ml, liters for water)
- [ ] Sleep quality correlation with performance

### Phase 4: Nudge Agent & Scheduling (Week 7-8)
- [ ] Nudge Agent autonomous scheduling with APScheduler
- [ ] Daily nudges (morning, midday, evening, streak protection)
- [ ] Weekly synthesis report
- [ ] Focus goal selection algorithm
- [ ] Timezone-aware scheduling

### Phase 5: Integration & Testing (Week 9-10)
- [ ] Multi-agent orchestration and delegation
- [ ] Session state persistence and recovery
- [ ] Comprehensive test suite (unit + integration)
- [ ] Golden test set validation
- [ ] Performance optimization and latency testing

### Phase 6: Production Deployment (Week 11-12)
- [ ] Docker containerization
- [ ] Cloud Run deployment configuration
- [ ] Monitoring and logging setup
- [ ] User acceptance testing
- [ ] Production launch and monitoring

---

## Constitution Compliance Verification

All specifications must align with the project constitution:

### ✅ Constitution Alignment Checklist
- [x] **User-Centric Design**: All features prioritize UX and mental health
- [x] **Data Minimization**: Only essential data collected, local storage
- [x] **Transparency**: Clear confidence levels, disclose limitations
- [x] **Recommendation-Only**: Agent never executes autonomously
- [x] **Emotional Intelligence**: Crisis detection, appropriate escalation
- [x] **Cost Effectiveness**: Free APIs only (USDA, Nutritionix, Telegram)
- [x] **Technology Stack**: Python 3.12+, Google ADK, Gemini 2.5 Flash, LangGraph, SQLite
- [x] **4-Agent Architecture**: Root + Nutrition + Fitness + Wellness + Nudge
- [x] **Batch Processing**: All-or-nothing atomicity, 10-item limits, 30-min timeout
- [x] **Guardrails**: Input validation, confidence thresholding, hallucination prevention
- [x] **Code Quality**: 100% type hints, 80%+ test coverage, Google docstrings
- [x] **Privacy-First**: GDPR compliance, device-local storage, no cloud sync

---

## Technical Implementation Details

### API Integration Specifications

#### 1. USDA FoodData Central API

**Base URL:** https://api.nal.usda.gov/fdc/v1/

**Main Endpoints:**
1. GET /foods/search - Search for foods by keywords
2. GET /food/{fdcId} - Get detailed nutrition for one food
3. GET /foods - Get details for multiple foods by FDC IDs
4. GET /foods/list - Get paginated list of foods

**Food Search Endpoint:**
```
METHOD: GET or POST
URL: https://api.nal.usda.gov/fdc/v1/foods/search
REQUIRED PARAMETERS: api_key (string)
OPTIONAL PARAMETERS: query, pageSize (default: 25, max: 200), pageNumber, sortBy, sortOrder
AUTHENTICATION: API key in query parameter
RESPONSE FORMAT: JSON with foods array containing fdcId, description, foodNutrients
```

**Key Nutrient IDs to Extract:**
- 203 = Protein (grams)
- 204 = Total Fat (grams)
- 205 = Carbohydrate (grams)
- 208 = Energy/Calories (kcal)

**Rate Limits:** 1,200 requests/hour, exponential backoff on failures

#### 2. Nutritionix API (Fallback)

**Base URL:** https://www.nutritionix.com/api/v2/

**Main Endpoints:**
1. POST /search/instant - Quick search (no auth required)
2. GET /search/item - Detailed search by UPC
3. POST /natural/nutrients - Parse natural language

**Instant Search Endpoint:**
```
METHOD: POST
URL: https://www.nutritionix.com/api/v2/search/instant
PARAMETERS: {"query": "eggs", "detailed": false, "limit": 10}
RESPONSE: common[] and branded[] arrays with nutrition data
```

**Fallback Logic:** Try USDA first (5s timeout), then Nutritionix (3s timeout), then local DB, finally ask user

#### 3. Google Gemini API Configuration

**Model:** Gemini 2.5 Flash
**Configuration:**
```python
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 1024
}
safety_settings = [BLOCK_MEDIUM_AND_ABOVE for harassment, hate_speech, etc.]
```

**Rate Limits:** 60 requests/minute, 1500/day (free tier)
**Cost Tracking:** $0.075/1M input tokens, $0.30/1M output tokens

### Database Schema Definition

#### SQLite Table Structures

```sql
-- Users table
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    telegram_user_id INTEGER UNIQUE NOT NULL,
    first_name TEXT, last_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP,
    consent_gdpr BOOLEAN DEFAULT 0,
    consent_data_processing BOOLEAN DEFAULT 0,
    deleted_at TIMESTAMP
);

-- Profiles table
CREATE TABLE profiles (
    profile_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL UNIQUE,
    age INTEGER CHECK(age >= 18 AND age <= 120),
    height_cm DECIMAL(5, 2),
    current_weight_kg DECIMAL(5, 2),
    target_weight_kg DECIMAL(5, 2),
    activity_level TEXT DEFAULT 'moderate',
    daily_calorie_goal INTEGER DEFAULT 1500,
    daily_protein_goal_g INTEGER DEFAULT 120,
    daily_water_goal_oz INTEGER DEFAULT 64,
    daily_steps_goal INTEGER DEFAULT 10000,
    timezone TEXT DEFAULT 'UTC',
    preferences_json TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Daily logs tables (nutrition, fitness, wellness)
CREATE TABLE daily_logs_nutrition (
    log_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    meal_type TEXT NOT NULL,
    food_items TEXT NOT NULL,
    total_calories INTEGER, total_protein_g DECIMAL(5, 1),
    confidence DECIMAL(3, 2),
    created_at TIMESTAMP NOT NULL,
    log_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Sessions, nudges, streaks, api_usage tables
-- (Complete schema in technical_clarifications.md)
```

**Data Types & Constraints:**
- user_id: TEXT PRIMARY KEY
- calories: INTEGER >=0
- age: 18-120
- weight_kg: 30-300
- confidence: 0.0-1.0

### Tool Function Specifications

#### Function Signature Template

```python
from typing import Dict, List, Optional, Any
from google.adk.tools import ToolContext

async def tool_name(
    param1: str,
    param2: int,
    tool_context: Optional[ToolContext] = None
) -> Dict[str, Any]:
    """
    One-line summary.
    
    Detailed description with Args, Returns, Raises sections.
    """
    
    # Input validation
    if not param1 or len(param1) < 3:
        raise ValueError("param1 too short")
    
    # Main logic with timeout
    try:
        result = await asyncio.wait_for(
            _do_work(param1, param2),
            timeout=5
        )
        return {
            "status": "success",
            "data": result,
            "confidence": 0.95
        }
    except asyncio.TimeoutError:
        return {"status": "error", "error": "timeout"}
    except Exception as e:
        return {"status": "error", "error": str(e)}
```

#### Key Tool Functions

- **parse_meal_batch()**: Parse complete meal, lookup nutrition, return totals
- **detect_sentiment()**: Analyze emotional state, return sentiment score and alert level
- **calculate_daily_progress()**: Aggregate all metrics, return progress summary
- **select_focus_goal()**: Choose one goal for evening nudge based on adherence

### Nudge Agent Scheduling Configuration

#### APScheduler Setup

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()
scheduler.add_job(
    execute_morning_nudge,
    CronTrigger(hour=7, minute=0, timezone='UTC'),
    id='nudge_morning'
)
# Similar for midday (12:00), evening (19:00), weekly (Sun 18:00), streak (23:55)
```

#### Cron Expressions
- Morning: `CronTrigger(hour=7, minute=0)`
- Midday: `CronTrigger(hour=12, minute=0)`
- Evening: `CronTrigger(hour=19, minute=0)`
- Weekly: `CronTrigger(day_of_week=6, hour=18, minute=0)`
- Streak: `CronTrigger(hour=23, minute=55)`

#### Focus Goal Algorithm
Select lowest-adherence goal from past 7 days, rotate if same as yesterday.

### Guardrail Implementation Details

#### Validation Thresholds

```python
class GuardrailThresholds:
    AGE_MIN = 18
    AGE_MAX = 100
    WEIGHT_MIN_KG = 30
    WEIGHT_MAX_KG = 300
    CALORIE_MAX_PER_MEAL = 2000
    CALORIE_MIN_PER_MEAL = 50
    WATER_MAX_DAILY_OZ = 300
    SLEEP_MIN_HOURS = 4
    SLEEP_MAX_HOURS = 12
    CONFIDENCE_LOW_THRESHOLD = 0.75
    CONFIDENCE_HIGH_THRESHOLD = 0.85
```

#### Confidence Calculation

```python
def calculate_food_confidence(source, exact_match, quantity_specified):
    confidence = {"usda": 0.95, "nutritionix": 0.80, "local": 0.60}[source]
    if not exact_match: confidence *= 0.90
    if not quantity_specified: confidence *= 0.85
    return confidence
```

### Session State Structure

#### Complete Session Data Model

```python
class SessionState:
    def __init__(self, user_id, profile_data):
        self.user_id = user_id
        self.user_profile = {
            "age": profile_data.get("age"),
            "height_cm": profile_data.get("height_cm"),
            "weight_kg": profile_data.get("weight_kg"),
            "daily_calorie_goal": profile_data.get("daily_calorie_goal", 1500),
            # ... other profile fields
        }
        self.current_batch = {
            "active": False,
            "type": None,  # "meal", "workout", "hydration"
            "items": [],
            "started_at": None
        }
        self.today_logs = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "nutrition": {"meals": [], "total_calories": 0},
            "fitness": {"workouts": [], "total_volume": 0},
            "wellness": {"water_oz": 0, "sleep_hours": 0, "steps": 0}
        }
        self.streak_data = {
            "current_streak": 0,
            "longest_streak": 0,
            "last_log_date": None
        }
        # ... nudge preferences, metadata
```

#### Persistence Strategy
- Auto-save every 60 seconds
- Load on session start
- Expire after 24 hours of inactivity

### Error Handling & User Messages

#### Standard Error Codes

```python
class ErrorCode:
    API_TIMEOUT = "api_timeout"
    API_RATE_LIMIT = "api_rate_limit"
    VALIDATION_INVALID_INPUT = "validation_invalid_input"
    BATCH_EMPTY = "batch_empty"
    DATABASE_ERROR = "database_error"
    TIMEOUT_ERROR = "timeout_error"
```

#### User-Friendly Messages

```python
MESSAGES = {
    "api_timeout": "System is a bit slow. Please try again in a moment.",
    "validation_invalid_input": "I didn't understand that. Could you rephrase?",
    "batch_empty": "Oops! No items in batch. Start over?",
    "database_error": "System error. Your data is safe. Try again?"
}
```

### Testing Data & Golden Sets

#### Test User Profiles

```python
TEST_USERS = {
    "user_normal": {
        "age": 30, "height_cm": 175, "weight_kg": 85,
        "daily_calorie_goal": 1800, "daily_protein_goal_g": 150
    },
    "user_petite": {
        "age": 25, "height_cm": 155, "weight_kg": 55,
        "daily_calorie_goal": 1500, "daily_protein_goal_g": 100
    }
}
```

#### Golden Test Cases

```python
GOLDEN_TEST_CASES = [
    {
        "id": "test_simple_meal",
        "user_input": "Had 2 eggs and toast",
        "expected_steps": [
            {"step": "1: Parse input", "expected": "Intent recognized"},
            {"step": "2: Ask confirmation", "expected": "Bot asks 'Anything else?'"},
            {"step": "3: User confirms", "input": "That's all", "expected": "Bot processes batch"},
            {"step": "4: Lookup nutrition", "expected": "USDA returns nutrition data"},
            {"step": "5: Calculate totals", "expected": "260 cal, 14g protein"},
            {"step": "6: Return to user", "expected": "Logged ✅ 260 cal, 14g protein"}
        ]
    }
]
```

### Telegram Bot Setup

#### Step 1: Create Bot via BotFather

```
1. Open Telegram
2. Search for @BotFather
3. Send /newbot
4. Follow prompts:
   - Bot name: "Weight Loss Coach"
   - Bot username: "weight_loss_coach_bot" (must be unique)
5. Receive: BOT_TOKEN (keep secret!)

Example: "123456789:ABCdefGHIjklMNOpqrsTUVwxyzABCDEFGhi"
```

#### Step 2: Get Your User ID

```
1. Search for @userinfobot
2. Send /start
3. Get your user_id (e.g., 987654321)
```

### Project Setup & Environment

#### Prerequisites

```bash
# Python 3.12+
python --version

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Create Virtual Environment

```bash
# Create project
mkdir weight_loss_agent_telegram && cd weight_loss_agent_telegram

# Create venv
uv venv --python 3.12
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

#### Install Dependencies

```bash
# Core libraries
uv pip install google-adk python-telegram-bot google-generativeai

# Additional tools
uv pip install python-dotenv requests pydantic apscheduler sqlalchemy

# Free API access
uv pip install requests  # For USDA Food Database API

# Testing & deployment
uv pip install pytest pytest-asyncio fastapi uvicorn

# Generate requirements
uv pip freeze > requirements.txt
```

### Agent Implementation Examples

#### Root Agent (Orchestrator)

```python
from google.adk.agents import Agent, LlmAgent
from google.adk.tools import FunctionTool

# Define tools for root agent
intent_tool = FunctionTool(func=classify_intent)
sentiment_tool = FunctionTool(func=detect_sentiment)
response_tool = FunctionTool(func=format_response)
batch_state_tool = FunctionTool(func=get_batch_state)

root_agent = LlmAgent(
    name="weight_loss_coach_root",
    model=Config.LLM_MODEL,
    description="Main orchestrator for weight loss tracking via Telegram. Routes user requests to specialized agents (Nutrition, Fitness, Wellness). Manages batch collection workflows.",
    instruction="""
    You are a supportive, non-judgmental weight loss coach assistant on Telegram.
    
    YOUR RESPONSIBILITIES:
    1. Understand user intent (logging meals, asking questions, viewing progress)
    2. Detect emotional state and respond with empathy
    3. For multi-item logging: Use BATCH MODE
       - MEALS: "Logged [item]. Is that all for this meal? Any sides?"
       - WORKOUTS: "Logged [exercise]. Any more sets? Different exercise?"
       - HYDRATION: "Logged [amount]. More water logged today? Anything else?"
    4. After user confirms "that's all": Delegate batch to appropriate agent
    5. Route requests:
       - Food logs → nutrition_agent (BATCH)
       - Workouts → fitness_agent (BATCH)
       - Water/Sleep/Steps → wellness_agent (BATCH)
    6. Synthesize multi-agent responses into single supportive message
    
    TONE: Supportive coach, warm, encouraging. Use 1-2 emojis max per message.
    
    BATCH MODE RULES:
    - After each item, ALWAYS ask "Is that all?" or "Anything else?"
    - Never process partially - wait for complete batch
    - Once user confirms complete, delegate full batch to agent
    """,
    tools=[intent_tool, sentiment_tool, response_tool, batch_state_tool],
)
```

#### Nutrition Agent (Batch Mode)

```python
nutrition_agent = LlmAgent(
    name="nutrition_agent_batch",
    model=Config.LLM_MODEL,
    description="Processes complete meal batches (not individual items). Receives list of food items from Root Agent, calculates total calories and macros using USDA database.",
    instruction="""
    You are a nutrition specialist receiving COMPLETE MEAL BATCHES.
    
    YOUR TASK:
    - Receive: List of all foods user logged for one meal (e.g., ["2 eggs", "1 toast", "1 glass OJ"])
    - Lookup: Each food in USDA FoodData Central database
    - Calculate: Total calories, protein, carbs, fat for this meal
    - Include: Confidence levels for each food estimate
    - Return: Summarized meal data
    
    NEVER process individual items - you receive COMPLETE meals only.
    
    CONSTRAINTS:
    - If food not found in USDA DB: Use Nutritionix API as backup
    - If still not found: Use best guess with uncertainty note
    - Always show confidence scores (e.g., "~260 cal, high confidence")
    - Flag if total seems high (>1000 cal single meal) or low (<200 cal)
    
    RETURN FORMAT:
    {
        "status": "success",
        "meal_type": "breakfast",
        "foods": [
            {"name": "eggs", "quantity": "2 large", "calories": 140, "protein": 12},
            {"name": "toast", "quantity": "1 slice", "calories": 120, "protein": 4}
        ],
        "totals": {"calories": 260, "protein": 16, "carbs": 25, "fat": 8},
        "confidence": 0.92,
        "notes": "High confidence estimates from USDA database"
    }
    """,
    tools=[batch_parser_tool, batch_calculator_tool, usda_tool],
)
```

#### Nudge Agent (Autonomous)

```python
nudge_agent = LlmAgent(
    name="nudge_agent_autonomous",
    model=Config.LLM_MODEL,
    description="Autonomous agent that generates personalized nudges on schedule. Runs independently via APScheduler, but ROOT AGENT delivers all messages to maintain consistency.",
    instruction="""
    You are an autonomous nudge generator for engagement and adherence.
    
    YOUR ROLE: Generate (NOT send) personalized nudges based on user data.
    
    IMPORTANT: You do NOT send messages directly to users.
    Your outputs are formatted for ROOT AGENT to send via Telegram.
    
    NUDGE TYPES:
    
    1. DAILY MORNING NUDGE (07:00)
       - Check: Did user log anything yesterday?
       - Personalize: Reference their streak or yesterday's achievement
       - Tone: Motivational
       - Example: "Great streak! 5 days strong 🔥 Ready for today?"
    
    2. MIDDAY NUDGE (12:00)
       - Check: Any meals logged today?
       - Personalize: Next meal coming up (lunch time)
       - Tone: Casual, helpful
       - Example: "Lunch time! Ready to log? 🍽️"
    
    3. EVENING NUDGE (19:00)
       - Check: Which of the 6 goals are missing?
       - Personalize: Suggest the ONE goal to focus on tomorrow
       - Tone: Non-judgmental, supportive
       - Example: "Noticed you skipped workouts today. No worries! 💪 Let's make tomorrow leg day?"
    
    4. WEEKLY REPORT (Sunday 18:00)
       - Generate: Summary of week's data
       - Highlight: Best day, best metric, consistency score
       - Personalize: Call out their "hero stat"
       - Tone: Celebratory
       - Example: "Your week: 5/7 days logged! 🏆 You crushed protein targets. Keep it up!"
    
    5. STREAK PROTECTION (23:55)
       - Check: Did user log any metric today?
       - Personalize: Which streak is at risk?
       - Tone: Gentle urgency, not pushy
       - Example: "5 min left to keep your 7-day streak! Quick log? ⏰"
    
    6. FOCUS GOAL (06:00)
       - Algorithm:
         1. Identify goal with lowest adherence (past 7 days)
         2. Select ONE goal only (prevent overwhelm)
         3. Next day: Different goal (rotate)
       - Tone: Motivational, specific
       - Example: "This week's focus: 💧 HYDRATION. Let's hit 10 glasses today!"
    
    OUTPUT FORMAT:
    {
        "nudge_type": "morning" | "midday" | "evening" | "weekly" | "streak" | "focus",
        "scheduled_time": "07:00",
        "message": "User-friendly message (under 140 chars for Telegram)",
        "emoji": "Single emoji if appropriate",
        "personalization_used": ["yesterday_streak", "best_metric"],
        "next_action": "Log meal?" | "Complete workout?" | "Fill data?"
    }
    
    GUARDRAILS:
    - NO judgment or shame language
    - NO comparison to other users
    - NO medical advice
    - NO pressure if user has missed days
    - DO normalize struggle, celebrate consistency
    """,
    tools=[nudge_daily, nudge_weekly, nudge_streak, nudge_goal],
)
```

### Batch Processing Workflow Examples

#### Meal Logging: Complete Flow

```
User: "Had eggs for breakfast"

ROOT AGENT:
- Detect intent: log_meal
- Start batch collection
- Ask for complete batch: "Logged eggs! Any sides? (toast, butter, etc.)"

User: "Toast too"

ROOT AGENT:
- Add to batch: ["eggs", "toast"]
- Ask: "Milk with that? Anything else?"

User: "That's all for breakfast"

ROOT AGENT:
- Batch complete: ["eggs", "toast"]
- DELEGATE TO NUTRITION_AGENT (BATCH MODE)

NUTRITION_AGENT:
- Receives: ["eggs", "toast"]
- Queries USDA FoodData Central:
  - "eggs": 70 cal, 6g protein (per large egg)
  - "toast": 120 cal, 4g protein
- Calculates: 260 cal, 14g protein total
- Returns to ROOT_AGENT

ROOT AGENT:
- Synthesizes: "Breakfast logged! ✅
  Eggs + Toast = 260 cal, 14g protein
  You've got 1200 cal left today. Great start! 💪"
- Stores in session memory
```

### Tool Development: Complete USDA Integration

#### Batch Food Parser Tool

```python
from typing import Dict, List
import aiohttp
from config import Config

async def parse_meal_batch(
    food_items: List[str],
    meal_type: str,
    user_id: str,
    tool_context=None
) -> Dict:
    """
    Parse complete meal batch and look up nutrition in USDA database.
    
    Args:
        food_items (List[str]): List of foods user logged (e.g., ["2 eggs", "1 toast"])
        meal_type (str): "breakfast" | "lunch" | "dinner" | "snack"
        user_id (str): User ID
        tool_context (optional): ADK context
    
    Returns:
        dict: Complete meal nutrition data
    """
    
    # GUARDRAIL 1: Input validation
    if not food_items or len(food_items) == 0:
        return {"status": "error", "message": "No food items in batch"}
    
    if len(food_items) > 10:
        return {"status": "error", "message": "Too many items in batch (max 10 per meal)"}
    
    parsed_foods = []
    total_calories = 0
    total_protein = 0.0
    confidence_scores = []
    
    for food_item in food_items:
        try:
            food_data = await _parse_food_item(food_item)
            
            if food_data["status"] == "success":
                parsed_foods.append({
                    "name": food_data["name"],
                    "quantity": food_data["quantity"],
                    "calories": food_data["calories"],
                    "protein": food_data["protein"],
                    "confidence": food_data["confidence"]
                })
                
                total_calories += food_data["calories"]
                total_protein += food_data["protein"]
                confidence_scores.append(food_data["confidence"])
            
            else:
                parsed_foods.append({
                    "name": food_item,
                    "quantity": "unknown",
                    "calories": 0,
                    "protein": 0,
                    "confidence": 0,
                    "warning": "Could not find nutritional data"
                })
        
        except Exception as e:
            print(f"❌ Error parsing {food_item}: {e}")
    
    avg_confidence = (sum(confidence_scores) / len(confidence_scores)) if confidence_scores else 0.5
    
    warning_notes = []
    if total_calories > 1500:
        warning_notes.append(f"High calorie meal ({total_calories} cal) - verify accuracy")
    if total_calories < 100:
        warning_notes.append(f"Low calorie meal ({total_calories} cal) - might be missing items")
    
    return {
        "status": "success",
        "meal_type": meal_type,
        "foods": parsed_foods,
        "totals": {
            "calories": total_calories,
            "protein": round(total_protein, 1),
            "confidence": round(avg_confidence, 2)
        },
        "notes": "; ".join(warning_notes) if warning_notes else "Normal meal"
    }

async def _parse_food_item(food_item: str) -> Dict:
    """Parse single food item using USDA FoodData Central API"""
    
    parts = food_item.lower().strip().split(maxsplit=1)
    
    if len(parts) == 2:
        try:
            quantity = int(parts[0])
            food_name = parts[1]
        except ValueError:
            quantity = 1
            food_name = food_item.lower().strip()
    else:
        quantity = 1
        food_name = food_item.lower().strip()
    
    # Query USDA Food Database (free API with key)
    usda_result = await _query_usda_fdc(food_name)
    
    if usda_result["found"]:
        return {
            "status": "success",
            "name": food_name,
            "quantity": f"{quantity} serving" if quantity == 1 else f"{quantity} servings",
            "calories": usda_result["calories"] * quantity,
            "protein": usda_result["protein"] * quantity,
            "confidence": usda_result["confidence"]
        }
    
    # Fallback: Use local database
    local_db_result = await _query_local_food_db(food_name)
    
    if local_db_result:
        return {
            "status": "success",
            "name": food_name,
            "quantity": f"{quantity} serving",
            "calories": local_db_result["calories"] * quantity,
            "protein": local_db_result["protein"] * quantity,
            "confidence": 0.6
        }
    
    return {
        "status": "error",
        "message": f"Could not find nutritional data for '{food_name}'",
        "suggestion": f"Try 'egg' instead of '{food_name}' or provide more detail"
    }

async def _query_usda_fdc(food_name: str) -> Dict:
    """Query USDA Food Data Central API"""
    
    api_key = Config.USDA_FDC_API_KEY
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    
    params = {
        "api_key": api_key,
        "query": food_name,
        "pageSize": 5
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if data.get("foods"):
                        food = data["foods"][0]
                        nutrients = food.get("foodNutrients", [])
                        
                        calories = 0
                        protein = 0
                        
                        for nutrient in nutrients:
                            if nutrient.get("nutrientName") == "Energy":
                                calories = int(nutrient.get("value", 0))
                            elif nutrient.get("nutrientName") == "Protein":
                                protein = float(nutrient.get("value", 0))
                        
                        return {
                            "found": True,
                            "name": food.get("description", food_name),
                            "calories": calories,
                            "protein": protein,
                            "confidence": 0.95
                        }
        
        return {"found": False}
    
    except Exception as e:
        print(f"❌ USDA API error: {e}")
        return {"found": False}

async def _query_local_food_db(food_name: str) -> Dict:
    """Fallback local food database"""
    
    local_db = {
        "eggs": {"calories": 70, "protein": 6},
        "toast": {"calories": 120, "protein": 4},
        "chicken": {"calories": 165, "protein": 31},
        "rice": {"calories": 130, "protein": 2.7},
        "broccoli": {"calories": 55, "protein": 3.7},
        "oatmeal": {"calories": 150, "protein": 5},
        "banana": {"calories": 105, "protein": 1.3},
        "apple": {"calories": 95, "protein": 0.5},
    }
    
    for key, value in local_db.items():
        if key in food_name.lower():
            return value
    
    return None
```

### Telegram Bot Integration

#### Main Bot Handler

```python
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
import asyncio
from config import Config
from agents.root.agent import get_root_agent_with_sub_agents
from scheduler.nudge_scheduler import NudgeScheduler
from tools.batch_state_manager import batch_collector
from google.adk.runners import InMemoryRunner
from google.adk.sessions import LocalSessionService

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class WeightLossBot:
    def __init__(self):
        self.application = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()
        self.root_agent = get_root_agent_with_sub_agents()
        self.runner = InMemoryRunner()
        self.session_service = LocalSessionService()
        self.nudge_scheduler = NudgeScheduler(self.application.bot)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_id = update.effective_user.id
        first_name = update.effective_user.first_name
        
        welcome_message = f"""
👋 Welcome {first_name}! I'm your Weight Loss Coach.

I help you track:
🍽️  Meals & calories
💪 Workouts & strength
💧 Water intake
😴 Sleep quality
👟 Daily steps

Let's get started! What would you like to log today?

/help - Show all commands
/profile - Set up your profile
/log - Start logging
/stats - View your progress
/report - Weekly report
/streak - Check your logging streak
/settings - Adjust notification times
"""
        await update.message.reply_text(welcome_message)
        
        logger.info(f"✅ User {user_id} started bot")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular messages"""
        user_id = update.effective_user.id
        user_message = update.message.text
        
        logger.info(f"📨 Message from {user_id}: {user_message}")
        
        try:
            await update.message.chat.send_action("typing")
            
            session_id = f"telegram_{user_id}"
            
            response = await self.runner.run(
                agent=self.root_agent,
                user_id=str(user_id),
                session_id=session_id,
                content=user_message
            )
            
            if len(response) <= 4096:
                await update.message.reply_text(response)
            else:
                for i in range(0, len(response), 4096):
                    await update.message.reply_text(response[i:i+4096])
            
            logger.info(f"✅ Response sent to {user_id}")
        
        except Exception as e:
            logger.error(f"❌ Error processing message: {e}")
            await update.message.reply_text(
                "Oops! Something went wrong. Please try again.\n\n"
                "If the problem persists, contact support."
            )
    
    def register_handlers(self):
        """Register all event handlers"""
        
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )
        
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
        
        self.application.add_error_handler(self.error_handler)
    
    async def run(self):
        """Start the bot"""
        logger.info("🤖 Weight Loss Bot starting...")
        
        self.register_handlers()
        
        await self.nudge_scheduler.start()
        
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling(
            allowed_updates=Update.ALL_TYPES
        )
        
        logger.info("✅ Bot is running! Press Ctrl+C to stop.")
        
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            await self.nudge_scheduler.stop()
            await self.application.updater.stop()
            await self.application.stop()


async def main():
    """Main entry point"""
    bot = WeightLossBot()
    await bot.run()


if __name__ == "__main__":
    asyncio.run(main())
```

### Deployment & Monitoring

#### Docker Containerization

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8080

CMD ["python", "-m", "uvicorn", "telegram_bot.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

#### Cloud Run Deployment

```bash
#!/bin/bash

PROJECT_ID="weight-loss-agent-prod"
REGION="us-central1"
SERVICE_NAME="weight-loss-agent-telegram"
IMAGE_NAME="weight-loss-agent:latest"

# Build Docker image
echo "🔨 Building Docker image..."
docker build -t $IMAGE_NAME .

# Tag for Google Container Registry
docker tag $IMAGE_NAME gcr.io/$PROJECT_ID/$IMAGE_NAME

# Push to GCR
echo "📤 Pushing to Google Container Registry..."
docker push gcr.io/$PROJECT_ID/$IMAGE_NAME

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$IMAGE_NAME \
  --platform managed \
  --region $REGION \
  --memory 2Gi \
  --timeout 3600 \
  --set-env-vars "GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=$REGION" \
  --env-vars-file .env

echo "✅ Deployed successfully!"
gcloud run services describe $SERVICE_NAME --region $REGION --format='value(status.url)'
```

### Testing Strategy & Golden Sets

#### Golden Test Cases

```python
GOLDEN_TEST_CASES = [
    {
        "id": "batch_meal_001",
        "name": "Complete breakfast batch",
        "user_flow": [
            {"user_input": "Had 2 eggs for breakfast", "expected_agent_response_contains": "Is that all?"},
            {"user_input": "Toast too", "expected_agent_response_contains": "Anything else?"},
            {"user_input": "That's all", "expected_agent_behavior": "process_batch"}
        ],
        "batch_data": {"items": ["2 eggs", "toast"], "meal_type": "breakfast"},
        "expected_nutrition_output": {
            "total_calories": 260,
            "total_protein": 14,
            "confidence": "> 0.85"
        },
        "final_agent_response": "Breakfast logged! ✅ 2 eggs + toast = ~260 cal, 14g protein. You're on track today!"
    },
    {
        "id": "batch_meal_002",
        "name": "Ambiguous batch requiring clarification",
        "user_flow": [
            {"user_input": "Had some eggs", "expected_agent_response": "How many eggs?"},
            {"user_input": "2", "expected_agent_response": "Scrambled or fried?"},
            {"user_input": "Scrambled", "expected_agent_response": "Anything else?"}
        ],
        "evaluation_criteria": {
            "asks_clarifying_questions": true,
            "doesn_process_until_complete": true,
            "confidence_properly_qualified": true
        }
    }
]
```

### MVP Constraints & Free APIs

#### What's Included in MVP

| Feature | Status | Implementation |
|---------|--------|-----------------|
| **Meal Logging** | ✅ | Manual text entry + USDA FDC API (free) |
| **Calorie Calculation** | ✅ | USDA FoodData Central API |
| **Protein Tracking** | ✅ | Included in USDA API data |
| **Workout Logging** | ✅ | Manual reps/weight text entry |
| **Progressive Overload** | ✅ | Simple rules (add 2-5 lbs when 3×8 feels easy) |
| **Water Tracking** | ✅ | Manual entry (cups/liters/oz) |
| **Sleep Logging** | ✅ | Manual hours + quality (1-10) |
| **Steps Tracking** | ✅ | Manual daily count entry |
| **Emotional Awareness** | ✅ | Sentiment analysis (Gemini NLU) |
| **Nudge Agent** | ✅ | Scheduled (APScheduler) + autonomous |
| **Weekly Report** | ✅ | Data aggregation + synthesis |
| **Telegram Bot** | ✅ | python-telegram-bot library |
| **Batch Processing** | ✅ | Confirmation before aggregating |
| **Session Management** | ✅ | ADK LocalSessionService (local DB) |

#### What's NOT in MVP

| Feature | Timeline | Why Later |
|---------|----------|-----------|
| HealthKit Sync | Q2 | Complex iOS integration |
| Google Fit Sync | Q2 | Android API setup |
| Image Recognition (photos) | Q2 | Requires vision model |
| Advanced NLP | Q2 | Need production data for fine-tuning |
| Cloud Sync | Q2 | GDPR complexity, MVP privacy-first |
| Multi-language | Q3 | Focus on English first |
| Premium Tier | Q4 | Need retention data first |

#### Free APIs for MVP

**USDA Food Data Central API**
- Free with API key
- No rate limits for registered users
- Comprehensive nutrition database

**Nutritionix API**
- Free instant search (no auth required)
- Backup for USDA failures
- Good coverage for common foods

**Google Gemini**
- Free tier available
- 60 requests/minute, 1500/day
- Cost-effective for MVP

**Telegram Bot API**
- Completely free
- No usage limits
- Open source library available

---

## Constitution Compliance Verification

All technical specifications align with the project constitution:

### ✅ Constitution Alignment Checklist
- [x] **User-Centric Design**: All features prioritize UX and mental health
- [x] **Data Minimization**: Only essential data collected, local storage
- [x] **Transparency**: Clear confidence levels, disclose limitations
- [x] **Recommendation-Only**: Agent never executes autonomously
- [x] **Emotional Intelligence**: Crisis detection, appropriate escalation
- [x] **Cost Effectiveness**: Free APIs only (USDA, Nutritionix, Telegram)
- [x] **Technology Stack**: Python 3.12+, Google ADK, Gemini 2.5 Flash, LangGraph, SQLite
- [x] **4-Agent Architecture**: Root + Nutrition + Fitness + Wellness + Nudge
- [x] **Batch Processing**: All-or-nothing atomicity, 10-item limits, 30-min timeout
- [x] **Guardrails**: Input validation, confidence thresholding, hallucination prevention
- [x] **Code Quality**: 100% type hints, 80%+ test coverage, Google docstrings
- [x] **Privacy-First**: GDPR compliance, device-local storage, no cloud sync

---

**Technical Specifications Status:** ✅ COMPLETE  
**Ready for Implementation:** Yes  
**Next Step:** `/speckit.plan` - Create detailed implementation plan