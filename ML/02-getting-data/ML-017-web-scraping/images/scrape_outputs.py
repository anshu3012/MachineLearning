"""What the Note's scraping code returns on the saved AmbitionBox pages (August 2022 copies in data/). Plotly.
tag_counts.png  - how many tags each query finds on page 1 (and infoEntity on page 2);
final_table.png - the 60 x 7 table from both pages, with its 3 NaN cells marked."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from bs4 import BeautifulSoup

HERE = Path(__file__).parent
DATA = HERE.parent / "data"
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=24)
html = [(DATA / f"ambitionbox_2022_page{k}.html").read_text(encoding="utf-8") for k in (1, 2)]
soups = [BeautifulSoup(h, "html.parser") for h in html]

# 1. tag counts: a tag name alone vs tag name + class
s1, s2 = soups
q = [('find_all("p")', len(s1.find_all("p")), GREY),
     ('find_all("h2")', len(s1.find_all("h2")), BLUE),
     ('find_all("p", class_="rating")', len(s1.find_all("p", class_="rating")), BLUE),
     ('find_all("p", class_="infoEntity")', len(s1.find_all("p", class_="infoEntity")), BLUE),
     ('same, on page 2', len(s2.find_all("p", class_="infoEntity")), RED)]
assert [n for _, n, _ in q] == [221, 30, 30, 120, 117]
fig = go.Figure(go.Bar(y=[t for t, _, _ in q][::-1], x=[n for _, n, _ in q][::-1], orientation="h",
                       marker_color=[c for _, _, c in q][::-1], text=[n for _, n, _ in q][::-1],
                       textposition="outside", cliponaxis=False))
fig.update_layout(template="simple_white", width=1200, height=520, font=FONT, showlegend=False,
                  xaxis=dict(title="tags found (page 1 unless stated)", range=[0, 250]),
                  yaxis=dict(tickfont=dict(family="Latin Modern Mono", size=21)), margin=dict(l=440, r=40, t=20, b=80))
fig.write_image(HERE / "tag_counts.png", scale=1.5)


# 2. the Note's scrape_page on both pages, joined with pd.concat
def text_or_nan(tag):
    return tag.text.strip() if tag is not None else np.nan


def scrape_page(soup):
    rows = []
    for i in soup.find_all("div", class_="company-content-wrapper"):
        info = [p.text.strip() for p in i.find_all("p", class_="infoEntity")]
        info += [np.nan] * (4 - len(info))
        rows.append({"name": i.find("h2")["title"].strip(),
                     "rating": text_or_nan(i.find("p", class_="rating")),
                     "reviews": text_or_nan(i.find("a", class_="review-count")),
                     "company_type": info[0], "head_quarters": info[1],
                     "company_age": info[2], "no_of_employees": info[3]})
    return pd.DataFrame(rows)


final = pd.concat([scrape_page(s) for s in soups], ignore_index=True)
assert final.shape == (60, 7) and final.isna().sum().sum() == 3
assert final.loc[final.isna().any(axis=1), "name"].tolist() == ["Infosys BPM", "HCL Group"]
nan_rows = final[final.isna().any(axis=1)]
print(nan_rows[["name"]].assign(n=nan_rows.isna().sum(axis=1)))
page = np.repeat([[0], [0.35]], 30, axis=0) * np.ones((1, 7))
fig = go.Figure(go.Heatmap(z=np.where(final.isna(), 1.0, page), x=list(final.columns), y=list(range(60)),
                           colorscale=[[0, "#dce6f2"], [0.35, "#fde3c8"], [1, RED]], zmin=0, zmax=1,
                           showscale=False, xgap=2, ygap=1, hoverinfo="skip"))
for r, row in nan_rows.iterrows():
    fig.add_annotation(x=6.6, y=r, text=f"{row['name']}: {row.isna().sum()} NaN", showarrow=False, xanchor="left",
                       font=dict(color=RED, size=22))
fig.add_annotation(x=-0.01, xref="paper", y=14.5, text="page 1", showarrow=False, xanchor="right", font=dict(color=BLUE))
fig.add_annotation(x=-0.01, xref="paper", y=44.5, text="page 2", showarrow=False, xanchor="right", font=dict(color=ORANGE))
fig.update_layout(template="simple_white", width=1400, height=600, font=FONT,
                  xaxis=dict(side="top", tickangle=-30, range=[-0.5, 9.5], showline=False, ticks=""),
                  yaxis=dict(autorange="reversed", showticklabels=False, showline=False,
                             ticks=""), margin=dict(l=150, r=20, t=150, b=20))
fig.write_image(HERE / "final_table.png", scale=1.5)
