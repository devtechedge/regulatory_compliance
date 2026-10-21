import { NextResponse } from "next/server";
import { renderMarkdown } from "@/lib/demo-export";
import { getRun } from "@/lib/demo-store";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

export async function GET(_req: Request, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const run = getRun(id);
  if (!run) {
    return NextResponse.json({ detail: "Run not found" }, { status: 404 });
  }
  const md = renderMarkdown(run);
  const filename = `regtrace-${run.project_id}-${run.id.slice(0, 8)}.md`;
  return new NextResponse(md, {
    status: 200,
    headers: {
      "Content-Type": "text/markdown; charset=utf-8",
      "Content-Disposition": `attachment; filename="${filename}"`,
    },
  });
}
