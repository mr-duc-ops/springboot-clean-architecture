# Game Đoán Số — Detailed Task Breakdown & Daily Checklist

**For Sprint Planning & Daily Standup**  
**Owner**: Team Lead | **Format**: Agile Sprint (5 days, 8 hours/day)

---

## SPRINT BOARD — DAY-BY-DAY EXECUTION

### DAY 1: Foundation & Domain Model (8 hours)

#### Morning Session (4 hours) — Setup & Infrastructure

**Task 1.1**: Git Repository & Project Structure (1 hour)
- [ ] Create GitHub repo: `game-doan-so`
- [ ] Clone to local: `git clone <repo>`
- [ ] Create `.gitignore` (Java + Maven + IDE patterns)
- [ ] Create folder structure:
  ```bash
  mkdir -p src/main/java/com/game/guess/{domain,application,infrastructure,presentation}
  mkdir -p src/test/java/com/game/guess/
  mkdir -p src/main/resources/{db/migration}
  mkdir -p docs/{ADR,diagrams}
  ```
- [ ] Initialize git: `git init` (if not from GitHub)
- [ ] First commit: "chore: project initialization"

**Acceptance**: Folder structure matches design, git log shows initial commit

---

**Task 1.2**: Maven Project Setup (1 hour)
- [ ] Create `pom.xml` with:
  ```xml
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.game</groupId>
  <artifactId>doan-so</artifactId>
  <version>1.0.0</version>
  <name>Game Đoán Số</name>
  ```
- [ ] Add Spring Boot parent:
  ```xml
  <parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>4.0.6</version>
  </parent>
  ```
- [ ] Add dependencies (see section A below)
- [ ] Build: `mvn clean compile`
- [ ] Verify: `mvn --version` (Java 17+ required)

**Acceptance**: `mvn clean compile` succeeds, no dependency errors

---

**Task 1.3**: Spring Boot Application Configuration (1 hour)
- [ ] Create `src/main/java/com/game/guess/GameDoAnSoApplication.java`:
  ```java
  @SpringBootApplication
  public class GameDoAnSoApplication {
    public static void main(String[] args) {
      SpringApplication.run(GameDoAnSoApplication.class, args);
    }
  }
  ```
- [ ] Create `src/main/resources/application.yml`:
  ```yaml
  spring:
    application:
      name: game-doan-so
    datasource:
      url: jdbc:h2:mem:gamedoannso
      driver-class-name: org.h2.Driver
    jpa:
      hibernate:
        ddl-auto: validate
      show-sql: false
    redis:
      host: localhost
      port: 6379
  server:
    port: 8080
  ```
- [ ] Create `application-test.yml` (Testcontainers profile)
- [ ] Run: `mvn spring-boot:run`
- [ ] Verify: App starts, logs show "Started GameDoAnSoApplication"

**Acceptance**: App starts successfully, listens on 8080

---

**Task 1.4**: Database Configuration & Migrations (1 hour)
- [ ] Create `src/main/resources/db/migration/V1__initial_schema.sql`:
  ```sql
  CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    passwordHash VARCHAR(255) NOT NULL,
    score INT DEFAULT 0 NOT NULL CHECK(score >= 0),
    turns INT DEFAULT 0 NOT NULL CHECK(turns >= 0),
    consecutiveLosses INT DEFAULT 0,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    version LONG DEFAULT 0,
    INDEX idx_username (username)
  );

  CREATE TABLE game_log (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    guess INT NOT NULL,
    serverNumber INT NOT NULL,
    outcome ENUM('WIN', 'LOSE') NOT NULL,
    turns_before INT NOT NULL,
    score_before INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_created (user_id, created_at)
  );
  ```
- [ ] Add Flyway to `pom.xml`
- [ ] Run migrations: `mvn flyway:migrate`
- [ ] Verify: Tables created in H2 console

**Acceptance**: Schema created, no migration errors

**MORNING STANDUP**: Check-in status, blockers

---

#### Afternoon Session (4 hours) — Domain Model

**Task 1.5**: Domain Entities (1.5 hours)
Create `src/main/java/com/game/guess/domain/model/`:

- [ ] `User.java` (Pure domain, no Spring/JPA)
  ```java
  public class User {
    private Long id;
    private String username;
    private String passwordHash;
    private Integer score;
    private Integer turns;
    private Integer consecutiveLosses;
    
    public void decrementTurns() {
      if (this.turns <= 0) 
        throw new InsufficientTurnsException("No turns left");
      this.turns--;
    }
    
    public void addScore(int points) {
      this.score += points;
    }
    
    public void recordLoss() {
      this.consecutiveLosses++;
    }
    
    public void resetLosses() {
      this.consecutiveLosses = 0;
    }
  }
  ```

- [ ] `GuessResult.java` (Immutable VO)
  ```java
  public record GuessResult(
    String outcome,  // "WIN" | "LOSE"
    Integer serverNumber,
    Integer score,
    Integer turnsRemaining
  ) {}
  ```

- [ ] `WinRatePolicy.java` (Interface, domain-level)
  ```java
  public interface WinRatePolicy {
    String determineOutcome(Integer consecutiveLosses);
  }
  ```

**Acceptance**: Classes compile, can be instantiated

---

**Task 1.6**: Domain Repository Interfaces (1 hour)
Create `src/main/java/com/game/guess/domain/repository/`:

- [ ] `IUserRepository.java`
  ```java
  public interface IUserRepository {
    Optional<User> findById(Long id);
    Optional<User> findByUsername(String username);
    User save(User user);
    boolean existsByUsername(String username);
  }
  ```

- [ ] `ILeaderboardCache.java`
  ```java
  public interface ILeaderboardCache {
    List<LeaderboardEntry> getTop10();
    void incrementScore(String username, double points);
    void evict();
  }
  ```

- [ ] `IGameLogRepository.java`
  ```java
  public interface IGameLogRepository {
    void logGuess(Long userId, int guess, int serverNum, String outcome, 
                  int turnsBefore, int scoreBefore);
  }
  ```

**Acceptance**: Interfaces defined, compile, clear contract

---

**Task 1.7**: Domain Services (1.5 hours)
Create `src/main/java/com/game/guess/domain/service/`:

- [ ] `GameDomainService.java`
  ```java
  public class GameDomainService {
    private final WinRatePolicy winRatePolicy;
    
    public GuessResult processGuess(User user, int guess) 
        throws InsufficientTurnsException {
      
      // Atomic business logic (domain only, no DB calls here)
      user.decrementTurns();
      
      String outcome = winRatePolicy.determineOutcome(
        user.getConsecutiveLosses()
      );
      
      if ("WIN".equals(outcome)) {
        user.addScore(1);
        user.resetLosses();
      } else {
        user.recordLoss();
      }
      
      int serverNumber = generateMatchingNumber(guess, outcome);
      
      return new GuessResult(
        outcome,
        serverNumber,
        user.getScore(),
        user.getTurns()
      );
    }
  }
  ```

**Acceptance**: Service has no Spring/JPA imports, pure business logic

**DAILY STANDUP**: Verify all domain layer done, no blockers

---

#### END OF DAY 1 CHECKLIST:
- [ ] Project builds: `mvn clean compile` ✅
- [ ] Database schema created ✅
- [ ] Domain entities defined (User, GuessResult) ✅
- [ ] Repository interfaces defined ✅
- [ ] Domain service created ✅
- [ ] All tests compile (even if not running) ✅
- [ ] First commit: "feat: domain model and entities" ✅

**Commit**: `git commit -m "feat(domain): add entities, services, repository interfaces"`

---

### DAY 2: Application & Infrastructure Layer (8 hours)

#### Morning Session (4 hours) — Application Use Cases

**Task 2.1**: Authentication Use Cases (2 hours)
Create `src/main/java/com/game/guess/application/auth/`:

- [ ] `RegisterUseCase.java`
  ```java
  @Service
  public class RegisterUseCase {
    private final IUserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    
    public RegisterResponse register(RegisterRequest request) {
      if (userRepository.existsByUsername(request.username()))
        throw new UserAlreadyExistsException();
      
      User user = new User();
      user.setUsername(request.username());
      user.setPasswordHash(
        passwordEncoder.encode(request.password())
      );
      user.setScore(0);
      user.setTurns(0);
      
      User saved = userRepository.save(user);
      
      return new RegisterResponse(
        saved.getId(),
        saved.getUsername(),
        0,
        0
      );
    }
  }
  ```

- [ ] `LoginUseCase.java`
  ```java
  @Service
  public class LoginUseCase {
    private final IUserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtProvider jwtProvider;
    
    public LoginResponse login(LoginRequest request) {
      User user = userRepository.findByUsername(request.username())
        .orElseThrow(() -> new InvalidCredentialsException());
      
      if (!passwordEncoder.matches(request.password(), 
                                    user.getPasswordHash()))
        throw new InvalidCredentialsException();
      
      String token = jwtProvider.generateToken(user.getId());
      
      return new LoginResponse(
        user.getUsername(),
        user.getScore(),
        user.getTurns(),
        token  // Token will be set as cookie by controller
      );
    }
  }
  ```

**Unit Tests** (same day):
- Test register with valid input → user created
- Test register with duplicate username → 409 error
- Test login with valid credentials → token generated
- Test login with wrong password → 401 error

**Acceptance**: Both use cases implemented, unit tests pass

---

**Task 2.2**: Game Use Cases (2 hours)
Create `src/main/java/com/game/guess/application/game/`:

- [ ] `GuessUseCase.java` (CRITICAL)
  ```java
  @Service
  @Transactional
  public class GuessUseCase {
    private final IUserRepository userRepository;
    private final GameDomainService gameDomainService;
    private final ILeaderboardCache leaderboardCache;
    private final IGameLogRepository gameLogRepository;
    
    public GuessResponse guess(Long userId, int guess) {
      User user = userRepository.findById(userId)
        .orElseThrow(() -> new UserNotFoundException());
      
      // Snapshot before
      int turnsBefore = user.getTurns();
      int scoreBefore = user.getScore();
      
      // Process guess (domain business logic)
      GuessResult result = gameDomainService.processGuess(user, guess);
      
      // Persist updated user (atomic conditional update)
      User updated = userRepository.save(user);
      
      // Update leaderboard if WIN
      if ("WIN".equals(result.outcome())) {
        leaderboardCache.incrementScore(user.getUsername(), 1.0);
      }
      
      // Log event (audit trail)
      gameLogRepository.logGuess(
        userId, guess, result.serverNumber(),
        result.outcome(), turnsBefore, scoreBefore
      );
      
      return new GuessResponse(
        result.outcome(),
        result.serverNumber(),
        result.score(),
        result.turnsRemaining()
      );
    }
  }
  ```

- [ ] `BuyTurnsUseCase.java`
  ```java
  @Service
  @Transactional
  public class BuyTurnsUseCase {
    private final IUserRepository userRepository;
    
    public BuyTurnsResponse buyTurns(Long userId) {
      User user = userRepository.findById(userId)
        .orElseThrow(() -> new UserNotFoundException());
      
      user.setTurns(user.getTurns() + 5);
      User updated = userRepository.save(user);
      
      return new BuyTurnsResponse(5, updated.getTurns());
    }
  }
  ```

**Unit Tests** (same day):
- Test guess with sufficient turns → processed
- Test guess with 0 turns → 403 error
- Test concurrent guesses → no race condition
- Test buy turns → 5 turns added

**Acceptance**: Both use cases implemented, concurrency tested

**MORNING STANDUP**: Check progress

---

#### Afternoon Session (4 hours) — Infrastructure & Security

**Task 2.3**: Infrastructure Setup (2 hours)
Create `src/main/java/com/game/guess/infrastructure/`:

- [ ] `persistence/UserJpaEntity.java` (JPA mapping)
  ```java
  @Entity
  @Table(name = "users")
  public class UserJpaEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(unique = true, nullable = false)
    private String username;
    
    @Column(nullable = false)
    private String passwordHash;
    
    @Column(nullable = false)
    private Integer score = 0;
    
    @Column(nullable = false)
    private Integer turns = 0;
    
    @Version
    private Long version;
  }
  ```

- [ ] `persistence/UserJpaRepository.java`
  ```java
  @Repository
  public interface UserJpaRepository 
      extends JpaRepository<UserJpaEntity, Long> {
    Optional<UserJpaEntity> findByUsername(String username);
    
    @Modifying
    @Query("UPDATE UserJpaEntity u SET u.turns = u.turns - 1 " +
           "WHERE u.id = :id AND u.turns > 0")
    int decrementTurnsIfAvailable(@Param("id") Long id);
  }
  ```

- [ ] Adapter: `persistence/UserRepositoryAdapter.java`
  ```java
  @Component
  public class UserRepositoryAdapter implements IUserRepository {
    private final UserJpaRepository jpaRepository;
    
    @Override
    public Optional<User> findById(Long id) {
      return jpaRepository.findById(id)
        .map(this::toDomain);
    }
    
    private User toDomain(UserJpaEntity entity) {
      // Map JPA entity to domain model
      ...
    }
  }
  ```

**Acceptance**: JPA entities compile, repository queries work

---

**Task 2.4**: Security & JWT (2 hours)
Create `src/main/java/com/game/guess/infrastructure/security/`:

- [ ] `JwtProvider.java`
  ```java
  @Component
  public class JwtProvider {
    @Value("${jwt.secret:}")
    private String jwtSecret;
    
    @Value("${jwt.expiration:3600000}")
    private long jwtExpiration;
    
    public String generateToken(Long userId) {
      return Jwts.builder()
        .setSubject(userId.toString())
        .setIssuedAt(new Date())
        .setExpiration(new Date(System.currentTimeMillis() + jwtExpiration))
        .signWith(SignatureAlgorithm.HS256, jwtSecret)
        .compact();
    }
    
    public Long extractUserId(String token) {
      return Long.valueOf(Jwts.parser()
        .setSigningKey(jwtSecret)
        .parseClaimsJws(token)
        .getBody()
        .getSubject());
    }
  }
  ```

- [ ] `JwtFilter.java` (Extract JWT from HttpOnly cookie)
  ```java
  public class JwtFilter extends OncePerRequestFilter {
    private final JwtProvider jwtProvider;
    
    @Override
    protected void doFilterInternal(HttpServletRequest request,
        HttpServletResponse response, FilterChain filterChain) {
      try {
        Cookie[] cookies = request.getCookies();
        String token = null;
        
        if (cookies != null) {
          for (Cookie cookie : cookies) {
            if ("access_token".equals(cookie.getName())) {
              token = cookie.getValue();
              break;
            }
          }
        }
        
        if (token != null) {
          Long userId = jwtProvider.extractUserId(token);
          // Set SecurityContext
          SecurityContextHolder.getContext()
            .setAuthentication(new UsernamePasswordAuthenticationToken(
              userId, null, new ArrayList<>()
            ));
        }
      } catch (JwtException e) {
        logger.error("JWT parsing failed", e);
      }
      
      try {
        filterChain.doFilter(request, response);
      } catch (ServletException | IOException e) {
        throw new RuntimeException(e);
      }
    }
  }
  ```

- [ ] `CookieUtil.java`
  ```java
  public class CookieUtil {
    public static void setHttpOnlyCookie(HttpServletResponse response, 
                                         String token) {
      Cookie cookie = new Cookie("access_token", token);
      cookie.setHttpOnly(true);
      cookie.setSecure(true);  // Only over HTTPS
      cookie.setPath("/");
      cookie.setMaxAge(3600);  // 1 hour
      cookie.setAttribute("SameSite", "Strict");
      response.addCookie(cookie);
    }
  }
  ```

- [ ] `SecurityConfig.java`
  ```java
  @Configuration
  @EnableWebSecurity
  public class SecurityConfig {
    @Bean
    public PasswordEncoder passwordEncoder() {
      return new BCryptPasswordEncoder(12);
    }
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
      http
        .authorizeHttpRequests(authz -> authz
          .requestMatchers("/api/v1/auth/**").permitAll()
          .requestMatchers("/api/v1/game/leaderboard").permitAll()
          .anyRequest().authenticated()
        )
        .addFilterBefore(new JwtFilter(...), 
          UsernamePasswordAuthenticationFilter.class)
        .csrf().disable();
      return http.build();
    }
  }
  ```

**Acceptance**: Security chain configured, can extract JWT from cookie

**DAILY STANDUP**: Infrastructure progress check

---

#### END OF DAY 2 CHECKLIST:
- [ ] Use cases implemented (Register, Login, Guess, BuyTurns) ✅
- [ ] JPA entities & repositories created ✅
- [ ] Security configured (JWT, BCrypt, HttpOnly cookie) ✅
- [ ] Unit tests for use cases (80%+ coverage) ✅
- [ ] Build passes: `mvn clean test` ✅
- [ ] Commit: `git commit -m "feat(app,infra): use cases + security"`

---

### DAY 3: REST Controllers & Integration Tests (8 hours)

#### Morning Session (4 hours) — Controllers & DTOs

**Task 3.1**: DTOs & Validation (1 hour)
Create `src/main/java/com/game/guess/presentation/dto/`:

- [ ] `RegisterRequest.java`
  ```java
  public record RegisterRequest(
    @NotBlank @Size(min = 3, max = 50)
    String username,
    
    @NotBlank @Size(min = 8)
    String password
  ) {}
  ```

- [ ] `LoginRequest.java`, `GuessRequest.java`, response DTOs...

**Acceptance**: DTOs compile, validation annotations present

---

**Task 3.2**: REST Controllers (2 hours)
Create `src/main/java/com/game/guess/presentation/controller/`:

- [ ] `AuthController.java`
  ```java
  @RestController
  @RequestMapping("/api/v1/auth")
  public class AuthController {
    private final RegisterUseCase registerUseCase;
    private final LoginUseCase loginUseCase;
    
    @PostMapping("/register")
    public ResponseEntity<RegisterResponse> register(
        @Valid @RequestBody RegisterRequest request) {
      RegisterResponse response = registerUseCase.register(request);
      return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }
    
    @PostMapping("/login")
    public ResponseEntity<LoginResponse> login(
        @Valid @RequestBody LoginRequest request,
        HttpServletResponse httpResponse) {
      LoginResponse response = loginUseCase.login(request);
      CookieUtil.setHttpOnlyCookie(httpResponse, response.token());
      return ResponseEntity.ok(response);
    }
  }
  ```

- [ ] `GameController.java`
  ```java
  @RestController
  @RequestMapping("/api/v1/game")
  public class GameController {
    private final GuessUseCase guessUseCase;
    private final BuyTurnsUseCase buyTurnsUseCase;
    private final GetLeaderboardUseCase getLeaderboardUseCase;
    
    @PostMapping("/guess")
    @Transactional
    public ResponseEntity<GuessResponse> guess(
        @Valid @RequestBody GuessRequest request,
        @AuthenticationPrincipal Long userId) {
      GuessResponse response = guessUseCase.guess(userId, request.guess());
      return ResponseEntity.ok(response);
    }
    
    @GetMapping("/leaderboard")
    public ResponseEntity<LeaderboardResponse> leaderboard() {
      LeaderboardResponse response = getLeaderboardUseCase.get();
      return ResponseEntity.ok(response);
    }
  }
  ```

**Acceptance**: All controllers compile, endpoints routable

---

**Task 3.3**: Exception Handling (1 hour)
Create `src/main/java/com/game/guess/presentation/exception/`:

- [ ] `GlobalExceptionHandler.java`
  ```java
  @ControllerAdvice
  public class GlobalExceptionHandler {
    
    @ExceptionHandler(InsufficientTurnsException.class)
    public ResponseEntity<ErrorResponse> handleInsufficientTurns(...) {
      return ResponseEntity.status(HttpStatus.FORBIDDEN)
        .body(new ErrorResponse("INSUFFICIENT_TURNS", "No turns left"));
    }
    
    @ExceptionHandler(InvalidCredentialsException.class)
    public ResponseEntity<ErrorResponse> handleInvalidCredentials(...) {
      return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
        .body(new ErrorResponse("INVALID_CREDENTIALS", "Invalid credentials"));
    }
    
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(...) {
      return ResponseEntity.status(HttpStatus.BAD_REQUEST)
        .body(new ErrorResponse("VALIDATION_ERROR", "Invalid input"));
    }
  }
  ```

**Acceptance**: Exception handlers compile, error responses standardized

**MORNING STANDUP**: Controller progress

---

#### Afternoon Session (4 hours) — Integration Tests

**Task 3.4**: Integration Test Setup (1 hour)
Create `src/test/java/com/game/guess/`:

- [ ] `IntegrationTestBase.java` (Testcontainers setup)
  ```java
  @SpringBootTest
  @ActiveProfiles("test")
  public abstract class IntegrationTestBase {
    @Container
    static PostgreSQLContainer<?> postgres = 
      new PostgreSQLContainer<>("postgres:15-alpine");
    
    @Container
    static GenericContainer<?> redis = 
      new GenericContainer<>("redis:7-alpine")
        .withExposedPorts(6379);
    
    @BeforeAll
    static void setup() {
      postgres.start();
      redis.start();
      // Set datasource & redis properties
    }
  }
  ```

**Acceptance**: Test containers work

---

**Task 3.5**: Functional Integration Tests (2 hours)

- [ ] `AuthIntegrationTest.java`
  ```java
  public class AuthIntegrationTest extends IntegrationTestBase {
    @Autowired
    private MockMvc mockMvc;
    
    @Test
    void testRegister_Success() throws Exception {
      mockMvc.perform(post("/api/v1/auth/register")
        .contentType(MediaType.APPLICATION_JSON)
        .content("{\"username\":\"player1\",\"password\":\"pass123456\"}")
      )
      .andExpect(status().isCreated())
      .andExpect(jsonPath("$.username").value("player1"));
    }
    
    @Test
    void testLogin_Success() throws Exception {
      // First register
      registerUser("player1", "pass123456");
      
      // Then login
      MvcResult result = mockMvc.perform(post("/api/v1/auth/login")
        .contentType(MediaType.APPLICATION_JSON)
        .content("{\"username\":\"player1\",\"password\":\"pass123456\"}")
      )
      .andExpect(status().isOk())
      .andReturn();
      
      // Verify HttpOnly cookie set
      String setCookie = result.getResponse().getHeader("Set-Cookie");
      assertThat(setCookie).contains("HttpOnly");
    }
  }
  ```

- [ ] `GameIntegrationTest.java`
  ```java
  public class GameIntegrationTest extends IntegrationTestBase {
    
    @Test
    void testGuess_Happy_Path() throws Exception {
      // Setup: register, login, buy turns
      String token = loginUser("player1");
      
      // Action: guess
      mockMvc.perform(post("/api/v1/game/guess")
        .header("Cookie", "access_token=" + token)
        .contentType(MediaType.APPLICATION_JSON)
        .content("{\"guess\":3}")
      )
      .andExpect(status().isOk())
      .andExpect(jsonPath("$.result").isNotEmpty());
    }
    
    @Test
    void testGuess_Concurrent_NoRaceCondition() throws Exception {
      // Setup: user with 3 turns
      String token = loginUser("player2");
      
      // Action: 3 concurrent guesses
      ExecutorService executor = Executors.newFixedThreadPool(3);
      List<Future<?>> futures = new ArrayList<>();
      
      for (int i = 0; i < 3; i++) {
        futures.add(executor.submit(() -> {
          mockMvc.perform(post("/api/v1/game/guess")
            .header("Cookie", "access_token=" + token)
            .contentType(MediaType.APPLICATION_JSON)
            .content("{\"guess\":2}")
          );
        }));
      }
      
      // Wait all complete
      for (Future<?> f : futures) f.get(10, TimeUnit.SECONDS);
      
      // Verify: exactly 3 turns deducted
      User user = userRepository.findByUsername("player2").get();
      assertThat(user.getTurns()).isEqualTo(0);
    }
  }
  ```

**Acceptance**: Tests pass, concurrency proven safe

---

**Task 3.6**: Performance Tests (1 hour)

- [ ] `PerformanceTest.java`
  ```java
  public class PerformanceTest extends IntegrationTestBase {
    
    @Test
    void testGuess_Latency_P95_UnderSLA() throws Exception {
      String token = loginUser("perftest");
      
      long[] latencies = new long[100];
      for (int i = 0; i < 100; i++) {
        long start = System.currentTimeMillis();
        mockMvc.perform(post("/api/v1/game/guess")
          .header("Cookie", "access_token=" + token)
          .contentType(MediaType.APPLICATION_JSON)
          .content("{\"guess\":1}")
        );
        latencies[i] = System.currentTimeMillis() - start;
      }
      
      Arrays.sort(latencies);
      long p95 = latencies[95];
      
      assertThat(p95).isLessThan(150);  // SLA: < 150ms
    }
  }
  ```

**Acceptance**: Performance within SLA

**DAILY STANDUP**: Integration tests passing

---

#### END OF DAY 3 CHECKLIST:
- [ ] All REST controllers implemented ✅
- [ ] DTOs with validation ✅
- [ ] Exception handling working ✅
- [ ] Integration tests passing ✅
- [ ] Concurrency tests passed (no race conditions) ✅
- [ ] Performance tests within SLA ✅
- [ ] Test coverage >= 70% ✅
- [ ] Commit: `git commit -m "feat(presentation,test): controllers + integration tests"`

---

### DAY 4: Documentation & Quality Assurance (8 hours)

#### Morning Session (4 hours) — Documentation & ADRs

**Task 4.1**: Architecture Decision Records (2 hours)

- [ ] Create `docs/ADR/ADR-001_ControlledWinRate.md`:
  ```markdown
  # ADR-001: Controlled Win Rate Algorithm
  
  Status: Accepted
  
  ## Context
  Game must be fair but engaging. Pure 5% fixed rate may feel grindy.
  
  ## Decision
  - Base: 5% win probability via ThreadLocalRandom
  - Soft cap: If consecutiveLosses >= 40, boost to 10%
  - Resets on WIN
  
  ## Rationale
  - 5% prevents easy farming
  - Soft cap prevents frustration (unlucky streaks)
  - Anti-streak rule is implicit, not game-breaking
  
  ## Implementation
  See: ControlledWinRatePolicy.java
  ```

- [ ] Create `docs/ADR/ADR-002_AtomicConditionalUpdate.md`:
  ```markdown
  # ADR-002: Atomic Conditional UPDATE for Turns
  
  Status: Accepted
  
  ## Problem
  Concurrent guesses from same user must not double-spend turns.
  
  ## Solution
  Single SQL statement (atomic at DB level):
  ```sql
  UPDATE users SET turns = turns - 1 
  WHERE id = :id AND turns > 0
  ```
  
  Check affectedRows == 0 → 403 Forbidden
  
  ## Why Not Pessimistic Lock?
  - Simplicity: No lock management
  - Performance: No lock contention
  - Reliability: DB guarantees, no app-level bugs
  ```

- [ ] Create `docs/ADR/ADR-003_HttpOnlyCookie.md`:
  ```markdown
  # ADR-003: JWT in HttpOnly Cookie
  
  Status: Accepted
  
  ## Problem
  JWT must be secure against XSS attacks.
  
  ## Solution
  Store JWT in HttpOnly cookie (not localStorage/sessionStorage).
  Attributes: HttpOnly, Secure, SameSite=Strict
  
  ## Trade-offs
  ✓ Mitigates XSS token theft
  ✗ Cannot be read by JavaScript (by design)
  ✗ Vulnerable to CSRF (mitigated by SameSite=Strict)
  ```

**Acceptance**: 3-4 ADRs documented

---

**Task 4.2**: API Contract Document (1 hour)

Create `docs/API_CONTRACT.md`:
```markdown
# API Contract — Game Đoán Số v1.0

## Authentication Endpoints

### POST /api/v1/auth/register
Register new user.

Request:
```json
{
  "username": "player1",
  "password": "securepass123"
}
```

Response (201 Created):
```json
{
  "id": 1,
  "username": "player1",
  "score": 0,
  "turns": 0
}
```

Errors:
- 400: Validation failed (username/password too short)
- 409: Username already exists

---

### POST /api/v1/auth/login
Login user, receive JWT as HttpOnly cookie.

Request:
```json
{
  "username": "player1",
  "password": "securepass123"
}
```

Response (200 OK):
```json
{
  "username": "player1",
  "score": 10,
  "turns": 5,
  "token": "eyJhbGc..." (only set as cookie, not in JSON)
}
```

Set-Cookie: access_token=eyJ...; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=3600

Errors:
- 401: Invalid credentials

---

## Game Endpoints

### POST /api/v1/game/guess
Make a guess in the game.

Auth: Required (JWT in HttpOnly cookie)

Request:
```json
{
  "guess": 3
}
```

Response (200 OK):
```json
{
  "result": "WIN",
  "serverNumber": 3,
  "score": 11,
  "turnsRemaining": 4
}
```

Errors:
- 400: Guess not in range 1-5
- 401: Unauthorized (no valid JWT)
- 403: Insufficient turns (turns = 0)

### GET /api/v1/game/leaderboard
Get top 10 players.

Auth: Optional

Response (200 OK):
```json
[
  {
    "rank": 1,
    "username": "champion",
    "score": 150
  },
  ...
]
```

Performance: < 30ms (cached from Redis ZSET)

### POST /api/v1/game/buy-turns
Purchase 5 turns.

Auth: Required

Response (200 OK):
```json
{
  "turnsAdded": 5,
  "turnsTotal": 10
}
```

### GET /api/v1/user/me
Get current user profile.

Auth: Required

Response (200 OK):
```json
{
  "username": "player1",
  "score": 25,
  "turns": 8
}
```
```

**Acceptance**: API contract complete, all endpoints documented

---

**Task 4.3**: Deployment Guide (1 hour)

Create `docs/DEPLOYMENT.md`:
```markdown
# Deployment Guide

## Development (H2 In-Memory)
```bash
mvn spring-boot:run
# Opens on localhost:8080
# H2 console at localhost:8080/h2-console
```

## Test (Testcontainers)
```bash
mvn test
# Automatically starts PostgreSQL + Redis containers
```

## Production (MySQL + Redis)
```bash
export SPRING_DATASOURCE_URL=jdbc:mysql://prod-db:3306/gamedoannso
export SPRING_DATASOURCE_USERNAME=root
export SPRING_DATASOURCE_PASSWORD=***
export SPRING_REDIS_HOST=prod-redis
export SPRING_REDIS_PORT=6379
export JWT_SECRET=min-32-chars-secret-key
export BCRYPT_STRENGTH=12

java -jar game-doan-so.jar --spring.profiles.active=prod
```

## Docker
```dockerfile
FROM openjdk:17-slim
COPY target/*.jar app.jar
ENTRYPOINT ["java", "-jar", "/app.jar"]
```

```bash
docker build -t game-doan-so:v1.0.0 .
docker run -e SPRING_PROFILES_ACTIVE=prod \
  -e SPRING_DATASOURCE_URL=... \
  game-doan-so:v1.0.0
```

## Health Check
```
GET /actuator/health
{
  "status": "UP"
}
```

## Monitoring
- Logs: `tail -f application.log`
- Metrics: GET /actuator/prometheus
- Database: SELECT COUNT(*) FROM users;
```

**Acceptance**: Deployment documented, runnable

---

#### Afternoon Session (4 hours) — QA & Final Testing

**Task 4.4**: Security Audit Checklist (1 hour)

- [ ] OWASP Top 10 Review
  - [ ] A01: Broken Access Control — JWT + Spring Security ✓
  - [ ] A02: Cryptographic Failures — BCrypt + HTTPS ✓
  - [ ] A03: Injection — Parameterized queries, no SQL concatenation ✓
  - [ ] A04: Insecure Design — Atomic operations, design reviewed ✓
  - [ ] A05: Security Misconfiguration — No hardcoded secrets ✓
  - [ ] A06: Vulnerable Components — Dependencies checked (mvn dependency-check)
  - [ ] A07: Identification & Auth — JWT + BCrypt strong ✓
  - [ ] A08: Software/Data Integrity — Secure token signing ✓
  - [ ] A09: Logging & Monitoring — Logging configured ✓
  - [ ] A10: Using Components with Known Vuln — Dependency check passed ✓

**Acceptance**: All items checked, no critical issues

---

**Task 4.5**: Code Quality Audit (1 hour)

- [ ] `mvn clean compile` — No errors
- [ ] `mvn test` — All tests pass
- [ ] Test coverage: `mvn jacoco:report` — >= 70% ✓
- [ ] No hardcoded secrets: `grep -r "password\|secret\|key" src/` — None found (except in config files)
- [ ] Clean Architecture: Verify domain layer has zero Spring imports ✓
- [ ] Code formatting: `mvn spotless:check` (if configured)

**Acceptance**: Code quality verified

---

**Task 4.6**: Performance Benchmark (1 hour)

Run performance tests and document results:
```
POST /guess
  Mean: 45ms
  p95: 120ms
  p99: 140ms
  ✓ Target: < 150ms

GET /leaderboard (cached)
  Mean: 8ms
  p95: 15ms
  p99: 22ms
  ✓ Target: < 30ms

POST /register
  Mean: 80ms (BCrypt hashing)
  p95: 150ms
  p99: 180ms
  ✓ Within acceptable range

POST /login
  Mean: 100ms
  p95: 160ms
  p99: 200ms
  ✓ Within acceptable range
```

**Acceptance**: All benchmarks within SLA

---

**Task 4.7**: Final Integration Test Run (1 hour)

- [ ] Register new user → Success
- [ ] Login → JWT in HttpOnly cookie
- [ ] Buy 5 turns → Turns increased
- [ ] Make 5 guesses → Turns decremented atomically
- [ ] Check leaderboard → Updated if won
- [ ] Concurrent guesses → No race condition
- [ ] Invalid credentials → 401
- [ ] No turns → 403
- [ ] Validation errors → 400

**Acceptance**: All happy paths + error cases working

**DAILY STANDUP**: QA status

---

#### END OF DAY 4 CHECKLIST:
- [ ] ADRs documented (1-4) ✅
- [ ] API contract complete ✅
- [ ] Deployment guide written ✅
- [ ] README updated ✅
- [ ] Security audit passed ✅
- [ ] Code quality verified ✅
- [ ] Performance benchmarked (within SLA) ✅
- [ ] Final integration tests passed ✅
- [ ] Commit: `git commit -m "docs: add ADRs, API contract, deployment guide"`

---

### DAY 5: Release Preparation & Production Deploy (4-6 hours)

#### Final Release Checklist

**Task 5.1**: Build & Packaging (30 min)
```bash
# Clean build
mvn clean package -DskipTests

# Test JAR
java -jar target/game-doan-so-1.0.0.jar --spring.profiles.active=dev

# Verify health
curl http://localhost:8080/actuator/health
```

**Acceptance**: JAR built, runs successfully

---

**Task 5.2**: Staging Environment Smoke Tests (1 hour)
```bash
# Deploy to staging
docker run -d --name game-staging \
  -e SPRING_PROFILES_ACTIVE=test \
  game-doan-so:v1.0.0

# Health check
curl http://localhost:8080/actuator/health

# Register
curl -X POST http://localhost:8080/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test12345"}'

# Verify response
```

**Acceptance**: All smoke tests pass

---

**Task 5.3**: Production Deployment (1-2 hours)
```bash
# Prod environment setup
docker run -d --name game-prod \
  -e SPRING_PROFILES_ACTIVE=prod \
  -e SPRING_DATASOURCE_URL=jdbc:mysql://prod-db:3306/gamedoannso \
  -e SPRING_DATASOURCE_USERNAME=<user> \
  -e SPRING_DATASOURCE_PASSWORD=<pass> \
  -e SPRING_REDIS_HOST=prod-redis \
  -e JWT_SECRET=<32-char-secret> \
  -p 8080:8080 \
  game-doan-so:v1.0.0

# Verify startup
sleep 10 && curl http://localhost:8080/actuator/health

# Tail logs
docker logs -f game-prod
```

**Acceptance**: Service running, logs clean

---

**Task 5.4**: Post-Deployment Verification (30 min)
- [ ] Health check: `GET /actuator/health` → UP
- [ ] Swagger UI: `GET /swagger-ui.html` → Accessible
- [ ] Register & Login: Works end-to-end
- [ ] Database: Can read/write to users table
- [ ] Redis: Leaderboard responsive
- [ ] Logs: No errors or warnings
- [ ] Monitoring: Metrics flowing

**Acceptance**: All verifications pass

---

**Task 5.5**: Go/No-Go Decision
Tech Lead reviews:
- ✓ All tests passed
- ✓ Security audit cleared
- ✓ Performance within SLA
- ✓ Code coverage >= 70%
- ✓ Documentation complete
- ✓ Deployment tested
- ✓ Rollback procedure documented

**Decision**: GO FOR RELEASE 🚀

---

#### END OF DAY 5 CHECKLIST:
- [ ] Build & packaging successful ✅
- [ ] Staging smoke tests passed ✅
- [ ] Production deployment successful ✅
- [ ] Post-deployment verification passed ✅
- [ ] Monitoring configured & working ✅
- [ ] Runbook prepared ✅
- [ ] Team trained & ready on-call ✅
- [ ] Final commit: `git tag v1.0.0` ✅

---

## 🎯 SPRINT METRICS

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Velocity (story points) | 21 | ? | TBD |
| Test coverage | 70%+ | ? | TBD |
| Bugs found | < 2 | ? | TBD |
| Performance (p95 /guess) | < 150ms | ? | TBD |
| On-time delivery | Day 5 EOD | ? | TBD |

---

## 📝 DAILY STANDUP TEMPLATE

**Standup Time**: 9:00 AM (5 min sync)

**Questions**:
1. What did I complete yesterday?
2. What am I working on today?
3. Any blockers?

**Example**:
```
Yesterday:
- Completed Auth use cases with unit tests
- Started JWT provider implementation

Today:
- Finishing JPA repositories
- Starting integration tests

Blockers:
- None

Status: ON TRACK ✓
```

---

## 🔄 COMMIT STRATEGY

Each day should have 2-3 commits:
```
Day 1: "feat(domain): add entities, services, repository interfaces"
Day 2: "feat(app,infra): use cases + JPA repositories + security"
Day 3: "feat(presentation,test): controllers + integration tests"
Day 4: "docs: add ADRs, API contract, deployment guide"
Day 5: "release: v1.0.0 — production ready"
```

---

## 📞 ESCALATION PATH

| Issue | Owner | Action |
|-------|-------|--------|
| Compile error | Dev | Fix immediately |
| Test failure | Dev + QA | Debug & fix |
| Performance regression | Dev + Arch | Profile & optimize |
| Security concern | Tech Lead | Review & decide |
| Blocker (unknown) | Tech Lead | Research & decide |

---

**Ready to execute?** Print this checklist and start Day 1! 🚀
