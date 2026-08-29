import { NextResponse } from "next/server";
import { listProjects } from "@/lib/demo-store";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

export function GET() {
  return NextResponse.json(listProjects());
}
