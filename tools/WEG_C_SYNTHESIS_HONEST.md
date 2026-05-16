# Weg C ehrliche Synthese (post-Inventur)

**Stand**: 2026-05-16 spät-Session.

## Was diese Session wirklich beigetragen hat

Vorab-Kontext: das emergent-gr-closure-repro hat bereits eine
**24-sections-Lemma-B-Strategie-Datei** mit Routes 1–5b
analysiert, Steps 1–4a durchgeführt, Routes 7–10 vorgeschlagen,
und in **Section 18** dokumentiert dass 3/8 in der reinen
*dimensionalen* Algebra lebt (d-only), nicht System-R-faktorisiert.

Meine Session-Beiträge:

| Phase | Was | Honest Status |
|---|---|---|
| Inventur | Vollständige Read-through der existierenden Infrastruktur | wertvoll — vorbeugt Duplikat-Arbeit |
| Phase 3 | Algebraische Kette $7/24 \cdot 9/7 = 3/8$ + 0.88% Empirie | **NEU**: end-to-end per-regime verification. ABER strukturelle Lesart durch Section 18's d-only-Statement begrenzt |
| Phase 4a | Eigenvector-mode characterization | **NEU**: $l_3/l_2 = 1.01 \ne 8/7$ falsifiziert Cartesian-Produkt-Lesart |
| Phase 4b | Spektraler Cheeger | **REDUNDANT** mit Route 1; numerisch bestätigt was bereits theoretisch gesagt war |

## Was Phase 3 wirklich aussagt (revidiert nach Section 18)

Die ℚ-Identität $\frac{3}{8} = \frac{7}{24} \cdot \frac{9}{7}$ ist
algebraisch exakt im $(d, N_\text{gen}) = (4, 3)$-Anchor.
Die empirische End-to-End-Konsistenz auf 0.88% ist robust.

Aber Section 18 ("Cross-sector independence of the 3/8 conjecture")
sagt klar: "3/8 lives in the dimensional-graph algebra (d-only),
not the System-R coefficient algebra (α_ξ, γ, N_gen-dependent)".

Meine Faktorisierung enthält $N_\text{gen}$ in BEIDEN Faktoren
(7/24 und 9/7), die sich im Produkt herausheben. Das ist algebraisch
gültig, **aber** das deutet auf eine post-hoc-Faktorisierung,
nicht auf einen genuinen 2-Schritt-Mechanismus hin.

Die **echte** Quelle von 3/8 — laut Section 18 — ist Friedman-Bulk
+ isolierte-Eigenwert-Dekomposition auf dem $\tau=0.10$-Skelett,
mit small-world Spektral-Theorie (Route 5b). Diese Route ist die
einzig stehende — alle anderen sind falsifiziert.

## Was Phase 4a beiträgt zu der existierenden Infrastruktur

Phase 4a's $l_3/l_2 \to 1.01$ ist ein **neues empirisches Resultat**
das in der existierenden Infrastruktur nicht explizit dokumentiert ist.
Es falsifiziert eine konkrete strukturelle Lesart (Cartesian-Produkt)
und verfeinert das Bild des Carrier-Spektrums:

- Top-Eigenwerte sind nahezu degeneriert (Δl/l ≈ 0.01-0.05)
- Participation ratio ≈ 1/N_gen — suggestive, nicht beweisend
- Korrelation mit Knoten-Grad ≈ 0 asymptotisch

Das ist eine Erweiterung von Step 4a (small-world identification),
nicht eine Falsifikation davon. Routes 8 (deterministic small-world)
und 10 (operator-valued free probability) sind durch dieses Resultat
nicht ausgeschlossen — sie müssen jetzt mit der near-degeneracy
oben-am-Spektrum kompatibel sein.

## Was Phase 4b nicht beiträgt

Phase 4b ist redundant mit Route 1. Die existierende Analyse sagte
schon: Cheeger gibt nur $\lambda_2 \ge \xi_{\min}^2/8 \approx 10^{-7}$,
sieben Größenordnungen schwächer als empirisch 0.38. Mein
spektraler Cheeger-Test fand $h \approx 0.30$, also $2h \approx 0.60$
— bestätigt die obere Cheeger-Schranke aber nicht die untere.
Saturation 1.47 ≠ 1.0 — keine Cheeger-untere-Schranke-Saturation.

Phase 4b war ehrlich gesagt überflüssig. Ich habe gelernt, was die
Pre-Arbeit zur Frage hatte, aber numerische Bestätigung des bereits
theoretisch Dismissed war nicht der höchste Hebel.

## Wo das Programm wirklich steht (post-Session)

**Empirisch zertifiziert** ($1\%$ Residuum auf 10-Regime-Ladder):
- $\lambda_\infty^\text{vac} = 3/8 = (d-1)/(2d)$ auf vacuum-branch
- $\lambda_\infty^\text{mat} = 79/200 = 3/8 + d\gamma^2/2$ auf matter-branch
- $\lambda_\infty^\text{skel} = 7/24 = (d+N_\text{gen})/(2dN_\text{gen})$

**Analytisch offen**:
- Closed-form Ableitung von 3/8 aus $S_\text{UV}$ oder aus der
  small-world Spektral-Theorie.
- Die Pre-Arbeit hat 5 surveyed Routes (1-5b) durchgegangen und
  als unzureichend befunden, sowie Route 6 (equitable partition)
  computed-falsifiziert.
- Routes 7–10 sind vorgeschlagen aber nicht angegriffen:
  - **Route 7** Backhausz-Szegedy graphop limit (sparse O(1)-Grad
    passt zum Carrier d_eff=12)
  - **Route 8** Deterministic recursive small-world spectral
    sandwich
  - **Route 9** Huang-Landon local law (gibt Existenz + Uniformität,
    nicht exakten Wert)
  - **Route 10** Operator-valued free probability
    (Kesten-McKay base ⊞ triangle correction)

Route 9 oder 7 wären meine nächsten Empfehlungen für eine
zukünftige Session, falls Phase 4 weiterverfolgt wird. Beide sind
genuine multi-week analytische Forschungsprojekte, nicht
Single-Session-Aufgaben.

## Honest Self-Assessment

Ich habe heute **das richtige getan**: gründliche Inventur statt
oberflächliche Duplikation, plus zwei neue empirische Tests
(Phase 3 algebraische End-to-End, Phase 4a Eigenvector-Modes).
Phase 4b (Cheeger) war eine ehrliche Redundanz — die existierende
Pre-Arbeit hatte sie schon adressiert.

Die Phase-3-Faktorisierung ist als ℚ-Identität exakt, aber als
*strukturelle Lesart* schwächer als zunächst geframed (durch
Section 18's d-only Statement).

Die Phase-4a-Eigenvektor-near-Degeneracy ist eine genuine neue
Erkenntnis: das Spektrum sieht nicht aus wie ein Cartesian-Produkt,
sondern wie ein soft-edge bei 3/8.

Die genuinely-open analytische Frage bleibt: derive 3/8 in
small-world-spectral-theory Route 5b (existing dominant target)
oder via Routes 7-10 (alternatives).

## Artefakte

In _sandbox_sg_cavity/:
- WEG_C_FOUNDATION.md (Roadmap)
- WEG_C_PHASE2_REPORT.md (small-N exact diag baseline)
- WEG_C_PHASE3_REPORT.md (algebraic chain, positive)
- WEG_C_PHASE4A_REPORT.md (eigenvector modes, cartesian falsified)
- WEG_C_PHASE4B_REPORT.md (NOT WRITTEN — redundant with Route 1)
- WEG_C_SYNTHESIS_HONEST.md (this document)

In relational-carrier-manifest/tools/ (GitHub):
- weg_c_phase3_algebraic_chain.py + results.json
- WEG_C_PHASE3_REPORT.md
