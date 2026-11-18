# Working with the ERP blueprint

Use this repository as the functional specification for ERP design, implementation and analysis. Start with the [business workflows](README.md). Follow their internal links to the owning records, service contracts, settings, calculations and worked examples. Explain a result in terms of the actor, operation, affected records and observable outcome.

When an outcome depends on an installation choice, identify the setting or grant and describe the applicable branches. When evidence belongs to another party, name the record that establishes the outcome, such as a bank settlement or a filing acknowledgment. The [coverage guide](docs/coverage/checkpoint.md) identifies the scope of each catalogue and where those decisions are documented.

When revising a rule, update the owning functional chapter and its dependent examples so they describe the current behaviour in the present tense. Preserve the field names, relationships and calculations a reader needs to implement it. Keep all reading paths within the blueprint.
