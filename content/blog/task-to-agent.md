---
title: From a Federated Task to an Agent
slug: task-to-agent
summary: Understand how Tasks, Releases, Campaigns, and Model Versions connect in the FedOps 1.3 lifecycle.
category: Concepts
status: draft
sample: true
reading_time: 3 min read
---

This sample article introduces the lifecycle described in the FedOps 1.3 manual. It is a content preview for the proposed website.

## Start with a Task

A **Federated Task** describes a shared learning objective. An owner can create a draft in the Console, then open it in Agent Studio to connect code, a Python environment, and local data.

The draft is not yet a public Registry entry. After local training and Release Readiness checks, the owner submits a Release Candidate and publishes it from the web interface.

## Publish a Release, run a Campaign

A **Release** gives participants the published task configuration they can use. The Registry helps them discover a Task and request participation.

A **Campaign** defines the federated training policy, including rounds, clients per round, and the aggregation strategy. Approved participants prepare their local environments before starting their clients.

The FL Server coordinates rounds and aggregates model updates. The completed result becomes a new **Global Model Version**, with a relationship to its source Task and training run.

## Use a version in an Agent

Agent Studio lets users select available model versions when building an Agent. A build keeps its selected versions fixed. A newly trained Global Model does not silently replace the model in an existing build.

To improve a component, return to its source Federated Task, train a new version, and validate a new Agent build.

- [Explore My Federated Tasks](http://127.0.0.1:4314/fedops/task)
- [Read the FedOps 1.3 overview](https://gachon-cclab.github.io/fedops-docs-1.3/)
- [Follow the Agent Builder manual](https://gachon-cclab.github.io/fedops-docs-1.3/v1.3/agent-builder/)
