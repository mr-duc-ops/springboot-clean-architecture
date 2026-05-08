# Game Đoán Số — Quick Reference & Command Guide

**For rapid development & deployment**

---

## 🚀 QUICK START (5 minutes)

```bash
# 1. Clone repo
git clone <repo> game-doan-so
cd game-doan-so

# 2. Install Java 17+
java -version  # Should show 17+

# 3. Run app (dev mode with H2)
mvn spring-boot:run

# 4. App should start
# → Listen on localhost:8080
# → H2 console at localhost:8080/h2-console

# 5. Test register endpoint
curl -X POST http://localhost:8080/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

---

## 📋 MAVEN COMMANDS CHEAT SHEET

```bash
# Build
mvn clean compile          # Compile only
mvn clean package          # Full build + package into JAR
mvn clean package -DskipTests  # Build without running tests

# Testing
mvn test                   # Run all tests
mvn test -Dtest=GuessUseCaseTest  # Run single test class
mvn jacoco:report          # Generate coverage report

# Running
mvn spring-boot:run        # Dev mode
mvn spring-boot:run -Dspring-boot.run.arguments="--spring.profiles.active=test"

# Dependency Management
mvn dependency:tree        # View dependency tree
mvn dependency:check       # Check for vulnerable dependencies

# Clean
mvn clean                  # Delete target/ folder
```

---

## 🏗️ PROJECT STRUCTURE

```
game-doan-so/
├── src/main/java/com/game/guess/
│   ├── domain/               # Pure business logic (NO Spring imports)
│   │   ├── model/            # Entities (User, GuessResult)
│   │   ├── repository/       # Repository interfaces
│   │   └── service/          # Domain services
│   ├── application/          # Use cases (orchestration)
│   │   ├── auth/             # Login/Register
│   │   ├── game/             # Guess/BuyTurns
│   │   └── user/             # Profile/Leaderboard
│   ├── infrastructure/       # Framework implementations
│   │   ├── persistence/      # JPA entities & repos
│   │   ├── cache/            # Redis implementation
│   │   └── security/         # JWT, BCrypt, filters
│   └── presentation/         # REST API layer
│       ├── controller/       # REST endpoints
│       ├── dto/              # Request/Response DTOs
│       └── exception/        # Exception handlers
├── src/test/java/...        # Integration & unit tests
├── src/main/resources/
│   ├── application.yml       # Default config
│   ├── application-dev.yml   # Dev (H2)
│   ├── application-test.yml  # Test (Testcontainers)
│   └── db/migration/         # Flyway SQL migrations
├── docs/
│   ├── ADR/                  # Architecture decisions
│   ├── API_CONTRACT.md       # API documentation
│   └── DEPLOYMENT.md         # Deployment guide
├── pom.xml                   # Maven config
└── Dockerfile                # Docker image
```

---

## 🔑 KEY ENDPOINTS

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| POST | `/api/v1/auth/register` | No | Create account |
| POST | `/api/v1/auth/login` | No | Login (JWT cookie) |
| POST | `/api/v1/game/guess` | Yes | Make guess |
| POST | `/api/v1/game/buy-turns` | Yes | Buy 5 turns |
| GET | `/api/v1/game/leaderboard` | No | Top 10 players |
| GET | `/api/v1/user/me` | Yes | My profile |
| GET | `/actuator/health` | No | Health check |
| GET | `/swagger-ui.html` | No | API docs |

---

## 🧪 TESTING COMMANDS

```bash
# Run all tests
mvn test

# Run specific test
mvn test -Dtest=AuthIntegrationTest#testRegister_Success

# Run with coverage report
mvn clean test jacoco:report
# Report generated at: target/site/jacoco/index.html

# Performance testing (load test with 100 requests)
for i in {1..100}; do
  curl -X POST http://localhost:8080/api/v1/game/guess \
    -H "Cookie: access_token=<valid_jwt>" \
    -H "Content-Type: application/json" \
    -d '{"guess":1}'
done
```

---

## 🔐 SECURITY CHECKLIST

```bash
# 1. Verify no hardcoded secrets
grep -r "password\|secret\|key" src/ | grep -v "\.yml"

# 2. Verify dependencies for vulnerabilities
mvn dependency-check:check

# 3. Verify BCrypt is used
grep -r "BCryptPasswordEncoder" src/

# 4. Verify JWT HttpOnly cookie
grep -r "HttpOnly\|Secure" src/

# 5. Check SQL injection protection
grep -r "Query\|@Param\|PreparedStatement" src/
```

---

## 📊 DATABASE DEBUGGING

```bash
# H2 Console (dev mode)
# Open: http://localhost:8080/h2-console
# URL: jdbc:h2:mem:gamedoannso
# User: sa (no password)

# SQL Queries
SELECT * FROM users;
SELECT COUNT(*) FROM game_log;
SELECT * FROM users ORDER BY score DESC LIMIT 10;

# Check concurrent updates
SELECT * FROM users WHERE id = 1;
UPDATE users SET turns = turns - 1 WHERE id = 1 AND turns > 0;
SELECT ROW_COUNT() as affected_rows;  -- Should be 1
```

---

## 🎮 API TESTING WITH CURL

```bash
# 1. Register
curl -X POST http://localhost:8080/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"player1","password":"securepass123"}'
# Response: { "id": 1, "username": "player1", "score": 0, "turns": 0 }

# 2. Login (get HttpOnly cookie)
curl -i -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"player1","password":"securepass123"}'
# Look for: Set-Cookie: access_token=eyJ...

# 3. Buy turns (save cookie)
TOKEN="eyJ..." # from Set-Cookie header
curl -X POST http://localhost:8080/api/v1/game/buy-turns \
  -H "Cookie: access_token=$TOKEN" \
  -H "Content-Type: application/json"
# Response: { "turnsAdded": 5, "turnsTotal": 5 }

# 4. Make guess
curl -X POST http://localhost:8080/api/v1/game/guess \
  -H "Cookie: access_token=$TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"guess":3}'
# Response: { "result": "WIN"|"LOSE", "serverNumber": 3, "score": 1, "turnsRemaining": 4 }

# 5. Leaderboard
curl http://localhost:8080/api/v1/game/leaderboard
# Response: [ { "rank": 1, "username": "player1", "score": 1 }, ... ]

# 6. My Profile
curl -H "Cookie: access_token=$TOKEN" \
  http://localhost:8080/api/v1/user/me
# Response: { "username": "player1", "score": 1, "turns": 4 }
```

---

## 🐳 DOCKER COMMANDS

```bash
# Build image
docker build -t game-doan-so:v1.0.0 .

# Run dev (H2 in-memory)
docker run -p 8080:8080 game-doan-so:v1.0.0

# Run prod (MySQL + Redis)
docker run -d \
  -e SPRING_PROFILES_ACTIVE=prod \
  -e SPRING_DATASOURCE_URL=jdbc:mysql://prod-db:3306/gamedoannso \
  -e SPRING_DATASOURCE_USERNAME=root \
  -e SPRING_DATASOURCE_PASSWORD=password \
  -e SPRING_REDIS_HOST=prod-redis \
  -e JWT_SECRET=your-secret-key-min-32-chars \
  -p 8080:8080 \
  game-doan-so:v1.0.0

# View logs
docker logs -f <container_id>

# Stop container
docker stop <container_id>

# Docker Compose (optional)
docker-compose up  # Requires docker-compose.yml
```

---

## 🔍 DEBUGGING TIPS

```bash
# 1. View application logs
tail -f target/logs/application.log

# 2. Enable SQL logging
# Add to application.yml:
spring:
  jpa:
    show-sql: true
    properties:
      hibernate:
        format_sql: true

# 3. Debug a specific method
# Add @Transactional and use breakpoints in IDE

# 4. Check Spring context
# Add logging:
logging:
  level:
    org.springframework: DEBUG

# 5. Profile performance
# Add JMH (Java Microbenchmark Harness) tests

# 6. Memory leak detection
java -XX:+PrintGCDetails -XX:+PrintGCTimeStamps -jar target/game-doan-so.jar

# 7. Thread dump (find deadlocks)
jps  # Get process ID
jstack <pid> | grep -A 20 "nid="
```

---

## 📈 MONITORING & METRICS

```bash
# Health check
curl http://localhost:8080/actuator/health

# Metrics
curl http://localhost:8080/actuator/metrics

# Specific metric (e.g., HTTP requests)
curl http://localhost:8080/actuator/metrics/http.server.requests

# Prometheus format (if configured)
curl http://localhost:8080/actuator/prometheus

# Environment info
curl http://localhost:8080/actuator/env
```

---

## 🚨 COMMON ERRORS & SOLUTIONS

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to start ApplicationContext` | Missing properties | Check `application.yml`, ensure DB/Redis accessible |
| `Table 'users' doesn't exist` | Migrations not run | Run `mvn flyway:migrate` |
| `Connection refused: localhost:6379` | Redis not running | `docker run -d redis:7-alpine` or install Redis locally |
| `Unsupported class version 63.0` | Wrong Java version | Install Java 17+, check `JAVA_HOME` |
| `401 Unauthorized` | Invalid JWT | Login first, get new token from Set-Cookie header |
| `403 Forbidden: Insufficient Turns` | No turns left | Use `POST /buy-turns` to get more |
| `409 Conflict: User already exists` | Username taken | Use different username |
| `p95 latency > SLA` | Performance issue | Profile with JProfiler or check DB queries |

---

## 📋 PRE-DEPLOYMENT CHECKLIST

```bash
# 1. Build succeeds
mvn clean package -DskipTests

# 2. Tests pass
mvn clean test

# 3. No hardcoded secrets
grep -r "password\|secret\|key" src/ | grep -v "\.yml"

# 4. Coverage > 70%
mvn jacoco:report
# Check: target/site/jacoco/index.html

# 5. Performance within SLA
# Run performance tests, verify p95 < 150ms for /guess

# 6. Security audit passed
# Review all authentication paths, SQL injection protection

# 7. Documentation complete
ls docs/ADR/  # Should have 3-4 ADRs
cat docs/API_CONTRACT.md  # Should be complete
cat docs/DEPLOYMENT.md  # Should have prod instructions

# 8. Git tags
git tag v1.0.0
git push origin v1.0.0

# 9. JAR runnable
java -jar target/game-doan-so-1.0.0.jar --spring.profiles.active=dev

# 10. Health check
curl http://localhost:8080/actuator/health
```

---

## 🎯 PERFORMANCE BENCHMARKS (Target SLA)

| Endpoint | Operation | SLA | Current | Status |
|----------|-----------|-----|---------|--------|
| POST /guess | Make guess (atomic UPDATE) | < 150ms p95 | ? | Testing |
| GET /leaderboard | Fetch cached top 10 | < 30ms p95 | ? | Testing |
| POST /register | Create user + hash password | < 200ms p95 | ? | Testing |
| POST /login | Verify + generate JWT | < 200ms p95 | ? | Testing |
| POST /buy-turns | Atomic INCREMENT | < 100ms p95 | ? | Testing |

---

## 📚 USEFUL LINKS

- **Spring Boot Docs**: https://spring.io/projects/spring-boot
- **JPA Docs**: https://spring.io/projects/spring-data-jpa
- **Redis Docs**: https://redis.io/documentation
- **JWT Docs**: https://jwt.io/
- **OWASP Top 10**: https://owasp.org/www-project-top-ten/

---

## 👥 TEAM CONTACTS

| Role | Name | Email | Phone |
|------|------|-------|-------|
| Tech Lead | Mr. Đức | duch9707@gmail.com | +84 389 086 502 |
| Backend Dev | [Name] | [Email] | [Phone] |
| QA Engineer | [Name] | [Email] | [Phone] |
| DevOps | [Name] | [Email] | [Phone] |

---

## 🎓 LEARNING RESOURCES

- **Clean Architecture**: Read "Clean Code" by Robert Martin
- **4+1 View Model**: https://duc-huynh-2003.vercel.app/posts/view-model-4-plus-1
- **Atomic Operations**: Study MySQL's `ACID` properties
- **Spring Security**: Spring official tutorials
- **Testing**: "Test Driven Development" by Kent Beck

---

**Last Updated**: May 7, 2026  
**Version**: 1.0  
**Status**: ✅ READY TO USE

---

**Quick Start**: `mvn spring-boot:run` → Open `http://localhost:8080/swagger-ui.html` 🚀
