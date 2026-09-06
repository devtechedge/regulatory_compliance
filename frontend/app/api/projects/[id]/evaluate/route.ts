import { NextResponse } from "next/server";
import { evaluateProject } from "@/lib/demo-store";
import { gateMutation } from "@/lib/demo-gate";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

export async function POST(req: Request, { params }: { params: { id: string } }) {
  const blocked = gateMutation(req);
  if (blocked) return blocked;

  const run = evaluateProject(params.id);
  if (!run) {
    return NextResponse.json({ detail: "Project not found" }, { status: 404 });
  }
  return NextResponse.json(run);
}
