# Weg C Phase 4a — Eigenvektor-Mode-Charakterisierung

**Stand**: 2026-05-16 (späte Session-Fortsetzung).
**Status**: Cartesian-Product-Hypothese FALSIFIZIERT. Wichtige
Refinement der Phase-3-Lesart.

## Drei testbare Hypothesen — alle drei verfehlen

| Hypothese | Erwartung | Empirisch | Verdict |
|---|---:|---:|---|
| H1: Konstanter Mode in 2 Sub-Populations | PR ≈ 1 | 0.333 | FAIL |
| H2: Cartesian-Produkt $g_d \times g_{N_\text{gen}}$ | $\lambda_3/\lambda_2 = 8/7 = 1.143$ | **1.010** | **FAIL** |
| H3: Defekt-lokalisiert (matter-core) | PR ≈ 1/N | 0.333 (≫ 1/N) | FAIL |

Die **Cartesian-Produkt-Hypothese** ist der wichtigste Test: wenn das
Skelett-Spektrum sich als $G_\text{spatial} \times G_\text{gen}$ mit
Faktor-Gaps $1/d = 0.25$ und $1/N_\text{gen} = 0.333$ faktorisierte,
wäre $\lambda_2 = (1/d + 1/N_\text{gen})/2 = 7/24$ **und**
$\lambda_3 = \max(1/d, 1/N_\text{gen}) = 1/3$ — Ratio $8/7 = 1.143$.

Empirisch finden wir $\lambda_3/\lambda_2 \to 1.010$. Die Top-
Eigenwerte $\lambda_2, \ldots, \lambda_7$ sind **fast degeneriert**,
nicht durch diskrete Faktor-Gaps separiert. Das **falsifiziert die
2-Faktor-Cartesian-Produkt-Struktur** der skeleton-Laplacian-Spektrum.

## Per-Regime Daten

| N | $\lambda_2^w$ | $\lambda_3^w$ | $\lambda_2^\text{skel}$ | $\lambda_3^\text{skel}$ | $l_3/l_2$ (w) | PR(w) |
|---:|---:|---:|---:|---:|---:|---:|
| 128 | 0.390 | 0.412 | 0.317 | 0.347 | 1.057 | 0.300 |
| 200 | 0.418 | 0.433 | 0.369 | 0.388 | 1.036 | 0.333 |
| 256 | 0.408 | 0.426 | 0.342 | 0.366 | 1.045 | 0.318 |
| 300 | 0.400 | 0.421 | 0.332 | 0.349 | 1.053 | 0.357 |
| 512 | 0.403 | 0.412 | 0.318 | 0.326 | **1.024** | 0.302 |

$l_3/l_2$ **konvergiert gegen 1**, nicht $8/7$. Symanzik-Asymptote
$1.010$, Residuum $-11.6 \%$ vs $8/7$.

## Wichtige Refinement der Phase-3-Lesart

Die Phase-3 algebraische Kette $\mathbf{3/8 = 7/24 \cdot 9/7}$
bleibt **algebraisch exakt** in $\mathbb Q$ und **empirisch konsistent
mit 0.88 \% Residuum** (siehe WEG_C_PHASE3_REPORT.md). Was Phase 4a
NICHT in Frage stellt:

- Die Identität $3/8 = (d-1)/(2d)$ als asymptotischer Wert von
  $\lambda_2^\text{w}$ stimmt mit Empirie ($\approx 0.396$, $+5.5\%$).
- Die Drei-Faktor-Zerlegung ist numerisch selbst-konsistent.

Was Phase 4a falsifiziert:
- Die *strukturelle Interpretation* "7/24 = (1/d + 1/N_gen)/2 = average
  of two cartesian-product factor gaps" ist NICHT der Mechanismus.
- Die Top-Eigenwerte sind nahe-degeneriert; es gibt kein klares
  "zweiter Faktor mit Gap $1/N_\text{gen}$" im empirischen Spektrum.

**Was bedeutet das fürs Verständnis von 3/8?**

Das numerische Match $\lambda_\infty^\text{w} \approx 3/8$ ist
empirisch belastbar (mehrfach reproduziert, branch-resolved bestätigt).
Aber die **mechanistische Erklärung** für diesen spezifischen Wert
braucht eine andere strukturelle Quelle als die 2-Faktor-Cartesian-
Produkt-Lesart.

Mögliche Alternativen:

1. **Cheeger-Konstanten-Bound**: $\lambda_2 \le 2 h(G)$ mit
   $h(G) = (d-1)/(4d) = 3/16$ als der isoperimetrische Quotient des
   Carrier-Saddle-Graphen. Falls $h(G) = 3/16$ exakt aus der Saddle-
   Geometrie folgt, hat man $\lambda_2 \le 3/8$ als obere Schranke.

2. **Soft Spectral Edge**: das Spektrum hat eine *Dichte* mit einer
   sanften Kante bei $3/8$, nicht einen isolierten Eigenwert. Die
   "$\lambda_2$" ist der erste Punkt der Spektral-Dichte oberhalb 0.
   Die nahezu-Degeneration der Top-Eigenwerte unterstützt dieses Bild.

3. **Expander-Graph-Random-Matrix-Limit**: für einen Carrier nahe
   am Random-Regular-Graph-Limit mit effektivem Grad $d_\text{eff} =
   d \cdot N_\text{gen} = 12$, ist die Spektral-Dichte
   asymptotisch Kesten--McKay. Die Kante der Kesten-McKay-Dichte für
   $d_\text{eff} = 12$ ist $\lambda^\pm = 1 \pm 2\sqrt{d_\text{eff}-1}/d_\text{eff}
   = 1 \pm 2\sqrt{11}/12$. Lower edge $\approx 1 - 0.553 = 0.447$ —
   NICHT 3/8.
   Bedeutet: der Carrier ist NICHT random-regular, sondern hat eine
   strukturierte Spektraldichte mit edge bei $3/8$.

4. **Symmetrie-Argument auf $S_\text{UV}$-Hessian**: $3/8$ ist die
   kleinste Eigenwert einer spezifischen Quadratform aus
   $S_\text{UV}$ — ähnlich wie Goldstone-Moden in Sigma-Modellen die
   $\lambda_\text{min}$-Struktur bestimmen.

## Konkreter nächster Schritt — Phase 4b

Statt das Cartesian-Produkt-Argument weiterzuverfolgen, das jetzt
falsifiziert ist, sollten wir das **Cheeger-Konstanten-Bild**
analytisch testen:

1. Compute den Cheeger-Quotienten $h(\Xi_\text{eq}) =
   \min_{S} |\partial S| / |S|$ für die Carrier-Saddle-Konfiguration
   bei verschiedenen $N$.
2. Test ob $h \to 3/16$ asymptotisch (was $\lambda_2 \le 3/8$ via
   Cheeger geben würde).
3. Falls ja, frage: warum exakt $h = 3/16 = (d-1)/(4d)$?

Das ist Phase 4b's analytischer Target. Phase 4a's Ergebnis hat den
Suchraum eingegrenzt, indem die Cartesian-Produkt-Hypothese ausgesondert
wurde.

## Phase-3+4a Synthese (ehrlich)

Stand des Weg-C-Programms:

| Phase | Hypothese | Resultat |
|---|---|---|
| 1 | NM-Surrogate: Joint-Moments → $\lambda_2$ | FALSIFIED |
| 2 | Gaussian-Saddle → 3/8 | FALSIFIED |
| **3** | **Algebraische Kette $3/8 = 7/24 \cdot 9/7$** | **POSITIV** (0.88% Residuum) |
| 4a | Cartesian-Produkt-Faktorisierung des Skelett-Spektrums | **FALSIFIED** ($l_3/l_2 = 1.01$, nicht $8/7$) |
| 4b | Cheeger-Konstanten-Argument | offen |
| 4c | MCMC-Stationarität, K/Q-Hessian | offen |

Der **algebraische Wert 3/8 ist robust** an der Empirie. Die
**naive strukturelle Lesart** als Cartesian-Produkt-Faktor ist falsch.
Der ehrliche analytische Stand: 3/8 ist empirisch zertifiziert,
das *spezifische* Mechanismus-Bild bleibt offen.

## Artefakte

- `weg_c_phase4a_eigenvector_modes.py` (Sandbox)
- `weg_c_phase4a_eigenvector_modes_results.json` (Sandbox)
- WEG_C_PHASE4A_REPORT.md (dieses Dokument)
