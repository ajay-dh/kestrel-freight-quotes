"""Print a Markdown rate preview for the GitHub Actions job summary.

Usage in CI:  python -m kestrel.preview >> "$GITHUB_STEP_SUMMARY"
"""

from kestrel.lanes import LANES, WEIGHTS_KG
from kestrel.quote import quote


def money(x: float) -> str:
    return f"-${abs(x):,.2f}" if x < 0 else f"${x:,.2f}"


def render() -> str:
    header = "| Lane | " + " | ".join(f"{w:,} kg" for w in WEIGHTS_KG) + " |"
    divider = "|---|" + "---:|" * len(WEIGHTS_KG)
    rows = []
    problems = 0
    for lane, km in LANES:
        cells = []
        for w in WEIGHTS_KG:
            price = quote(w, km)
            if price <= 0:
                problems += 1
                cells.append(f"❌ **{money(price)}**")
            else:
                cells.append(money(price))
        rows.append(f"| {lane} ({km:,} km) | " + " | ".join(cells) + " |")

    status = (
        f"> ❌ **{problems} quotes are zero or negative.** Do not ship this."
        if problems
        else "> ✅ All sample quotes are positive."
    )
    return "\n".join(["## 📦 Rate card preview (standard service)", "", status, "", header, divider, *rows, ""])


if __name__ == "__main__":
    print(render())
