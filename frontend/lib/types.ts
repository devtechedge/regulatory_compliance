export type Citation = {
  module_id: string;
  framework: string;
  title: string;
  article: string;
  clause: string | null;
  url: string;
  category: string;
};

export type Locator = {
  title: string;
  article: string;
  clause: string | null;
  url: string;
};

export type Framework = {
  id: string;
  name: string;
  jurisdiction: string;
  instrument: string;
  source_url: string;
  description: string;
  module_count: number;
};

export type Document = {
  id: string;
  title: string;
  kind: string;
  content: string;
};

export type ProjectSummary = {
  id: string;
  name: string;
  tagline: string;
  jurisdictions: string[];
  offerings: string[];
  target_licences: string[];
  summary: string;
  document_count: number;
  last_run_id: string | null;
  last_run_at: string | null;
};

export type Project = ProjectSummary & { documents: Document[] };

export type FindingStatus = "grounded" | "needs_human_verification" | "unsupported";

export type Finding = {
  id: string;
  run_id: string;
  module_id: string;
  framework: string;
  category: string;
  status: FindingStatus;
  confidence: number;
  claim: string;
  citations: Citation[];
  flags: string[];
  coverage: string;
  retrieval_score: number;
  review_action: string | null;
};

export type Gap = {
  id: string;
  module_id: string;
  framework: string;
  category: string;
  coverage: "covered" | "partial" | "missing";
  missing_items: string[];
  present_items: string[];
  obligation: string | null;
  locator: Locator | null;
};

export type ReviewAction = {
  id: string;
  finding_id: string;
  action: string;
  original_text: string;
  override_text: string | null;
  note: string | null;
  created_at: string;
  framework: string | null;
  module_id: string | null;
  run_id: string | null;
};

export type Readiness = {
  framework: string;
  covered: number;
  partial: number;
  missing: number;
  total: number;
};

export type Run = {
  id: string;
  project_id: string;
  frameworks: string[];
  generator: string;
  created_at: string;
  module_count: number;
  findings: Finding[];
  gaps: Gap[];
  reviews: ReviewAction[];
  readiness: Readiness[];
};
