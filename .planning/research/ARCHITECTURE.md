# Architecture Patterns

**Domain:** AI-powered text analysis system
**Researched:** 2026-03-14
**Overall confidence:** HIGH

## Recommended Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         React Frontend                        │
│  ┌──────────┐  ┌───────────┐  ┌──────────────────┐   │
│  │  Header  │  │HeroSection │  │  ResultsSection  │   │
│  └──────────┘  └───────────┘  └──────────────────┘   │
│       │              │                    │               │
│       └──────────────┴────────────────────┘               │
│                       ▼                                  │
│                  API Service Layer                         │
│              (fetch, error handling)                       │
└────────────────────────────┬───────────────────────────────────┘
                         │
                    HTTP/REST (JSON)
                         │
┌────────────────────────────┴───────────────────────────────────┐
│                       Flask Backend                          │
│  ┌────────────────────────────────────────────────────┐   │
│  │            API Gateway Layer                      │   │
│  │  (CORS, rate limiting, request validation)      │   │
│  └────────────────────────────────────────────────────┘   │
│                         │                                  │
│      ┌──────────────────┴──────────────────┐             │
│      │                                        │             │
│      ▼                                        ▼             │
│  ┌───────────┐                        ┌──────────┐     │
│  │  Routes   │                        │  Models  │     │
│  │ (Blueprint)│                        │ (SQLAlchemy)│    │
│  └───────────┘                        └──────────┘     │
│      │                                        │             │
│      ▼                                        │             │
│  ┌────────────────────────────────────────────┐   │
│  │     AI Integration Layer                 │   │
│  │  (OpenAI client, prompt engineering)     │   │
│  └────────────────────────────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
                     ┌────────────────┐
                     │   OpenAI API   │
                     └────────────────┘
```

### Component Boundaries

| Component | Responsibility | Communicates With |
|-----------|---------------|------------------|
| **React Components** | UI rendering, user interaction, state management | API Service Layer |
| **API Service Layer** | HTTP requests, response parsing, error handling | Flask Backend (REST API) |
| **Flask API Gateway** | CORS, rate limiting, request validation, error handling | Routes, Models |
| **Routes (Blueprints)** | Endpoint definitions, business logic | AI Integration Layer, Models |
| **Models** | Data persistence, database operations | Routes |
| **AI Integration Layer** | OpenAI API calls, prompt engineering, response parsing | OpenAI API |
| **OpenAI API** | LLM inference, fallacy detection | AI Integration Layer |

### Data Flow

**Analysis Request Flow:**

```
1. User enters text in HeroSection
   ↓ (React state update)
2. API Service Layer initiates POST /api/analyze
   ↓ (HTTP/JSON)
3. Flask API Gateway validates request
   - CORS check
   - Rate limit check
   - Request validation (text not empty)
   ↓
4. Routes handler receives request
   ↓
5. AI Integration Layer calls OpenAI API
   - Constructs prompt
   - Calls client.chat.completions.create()
   - Parses JSON response
   ↓
6. Routes returns JSON response to frontend
   ↓ (HTTP/JSON)
7. API Service Layer receives response
   - Parses JSON
   - Handles errors
   ↓
8. React updates state
   - setAnalysisResults(result)
   - setShowResults(true)
9. ResultsSection re-renders with new data
```

## Patterns to Follow

### Pattern 1: REST API Design with Flask Blueprints

**What:** Organize Flask routes into modular blueprints following REST conventions

**When:** Building backend APIs with Flask

**Why:**
- **Modularity**: Separate concerns (user routes vs fallacy analysis routes)
- **Scalability**: Easy to add new features without monolithic routes
- **Maintainability**: Clear separation of logic
- **Best Practice**: Follow Flask documentation patterns

**Example:**

```python
# src/routes/fallacy.py
from flask import Blueprint, request, jsonify

fallacy_bp = Blueprint('fallacy', __name__)

@fallacy_bp.route('/analyze', methods=['POST'])
def analyze_text():
    """POST /api/analyze - Analyze text for fallacies"""
    data = request.get_json()
    # Validation
    if not data or 'text' not in data:
        return jsonify({'error': 'Text is required'}), 400

    text = data['text'].strip()
    if not text:
        return jsonify({'error': 'Text cannot be empty'}), 400

    # Business logic
    result = analyze_fallacies(text)
    return jsonify(result)

@fallacy_bp.route('/fallacy-types', methods=['GET'])
def get_fallacy_types():
    """GET /api/fallacy-types - Get reference fallacy types"""
    types = load_fallacy_types()
    return jsonify({"fallacy_types": types})
```

**Register in main.py:**

```python
from src.routes.fallacy import fallacy_bp

app.register_blueprint(fallacy_bp, url_prefix='/api')
```

**Confidence:** HIGH - Direct from Flask documentation

---

### Pattern 2: React State Management with useState + useEffect

**What:** Use React hooks for component state and side effects

**When:** Managing UI state and API calls in React

**Why:**
- **Standard React Pattern**: useState for state, useEffect for side effects
- **Avoids Prop Drilling**: Keep state local where possible
- **Cleanup Handling**: useEffect cleanup prevents memory leaks
- **Performance**: React handles re-renders efficiently

**Example:**

```jsx
// components/ResultsSection.jsx
import { useState, useEffect } from 'react'
import { analyzeText } from '../services/api'

function ResultsSection({ isVisible }) {
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Effect for API calls
  useEffect(() => {
    if (!isVisible || !text) return

    const fetchResults = async () => {
      setLoading(true)
      setError(null)
      try {
        const data = await analyzeText(text)
        setResults(data)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchResults()

    // Cleanup function (optional, for cancellation)
    return () => {
      // Cancel pending requests if needed
    }
  }, [isVisible, text])

  if (loading) return <LoadingSpinner />
  if (error) return <ErrorMessage message={error} />
  if (!results) return null

  return <ResultsDisplay data={results} />
}
```

**Confidence:** HIGH - Direct from React documentation

---

### Pattern 3: Error Boundary Pattern (Frontend)

**What:** Catch JavaScript errors in component trees and display fallback UI

**When:** Preventing app crashes from component errors

**Why:**
- **Graceful Degradation**: One component error doesn't break entire app
- **Better UX**: Users see error message instead of white screen
- **Debugging**: Captures error details for logging

**Example:**

```jsx
// components/ErrorBoundary.jsx
import { Component } from 'react'

class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, errorInfo) {
    // Log error to service (Sentry, etc.)
    console.error('ErrorBoundary caught:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-fallback">
          <h2>Bir şeyler yanlış gitti</h2>
          <p>Lütfen sayfayı yenileyin.</p>
        </div>
      )
    }

    return this.props.children
  }
}

export default ErrorBoundary

// Wrap components in App.jsx
<ErrorBoundary>
  <ResultsSection results={results} />
</ErrorBoundary>
```

**Confidence:** HIGH - React best practice

---

### Pattern 4: Flask Error Handlers with Custom Exceptions

**What:** Centralized error handling with custom exception classes

**When:** Building robust APIs with consistent error responses

**Why:**
- **Consistency**: All errors follow same JSON structure
- **Maintainability**: Error logic in one place, not scattered
- **Debugging**: Easy to add logging (Sentry) to all errors
- **Best Practice**: Direct from Flask documentation

**Example:**

```python
# src/exceptions.py
class APIError(Exception):
    """Base class for API errors"""
    status_code = 400
    message = "Bad request"

    def __init__(self, message=None, status_code=None, payload=None):
        super().__init__()
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class ValidationError(APIError):
    """Request validation failed"""
    status_code = 400

class AIServiceError(APIError):
    """OpenAI API error"""
    status_code = 502

# app.py error handlers
@app.errorhandler(APIError)
def handle_api_error(e):
    return jsonify(e.to_dict()), e.status_code

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(Exception)
def handle_exception(e):
    # Log unexpected errors
    sentry_sdk.capture_exception(e)
    return jsonify({'error': 'Internal server error'}), 500
```

**Usage in routes:**

```python
@fallacy_bp.route('/analyze', methods=['POST'])
def analyze_text():
    try:
        text = validate_text(request)
    except ValidationError as e:
        raise e  # Caught by error handler

    try:
        result = call_openai_api(text)
    except openai.APIError as e:
        raise AIServiceError("AI service unavailable")
```

**Confidence:** HIGH - Direct from Flask documentation

---

### Pattern 5: Request Validation with Decorators

**What:** Decorators to validate and sanitize request data

**When:** Reusable validation across multiple endpoints

**Why:**
- **DRY Principle**: Don't repeat validation logic
- **Cleaner Code**: Handlers focus on business logic
- **Consistency**: Same validation everywhere
- **Security**: Input sanitization in one place

**Example:**

```python
# src/decorators.py
from functools import wraps
from flask import request, jsonify
from src.exceptions import ValidationError

def validate_json(*required_fields):
    """Decorator to validate JSON request body"""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            data = request.get_json()
            if not data:
                raise ValidationError("JSON body required")

            for field in required_fields:
                if field not in data:
                    raise ValidationError(f"'{field}' field required")

                if not data[field] or not str(data[field]).strip():
                    raise ValidationError(f"'{field}' cannot be empty")

            return f(*args, **kwargs)
        return wrapped
    return decorator

def validate_text_length(max_length=5000):
    """Decorator to validate text length"""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            data = request.get_json()
            text = data.get('text', '')
            if len(text) > max_length:
                raise ValidationError(f"Text exceeds {max_length} characters")
            return f(*args, **kwargs)
        return wrapped
    return decorator

# Usage in routes
@fallacy_bp.route('/analyze', methods=['POST'])
@validate_json('text')
@validate_text_length(5000)
def analyze_text():
    data = request.get_json()
    text = data['text']
    # Handler logic (validation already done)
    result = analyze_fallacies(text)
    return jsonify(result)
```

**Confidence:** MEDIUM - Pattern from Flask documentation, applied to this use case

---

### Pattern 6: Caching Strategy for AI Responses

**What:** Cache OpenAI API responses to reduce latency and costs

**When:** Users may analyze similar text repeatedly

**Why:**
- **Performance**: 100ms cache hit vs 2-5s API call
- **Cost Reduction**: Fewer OpenAI API calls = lower bill
- **User Experience**: Faster feedback
- **Rate Limiting**: Reduces API quota usage

**Implementation Options:**

**Option A: In-Memory Cache (Simple, dev-only)**

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def cached_analyze_text(text: str) -> dict:
    """Cache up to 100 unique text analyses"""
    # Call OpenAI API
    result = call_openai_api(text)
    return result

# In route
def analyze_text():
    text = request.json['text']
    result = cached_analyze_text(text)
    return jsonify(result)
```

**Option B: Flask-Caching (Redis-backed, production)**

```python
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0',
    'CACHE_DEFAULT_TIMEOUT': 3600  # 1 hour
})

@cache.memoize(timeout=3600)
def analyze_fallacies(text: str) -> dict:
    """Cache results for 1 hour"""
    return call_openai_api(text)

# In route
@fallacy_bp.route('/analyze', methods=['POST'])
def analyze_text():
    text = request.json['text']
    result = analyze_fallacies(text)
    return jsonify(result)

# Invalidate cache when needed
# cache.delete_memoized(analyze_fallacies)
```

**Cache Key Strategy:**

```python
import hashlib

def get_cache_key(text: str) -> str:
    """Generate unique cache key from text"""
    # Hash text to create consistent key
    return f"fallacy_analysis:{hashlib.sha256(text.encode()).hexdigest()}"

# Use with explicit cache control
cache.set(get_cache_key(text), result, timeout=3600)
cached_result = cache.get(get_cache_key(text))
```

**Confidence:** HIGH - Flask-Caching is documented and production-tested

---

### Pattern 7: Rate Limiting (Prevent API Abuse)

**What:** Limit number of requests per user/IP to prevent abuse

**When:** Public-facing API, OpenAI API costs money

**Why:**
- **Cost Control**: Prevent excessive OpenAI API usage
- **Fair Use**: Prevent one user from monopolizing resources
- **DoS Protection**: Mitigate denial-of-service attacks
- **Resource Management**: Keep server responsive

**Implementation Options:**

**Option A: Flask-Limiter (Simple, in-memory)**

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["10 per minute", "100 per hour"]
)

# Apply to specific routes
@fallacy_bp.route('/analyze', methods=['POST'])
@limiter.limit("5 per minute")
def analyze_text():
    """Allow 5 analyses per minute per IP"""
    # Handler logic
    pass
```

**Response Headers (Automatic):**

```
HTTP/1.1 200 OK
X-RateLimit-Limit: 5
X-RateLimit-Remaining: 3
X-RateLimit-Reset: 60
```

**Option B: Redis-backed (Distributed, production)**

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from redis import Redis

redis = Redis(host='localhost', port=6379, db=1)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379/1",
    default_limits=["10 per minute", "100 per hour"]
)
```

**Option C: Custom Rate Limiting (More granular)**

```python
from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, max_requests, period):
        self.max_requests = max_requests
        self.period = period
        self.requests = defaultdict(list)

    def is_allowed(self, identifier: str) -> bool:
        now = time.time()
        # Clean old requests
        self.requests[identifier] = [
            t for t in self.requests[identifier]
            if now - t < self.period
        ]
        # Check limit
        if len(self.requests[identifier]) >= self.max_requests:
            return False
        # Record request
        self.requests[identifier].append(now)
        return True

# Usage in route
limiter = RateLimiter(max_requests=5, period=60)

@fallacy_bp.route('/analyze', methods=['POST'])
def analyze_text():
    ip = request.remote_addr
    if not limiter.is_allowed(ip):
        return jsonify({
            'error': 'Rate limit exceeded',
            'retry_after': 60
        }), 429
    # Handler logic
```

**Confidence:** HIGH - Flask-Limiter is production-tested, patterns from REST best practices

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Direct OpenAI API Calls from Frontend

**What:** Calling OpenAI API directly from React components

**Why bad:**
- **Security**: Exposes API keys in client-side code
- **No Rate Limiting**: Can't control usage or costs
- **No Caching**: Every user pays for same analysis
- **No Validation**: Bypasses backend validation

**Instead:**
- Route all AI calls through Flask backend
- Store API keys server-side (environment variables)
- Implement caching and rate limiting on backend

---

### Anti-Pattern 2: Props Drilling for State

**What:** Passing state through multiple component layers

**Why bad:**
- **Coupling**: Components depend on parent structure
- **Difficult Refactoring**: Changes cascade through component tree
- **Poor Performance**: Unnecessary re-renders

**Example:**

```jsx
// BAD: Props drilling
function App() {
  const [results, setResults] = useState(null)
  return (
    <ResultsSection
      results={results}
      setResults={setResults}
    />
  )
}

function ResultsSection({ results, setResults }) {
  return (
    <FallacyCard
      results={results}
      setResults={setResults}
    />
  )
}
```

**Instead:**
- Keep state where it's used
- Use context API if shared across deep hierarchy
- Use custom hooks for reusable state logic

```jsx
// GOOD: Local state
function ResultsSection({ onResultsChange }) {
  const [results, setResults] = useState(null)

  useEffect(() => {
    // Fetch results
    const data = await fetchResults()
    setResults(data)
  }, [])

  return <FallacyCard results={results} />
}
```

**Confidence:** HIGH - React documentation explicitly warns against this

---

### Anti-Pattern 3: Global State for Everything

**What:** Using React Context or Redux for all state

**Why bad:**
- **Complexity**: Over-engineering simple components
- **Performance**: Unnecessary re-renders of entire app
- **Debugging**: Harder to trace state changes

**Instead:**
- Use local state (useState) for component-specific data
- Use context only for truly global state (theme, user auth)
- Use Redux for complex state management (not needed here)

**Confidence:** HIGH - React best practices

---

### Anti-Pattern 4: Blocking API Calls (No Async/Await)

**What:** Synchronous HTTP requests that block UI

**Why bad:**
- **Poor UX**: UI freezes during API calls
- **Browser Timeout**: Can trigger long-script warnings
- **No Cancellation**: Can't cancel pending requests

**Example:**

```jsx
// BAD: Synchronous (hypothetical, JS doesn't actually support this)
function analyzeText() {
  const result = fetch('/api/analyze', {  // This blocks!
    method: 'POST',
    body: JSON.stringify({ text })
  })
  setResults(result)  // UI frozen until here
}
```

**Instead:**
- Always use async/await
- Show loading states
- Handle errors gracefully

```jsx
// GOOD: Async with loading state
const [loading, setLoading] = useState(false)

const analyzeText = async () => {
  setLoading(true)
  try {
    const response = await fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    })
    const result = await response.json()
    setResults(result)
  } catch (error) {
    setError(error.message)
  } finally {
    setLoading(false)
  }
}

return (
  <div>
    {loading && <Spinner />}
    {error && <Error message={error} />}
    <button onClick={analyzeText}>Analyze</button>
  </div>
)
```

**Confidence:** HIGH - Fundamental React pattern

---

### Anti-Pattern 5: Not Cleaning Up Side Effects

**What:** Creating event listeners, intervals, or API calls without cleanup

**Why bad:**
- **Memory Leaks**: Listeners persist after unmount
- **Stale State**: Updates to unmounted components cause warnings
- **Duplicate Requests**: Effects re-run without canceling previous

**Example:**

```jsx
// BAD: No cleanup
useEffect(() => {
  const interval = setInterval(() => {
    fetchResults()
  }, 5000)
  // Missing cleanup!
}, [])
```

**Instead:**
- Return cleanup function from useEffect
- Abort fetch requests on unmount

```jsx
// GOOD: With cleanup
useEffect(() => {
  const controller = new AbortController()

  const interval = setInterval(() => {
    fetchResults({ signal: controller.signal })
  }, 5000)

  return () => {
    clearInterval(interval)
    controller.abort()  // Cancel fetch
  }
}, [])
```

**Confidence:** HIGH - Directly from React useEffect documentation

---

## Scalability Considerations

| Concern | At 100 users | At 10K users | At 1M users |
|---------|--------------|--------------|-------------|
| **API Response Time** | 2-3s acceptable | <1s required | <500ms required |
| **OpenAI API Costs** | $10-50/mo | $500-2K/mo | $50K-200K/mo |
| **Database** | SQLite fine | PostgreSQL needed | Sharded PostgreSQL |
| **Caching** | In-memory OK | Redis required | Multi-level cache |
| **Rate Limiting** | Simple counter | Redis-backed | Distributed limits |
| **Static Files** | Flask serves | Nginx/CDN | Global CDN |
| **Error Tracking** | Console logs | Sentry required | Distributed logging |

### Scaling Recommendations

**Phase 1 (0-100 users):**
- Keep Flask serving static files
- In-memory cache (Python dict or SimpleCache)
- SQLite database
- Simple rate limiting (in-memory)
- Console logging

**Phase 2 (100-10K users):**
- Nginx reverse proxy
- Flask-Caching with Redis
- PostgreSQL database
- Flask-Limiter with Redis
- Sentry for error tracking
- CDN for static assets (Vercel/Netlify)

**Phase 3 (10K-1M users):**
- Separate frontend and backend deployments
- API Gateway (Kong/AWS API Gateway)
- Microservices (analyze, cache, user services)
- Database read replicas
- Multi-level caching (Redis CDN, in-memory L1)
- Distributed tracing (OpenTelemetry)
- Queue for batch analysis (Celery/RQ)

**Confidence:** MEDIUM - Based on general web app scaling patterns, no specific AI system benchmarks found

---

## Sources

- [Flask Documentation - Error Handling](https://flask.palletsprojects.com/en/3.0.x/errorhandling/) - HIGH confidence
- [Flask Documentation - View Decorators](https://flask.palletsprojects.com/en/3.0.x/patterns/viewdecorators/) - HIGH confidence
- [Flask-Caching Documentation](https://flask-caching.readthedocs.io/en/latest/) - HIGH confidence
- [React Documentation - useState](https://react.dev/learn/state-a-components-memory) - HIGH confidence
- [React Documentation - useEffect](https://react.dev/reference/react/useEffect) - HIGH confidence
- [REST API Tutorial - Rate Limiting](https://restfulapi.net/rest-api-rate-limit-guidelines/) - HIGH confidence
- [REST API Tutorial - What is REST](https://restfulapi.net/) - HIGH confidence
- [GraphQL.org Learn](https://graphql.org/learn/) - HIGH confidence
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference) - MEDIUM confidence (403 on production best practices)
- Current codebase analysis (main.py, fallacy.py, App.jsx) - HIGH confidence
