export const meta = {
  name: 'paper-workshop-act2-atelier',
  description: 'Act II (ATELIER): implement the verified findings as tracked edits + real re-runs under the Execution-Provenance Wall, multi-angle verified, into an impeccable revised paper + replication package.',
  phases: [
    { title: 'Intake', detail: 'assess achievable scope from the provided inputs' },
    { title: 'Triage', detail: 'sort each finding into lane A/B/C/D and draft the edit spec' },
    { title: 'Baseline', detail: 'reproduce the current paper numbers before any edit' },
    { title: 'Stage', detail: 'create the git working copy + branch the Scribe edits (never the original)' },
    { title: 'Implement', detail: 'Runner re-runs code, Scribe transcribes — never invents' },
    { title: 'Verify', detail: 'multi-angle panel clears every edit (fix/provenance/consistency/integrity)' },
    { title: 'Reconcile', detail: 'prove every number in the revised paper is true and consistent' },
    { title: 'Package', detail: 'assemble + clean-room replicate the package' },
    { title: 'Disclose', detail: 'auto-generate the AI-involvement disclosure' },
  ],
}

// args can arrive as a JSON-encoded string in some harnesses; parse defensively.
const A = (typeof args === 'string' ? JSON.parse(args) : args) || {}
const PATHS = A.paths || {}
const INPUTS = A.inputs || {}
const LEDGER = A.ledger || []        // the verified findings the author elected to implement
const PROMPTS_DIR = PATHS.prompts_dir || ''
const HELPERS_DIR = PATHS.helpers_dir || ''   // deterministic Act-II checkers live here (provenance/consistency/reproduces/integrity_diff.py)
const GP = { agentType: 'general-purpose' }
// Each agent reads its own prompt template from the installed skill and applies the
// substitutions; keeps args tiny and the skill self-contained. phase2 prompts are under
// the 'phase2/' subdir; the shared verifier is '05_verification_panel'.
const promptRef = (name, vars) =>
  'Your task instructions are in the file: ' + PROMPTS_DIR + '/' + name + '.md\n' +
  'READ that file with your tools and follow it EXACTLY as your role. If that exact path ' +
  'fails, glob for **/' + name + '.md and read the match. It contains {{TOKEN}} placeholders ' +
  '— substitute these values (and read any path given as a file):\n' +
  JSON.stringify(vars || {}, null, 2) +
  '\nYou MUST finish by returning the required structured output via the StructuredOutput tool — do NOT reply in prose, and do not stop until you have called it.'

// ---------- schemas ----------
const SCOPE = { type: 'object', additionalProperties: false, properties: { achievable_scope: { type: 'array', items: { type: 'string' } }, degraded: { type: 'array', items: { type: 'object', additionalProperties: false, properties: { finding_id: { type: 'string' }, missing_input: { type: 'string' }, consequence: { type: 'string' } }, required: ['finding_id', 'missing_input', 'consequence'] } }, blocking_gaps: { type: 'array', items: { type: 'string' } }, request_list: { type: 'array', items: { type: 'object', additionalProperties: false, properties: { input: { type: 'string' }, reason: { type: 'string' } }, required: ['input', 'reason'] } } }, required: ['achievable_scope', 'degraded', 'blocking_gaps', 'request_list'] }
const EDIT = { type: 'object', additionalProperties: false, properties: { edit_id: { type: 'string' }, finding_id: { type: 'string' }, lane: { type: 'string', enum: ['A-writing', 'B-recompute', 'C-new-analysis', 'D-author-decision'] }, file: { type: 'string' }, locator: { type: 'string' }, old_text: { type: ['string', 'null'] }, new_text: { type: ['string', 'null'] }, depends_on_run: { type: ['string', 'null'] }, provenance_token: { type: ['string', 'null'] }, justification_type: { type: 'string', enum: ['more-correct', 'clearer'] }, edit_class: { type: 'string', enum: ['presentation', 'additive-verified', 'numeric', 'result-suppressing', 'claim-altering'] }, author_signoff_required: { type: 'boolean' }, reverify_angles: { type: 'array', items: { type: 'string' } } }, required: ['edit_id', 'finding_id', 'lane', 'file', 'locator', 'old_text', 'new_text', 'depends_on_run', 'provenance_token', 'justification_type', 'edit_class', 'author_signoff_required', 'reverify_angles'] }
const EDIT_SPEC = { type: 'object', additionalProperties: false, properties: { edits: { type: 'array', items: EDIT } }, required: ['edits'] }
const RUNREC = { type: 'object', additionalProperties: false, properties: { run_id: { type: 'string' }, status: { type: 'string', enum: ['ok', 'failed', 'baseline-failed'] }, command: { type: 'string' }, provenance_tokens: { type: 'array', items: { type: 'object', additionalProperties: false, properties: { value: { type: 'string' }, script: { type: 'string' }, line_or_chunk: { type: 'string' }, run_id: { type: 'string' }, input_data_hash: { type: 'string' }, output_file: { type: 'string' }, output_hash: { type: 'string' } }, required: ['value', 'script', 'line_or_chunk', 'run_id', 'input_data_hash', 'output_file', 'output_hash'] } }, log_excerpt: { type: 'string' } }, required: ['run_id', 'status', 'command', 'provenance_tokens', 'log_excerpt'] }
const SCRIBE = { type: 'object', additionalProperties: false, properties: { status: { type: 'string' }, diff: { type: 'string' }, commit: { type: 'string' }, new_text: { type: 'string' } }, required: ['status', 'diff', 'commit', 'new_text'] }
const VERIF = { type: 'object', additionalProperties: false, properties: { target_id: { type: 'string' }, angle: { type: 'string' }, verdict: { type: 'string', enum: ['upheld', 'upheld-with-revision', 'rejected', 'cant-tell'] }, reason: { type: 'string' }, suggested_revision: { type: ['string', 'null'] } }, required: ['target_id', 'angle', 'verdict', 'reason', 'suggested_revision'] }
const VERIF_BATCH = { type: 'object', additionalProperties: false, properties: { verdicts: { type: 'array', items: VERIF } }, required: ['verdicts'] }
const RECON = { type: 'object', additionalProperties: false, properties: { reconciled: { type: 'array', items: { type: 'string' } }, orphans: { type: 'array', items: { type: 'string' } }, mismatches: { type: 'array', items: { type: 'string' } }, run_mismatches: { type: 'array', items: { type: 'string' } }, integrity_flags: { type: 'array', items: { type: 'string' } } }, required: ['reconciled', 'orphans', 'mismatches', 'run_mismatches', 'integrity_flags'] }
const PACKAGE = { type: 'object', additionalProperties: false, properties: { manifest: { type: 'string' }, readme: { type: 'string' }, reproduced: { type: ['boolean', 'string'] }, log: { type: 'string' }, labeled_gaps: { type: 'array', items: { type: 'string' } }, package_dir: { type: ['string', 'null'] }, redline_path: { type: ['string', 'null'] }, clean_manuscript_path: { type: ['string', 'null'] }, clean_pdf_path: { type: ['string', 'null'] }, tracked_docx_path: { type: ['string', 'null'] }, changes_map_path: { type: ['string', 'null'] }, map_path: { type: ['string', 'null'] } }, required: ['manifest', 'readme', 'reproduced', 'log', 'labeled_gaps', 'package_dir', 'redline_path', 'clean_manuscript_path', 'changes_map_path', 'map_path'] }
const DISCLOSURE = { type: 'object', additionalProperties: false, properties: { long_form: { type: 'string' }, short_form: { type: 'string' } }, required: ['long_form', 'short_form'] }

const ANGLE_Q = {
  'fix-safety': 'Would the edit introduce a NEW error or break a correct passage? Does it target the right span?',
  'numeric-provenance': 'Does every number in this edit trace to a content-hashed run artifact produced in THIS session? Missing token => reject.',
  'consistency': 'After this edit, does the value match every other place the same quantity appears (abstract/body/table/appendix)?',
  'integrity': 'Does the edit suppress/attenuate a result, narrow a sample, drop a control/observation, weaken a caveat, swap the headline spec, or HARK?',
  'logical-validity': 'Does the edit faithfully implement the finding without overreaching?',
  'steelman-charity': 'Is the original passage actually fine as-is, making this edit unnecessary or harmful?',
  'human-voice': 'Does this edit read as the AUTHOR wrote it, not AI? Judge against the author-voice standard in prompts/phase2/12_scribe_implementer.md and GROUND it: quote an adjacent author sentence as the benchmark and report a style diff (em/en-dash, semicolon and hedge counts, words-per-sentence, plus any banned-lexicon or negation-correction-antithesis hits). Reject on any banned token, the antithesis in any form, or a punctuation spike above the author baseline; no quoted benchmark => cant-tell, never upheld.',
}

// ---------- Intake ----------
phase('Intake')
const scope = await agent(promptRef('phase2/10_intake', { LEDGER_PATH: PATHS.ledger_path || '(inline)', INPUT_MANIFEST_JSON: INPUTS, RULES_PATH: PATHS.rules || '' }), { ...GP, label: 'intake', phase: 'Intake', schema: SCOPE })
log('Intake: ' + scope.achievable_scope.length + ' achievable, ' + scope.degraded.length + ' degraded, ' + scope.blocking_gaps.length + ' blocking')
if (scope.blocking_gaps.length) {
  // FAIL CLOSED: surface every blocking gap for the author to fill (or to accept the
  // degraded scope) BEFORE any edit — never proceed silently just because some source exists.
  return { halted: 'blocking_gaps', scope }
}

// ---------- Triage ----------
phase('Triage')
const spec = await agent(promptRef('phase2/11_triage', { LEDGER_PATH: PATHS.ledger_path || JSON.stringify(LEDGER), INPUT_MANIFEST_JSON: INPUTS, RULES_PATH: PATHS.rules || '' }), { ...GP, label: 'triage', phase: 'Triage', schema: EDIT_SPEC })
const edits = spec.edits || []
log('Triage: ' + edits.length + ' edits (' + edits.filter(e => e.lane === 'A-writing').length + ' writing, ' + edits.filter(e => e.lane === 'B-recompute').length + ' recompute, ' + edits.filter(e => e.lane === 'C-new-analysis').length + ' new-analysis, ' + edits.filter(e => e.lane === 'D-author-decision').length + ' author-decision)')

// ---------- Baseline gate ----------
// Run whenever code+data exist (not only for B-recompute edits): the package clean-room
// check and the reconciler both need a baseline anchor, so a writing-only run that has the
// code should still establish one. The Runner derives reproduced/baseline-failed from the
// deterministic reproduces.py predicate, not LLM judgment.
phase('Baseline')
let baseline = { run_id: 'baseline', status: 'ok', command: '(skipped: no code/data provided)', provenance_tokens: [], log_excerpt: '' }
let baselineRan = false
if (INPUTS.code && INPUTS.data) {
  baseline = await agent(promptRef('phase2/13_runner_rerun', { FINDING_JSON: { note: 'BASELINE REPRODUCTION GATE — run the master script unchanged and confirm the current headline numbers reproduce.' }, EDIT_JSON: {}, CODE_DIR: INPUTS.code, DATA_DIR: INPUTS.data, RUN_DIR: (PATHS.session || '.') + '/phase2/runs/baseline', SANDBOX_NOTES_PATH: PATHS.sandbox_notes || '', HELPERS_DIR }), { ...GP, label: 'baseline-gate', phase: 'Baseline', schema: RUNREC })
  baselineRan = true
  log('Baseline: ' + baseline.status)
  if (baseline.status === 'baseline-failed') {
    return { halted: 'baseline-failed', scope, baseline }
  }
}

// ---------- Stage the working copy (the git branch the Scribe commits each edit to) ----------
// The Scribe must edit a COPY on a branch, never the author's original (grounding rule 12).
// Nothing downstream can resolve an annotated path string, so we materialize a real working
// tree here and thread its ABSOLUTE path into Scribe / Reconcile / Package.
phase('Stage')
const WORK_BRANCH = 'paper-workshop/phase2'
let workDir = INPUTS.source || ''
if (INPUTS.source) {
  const staged = await agent(
    'Create the Act-II working copy the Scribe will edit — NEVER touch the author\'s original. Using Bash:\n' +
    '1) mkdir -p "' + (PATHS.session || '.') + '/phase2/work"\n' +
    '2) copy the ENTIRE manuscript source tree from "' + INPUTS.source + '" into that work dir, preserving the \\input/child-file structure (use cp -a / robocopy / xcopy as the OS requires).\n' +
    '3) cd into the work dir and run: git init -q && git add -A && git commit -q -m "act2 baseline (verbatim author source)" && git checkout -q -b ' + WORK_BRANCH + '\n' +
    '4) Return the ABSOLUTE path of the work dir, the branch name, and git_ok. If git is unavailable, still copy the tree and return git_ok:false (edits are then tracked by unified diff, not commits).',
    { ...GP, label: 'stage-worktree', phase: 'Stage', schema: { type: 'object', additionalProperties: false, properties: { work_dir: { type: 'string' }, branch: { type: 'string' }, git_ok: { type: 'boolean' } }, required: ['work_dir', 'branch', 'git_ok'] } })
  workDir = staged.work_dir || workDir
  log('Stage: working copy at ' + workDir + ' (branch ' + (staged.branch || WORK_BRANCH) + ', git ' + (staged.git_ok ? 'ok' : 'unavailable') + ')')
}

// ---------- Implement + Verify (pipeline per edit) ----------
phase('Implement')
function anglesForEdit(e) {
  const set = new Set(['fix-safety', 'logical-validity', 'steelman-charity'])
  ;(e.reverify_angles || []).forEach(a => set.add(a))
  if (e.edit_class === 'numeric') { set.add('numeric-provenance'); set.add('consistency') }
  if (e.edit_class === 'result-suppressing' || e.edit_class === 'claim-altering') set.add('integrity')
  if (e.lane === 'A-writing' || e.new_text) set.add('human-voice') // any prose edit must read as the author, not AI
  return [...set]
}
function decideEdit(e, run, scribe, verdicts) {
  const hard = ['fix-safety', 'numeric-provenance', 'consistency', 'integrity', 'human-voice']
  // any explicit 'rejected' on a hard-gate angle blocks the edit outright
  const failed = verdicts.filter(v => hard.includes(v.angle) && v.verdict === 'rejected')
  if (scribe && /blocked/.test(scribe.status || '')) return { ...wrap(e, run, scribe, verdicts), status: 'blocked', reason: scribe.status }
  if (failed.length) return { ...wrap(e, run, scribe, verdicts), status: 'blocked', reason: failed.map(f => f.angle + ': ' + f.reason).join('; ') }
  // FAIL CLOSED: every hard-gate angle this edit REQUIRES must have come back present AND
  // upheld. A missing verdict (a dropped verifier) or a 'cant-tell' is NOT a free pass —
  // such an edit may never auto-apply; it routes to author sign-off instead.
  const requiredHard = anglesForEdit(e).filter(a => hard.includes(a))
  const upheld = a => verdicts.some(v => v.angle === a && (v.verdict === 'upheld' || v.verdict === 'upheld-with-revision'))
  const unresolved = requiredHard.filter(a => !upheld(a))
  // record-touching edits always wait for the human, even when clean
  const mustSignoff = e.author_signoff_required || ['numeric', 'result-suppressing', 'claim-altering'].includes(e.edit_class)
  if (e.lane === 'C-new-analysis' || e.lane === 'D-author-decision') return { ...wrap(e, run, scribe, verdicts), status: 'proposal' }
  if (unresolved.length) return { ...wrap(e, run, scribe, verdicts), status: 'queued-for-signoff', reason: 'unverified hard-gate angle(s) — not auto-applied: ' + unresolved.join(', ') }
  return { ...wrap(e, run, scribe, verdicts), status: mustSignoff ? 'queued-for-signoff' : 'applied' }
}
function wrap(e, run, scribe, verdicts) { return { edit: e, run, scribe, verdicts } }

const results = (await pipeline(
  edits,
  async (e) => {
    // lane D never runs code or edits; lane C drafts+runs but proposal-only downstream
    let run = null
    if (e.lane === 'B-recompute' || e.lane === 'C-new-analysis') {
      run = await agent(promptRef('phase2/13_runner_rerun', { FINDING_JSON: { finding_id: e.finding_id }, EDIT_JSON: e, CODE_DIR: INPUTS.code || '(none)', DATA_DIR: INPUTS.data || '(none)', RUN_DIR: (PATHS.session || '.') + '/phase2/runs/' + e.edit_id, SANDBOX_NOTES_PATH: PATHS.sandbox_notes || '', HELPERS_DIR }), { ...GP, label: ('run:' + e.edit_id).slice(0, 56), phase: 'Implement', schema: RUNREC })
    }
    return { e, run }
  },
  async (prev, e) => {
    if (e.lane === 'D-author-decision') return { e, run: prev.run, scribe: null }
    const tok = (prev.run && prev.run.provenance_tokens && prev.run.provenance_tokens[0]) ? JSON.stringify(prev.run.provenance_tokens[0]) : (e.provenance_token || '')
    const eWithTok = { ...e, provenance_token: tok || e.provenance_token }
    const scribe = await agent(promptRef('phase2/12_scribe_implementer', { EDIT_JSON: eWithTok, SOURCE_FILE_PATH: workDir + '/' + e.file, WORKING_BRANCH: WORK_BRANCH, RULES_PATH: PATHS.rules || '' }), { ...GP, label: ('scribe:' + e.edit_id).slice(0, 56), phase: 'Implement', schema: SCRIBE })
    return { e: eWithTok, run: prev.run, scribe }
  },
  async (prev, e) => {
    const angles = anglesForEdit(e)
    const tgt = { id: e.edit_id, edit: prev.e, scribe_new_text: prev.scribe && prev.scribe.new_text, run_summary: prev.run ? { status: prev.run.status, tokens: (prev.run.provenance_tokens || []).length } : null }
    const res = (await parallel(angles.map(ang => () => agent(promptRef('05_verification_panel', { ANGLE: ang, ANGLE_QUESTION: ANGLE_Q[ang] || ('Judge from the ' + ang + ' angle.'), TARGETS_JSON: [tgt], PAPER_TXT_PATH: workDir + '/' + e.file, STAGED_SOURCES_DIR: PATHS.staged_sources || '(none)', QUOTE_GATE_PATH: PATHS.quote_gate || '', RULES_PATH: PATHS.rules || '', RUBRIC_PATH: PATHS.rubric || '' }), { ...GP, label: ('vfy:' + ang + ':' + e.edit_id).slice(0, 56), phase: 'Verify', schema: VERIF_BATCH })))).filter(Boolean)
    const verdicts = res.flatMap(r => r.verdicts || [])
    return decideEdit(prev.e, prev.run, prev.scribe, verdicts)
  }
)).filter(Boolean)

const applied = results.filter(r => r.status === 'applied')
const queued = results.filter(r => r.status === 'queued-for-signoff')
const proposals = results.filter(r => r.status === 'proposal')
const blocked = results.filter(r => r.status === 'blocked')
log('Implement: ' + applied.length + ' auto-applied, ' + queued.length + ' queued for sign-off, ' + proposals.length + ' proposals, ' + blocked.length + ' blocked')

// ---------- Reconcile ----------
phase('Reconcile')
const runArtifacts = results.map(r => r.run).filter(Boolean).flatMap(r => r.provenance_tokens || [])
const reconcile = await agent(promptRef('phase2/14_consistency_reconciler', { REVISED_SOURCE_PATH: workDir, BASELINE_SOURCE_PATH: INPUTS.source || '(none)', RUN_ARTIFACTS_JSON: runArtifacts, BASELINE_NUMBERS_JSON: baseline.provenance_tokens || [], RUN_DIR: (PATHS.session || '.') + '/phase2/runs/reconcile', HELPERS_DIR }), { ...GP, label: 'reconcile', phase: 'Reconcile', schema: RECON })
const reconcileClean = !reconcile.orphans.length && !reconcile.mismatches.length && !reconcile.run_mismatches.length && !(reconcile.integrity_flags || []).length
log('Reconcile: ' + (reconcileClean ? 'clean' : (reconcile.orphans.length + ' orphans, ' + reconcile.mismatches.length + ' mismatches, ' + reconcile.run_mismatches.length + ' run-mismatches, ' + (reconcile.integrity_flags || []).length + ' integrity-flags')))

// ---------- Package ----------
phase('Package')
const pkg = await agent(promptRef('phase2/15_repro_package', { SESSION_PATH: PATHS.session || '.', INPUT_MANIFEST_JSON: INPUTS, RUN_RECORDS_JSON: results.map(r => r.run).filter(Boolean), REVISED_SOURCE_PATH: workDir, BASELINE_RAN: baselineRan, PACKAGE_DIR: (PATHS.session || '.') + '/phase2/replication_package', SANDBOX_NOTES_PATH: PATHS.sandbox_notes || '', HELPERS_DIR }), { ...GP, label: 'repro-package', phase: 'Package', schema: PACKAGE })

// ---------- Disclose ----------
phase('Disclose')
const auditTrail = { applied: applied.map(r => ({ edit_id: r.edit.edit_id, finding_id: r.edit.finding_id, lane: r.edit.lane, justification: r.edit.justification_type })), queued: queued.map(r => r.edit.edit_id), proposals: proposals.map(r => r.edit.edit_id), reruns: results.map(r => r.run).filter(Boolean).map(r => r.run_id), reconcile, package_reproduced: pkg.reproduced }
const disclosure = await agent(promptRef('phase2/16_disclosure', { AUDIT_TRAIL_JSON: auditTrail }), { ...GP, label: 'disclosure', phase: 'Disclose', schema: DISCLOSURE })

return {
  scope, baseline_status: baseline.status, baseline_ran: baselineRan, work_dir: workDir, branch: WORK_BRANCH,
  counts: { edits: edits.length, applied: applied.length, queued_for_signoff: queued.length, proposals: proposals.length, blocked: blocked.length },
  applied, queued_for_signoff: queued, proposals, blocked,
  reconcile, reconcile_clean: reconcileClean,
  package: pkg, package_reproduced: pkg.reproduced,
  deliverables: { redline: pkg.redline_path || null, clean_manuscript: pkg.clean_manuscript_path || null, clean_pdf: pkg.clean_pdf_path || null, tracked_docx: pkg.tracked_docx_path || null, changes_map: pkg.changes_map_path || null, map: pkg.map_path || null, package_dir: pkg.package_dir || null },
  disclosure,
  signoff_queue: queued.concat(proposals).map(r => ({ edit_id: r.edit.edit_id, finding_id: r.edit.finding_id, lane: r.edit.lane, edit_class: r.edit.edit_class, status: r.status })),
}
