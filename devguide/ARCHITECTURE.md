# Praxis Architecture

## Mission

Encode reusable, inspectable, versionable, and validated scientific know-how.

## Core concepts

### Capability

A semantic scientific ability: **WHAT** the platform knows how to do.

A Capability may describe identity/version, scientific intent, semantic input/output contracts, applicability/preconditions, available Protocols, validation status, limitations, maturity, and deprecation.

### Protocol

A reproducible implementation of a Capability: **HOW** the task is performed.

A Protocol may define prerequisites, tool/engine versions, parameters, steps, outputs, checks, provenance requirements, and resource/cost/fidelity characteristics.

Multiple Protocols may implement one Capability.

## Boundaries

Praxis owns methodological context. It does not own:

- molecular knowledge (Sabueso);
- DiscoveryProject state or project Evidence (Nextia);
- molecular modeling APIs (MolSysSuite);
- scientific reasoning/agency (MOLI Agent);
- certification by opaque AI judgment.

## Execution relationship

DiscoveryEngine may request a Capability and select/accept a Protocol under explicit policy. Protocols may orchestrate MolSysSuite and external engines.

Semantic abstraction must not prevent direct expert API access.

## Learning

Ad-hoc workflows may become formalized Protocols. Protocols may become associated with reusable Capabilities only after appropriate validation/generalization.

MOLI Agent may help propose or formalize methodology; it does not certify it.
