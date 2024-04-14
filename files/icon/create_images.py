import cairosvg

for i in [0.1, 0.125, 0.15, 0.2, 0.25, 0.333, 0.375, 0.5, 0.625, 0.667, 0.75, 0.825, 1, 1.25, 1.333, 1.5, 1.667, 1.75, 2, 2.5, 3]:
    cairosvg.svg2png(url="files/icon/icon.svg", write_to=f"files/icon/icon{i}.png", scale=i)