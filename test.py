from datetime import datetime, timezone, timedelta

cutoff = datetime.now(timezone.utc) - timedelta(days=30)

test_dates = [
    '2026-03-19T21:28:26.368926Z',  # Magalie - 2 days ago
    '2026-02-25T01:53:05.126082Z',  # njcta - 24 days ago
    '2026-02-07T23:50:15.251663Z',  # Angie - 42 days ago
    '2026-02-04T23:24:24.024791Z',  # Dewayne - 45 days ago
]

for date in test_dates:
    review_time = datetime.fromisoformat(date.replace("Z", "+00:00"))
    print(f"{date[:10]} - Skip: {review_time < cutoff}")