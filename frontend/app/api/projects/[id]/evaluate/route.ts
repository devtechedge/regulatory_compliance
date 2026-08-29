import { NextResponse } from "next/server";
import { evaluateProject } from "@/lib/demo-store";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

export async function POST(_req: Request, { params }: { params: { id: string } }) {
  const run = evaluateProject(params.id);
  if (!run) {
    return NextResponse.json({ detail: "Project not found" }, { status: 404 });
  }
  return NextResponse.json(run);
}
