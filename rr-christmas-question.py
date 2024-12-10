TEXT: str = """
Pizza Eggs Rioja Figs Orange juice
Razor Mixed nuts Frying steak Rusks Emery boards
Quiche Unsweetened squash Expectorant Nectarines Cabbage
Yoghurt Coffee Oven chips Underwear Newspaper
TV guide"""

text = TEXT.lower().replace(" ", "").replace("\n", "")
letters = set(text)
counts = [(l, text.count(l)) for l in letters]
sorted_counts = sorted(counts, key=lambda x: x[1], reverse=True)
print(sorted_counts)
sorted_letters = [f[0] for f in sorted_counts]
print("".join(sorted_letters))
