"""Tips: total bill vs tip (bivariate), with sex as colour, smoker as marker, party size as dot size (multivariate)."""
import seaborn.objects as so
from common import load, save_so, THEME, BLUE, ORANGE

tips = load("tips")
plot = (
    so.Plot(tips, x="total_bill", y="tip", color="sex", marker="smoker", pointsize="size")
    .add(so.Dot(alpha=0.75))
    .scale(color={"Male": BLUE, "Female": ORANGE}, marker={"No": "o", "Yes": "X"}, pointsize=(4, 14))
    .label(x="Total bill (US dollars)", y="Tip (US dollars)", color="Sex", marker="Smoker", pointsize="Party size",
           title="244 restaurant bills: five columns in one plot")
    .layout(size=(8, 5.2))
    .theme(THEME)
)
save_so(plot, "scatter_tips")
