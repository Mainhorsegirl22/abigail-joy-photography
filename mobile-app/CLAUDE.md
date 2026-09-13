# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

@AGENTS.md

## Scope

This is a standalone Expo/React Native project living inside a larger repo whose root is a
separate static website (see `../CLAUDE.md`). The Tailwind/HTML rules in the parent CLAUDE.md
do not apply here.

## Commands

- `npm install` — install dependencies.
- `npm start` — start the Metro dev server; scan the printed QR with Expo Go, or press `w`/`i`/`a` to open web/iOS/Android.
- `npm run web` / `npm run ios` / `npm run android` — start targeting a specific platform directly.
- `npx tsc --noEmit` — typecheck. This is currently the only automated check in the project.
- `npx expo lint` — sets up and runs ESLint (no config is committed yet, so this runs a one-time interactive setup on first use). This fails in network-sandboxed environments (it fetches config templates), so don't rely on it there.
- `npx expo-doctor` — validates the Expo config/dependencies. Two of its checks call out to expo.dev and the React Native Directory and will fail in network-sandboxed environments; that's an environment limitation, not a real project issue.
- `npm run reset-project` — Expo template script that moves the starter code aside; not meaningful once real app code exists.
- No test runner is configured.

`expo-env.d.ts` (gitignored) is generated the first time you run `npm start`/`expo start`. It declares the `*.css`/`*.module.css` module types that `src/global.css` and `src/components/animated-icon.module.css` rely on — `npx tsc --noEmit` will show spurious "cannot find module" errors for those imports until you've started the dev server at least once.

## Architecture

- **Routing**: `expo-router`, file-based, rooted at `src/app` (see `"main": "expo-router/entry"` and `transform.routerRoot=src/app` in `app.json`). Currently a single route, `src/app/index.tsx`. `src/app/_layout.tsx` wraps the app in `ThemeProvider` and renders a plain `Stack` (no tab bar).
- **Path aliases**: `@/*` → `src/*`, `@/assets/*` → `assets/*` (defined in `tsconfig.json`).
- **Theming**: `src/constants/theme.ts` defines `Colors.light`/`Colors.dark` (semantic tokens: `text`, `background`, `backgroundElement`, `textSecondary`, `accent`, `positive`, `negative`, etc.) plus `Spacing` tokens. `useTheme()` (`src/hooks/use-theme.ts`) resolves the active scheme to a flat color object. `ThemedView`/`ThemedText` (`src/components/`) are the base styled primitives — prefer them over raw `View`/`Text` so components stay theme-aware; `ThemedText`'s `type` prop selects a typographic style, `themeColor` overrides its color.
- **Platform-specific files**: Metro auto-selects `*.web.tsx`/`*.web.ts` over the default file on web (e.g. `animated-icon.web.tsx` vs `animated-icon.tsx`, `use-color-scheme.web.ts` vs `use-color-scheme.ts`). Add a `.web` variant when a component needs different behavior on web vs native rather than branching on `Platform.OS` inline.
- **Splash animation**: `AnimatedSplashOverlay` (`src/components/animated-icon.tsx`) is rendered once in `_layout.tsx` and drives the native splash screen via `expo-splash-screen`.
