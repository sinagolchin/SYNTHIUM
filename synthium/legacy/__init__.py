"""Every earlier Synthium version, restored as live code (2026-11-24).

Sina's rule: nothing is retired. Each earlier version is a field still under study, so
each one is kept here as importable code that can be updated and extended, next to the
current ruler. Nothing here changes the ruler, the ledgers or any result. Every number
these modules print is UNTESTED unless a held-out test says otherwise.

| Module | Version | Source | Needs |
|---|---|---|---|
| ``omega_v1_5`` | V1 / Omega 1.5 (Dec 2025) | original, from ``synthium_omega_v1.5.zip`` | numpy |
| ``v2`` | V2 / Omega 2.0 (Dec 2025) | original; files renamed (``vectors_v2.py`` -> ``vectors.py``) | numpy |
| ``v3_4`` | V3.4 (Jan to Mar 2026) | original combined script; V2.2 to V3.3 survive only as PDF text, kept in ``archive/v2_2_to_v3_4_pdf_text/`` | numpy |
| ``v4`` | V4 (Apr 2026) | original (also archived byte for byte in ``archive/v4_original/``) | numpy, scipy, scikit-learn |
| ``v4_3_1`` | V4.3.1 (May 2026) | original package, the 2,045-line monolith (``monolith.py``), data, the trained neural encoder weights | numpy, scipy, scikit-learn, torch |
| ``v5`` | V5 honesty (May 2026) | original | numpy |
| ``v6`` | V6 predictive and CourtListener labeler (Jun 24 2026) | original | stdlib |
| ``v6_1`` | V6.1 (Jun 25 2026): the 12-unit judicial formula | original package | stdlib |
| ``v8`` | V8 parts not in the main package: the atlas loader and the July blind protocol | original | stdlib |
| ``synthiumbot`` | SynthiumBot (Apr 2026) | original, ``config.py`` reconstructed (token from environment) | python-telegram-bot, numpy |

Changes made while restoring, all marked ``RESTORED 2026-11-24`` in the code: absolute
``synthium.`` imports point at this folder; data paths point at each copy's
``data_files/``. No formula, coefficient or unit was changed.

See ``docs/UNDER_CONSIDERATION.md`` for what each one claimed and why it was set aside.
"""
