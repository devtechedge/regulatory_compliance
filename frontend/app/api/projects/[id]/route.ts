import { NextResponse } from "next/server";
import { getProject } from "@/lib/demo-store";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

export function GET(_req: Request, { params }: { params: { id: string } }) {
  const project = getProject(params.id);
  if (!project) {
    return NextResponse.json({ detail: "Project not found" }, { status: 404 });
  }
  return NextResponse.json(project);
}
