import requests
import pandas as pd
import matplotlib.pyplot as plt
import os

TOKEN = os.environ.get("GH_TOKEN")
USERNAME = "larissabrangel"

url = "https://api.github.com/graphql"

query = """
{
  user(login: "%s") {
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
      nodes {
        name
        languages(first: 10) {
          nodes { name }
          edges { size }
        }
      }
    }
  }
}
""" % USERNAME

headers = {"Authorization": f"Bearer {TOKEN}"}
response = requests.post(url, json={"query": query}, headers=headers)
data = response.json()

lang_count = {}
for repo in data["data"]["user"]["repositories"]["nodes"]:
    langs = repo["languages"]["nodes"]
    sizes = [e["size"] for e in repo["languages"]["edges"]]
    for i, lang in enumerate(langs):
        lang_count[lang["name"]] = lang_count.get(lang["name"], 0) + sizes[i]

df = pd.DataFrame(list(lang_count.items()), columns=["Language", "Bytes"])
df = df.sort_values("Bytes", ascending=False)

plt.figure(figsize=(10,6))
plt.bar(df["Language"], df["Bytes"], color='skyblue')
plt.xticks(rotation=45)
plt.title("Top Languages (Todos os Repos, inclusive privados)")
plt.tight_layout()
plt.savefig("top_langs.png")
