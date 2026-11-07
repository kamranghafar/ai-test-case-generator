# Example: Generated Test Cases (Markdown)

This is a sample output from `ai-testgen generate`.

---

# Password Reset Feature Tests

**Requirement:** User should be able to reset their password via email  
**Generated:** 2024-01-15T10:30:00  
**Model:** gpt-4  
**Total Test Cases:** 5

---

## TC-001: Verify successful password reset flow

**Type:** functional | **Priority:** critical | **Est. Duration:** 5 min

> Validate the complete happy-path flow for resetting a password via email.

### Preconditions

- User has an existing account with email user@example.com
- User is on the login page

### Steps

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Click "Forgot Password" link | Password reset form is displayed | — |
| 2 | Enter registered email address | Email field accepts input | user@example.com |
| 3 | Click "Send Reset Link" | Success message: "Reset link sent to your email" | — |
| 4 | Open email and click reset link | "Set New Password" page is displayed | — |
| 5 | Enter new password | Password field accepts input | NewP@ss123 |
| 6 | Confirm new password | Confirmation field accepts input | NewP@ss123 |
| 7 | Click "Reset Password" | Success message displayed, redirected to login | — |
| 8 | Log in with new password | Login successful, dashboard displayed | NewP@ss123 |

**Tags:** password-reset, happy-path, smoke

---

## TC-002: Verify password complexity validation

**Type:** negative | **Priority:** high | **Est. Duration:** 3 min

> Ensure the system rejects passwords that don't meet complexity requirements.

### Steps

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to password reset page | Reset form displayed | — |
| 2 | Enter password without uppercase | Error: "Must contain uppercase letter" | password1! |
| 3 | Enter password without number | Error: "Must contain a number" | Password!! |
| 4 | Enter password under 8 chars | Error: "Must be at least 8 characters" | Pa1! |
| 5 | Enter valid complex password | Password accepted | NewP@ss123 |

**Tags:** password-reset, validation, negative

---

## TC-003: Verify reset token expiration

**Type:** edge_case | **Priority:** high | **Est. Duration:** 3 min

> Ensure expired reset tokens are rejected after 24 hours.

### Steps

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Request password reset | Reset email sent | — |
| 2 | Wait 24+ hours (simulate) | Token should be expired | — |
| 3 | Click the reset link | Error: "This reset link has expired" | — |

**Tags:** password-reset, expiration, edge-case

---

## TC-004: Verify rate limiting on reset requests

**Type:** security | **Priority:** medium | **Est. Duration:** 2 min

> Ensure the system enforces rate limiting of 5 requests per hour.

### Steps

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send 5 password reset requests | All 5 emails sent successfully | — |
| 2 | Send 6th request within same hour | Error: "Too many requests. Try again later." | — |

**Tags:** password-reset, security, rate-limiting

---

## TC-005: Verify password history enforcement

**Type:** negative | **Priority:** medium | **Est. Duration:** 2 min

> Ensure users cannot reuse their last 3 passwords.

### Steps

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Reset password using previous password | Error: "Cannot reuse recent passwords" | OldP@ss1 |
| 2 | Reset with 2nd most recent password | Error: "Cannot reuse recent passwords" | OldP@ss2 |
| 3 | Reset with a brand new password | Password reset successful | BrandN3w! |

**Tags:** password-reset, password-history, negative

---
