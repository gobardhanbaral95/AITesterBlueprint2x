# Test Plan – VWO Login Dashboard  
**Jira Ticket:** VWO-25  
**Prepared By:** QA Architecture Team  
**Date:** 2026‑03‑28  

---  

## 1. Objectives
- Verify that the VWO login dashboard meets all functional requirements outlined in the PRD.  
- Ensure secure, reliable, and user‑friendly authentication flow for both new and returning users.  
- Validate that error handling, real‑time field validation, password‑management, and accessibility features work as intended.  
- Confirm that optional features (2FA, SSO, social login) are correctly integrated and do not impact the core login experience.  

## 2. Scope  
| In‑Scope | Out‑of‑Scope |
|----------|--------------|
| • Email & password login (including “Remember Me”).<br>• Real‑time input validation, password strength indicator.<br>• Forgot‑Password / Reset flow.<br>• Multi‑Factor Authentication (2FA) – OTP via email/SMS.<br>• Enterprise SSO (SAML/OAuth) integration points.<br>• Social login (Google, Microsoft).<br>• UI/UX elements: auto‑focus, clickable labels, loading states, light/dark themes.<br>• Accessibility: ARIA labels, keyboard navigation, high‑contrast mode.<br>• Session handling (timeout, secure cookies). | • Backend authentication service performance/load testing.<br>• CDN, asset optimization, network latency tests.<br>• Full GDPR/CCPA compliance audits.<br>• Non‑functional scalability & high‑availability tests.<br>• Future enhancements (biometric, adaptive auth). |

## 3. Test Strategy  
| Test Type | Description | Tools / Resources |
|-----------|-------------|-------------------|
| **Functional UI Testing** | Verify all UI components, field validation, navigation, and visual themes. | Selenium WebDriver, Cypress, Playwright, BrowserStack (cross‑browser). |
| **Authentication Flow Testing** | End‑to‑end verification of login, logout, session expiration, “Remember Me”, 2FA, SSO, social login. | Test accounts (admin, regular, SSO‑enabled), OTP generator/mock service. |
| **Negative & Edge‑Case Testing** | Invalid credentials, malformed emails, weak passwords, expired reset tokens, rate‑limit enforcement. | Custom scripts, Postman for API token validation. |
| **Accessibility Testing** | WCAG 2.1 AA compliance checks – screen reader, keyboard navigation, high‑contrast mode. | axe‑core, WAVE, NVDA/JAWS. |
| **Security‑Related Functional Tests** | Verify HTTPS enforcement, secure cookie flags, proper error messages (no info leakage), lockout after repeated failures. | OWASP ZAP, Burp Suite (passive scans). |
| **Regression Smoke** | Quick sanity run on each build to ensure core login path remains functional. | Cypress CI pipeline. |
| **Data‑Driven Validation** | Use data tables to cover combinations of valid/invalid inputs, password strengths, and locale variations. | CSV/Excel data sources integrated with test framework. |

### Test Levels & Environments
- **Development (DEV)** – Unit & component level checks, mock services.  
- **Staging (STG)** – Integrated functional testing with real authentication services, SSO mock endpoints.  
- **Production‑like (PRE‑PROD)** – Final acceptance testing with production configuration (HTTPS, secure cookies).  

## 4. Entry & Exit Criteria  

### Entry Criteria
| # | Condition |
|---|-----------|
| 1 | PRD signed off and all functional requirements traceable to test cases. |
| 2 | Test environment (STG) provisioned with required services (auth API, SSO mock, social‑login sandbox). |
| 3 | Test data set (valid/invalid credentials, OTP, SSO federation metadata) created and reviewed. |
| 4 | Test automation framework installed & baseline smoke suite passed. |
| 5 | Accessibility testing tools configured. |

### Exit Criteria
| # | Condition |
|---|-----------|
| 1 | **≥ 95 %** of total test cases executed. |
| 2 | No **Critical** or **High** severity defects open (must be fixed or deferred with justification). |
| 3 | All **Medium** severity defects either resolved or accepted with mitigation plan. |
| 4 | Regression smoke passes on the latest build. |
| 5 | Test Summary Report signed off by Product Owner & QA Lead. |
| 6 | Test artifacts (scripts, logs, evidence) archived per release governance. |

## 5. Test Cases  

> Test IDs follow the pattern **VWO‑TC‑<Module>-<Seq>**  

### 5.1 Authentication – Core Login  

| ID | Title | Preconditions | Steps | Expected Result |
|----|-------|---------------|-------|-----------------|
| VWO‑TC‑AUTH‑001 | Successful login with valid credentials | Valid user account (email/password) created. “Remember Me” unchecked. | 1. Navigate to `https://app.vwo.com`.<br>2. Verify email field is auto‑focused.<br>3. Enter valid email.<br>4. Enter valid password.<br>5. Click **Log In**.<br>6. Observe loading spinner.<br>7. Dashboard loads. | User is redirected to VWO dashboard; session cookie set with `Secure` & `HttpOnly`; no “Remember Me” persistence after browser close. |
| VWO‑TC‑AUTH‑002 | Login with “Remember Me” enabled | Same as above, but checkbox selected. | Steps 1‑5 as above, then close and reopen browser, navigate to login URL. | User remains logged in; session persisted via persistent cookie; dashboard loads without re‑authentication. |
| VWO‑TC‑AUTH‑003 | Invalid email format validation (blur) | None. | 1. Focus email field.<br>2. Enter `invalid-email` and tab out. | Inline validation message displayed: “Please enter a valid email address.” Field highlighted in error state. |
| VWO‑TC‑AUTH‑004 | Password strength indicator – weak password | None. | 1. Focus password field.<br>2. Type `abc123`.<br>3. Observe strength meter. | Strength indicator shows **Weak** with tooltip describing requirements. |
| VWO‑TC‑AUTH‑005 | Password strength indicator – strong password | None. | 1. Enter a password meeting all criteria (e.g., `Vw0$Secure!2025`). | Indicator shows **Strong** (green) and no tooltip warning. |
| VWO‑TC‑AUTH‑006 | Failed login – incorrect password | Valid email, wrong password. | 1. Enter valid email.<br>2. Enter wrong password.<br>3. Click **Log In**. | Error banner displayed: “Incorrect email or password.” No session cookie created. |
| VWO‑TC‑AUTH‑007 | Account lockout after 5 consecutive failures | Valid email. | Repeat steps of invalid password 5 times. | After 5th attempt, account is locked; message: “Your account has been locked. Contact support.” Subsequent attempts blocked. |
| VWO‑TC‑AUTH‑008 | OTP 2FA – successful flow | User with 2FA enabled; valid email/password. | 1. Complete primary login (valid credentials).<br>2. OTP entry screen appears.<br>3. Enter correct OTP received via email/SMS.<br>4. Submit. | Dashboard loads; session marked as 2FA‑verified. |
| VWO‑TC‑AUTH‑009 | OTP 2FA – invalid OTP | Same as above but OTP is wrong. | Enter wrong OTP and submit. | Error message: “Invalid verification code.” User remains on OTP screen; can retry up to 3 attempts. |
| VWO‑TC‑AUTH‑010 | SSO – successful SAML login | SSO‑enabled test identity provider (IdP) configured. | 1. Click **Enterprise SSO** button.<br>2. Select test IdP.<br>3. Authenticate at IdP (enter credentials).<br>4. Return to VWO. | User redirected to dashboard; SSO session cookie present; no password prompt on VWO side. |
| VWO‑TC‑AUTH‑011 | SSO – IdP authentication failure | Same as above but wrong IdP credentials. | Attempt SSO login with invalid IdP credentials. | Error displayed on IdP page; VWO shows generic “Authentication failed” message after redirect. |
| VWO‑TC‑AUTH‑012 | Social login – Google – success | Google test account provisioned. | 1. Click **Login with Google**.<br>2. Complete Google consent screen.<br>3. Allow access. | User returned to VWO dashboard; new VWO account linked/created automatically. |
| VWO‑TC‑AUTH‑013 | Social login – Microsoft – failure (user denies consent) | Microsoft test account. | Click **Login with Microsoft**, then click **Deny** on consent screen. | VWO displays “Microsoft authentication was cancelled.” No session created. |

### 5.2 Password Management  

| ID | Title | Preconditions | Steps | Expected Result |
|----|-------|---------------|-------|-----------------|
| VWO‑TC‑PWD‑001 | Navigate to “Forgot Password” link | None. | 1. Click **Forgot Password?** link on login page. | Password‑reset page loads with email input and **Send Reset Link** button. |
| VWO‑TC‑PWD‑002 | Request reset with registered email | User exists with email `user@example.com`. | Enter registered email → Submit. | Confirmation message: “If the email exists, a reset link has been sent.” Token generated (verified via DB). |
| VWO‑TC‑PWD‑003 | Request reset with unregistered email | Email not in system. | Same as above. | Same generic confirmation (no info leakage). No token created. |
| VWO‑TC‑PWD‑004 | Reset link – valid token | Reset email received with link containing valid token (expires in 30 min). | Click link → New password form appears. | Form loads; token validated server‑side. |
| VWO‑TC‑PWD‑005 | Reset link – expired token | Token generated >30 min ago. | Click link. | Error page: “Reset link has expired. Request a new one.” |
| VWO‑TC‑PWD‑006 | Password reset – weak new password | Valid token. | Enter weak password (`12345`) → Submit. | Inline validation: “Password does not meet complexity requirements.” |
| VWO‑TC‑PWD‑007 | Password reset – strong new password | Valid token. | Enter strong password (`Vw0$NewPass!2025`) → Submit. | Success message: “Your password has been reset.” User can log in with new password. |
| VWO‑TC‑PWD‑008 | Reset flow – mismatched confirm password | Valid token. | Enter new password and a different confirmation password. | Error: “Passwords do not match.” |

### 5.3 UI/UX & Accessibility  

| ID | Title | Preconditions | Steps | Expected Result |
|----|-------|---------------|-------|-----------------|
| VWO‑TC‑UI‑001 | Light/Dark theme toggle | None. | 1. Observe banner with theme toggle.<br>2. Switch to Dark Mode.<br>3. Refresh page. | UI persists in selected theme; colors meet contrast ratios (≥ 4.5:1). |
| VWO‑TC‑UI‑002 | Clickable label focus | None. | Click on **Email** label. | Cursor moves to email input field. |
| VWO‑TC‑UI‑003 | Loading spinner visibility | Enter valid credentials, network throttled (e.g., 2 s latency). | Click **Log In**. | Spinner appears immediately and stays until dashboard loads. |
| VWO‑TC‑UI‑004 | Keyboard navigation – full flow | None. | Use **Tab** to navigate: email → password → Remember Me → Log In → (if 2FA) OTP → Submit. | All controls reachable; focus outline visible; no mouse required. |
| VWO‑TC‑UI‑005 | Screen reader – ARIA labels | NVDA or VoiceOver active. | Navigate to email field. | Screen reader reads “Email address, edit text, required”. |
| VWO‑TC‑UI‑006 | High‑contrast mode activation | None. | Enable high‑contrast via OS settings or UI toggle. | All UI elements remain discernible; contrast ≥ 7:1. |
| VWO‑TC‑UI‑007 | Responsive layout – mobile viewport (375 px) | Browser set to mobile size. | Load login page. | Form fields stack vertically; touch targets ≥ 44 px; auto‑focus works. |
| VWO‑TC‑UI‑008 | Clickable “Create Free Trial” link | None. | Click the link. | User redirected to registration page; URL `https://app.vwo.com/signup`. |

### 5.4 Security‑Related Functional Tests  

| ID | Title | Preconditions | Steps | Expected Result |
|----|-------|---------------|-------|-----------------|
| VWO‑SEC‑001 | HTTPS enforcement | Access via http://app.vwo.com. | Attempt to load page. | Automatic redirect to `https://` (301). |
| VWO‑SEC‑002 | Secure cookie flags | Successful login. | Inspect cookies via browser dev tools. | Cookies have `Secure`, `HttpOnly`, and `