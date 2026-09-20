---
title: Learn together while data stays local
slug: learning-with-local-data
summary: Follow the boundary between shared coordination in the Console and local execution in Agent Studio.
category: Workflow
status: draft
sample: true
reading_time: 2 min read
---

This sample article explains the division of work described in the FedOps 1.3 manual. It is a content preview for the proposed website.

## Coordinate on the web

The **Console** is the place to manage Federated Tasks, publish Releases, review participation requests, and configure Campaigns. The **Registry** helps participants find published Tasks and their model versions.

These shared services coordinate the workflow. The training dataset is prepared in each participant's local environment.

## Prepare in Agent Studio

After a participation request is approved, a participant opens the published Task in Agent Studio, prepares its Python environment, and connects the required data folder.

**Participation Readiness** checks local preparation. Server availability is a separate condition: the local environment can be ready while the FL Server is still offline.

When participation is ready and the server is live, the participant can start the FL Client. The client receives a model, trains and evaluates locally, and sends model updates for aggregation.

## Keep the boundary visible

The raw training dataset is not uploaded to FedOps Web. Agent Studio shows the participant's own client metrics and participation history. The web interface shows the broader monitoring information allowed by the owner's permissions.

This separation helps explain the two interfaces: use the Console to coordinate a shared Task and Agent Studio to execute work with local code and data.

- [Browse the Registry preview](http://127.0.0.1:4314/fedops/registry)
- [Read Participant: Join & FL](https://gachon-cclab.github.io/fedops-docs-1.3/v1.3/participant/)
- [Open the documentation hub](/document/)
