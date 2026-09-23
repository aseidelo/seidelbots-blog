export type ProjectStatus = "Live" | "Beta" | "Planned";

export interface Project {
  name: string;
  /** Subdomain host, e.g. "ledger.seidelbots.com". Omit while unreleased. */
  host?: string;
  status: ProjectStatus;
  what: string;
  stack: string;
  /** When it went up (ISO date). Orders the shared stream on the home page. */
  shipped: string;
  /** What this unit's drawing should show — rendered as a Slot until it exists. */
  art: string;
  /** Related post id, if there's a writeup. */
  postSlug?: string;
}

// The shelf. Empty until the first project ships — see src/pages/projects/index.astro
// for the empty state this renders when this list is [].
export const PROJECTS: Project[] = [];
