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
    "LHG": {
        "pattern": re.compile(
            r"\bLHG\b|Long Hậu",
            re.IGNORECASE,
        ),
    },
    "LPB": {
        "pattern": re.compile(
            r"\bLPB\b|LienVietPostBank|Ngân hàng Bưu điện Liên Việt",
            re.IGNORECASE,
        ),
    },
}
