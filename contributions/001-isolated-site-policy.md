# Contribution 001 — Isolated-site service: policy expiry and dependency failure

**Actual local HTTP experiment, 24 November 2026.** A site can continue bounded work with a current local policy while central connectivity is unavailable. Local availability cannot silently turn an expired, missing or revoked policy into authority.

## Service contract

The [loopback service](../tools/site_service.py) exposes one synthetic case-A document. A preconfigured local bundle has a permission epoch and expiry. It admits only the recognised case-A actor and fails closed when the bundle is missing, expired, invalid or different from the locally required epoch. A restored older policy must reconcile the required epoch before serving.

The actor header is an explicitly synthetic identity adapter, not authenticated enterprise identity. The time and epoch inputs are fixture state, not signed production policy or measured clock trust. The service binds only to `127.0.0.1` inside the isolated verification container; it is not a remotely exposed bank API.

## What was actually exercised

The experiment performs seven HTTP exchanges: valid local access, cross-case denial, missing policy, expiry, required-epoch revocation, an older restored bundle and an unknown actor. Responses include 200, 403 and 503 with bounded JSON results. [Observed evidence](../evidence/results.json) records each exchange. Regression tests also exercise the decision boundary.

Final verification uses a read-only workspace and `--network none`. The [network observation](../evidence/verification.json) records loopback-only interfaces and an unreachable reserved external IP. This is tool-runtime isolation, not a physical air-gap assurance or a cloud-provider test. Central unavailability is represented by the synthetic scenario; no live provider dependency is shut down.

## Architecture interpretation

Define which local operations may continue and which require current central authority. Keep local identity, key access, DNS/time, policy distribution and recovery dependencies explicit. A locally running workload may still rely on a regional provider service; do not infer autonomous operation from physical placement alone. The broader [sovereign/disconnected cloud reference](https://github.com/cybersmeashish/sovereign-disconnected-cloud-security) holds those architecture decisions.

Treat restored policy as historical state until revocations/current grants reconcile. If required freshness cannot be established, return an explicit unavailable/review condition. A reviewed emergency-access process is separate from silently extending ordinary grants. It needs a named decision owner, scope, expiry and evidence.

## Remaining assurance work

A real deployment must authenticate actors, verify signed policy admission, protect required epochs against rollback, establish local time uncertainty, secure keys and storage, exercise full restoration and measure actual workload/capacity. This contribution implements none of those enterprise integrations. Its value is a reproducible failure contract, actual isolated HTTP cases and visible gaps.

Next experiments should test policy import authenticity, loss of the revocation ledger, clock uncertainty and clean restoration across separate services. Keep synthetic outcomes distinct from provider capabilities and contractual/regulatory claims.
