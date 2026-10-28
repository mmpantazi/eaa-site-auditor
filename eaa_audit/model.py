from dataclasses import dataclass


@dataclass(frozen=True)
class Finding:
    rule: str
    wcag: str
    level: str
    kind: str  # "fail" = definite problem, "review" = needs a human
    file: str
    line: int
    message: str
    snippet: str = ""
