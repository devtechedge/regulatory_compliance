import { NextResponse } from "next/server";
import { getRun } from "@/lib/demo-store";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

export function GET(_req: Request, { params }: { params: { id: string } }) {
  const run = getRun(params.id);
  if (!run) {
    return NextResponse.json({ detail: "Run not found" }, { status: 404 });
  }
  return NextResponse.json(run);
}
