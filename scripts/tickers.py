import re

TICKERS = {
    "PET": {
        "pattern": re.compile(
            r"\bPET\b|Petrosetco|Tổng công ty Dịch vụ Tổng hợp Dầu khí",
            re.IGNORECASE,
        ),
    },
    "PVS": {
        "pattern": re.compile(
            r"\bPVS\b|PTSC|Dịch vụ Kỹ thuật Dầu khí",
            re.IGNORECASE,
        ),
    },
    "PPY": {
        "pattern": re.compile(
            r"\bPPY\b",
            re.IGNORECASE,
        ),
    },
}
