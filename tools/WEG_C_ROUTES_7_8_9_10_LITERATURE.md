# Routes 7–10 — Literatur-Recherche + Volltext + Applicability

**Stand**: 2026-05-16 (späte Session-Fortsetzung).
**Methode**: WebSearch + WebFetch + Cross-reference mit `lemma_B_proof_strategy.md` + ROADMAP_NEXT_AUTOLOOP.md.

## Per-Route Applicability-Matrix

| Route | Werkzeug | Carrier-Anwendbarkeit | Liefert exakten Wert 3/8? | Was es liefert |
|---|---|---|---|---|
| 7 | Backhausz-Szegedy graphop (arXiv:1811.00626) | ✓ intermediäre Dichte | ✗ | Konvergenz-Framework + Limit-Objekt |
| 7 | Graphop-Size-Transferability (arXiv:2306.04495) | ✓ sparse O(1)-Grad | ✗ | Uniformität über N (M3-unconditional Hebel) |
| 8 | Hierarchische K_d-Replacement (Zhang, Sci Reports 2015) | ✗ (Clustering 9/16 ≠ 0.142) | ✗ | Falsche Graph-Klasse |
| 9 | Huang-Landon (arXiv:1510.06390) | ✗ (p ≥ N^δ/N braucht wachsenden Grad) | ✗ | Nur BULK, kein Edge |
| 10 | Bauerschmidt-Huang-Yau local KM (arXiv:1609.09052) | ✓ fester Grad d | ✗ direkt, aber gibt Baseline | Spektral-Edge tree-like d-regulär |
| 10 | Bordenave-Lelarge (free convolution) | ✓ sparse | ✗ | Spektral-Dichte aus Grad-Sequenz |

## Was die Recherche tatsächlich aufgedeckt hat

### Route 7 (Backhausz-Szegedy, arXiv:1811.00626)

- **Volltext**: WebFetch der PDF-Version konnte keinen lesbaren Text extrahieren (Binär-Layout). Cambridge-Core-Eintrag bestätigt: "applications on the empirical distribution of eigenvectors" sind im Paper, **keine explizite Spektralkanten-Theoreme** angekündigt.
- **Applicability**: Framework deckt intermediäre Dichte; carrier d_eff=12 fällt im Anwendungsbereich.
- **Limitation**: Action-convergence-Framework gibt CONVERGENCE-Begriff, aber nicht den GAP-Wert. Quantitative Spektral-Lücken-Stabilität ist nicht der Hauptbeitrag.
- **Verdict**: gibt **Existenz/Uniformität-Hebel** für M3-unconditional (Route 9-Territorium); gibt NICHT den exakten Wert 3/8.

### Route 9 (Huang-Landon, arXiv:1510.06390)

- **Regime**: $p \ge N^\delta/N$ für beliebiges $\delta > 0$, d.h.\ durchschnittlicher Grad $= p N \sim N^\delta$ **wächst** mit $N$.
- **Carrier**: $d_\text{eff} = 12 = O(1) = O(N^0)$, d.h.\ $\delta = 0$, **außerhalb des Anwendungsbereichs**.
- **Output**: nur **Bulk-Statistiken** (Korrelationsfunktionen, Gap-Statistik), KEIN Spektral-Edge.
- **Verdict**: NICHT anwendbar auf den Carrier. Route 9 wäre nur sinnvoll wenn wir den Carrier in einen wachsend-Grad-Regime erweitern könnten — was aber die Carrier-Identität zerstört.

### Route 8 (deterministische rekursive small-world, Zhang et al. Sci. Reports 2015)

- **Konstruktion**: hierarchischer $K_d$-Ersatz (Triangle für $d=3$, Tetraeder für $d=4$). Jeder Knoten wird in jeder Generation durch ein neues $K_d$ ersetzt. Endet bei $d^g$ Knoten.
- **Spektrum**: persistente Lücke im Intervall $[1, d)$. Für $d=4$: kleinste nichttriviale Eigenwert $\ge 1$, nicht $3/8 \approx 0.375$.
- **Clustering**: $\langle C\rangle \to ((d-1)/d)^2 = 9/16$. Carrier hat 0.142 — **andere Graph-Klasse**.
- **Spektrale Dimension**: $d_s = 2$, unabhängig von $d$. Carrier hat $d_\text{eff} = 12$ als mittlerer Grad — anderer Begriff.
- **Verdict**: Diese spezifische deterministische Konstruktion **matcht den Carrier nicht**. Andere deterministische Konstruktionen mit $d_\text{eff} = 12$ + Clustering $\approx 0.14$ + Spektral-Edge bei $3/8$ existieren möglicherweise, sind aber nicht in der gefundenen Literatur.

### Route 10 (Bauerschmidt-Huang-Yau, Local Kesten-McKay, arXiv:1609.09052)

- **Regime**: zufällige $d$-reguläre Graphen mit **fest großem** Grad $d$.
- **Triangle**: BHY adressieren Triangles explizit ("random regular graph contains a triangle with probability uniformly bounded from below... requires more delicate analysis").
- **Kernergebnis**: Kesten-McKay-Spektraldichte gilt bis zur kleinsten Skala $\eta \gtrsim N^{-1}$, plus vollständige Delokalisierung der Bulk-Eigenvektoren.
- **Carrier-Anwendbarkeit**: ✓ (festes $d_\text{eff} = 12$; das ist genau das BHY-Regime).
- **Spektraler Edge**: für $d$-regulär ohne Clustering ist die Kesten-McKay-Edge der Adjazenzmatrix bei $2\sqrt{d-1}$. Für die normierte Laplace $L = I - A/d$ ist der Smallest-non-trivial:
  $$\lambda_2^\text{KM}(d) = 1 - \frac{2\sqrt{d-1}}{d}$$

#### Neue numerische Beobachtung (heute computed)

Für $d = d_\text{eff} = 12$:
$$\lambda_2^\text{KM}(12) = 1 - \frac{2\sqrt{11}}{12} = 0.44723$$

Carrier-empirisch (vacuum-branch Symanzik): $\lambda_\infty^\text{vac} = 0.3732$, Target $3/8 = 0.3750$.

Differenz: $\lambda_2^\text{KM}(12) - 3/8 = 0.07223$ — **suggestiv nahe an** der universal-leakage Konstanten $\gamma^2(d+N_\text{gen}) = 7/100 = 0.07000$, die in $n_s$, $\Sigma m_\nu$, $D/H_\text{dressed}$, etc.\ auftritt.

**Konjektur**:
$$\lambda_\infty^\text{vac} \;\stackrel{?}{=}\; \underbrace{\left[1 - \frac{2\sqrt{d-1}}{d}\right]}_{\text{KM tree-like baseline}} \;-\; \underbrace{\gamma^2(d+N_\text{gen})}_{\text{universal-leakage triangle correction}}$$

Numerisch bei $(d, N_\text{gen}) = (12, 3)$ — wait, das passt nicht, $d$ ist hier der mittlere Grad nicht die spacetime-Dimension. Lass mich präzisieren:
- Carrier spacetime-Dimension $d_\text{ST} = 4$
- Carrier mittlerer Skelett-Grad $d_\text{eff} = 12 = d_\text{ST} \cdot N_\text{gen}$ — interessante Identität!

Mit $d_\text{eff} = 12$:
- KM tree-like baseline: $1 - 2\sqrt{11}/12 = 0.44723$
- Minus $\gamma^2 \cdot 7 = 0.07$: ergibt $0.37723$
- Vs $3/8 = 0.37500$: Residuum $+0.59\%$.

**Diese Übereinstimmung auf $0.6\%$ ist deutlich besser als die einzelnen Faktor-Residuen** der Phase-3-Kette (alle bei 2-8%).

#### Caveat: Irrationalität

Der KM-Baseline-Wert $1 - 2\sqrt{11}/12$ ist **irrational**. Eine exakte ℚ-Identität
$$\frac{3}{8} = 1 - \frac{2\sqrt{11}}{12} - \frac{7}{100}$$
gilt **nicht** algebraisch (Linke Seite rational, rechte Seite irrational). Die Match-auf-0.6% ist ein **numerisches Korrespondenz**, kein algebraischer Satz.

Mögliche Interpretationen:
1. Der Carrier ist NICHT regular-12 + tree-like; die wahre Spektralkante kommt aus der spezifischen Grad-Verteilung-Heterogenität (Bordenave-Lelarge free convolution); die irrationale KM-Baseline wird durch die Heterogenität auf eine rationale Form 3/8 verschoben.
2. Das 0.6%-Residuum ist genau die finite-$N$ Symanzik-Korrektur und in $N \to \infty$ verschwindet die Übereinstimmung.
3. Ein anderer Mechanismus (Bakry-Émery curvature, equitable partition, spectral synthesis) ergibt 3/8 direkter, und die KM-Annäherung ist Koinzidenz.

## Konkreter analytischer Pfad für Phase 5

Basierend auf der heutigen Recherche-Synthese, der konkreteste verbleibende Pfad zu $3/8$:

**Phase 5a (Route 10b, Bordenave-free-convolution)**: numerisch die freie multiplikative Faltung der Kesten-McKay-Halbkreis-Dichte mit der empirischen Grad-Verteilung des Carriers berechnen. Wenn der Spektral-Edge der gefalteten Dichte bei $3/8$ landet, ist die Erklärung: Carrier-Grad-Heterogenität verschiebt KM exakt um die richtige Menge.

**Phase 5b (M3-unconditional via Route 7/9)**: graphop size-transferability (arXiv:2306.04495) anwenden, um die Uniformität von $\lambda_2$ über $N$ zu beweisen (lade A1–A8 in M3). Gibt nicht den exakten Wert $3/8$, aber macht M3 unconditional unter der EMPIRISCHEN Beobachtung, dass $\lambda_2 \to$ konstant.

**Phase 5c (BHY Local KM exakt anwenden)**: das Bauerschmidt-Huang-Yau-Lemma direkt auf die Carrier-empirische Grad-Verteilung anwenden, mit expliziten Triangle-Korrekturen aus dem 5.3x-Triangle-Exzess.

## Sources

- **Route 7**: [Backhausz–Szegedy, arXiv:1811.00626](https://arxiv.org/abs/1811.00626), [Cambridge Core](https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/action-convergence-of-operators-and-graphs/F5900CA5BE554C9F4DEAAB518962D2DD); [arXiv:2306.04495](https://arxiv.org/abs/2306.04495) (size-transferability).
- **Route 8**: [Zhang et al., Sci. Reports 9024 (2015)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4356965/) (hierarchical small-world).
- **Route 9**: [Huang–Landon, arXiv:1510.06390](https://arxiv.org/abs/1510.06390); [Annales IHP 56, 120 (2020)](https://projecteuclid.org/euclid.aihp/1580720485).
- **Route 10**: [Bauerschmidt–Huang–Yau, arXiv:1609.09052](https://arxiv.org/abs/1609.09052); [Comm. Math. Phys. 369, 523 (2019)](https://link.springer.com/article/10.1007/s00220-019-03345-3).
- **Bordenave-Lelarge (free convolution)**: Sparse regular random graphs spectral density.
- **Carrier-Cavity (existing P4 inventory)**: [Pham–Peron–Metz, arXiv:2404.08152](https://arxiv.org/abs/2404.08152).

## Ehrliche Zusammenfassung

- **Route 7** (Backhausz-Szegedy + graphop transferability): nicht für exakten 3/8, **aber** für Uniformität (M3-unconditional Hebel).
- **Route 8** (deterministisch small-world): die gefundene Variante (Zhang et al.) matcht den Carrier nicht. Andere Konstruktionen denkbar, aber unbekannt.
- **Route 9** (Huang-Landon): NICHT anwendbar — Regime erfordert wachsenden Grad.
- **Route 10** (Bauerschmidt-Huang-Yau): **konkretester Pfad**, gibt Kesten-McKay-Baseline für $d_\text{eff}$-regulär, plus Triangle-Korrekturen. Numerische Beobachtung: KM-Baseline minus universal-leakage $\gamma^2(d_\text{ST}+N_\text{gen})$ stimmt zu $0.6\%$ mit $3/8$ überein. Suggestiv aber nicht algebraisch exakt.

Der **konkreteste nächste analytische Schritt** ist Phase 5a: free-convolution der KM-Dichte mit der carrier-empirischen Grad-Verteilung, numerisch durchgeführt. Falls der gefaltete Spektral-Edge bei $3/8$ landet, ist die Erklärung **Bordenave-Lelarge type**: $3/8$ aus KM-Baseline plus carrier-Grad-Verteilungs-Verschiebung.

Geschätzte Aufwände:
- **Phase 5a (free-convolution numerical)**: 1-2 Wochen
- **Phase 5b (graphop transferability)**: 2-4 Wochen
- **Phase 5c (BHY explicit triangle correction)**: 4-8 Wochen

Alle drei sind genuine multi-week-Forschungsprojekte, nicht Single-Session-Aufgaben.
