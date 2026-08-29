# RegTrace-AI gap report — Aurum Custody

- **Run ID:** `demo-aurum-001`
- **Project:** Aurum Custody (`aurum-custody`)
- **Frameworks:** MiCA, VARA
- **Generator:** deterministic (no uncited claims allowed)
- **Created:** 2026-08-29 17:30 UTC
- **Retrieved modules:** 18

## Licensing readiness

| Framework | Covered | Partial | Missing | Total |
|---|---:|---:|---:|---:|
| MiCA | 1 | 4 | 4 | 9 |
| VARA | 1 | 3 | 5 | 9 |

Every finding below is bound to a retrieved module locator.
Statuses: `grounded` (claim overlaps cited obligation),
`needs_human_verification` (partial evidence or weak overlap),
`unsupported` (failed citation validator).

## Findings (source-traced)

### MiCA · custody · `grounded`

- **Module:** `mica-custody-segregation`
- **Confidence:** 0.86 (retrieval 0.91)
- **Coverage:** covered
- **Citation:** [Title III Art. 75](https://eur-lex.europa.eu/eli/reg/2023/1114/oj)

The project pack appears to address MiCA Art. 75 (custody). Evidence aligned with the obligation to providers of custody and administration of crypto-assets on behalf of clients must establish a custody policy, maintain a register of positions, keep client crypto-assets segregated. Checklist items observed: written custody and administration policy; wallet inventory and position register; key-management and cold-wallet procedures. Pack excerpt: "Client virtual assets are never commingled with the firm's treasury. Each client is assigned a unique on-chain deposit address…"

### MiCA · custody · `grounded`

- **Module:** `mica-custody-safekeeping`
- **Confidence:** 0.81 (retrieval 0.84)
- **Coverage:** covered
- **Citation:** [Title V Art. 70](https://eur-lex.europa.eu/eli/reg/2023/1114/oj)

The pack describes client-asset segregation, a prohibition on rehypothecation, and a signed daily wallet inventory. Fiat placement with a credit institution is not evidenced. Pack excerpt: "The custody policy, titled Aurum Client Asset Segregation and Wallet Inventory Standard, is a 19-page controlled document."

### VARA · custody · `grounded`

- **Module:** `vara-custody-rulebook`
- **Confidence:** 0.84 (retrieval 0.88)
- **Coverage:** covered
- **Citation:** [Custody Services Rulebook Client VA Safekeeping — Segregation of Client Virtual Assets](https://www.vara.ae/en/rules-and-regulations/)

Wallet architecture (unique deposit addresses, 3-of-5 MPC, 2% hot-wallet cap, daily reconciliation) maps to the VARA Custody Services Rulebook segregation and key-management expectations. Cold-storage share is material. Independent key-ceremony vendor is named.

### MiCA · reserve · `grounded`

- **Module:** `mica-art-reserve`
- **Confidence:** 0.77 (retrieval 0.71)
- **Coverage:** missing
- **Citation:** [Title III Art. 36](https://eur-lex.europa.eu/eli/reg/2023/1114/oj)

Licensing gap against MiCA Art. 36: the pack does not evidence issuers of asset-referenced tokens must maintain a reserve of assets that matches the risks and composition of the referenced assets. Missing checklist items include: independent attestation or audit of reserve holdings; segregation of reserve from issuer operating funds; valuation methodology and frequency. The pack itself flags a founder-prepared spreadsheet and a vault letter of intent with no independent attestation.

### VARA · reserve · `grounded`

- **Module:** `vara-reserve-attestation`
- **Confidence:** 0.79 (retrieval 0.74)
- **Coverage:** missing
- **Citation:** [VA Issuance Rulebook Reserve and Backing Assets — Attestation and Safekeeping of Reserves](https://www.vara.ae/en/rules-and-regulations/)

AURUM-X is marketed as 1:1 allocated gold but the pack contains no independent attestation of quantity, quality, or segregation, and is silent on encumbrance / liens. Vault LoI is not a reserve report.

### MiCA · complaints · `grounded`

- **Module:** `mica-complaints-handling`
- **Confidence:** 0.82 (retrieval 0.69)
- **Coverage:** missing
- **Citation:** [Title V Art. 71](https://eur-lex.europa.eu/eli/reg/2023/1114/oj)

Licensing gap against MiCA Art. 71: no published complaints-handling procedure, no register, no free-of-charge filing channel. Support is described as Telegram for launch partners. The pack itself flags this as an open drafting gap.

### VARA · complaints · `grounded`

- **Module:** `vara-consumer-protection`
- **Confidence:** 0.80 (retrieval 0.66)
- **Coverage:** missing
- **Citation:** [Market Conduct Rulebook Consumer Protection — Fair Treatment and Complaints](https://www.vara.ae/en/rules-and-regulations/)

No complaints scheme, SLA, fair-treatment policy, or Arabic/English client-support plan. Consumer-protection evidence is absent.

### MiCA · market_abuse · `grounded`

- **Module:** `mica-market-abuse`
- **Confidence:** 0.83 (retrieval 0.72)
- **Coverage:** missing
- **Citation:** [Title VI Art. 86](https://eur-lex.europa.eu/eli/reg/2023/1114/oj)

No market-abuse surveillance policy, insider list, or suspicious-transaction playbook. Founders assert market-abuse rules "probably don't bite" because Aurum is "a custodian, not an exchange." That view is not tested against Title VI duties for issuers and persons professionally arranging transactions in AURUM-X.

### VARA · market_abuse · `grounded`

- **Module:** `vara-market-conduct`
- **Confidence:** 0.81 (retrieval 0.70)
- **Coverage:** missing
- **Citation:** [Market Conduct Rulebook Prohibition of Market Abuse — Manipulation and Insider Dealing](https://www.vara.ae/en/rules-and-regulations/)

Missing market-conduct policy, surveillance, insider-information procedure, and VARA escalation playbook. Staff personal-account dealing is unrestricted.

### MiCA · disclosures · `needs_human_verification`

- **Module:** `mica-whitepaper-disclosures`
- **Confidence:** 0.64 (retrieval 0.62)
- **Coverage:** partial
- **Citation:** [Title II Art. 6](https://eur-lex.europa.eu/eli/reg/2023/1114/oj)

This pack is treated as a disclosure document but is marked confidential and "not an offering document." Risk factors occupy half a page. Marketing claims ("fully reserved gold, always") are not reconciled to a filed MiCA white paper. Human review should confirm whether Title II or Title III ART white-paper rules apply to AURUM-X.

### VARA · disclosures · `needs_human_verification`

- **Module:** `vara-va-issuance`
- **Confidence:** 0.61 (retrieval 0.58)
- **Coverage:** partial
- **Citation:** [VA Issuance Rulebook Issuer Obligations — White Paper and Ongoing Disclosure](https://www.vara.ae/en/rules-and-regulations/)

Product narrative exists; a VARA-compliant issuance white paper, ongoing-disclosure procedure, and legal characterisation of the gold claim do not.

### MiCA · licensing · `needs_human_verification`

- **Module:** `mica-casp-authorisation`
- **Confidence:** 0.58 (retrieval 0.55)
- **Coverage:** missing
- **Citation:** [Title V Art. 59](https://eur-lex.europa.eu/eli/reg/2023/1114/oj)

No CASP authorisation has been granted or filed. A draft programme of operations exists only as an internal slide deck. Intent is documented; an application file is not.

### VARA · licensing · `needs_human_verification`

- **Module:** `vara-vasp-licensing`
- **Confidence:** 0.60 (retrieval 0.57)
- **Coverage:** partial
- **Citation:** [Virtual Assets and Related Activities Regulations 2023 Part III — Licensing](https://www.vara.ae/en/rules-and-regulations/)

Product-to-activity mapping (Custody Services + VA Issuance) is stated. Fit-and-proper files, licence application, and compliance programme submitted to VARA are not in the pack.

### MiCA · governance · `needs_human_verification`

- **Module:** `mica-governance-conflicts`
- **Confidence:** 0.66 (retrieval 0.60)
- **Coverage:** missing
- **Citation:** [Title V Art. 72](https://eur-lex.europa.eu/eli/reg/2023/1114/oj)

Conflicts of interest are not documented despite the dual role of issuer and custodian of AURUM-X and CEO control of disaster-recovery key material. Related-party MPC vendor is undisclosed.

### VARA · governance · `needs_human_verification`

- **Module:** `vara-conflicts-conduct`
- **Confidence:** 0.63 (retrieval 0.59)
- **Coverage:** missing
- **Citation:** [Company Rulebook Conflicts of Interest — Identification and Management](https://www.vara.ae/en/rules-and-regulations/)

No conflicts policy covering the issuer-custodian dual role, no related-party register, no personal-account dealing rules.

## Evidence gaps

### MiCA · missing · complaints (Art. 71)

_CASPs must establish and maintain effective, transparent procedures for prompt handling of client complaints…_

Missing:
- published complaints-handling procedure
- complaints register and SLA metrics
- free-of-charge filing channel
- template acknowledgements and outcome letters

### MiCA · missing · reserve (Art. 36)

Missing:
- independent attestation or audit of reserve holdings
- segregation of reserve from issuer operating funds
- valuation methodology and frequency

### MiCA · missing · market_abuse (Art. 86)

Missing:
- market-abuse surveillance policy
- insider list / inside-information handling procedure
- suspicious-transaction reporting playbook
- staff dealing and wall-crossing controls

### VARA · missing · complaints (Fair Treatment and Complaints)

Missing:
- published complaints scheme with timelines
- complaints log and root-cause analysis
- fair-treatment / consumer-protection policy
- client-support channels in English and Arabic as appropriate

### VARA · missing · reserve (Attestation and Safekeeping of Reserves)

Missing:
- independent attestation (quantity, quality, segregation)
- encumbrance / lien negative confirmation
- attestation frequency and public summary

## HITL overrides logged

- `edit` on `mica-whitepaper-disclosures` at 2026-08-29 17:41 UTC — Reviewer notes Title III ART white paper (not Title II) is the correct heading once AURUM-X is characterised as an ART.
  - Override: Characterise AURUM-X under MiCA Title III (ART) rather than Title II. Require a Title III white paper with reserve, redemption, and issuer-governance headings before any EU offer.
- `reject` on `vara-aml-cft` at 2026-08-29 17:44 UTC — Six-page AML skeleton is not a programme; do not treat CDD mentions as coverage.
- `accept` on `mica-custody-segregation` at 2026-08-29 17:46 UTC — Segregation policy + MPC runbook are sufficient to mark custody as covered for this pack, pending a live wallet inventory sample.

---
Generated by RegTrace-AI. Citations link to official sources; paraphrases are original.
