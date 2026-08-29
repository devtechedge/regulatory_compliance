import path from "node:path";
import { defineConfig, devices } from "@playwright/test";

const frontendDir = path.resolve(__dirname);
const repoRoot = path.resolve(frontendDir, "..");

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  workers: 1,
  reporter: [["list"], ["html", { open: "never" }]],
  timeout: 90_000,
  expect: { timeout: 20_000 },
  use: {
    baseURL: "http://localhost:3000",
    trace: "on-first-retry",
  },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
  webServer: [
    {
      command: "python3 -m uvicorn app.main:app --app-dir ../backend --host 0.0.0.0 --port 8000",
      url: "http://localhost:8000/api/health",
      reuseExistingServer: !process.env.CI,
      timeout: 120_000,
      env: {
        DATA_DIR: process.env.DATA_DIR || path.join(repoRoot, "data"),
        DATABASE_URL: process.env.DATABASE_URL || `sqlite:///${path.join(repoRoot, "backend", "e2e-playwright.db")}`,
        CORS_ORIGINS: "http://localhost:3000",
        PYTHONPATH: [path.join(repoRoot, "backend"), path.join(repoRoot, "backend", "deps"), process.env.PYTHONPATH || ""]
          .filter(Boolean)
          .join(":"),
      },
    },
    {
      command: "npx next dev -p 3000",
      url: "http://localhost:3000",
      reuseExistingServer: !process.env.CI,
      timeout: 120_000,
      env: {
        NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
      },
    },
  ],
});
