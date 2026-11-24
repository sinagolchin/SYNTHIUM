"""Synthium data layer.

  courtlistener  label real court records with rubric-INDEPENDENT outcomes

A model graded against its own rubric is grading its own homework, so
validation targets come from the court record, read by this labeler.
The data files themselves live in ``<repo>/data`` (see ``synthium.paths``).
"""

from . import courtlistener

__all__ = ["courtlistener"]
