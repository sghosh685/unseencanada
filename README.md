# 🍁 My Canada — Interactive Travel Map (Unseen Canada)

> Track your travels across Canada's provinces and territories, unlock achievements, and generate custom downloadable travel maps.

Inspired by [Unseen Bangladesh](https://unseenbangladesh.com/), **My Canada** provides an interactive canvas and SVG map experience designed to celebrate Canadian exploration.

---

## ✨ Features

- **Interactive Canada Vector Map**: High-detail interactive SVG/Canvas representation covering all 10 provinces and 3 territories.
- **Progress Tracking & Analytics**: Automatic calculation of territory completion percentages, regional breakdown, and exploration scores.
- **Achievement Engine**: Unlock milestones as you venture through Canada (e.g. Coast to Coast, Northern Explorer, Prairie Wanderer).
- **Custom Map Exporter**: Render and download high-resolution travel badge images featuring your name and personal stats ready for sharing on social media.
- **Offline & Local Storage Persistence**: State is saved automatically to localStorage so progress is never lost.

---

## 🛠️ Tech Stack

- **HTML5 & Vanilla JavaScript**: Zero bloat, fast load times, and native browser compatibility.
- **HTML5 Canvas & SVG Rendering**: Precise vector path drawing and high-DPI export canvas.
- **Custom CSS3 Design**: Fully responsive across mobile, tablet, and desktop viewports.
- **Vercel**: Edge-optimized static deployment.

---

## 🚀 Running Locally

Simply open `webapp/index.html` in any web browser, or run a local HTTP server:

```bash
# Using Python
python3 -m http.server 3000 --directory webapp

# Or using npx serve
npx serve webapp
```

Then navigate to `http://localhost:3000`.

---

## 🌐 Deployment

This project is pre-configured for Vercel with `vercel.json` pointing directly to the `webapp` directory.

```bash
npx vercel --prod
```

---

## 📄 License

MIT © Saikat Ghosh
