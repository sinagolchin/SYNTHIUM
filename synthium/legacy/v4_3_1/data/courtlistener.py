"""CourtListener API helpers.

This module is intentionally lightweight and uses urllib so the package has no
hard dependency on requests. It is designed for environments with network access.
"""
from __future__ import annotations

import json
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional


@dataclass
class CourtListenerSearchResult:
    case_name: str
    court: str
    date_filed: str
    docket_number: str
    absolute_url: str
    citation: str
    snippet: str
    raw: Dict


class CourtListenerClient:
    def __init__(self, api_token: Optional[str] = None, base_url: str = "https://www.courtlistener.com/api/rest/v4/search/"):
        self.api_token = api_token
        self.base_url = base_url

    def search(self, query: str, type_: str = "o", page_size: int = 10, **params) -> List[CourtListenerSearchResult]:
        q = {"q": query, "type": type_, "page_size": page_size}
        q.update({k: v for k, v in params.items() if v is not None})
        url = self.base_url + "?" + urllib.parse.urlencode(q)
        headers = {"User-Agent": "Synthium/4.3 neural research prototype"}
        if self.api_token:
            headers["Authorization"] = f"Token {self.api_token}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        results = data.get("results", data if isinstance(data, list) else [])
        return [self._parse_result(r) for r in results]

    def _parse_result(self, r: Dict) -> CourtListenerSearchResult:
        opinions = r.get("opinions") or []
        snippet = ""
        citation = ""
        if opinions and isinstance(opinions, list):
            snippet = opinions[0].get("snippet", "") or opinions[0].get("plain_text", "")[:500]
        citations = r.get("citation") or r.get("citations") or []
        if isinstance(citations, list):
            citation = "; ".join(str(x) for x in citations[:3])
        else:
            citation = str(citations)
        return CourtListenerSearchResult(
            case_name=r.get("caseName") or r.get("case_name") or "",
            court=r.get("court") or "",
            date_filed=r.get("dateFiled") or r.get("date_filed") or "",
            docket_number=r.get("docketNumber") or r.get("docket_number") or "",
            absolute_url=r.get("absolute_url") or r.get("absoluteUrl") or "",
            citation=citation,
            snippet=snippet,
            raw=r,
        )


def suppression_queries() -> List[str]:
    return [
        '"Fourth Amendment" "motion to suppress" "good faith"',
        '"Fourth Amendment" "exigent circumstances" "cell phone"',
        '"Fourth Amendment" curtilage suppression',
        '"Fourth Amendment" "geofence warrant"',
        '"Fourth Amendment" "private search"',
        '"Fourth Amendment" abandonment suppression',
        '"Fourth Amendment" "scope" "warrant" "cell phone"',
    ]
