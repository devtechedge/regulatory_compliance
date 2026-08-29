import { expect, test } from "@playwright/test";

test("dashboard shows Aurum Custody project card", async ({ page }) => {
  await page.goto("/");
  const card = page.getByTestId("project-card");
  await expect(card).toBeVisible();
  await expect(card).toContainText("Aurum Custody");
});

test("workspace split screen has document pane and evaluate control", async ({ page }) => {
  await page.goto("/projects/aurum-custody");
  await expect(page.getByTestId("workspace-split")).toBeVisible();
  await expect(page.getByTestId("document-pane")).toBeVisible();
  await expect(page.getByTestId("evaluate-button")).toBeVisible();
  await expect(page.getByTestId("findings-pane")).toBeVisible();
});

test("finding card with Accept is visible after evaluate or last run", async ({ page }) => {
  await page.goto("/projects/aurum-custody");
  await expect(page.getByTestId("evaluate-button")).toBeVisible();
  const existing = page.getByTestId("finding-card").first();
  if ((await existing.count()) === 0) {
    await page.getByTestId("evaluate-button").click();
  }
  const card = page.getByTestId("finding-card").first();
  await expect(card).toBeVisible({ timeout: 60_000 });
  await expect(card.getByTestId("accept-finding")).toBeVisible();
  await expect(card.getByRole("button", { name: "Accept" })).toBeVisible();
});

test("gap and readiness panel is visible after a run", async ({ page }) => {
  await page.goto("/projects/aurum-custody");
  const panel = page.getByTestId("gap-panel");
  if ((await panel.count()) === 0) {
    await page.getByTestId("evaluate-button").click();
  }
  await expect(page.getByTestId("gap-panel")).toBeVisible({ timeout: 60_000 });
  await expect(page.getByTestId("gap-panel")).toContainText("Licensing readiness");
});

test("eval-cases page loads", async ({ page }) => {
  await page.goto("/reviews");
  await expect(page.getByTestId("eval-cases-page")).toBeVisible();
  await expect(page.getByRole("heading", { name: /Human overrides/i })).toBeVisible();
});
