# QAWM UI — Query Workbench

A Next.js 14 web interface for the Quantum Archeological World Model (QAWM). Lets researchers compose and run `RECONSTRUCT`, `COMPARE`, and `COUNTERFACTUAL` queries against the QAWM FastAPI backend, with results rendered as typed, confidence-labelled world states.

## Setup

```bash
cd ui/web
npm install
cp .env.local.example .env.local
# Edit .env.local to point at your QAWM backend
npm run dev
```

Open [http://localhost:3000](http://localhost:3000). The app redirects to `/query`.

## Requirements

- Node.js 18+
- A running QAWM FastAPI backend (`cd ../../ && uvicorn api.main:app --reload`)

## Environment

| Variable | Default | Description |
|---|---|---|
| `NEXT_PUBLIC_QAWM_API_URL` | `http://localhost:8000` | Base URL of the QAWM FastAPI backend |

## Structure

```
ui/web/
├── app/
│   ├── layout.tsx          Root layout (fonts, metadata)
│   ├── page.tsx            Redirects → /query
│   ├── globals.css         Design tokens + Tailwind base
│   └── query/page.tsx      Main query workbench
├── components/
│   ├── ui/
│   │   ├── Badge.tsx         Confidence badge (VERIFIED/PLAUSIBLE/SPECULATIVE)
│   │   ├── Button.tsx        Primary/ghost button
│   │   └── LayerTag.tsx      L0–L4 layer chip
│   ├── QueryBuilder.tsx    Query form (3 modes)
│   ├── ResultsPanel.tsx    WorldState viewer (4 tabs)
│   ├── EntityCard.tsx      Entity display
│   └── EventList.tsx       Events sorted by time, filterable by confidence
├── lib/
│   ├── types.ts            TypeScript types mirroring QAWM Python schema
│   └── api.ts              Typed fetch wrappers for /reconstruct /compare /counterfactual
└── hooks/
    └── useQAWMQuery.ts     React hook managing query state
```

## Confidence System

| Level | Color | Meaning |
|---|---|---|
| `VERIFIED` | Green | ≥2 independent traces, high signal-to-noise |
| `PLAUSIBLE` | Amber | At least 1 trace; statistically likely |
| `SPECULATIVE` | Red | Inferred from gaps or weak signals |

## Layers

| Layer | Domain |
|---|---|
| L0 Physical | Matter, energy, entropy |
| L1 Biological | Life, ecosystems, genetics |
| L2 Cultural | Language, art, memes, rituals |
| L3 Techno-Economic | Markets, infrastructure, networks |
| L4 Metasystemic | Climate, geopolitics, global systems |
