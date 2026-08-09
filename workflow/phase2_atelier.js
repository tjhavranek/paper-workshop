export const meta = {
  name: 'paper-workshop-act2-atelier',
  description: 'Act II (ATELIER): implement the verified findings as tracked edits + real re-runs under the Execution-Provenance Wall, multi-angle verified, into an impeccable revised paper + replication package.',
  phases: [
    { title: 'Intake', detail: 'assess achievable scope from the provided inputs' },
    { title: 'Triage', detail: 'sort each finding into lane A/B/C/D and draft the edit spec' },
    { title: 'Baseline', detail: 'reproduce the current paper numbers before any edit' },
    { title: 'Stage', detail: 'create the git working copy + branch the Scribe edits (never the original)' },
    { title: 'Implement', detail: 'Runner re-runs code, Scribe transcribes, never invents' },
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
const TIER = A.tier || 'thorough'
// Improvement Mode (opt-in, default OFF; threaded from Act I / the orchestrator). When on, the
// Triage agent ALSO drafts the ledger's improvement-proposal findings as bold, author-rejectable
// tracked-change edits, more of them at heavier tiers. Every improvement edit stays proposal-only +
// author_signoff_required and rides the SAME gates (fix-safety, integrity, the Execution-Provenance
// Wall): nothing auto-applies, nothing skips a rail. OFF by default → the triage prompt receives an
// empty directive and behaves identically to a normal run (rail- and decision-identical; no-op).
const IMPROVE = A.improvement === true
const IMPROVE_TARGET = TIER === 'monumental' ? 'as many as the ledger genuinely supports, this is the most exhaustive mode, so be thorough'
  : TIER === 'exhaustive' ? 'a generous set'
  : 'a focused, high-value set'
const IMPROVE_NOTE = IMPROVE
  ? '\n\nIMPROVEMENT MODE IS ON (the author opted in and wants the paper improved more aggressively, in track changes). BEYOND the agreed defect fixes, ALSO draft the ledger\'s `improvement-proposal` findings (and any `contribution-undersell` the author forwarded) as concrete tracked-change edits: be bold and generous, proposing substantive ways to make the paper stronger (sharper framing, the boldest defensible claim the results support, additional analyses worth running, defensible extensions). Aim for ' + IMPROVE_TARGET + ' of improvement edits where the ledger supports them. NON-NEGOTIABLE on every improvement edit: set `author_signoff_required: true` and treat it as PROPOSAL-ONLY (the author accepts or rejects each one in track changes); a new analysis is lane C-new-analysis, a bolder claim is `claim-altering` (lane A or D), a reframing is lane A or D; any number it introduces still rides the Execution-Provenance Wall (no number without a logged re-run) and every improvement edit still carries `fix-safety` + `integrity` in `reverify_angles`. An improvement edit NEVER auto-applies and NEVER becomes a defect must-fix. Do not manufacture: propose an improvement only where the paper\'s own evidence supports it, exactly as conservatively grounded as a defect fix.'
  : ''
const PROMPTS_DIR = PATHS.prompts_dir || ''
const HELPERS_DIR = PATHS.helpers_dir || ''   // deterministic Act-II checkers live here (provenance/consistency/reproduces/integrity_diff.py)
const GP = { agentType: 'general-purpose' }

// ---------- casting (economy register; the default is session-model inheritance) ----------
// Same contract as Act I (see phase1_tribunal.js). Act II's economy is deliberately more
// conservative because it touches the record: the runner, triage, reconciler, package, and
// the verification panel pin at the Opus floor, never below; the SCRIBES always inherit the
// session model (author-facing prose under the provenance wall); only intake, staging, and
// the disclosure generator drop to Sonnet. The Execution-Provenance Wall is model-independent
// and identical in every mode.
const BUDGETED = typeof budget !== 'undefined' && budget && budget.total != null
const ECON = A.economy === true || (BUDGETED && A.economy !== false)
const ECONOMY_MAP = { intake: 'sonnet', stage: 'sonnet', disclosure: 'sonnet', triage: 'opus', runner: 'opus', verify: 'opus', reconcile: 'opus', package: 'opus' }
const MODELS = A.models || (ECON ? ECONOMY_MAP : {})
const CASTING_MODE = A.models ? 'custom' : (ECON ? 'economy' : 'inherit')
const DEGRADED = []
// Never-upgrade clamp, identical to Act I: a mapped model ranked above the
// orchestrator-passed `session_model` inherits instead, logged; absent session_model
// means no clamp (the doctor flags economy as not recommended on sub-Opus sessions).
const TIER_RANK = { haiku: 1, sonnet: 2, opus: 3, fable: 4 }
// accepts a bare tier ('fable') or a full model id ('claude-fable-5[1m]')
const SM_TIER = (String(A.session_model || '').toLowerCase().match(/fable|opus|sonnet|haiku/) || [])[0]
const SESSION_RANK = TIER_RANK[SM_TIER] || 0
const M = k => {
  const m = MODELS[k]
  if (!m) return {}
  if (SESSION_RANK && TIER_RANK[m] && TIER_RANK[m] > SESSION_RANK) {
    if (!DEGRADED.some(d => d.role === k && d.reason === 'above-session-tier')) DEGRADED.push({ role: k, label: k, tried: m, fell_back_to: 'inherit', reason: 'above-session-tier' })
    return {}
  }
  return { model: m }
}
async function cast(role, prompt, opts) {
  const m = M(role)
  let r = await agent(prompt, { ...opts, ...m })
  if (r === null && m.model) {
    DEGRADED.push({ role, label: opts.label || role, tried: m.model, fell_back_to: 'inherit', reason: 'spawn-returned-null' })
    r = await agent(prompt, opts)
  }
  return r
}
const CASTING = () => ({ mode: CASTING_MODE, session_model: A.session_model || 'not-passed', role_models: MODELS, degraded_casting: DEGRADED, scribe_batch: SCRIBE_BATCH, verify_batch: VBATCH, improvement: IMPROVE })
const SCRIBE_BATCH = A.scribe_batch || 5
const VBATCH = Math.min(30, A.verify_batch || 12)
// Each agent reads its own prompt template from the installed skill and applies the
// substitutions; keeps args tiny and the skill self-contained. phase2 prompts are under
// the 'phase2/' subdir; the shared verifier is '05_verification_panel'.
const promptRef = (name, vars) =>
  'Your task instructions are in the file: ' + PROMPTS_DIR + '/' + name + '.md\n' +
  'READ that file with your tools and follow it EXACTLY as your role. If that exact path ' +
  'fails, glob for **/' + name + '.md and read the match. It contains {{TOKEN}} placeholders ' +
  ', substitute these values (and read any path given as a file):\n' +
  JSON.stringify(vars || {}, null, 2) +
  '\nYou MUST finish by returning the required structured output via the StructuredOutput tool, do NOT reply in prose, and do not stop until you have called it.'

// ---------- schemas ----------
const SCOPE = { type: 'object', additionalProperties: false, properties: { achievable_scope: { type: 'array', items: { type: 'string' } }, degraded: { type: 'array', items: { type: 'object', additionalProperties: false, properties: { finding_id: { type: 'string' }, missing_input: { type: 'string' }, consequence: { type: 'string' } }, required: ['finding_id', 'missing_input', 'consequence'] } }, blocking_gaps: { type: 'array', items: { type: 'string' } }, request_list: { type: 'array', items: { type: 'object', additionalProperties: false, properties: { input: { type: 'string' }, reason: { type: 'string' } }, required: ['input', 'reason'] } } }, required: ['achievable_scope', 'degraded', 'blocking_gaps', 'request_list'] }
const EDIT = { type: 'object', additionalProperties: false, properties: { edit_id: { type: 'string' }, finding_id: { type: 'string' }, lane: { type: 'string', enum: ['A-writing', 'B-recompute', 'C-new-analysis', 'D-author-decision'] }, file: { type: 'string' }, locator: { type: 'string' }, old_text: { type: ['string', 'null'] }, new_text: { type: ['string', 'null'] }, depends_on_run: { type: ['string', 'null'] }, provenance_token: { type: ['string', 'null'] }, justification_type: { type: 'string', enum: ['more-correct', 'clearer'] }, edit_class: { type: 'string', enum: ['presentation', 'additive-verified', 'numeric', 'result-suppressing', 'claim-altering'] }, author_signoff_required: { type: 'boolean' }, reverify_angles: { type: 'array', items: { type: 'string' } }, edit_intent: { type: 'string', enum: ['defect-fix', 'proportional-caveat', 'presentation'] }, proportionality_note: { type: ['string', 'null'] } }, required: ['edit_id', 'finding_id', 'lane', 'file', 'locator', 'old_text', 'new_text', 'depends_on_run', 'provenance_token', 'justification_type', 'edit_class', 'author_signoff_required', 'reverify_angles'] }
const EDIT_SPEC = { type: 'object', additionalProperties: false, properties: { edits: { type: 'array', items: EDIT } }, required: ['edits'] }
const RUNREC = { type: 'object', additionalProperties: false, properties: { run_id: { type: 'string' }, status: { type: 'string', enum: ['ok', 'failed', 'baseline-failed'] }, command: { type: 'string' }, provenance_tokens: { type: 'array', items: { type: 'object', additionalProperties: false, properties: { value: { type: 'string' }, script: { type: 'string' }, line_or_chunk: { type: 'string' }, run_id: { type: 'string' }, input_data_hash: { type: 'string' }, output_file: { type: 'string' }, output_hash: { type: 'string' } }, required: ['value', 'script', 'line_or_chunk', 'run_id', 'input_data_hash', 'output_file', 'output_hash'] } }, log_excerpt: { type: 'string' } }, required: ['run_id', 'status', 'command', 'provenance_tokens', 'log_excerpt'] }
const SCRIBE_RESULT = { type: 'object', additionalProperties: false, properties: { edit_id: { type: 'string' }, status: { type: 'string' }, diff: { type: 'string' }, commit: { type: 'string' }, new_text: { type: 'string' } }, required: ['edit_id', 'status', 'diff', 'commit', 'new_text'] }
const SCRIBE_BATCH_SCHEMA = { type: 'object', additionalProperties: false, properties: { results: { type: 'array', items: SCRIBE_RESULT } }, required: ['results'] }
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
  'human-voice': 'Does this edit read as the AUTHOR wrote it, not AI? Judge against the author-voice standard in prompts/phase2/12_scribe_implementer.md and GROUND it with the deterministic counter: quote an adjacent author sentence as the benchmark and run the style gate (`python <STYLE_GATE_PATH> check --inserted-file <new_text> --baseline-file <benchmark>`), quoting its JSON as your style diff. Map its verdict: banned or antithesis => rejected; spike or no-baseline => cant-tell (routes to author sign-off; a rate spike is never an auto-reject because a legitimate author may use dashes); clean + your own read => upheld. No quoted benchmark and no gate output => cant-tell, never upheld.',
}

// ---------- Intake ----------
phase('Intake')
const scope = await cast('intake', promptRef('phase2/10_intake', { LEDGER_PATH: PATHS.ledger_path || JSON.stringify(LEDGER), INPUT_MANIFEST_JSON: INPUTS, RULES_PATH: PATHS.rules || '' }), { ...GP, label: 'intake', phase: 'Intake', schema: SCOPE })
log('Intake: ' + scope.achievable_scope.length + ' achievable, ' + scope.degraded.length + ' degraded, ' + scope.blocking_gaps.length + ' blocking')
if (scope.blocking_gaps.length) {
  // FAIL CLOSED: surface every blocking gap for the author to fill (or to accept the
  // degraded scope) BEFORE any edit, never proceed silently just because some source exists.
  return { halted: 'blocking_gaps', scope, casting: CASTING() }
}

// ---------- Triage ----------
phase('Triage')
const spec = await cast('triage', promptRef('phase2/11_triage', { LEDGER_PATH: PATHS.ledger_path || JSON.stringify(LEDGER), INPUT_MANIFEST_JSON: INPUTS, RULES_PATH: PATHS.rules || '', IMPROVEMENT_MODE: IMPROVE_NOTE }), { ...GP, label: 'triage', phase: 'Triage', schema: EDIT_SPEC })
const edits = spec.edits || []
log('Triage: ' + edits.length + ' edits (' + edits.filter(e => e.lane === 'A-writing').length + ' writing, ' + edits.filter(e => e.lane === 'B-recompute').length + ' recompute, ' + edits.filter(e => e.lane === 'C-new-analysis').length + ' new-analysis, ' + edits.filter(e => e.lane === 'D-author-decision').length + ' author-decision)' + (IMPROVE ? ' [improvement mode ON, ' + TIER + ']' : ''))

// ---------- Baseline gate ----------
// Run whenever code+data exist (not only for B-recompute edits): the package clean-room
// check and the reconciler both need a baseline anchor, so a writing-only run that has the
// code should still establish one. The Runner derives reproduced/baseline-failed from the
// deterministic reproduces.py predicate, not LLM judgment.
phase('Baseline')
let baseline = { run_id: 'baseline', status: 'ok', command: '(skipped: no code/data provided)', provenance_tokens: [], log_excerpt: '' }
let baselineRan = false
if (INPUTS.code && INPUTS.data) {
  baseline = await cast('runner', promptRef('phase2/13_runner_rerun', { FINDING_JSON: { note: 'BASELINE REPRODUCTION GATE, run the master script unchanged and confirm the current headline numbers reproduce. Take the paper\'s current numbers from the manuscript source below; record exactly which numbers you anchored.', manuscript_source: INPUTS.source || '(none provided, anchor on the code\'s own published-output comparison if available, and record that no manuscript anchor existed)' }, EDIT_JSON: {}, CODE_DIR: INPUTS.code, DATA_DIR: INPUTS.data, RUN_DIR: (PATHS.session || '.') + '/phase2/runs/baseline', SANDBOX_NOTES_PATH: PATHS.sandbox_notes || '', HELPERS_DIR }), { ...GP, label: 'baseline-gate', phase: 'Baseline', schema: RUNREC })
  baselineRan = true
  log('Baseline: ' + baseline.status)
  // FAIL CLOSED on ANY non-ok status: 'baseline-failed' (numbers diverge) and 'failed'
  // (the run crashed) both mean there is no reproduced baseline to edit on top of.
  if (baseline.status !== 'ok') {
    return { halted: 'baseline-' + (baseline.status === 'baseline-failed' ? 'failed' : 'run-error'), scope, baseline, casting: CASTING() }
  }
}

// ---------- Stage the working copy (the git branch the Scribe commits each edit to) ----------
// The Scribe must edit a COPY on a branch, never the author's original (grounding rule 12).
// Nothing downstream can resolve an annotated path string, so we materialize a real working
// tree here and thread its ABSOLUTE path into Scribe / Reconcile / Package.
phase('Stage')
const WORK_BRANCH = 'paper-workshop/phase2'
let workDir = INPUTS.source || INPUTS.manuscript_text || ''
if (INPUTS.source) {
  const staged = await cast('stage',
    'Create the Act-II working copy the Scribe will edit, NEVER touch the author\'s original. Using Bash:\n' +
    '1) mkdir -p "' + (PATHS.session || '.') + '/phase2/work"\n' +
    '2) copy the ENTIRE manuscript source tree from "' + INPUTS.source + '" into that work dir, preserving the \\input/child-file structure (use cp -a / robocopy / xcopy as the OS requires).\n' +
    '3) cd into the work dir and run: git init -q && git add -A && git commit -q -m "act2 baseline (verbatim author source)" && git checkout -q -b ' + WORK_BRANCH + '\n' +
    '4) Return the ABSOLUTE path of the work dir, the branch name, and git_ok. If git is unavailable, still copy the tree and return git_ok:false (edits are then tracked by unified diff, not commits).',
    { ...GP, label: 'stage-worktree', phase: 'Stage', schema: { type: 'object', additionalProperties: false, properties: { work_dir: { type: 'string' }, branch: { type: 'string' }, git_ok: { type: 'boolean' } }, required: ['work_dir', 'branch', 'git_ok'] } })
  workDir = staged.work_dir || workDir
  log('Stage: working copy at ' + workDir + ' (branch ' + (staged.branch || WORK_BRANCH) + ', git ' + (staged.git_ok ? 'ok' : 'unavailable') + ')')
} else if (INPUTS.manuscript_text) {
  // Referee / PDF-only context: no editable source TREE, but the manuscript TEXT exists
  // (e.g. reconstructed/extracted text). Stage a single-file working copy from it so the
  // writing-lane redline is produced THROUGH the guarded Scribe + panel + Package, never
  // hand-rolled outside the Atelier. Numeric findings still degrade to author-decision
  // (no code/data to re-run, baseline gate stays skipped); this path implements lane-A
  // writing edits only, and the Reconcile orphan check still blocks any number that moved.
  const staged = await cast('stage',
    'Create the Act-II working copy from the manuscript TEXT substrate (referee / PDF-only context; no source tree). Using Bash:\n' +
    '1) mkdir -p "' + (PATHS.session || '.') + '/phase2/work"\n' +
    '2) copy the manuscript text file from "' + INPUTS.manuscript_text + '" into that work dir, keeping its filename; this single file IS the editable substrate the Scribe edits.\n' +
    '3) cd into the work dir and run: git init -q && git add -A && git commit -q -m "act2 baseline (manuscript text substrate)" && git checkout -q -b ' + WORK_BRANCH + '\n' +
    '4) Return the ABSOLUTE path of the work dir, the branch name, and git_ok. If git is unavailable, still copy the file and return git_ok:false (edits tracked by unified diff).',
    { ...GP, label: 'stage-text', phase: 'Stage', schema: { type: 'object', additionalProperties: false, properties: { work_dir: { type: 'string' }, branch: { type: 'string' }, git_ok: { type: 'boolean' } }, required: ['work_dir', 'branch', 'git_ok'] } })
  workDir = staged.work_dir || workDir
  log('Stage: manuscript-text working copy at ' + workDir + ' (referee/PDF-only writing-lane redline; branch ' + (staged.branch || WORK_BRANCH) + ', git ' + (staged.git_ok ? 'ok' : 'unavailable') + ')')
}
// Fail closed: if we expected to stage a working copy (a source tree or a manuscript-text
// substrate was provided) but staging did not produce one DISTINCT from the author's original,
// refuse to edit that original in place (grounding rule 12). Halt rather than fall back to it.
if ((INPUTS.source || INPUTS.manuscript_text) && (!workDir || workDir === INPUTS.source || workDir === INPUTS.manuscript_text)) {
  return { halted: 'stage-failed', reason: 'no working copy was staged distinct from the author original; refusing to edit it in place (grounding rule 12)', scope, casting: CASTING() }
}

// ---------- Implement (Runners parallel, Scribes sequential) + Verify (batched by angle) ----------
// Structural defaults since v0.7.0, in EVERY mode (field-proven on a real Act II run):
// the Runners fan out in parallel (they write only into per-edit run dirs, never the
// manuscript); the Scribes run SEQUENTIALLY in batches, because the edits typically target
// one main.tex on one git branch and per-edit parallel scribes would race on the file and
// the commit history; the verification panel is batched BY ANGLE ACROSS edits (panel cost =
// angles x ceil(edits/batch), not edits x angles), with identical decideEdit() gating.
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
  // upheld. A missing verdict (a dropped verifier) or a 'cant-tell' is NOT a free pass, // such an edit may never auto-apply; it routes to author sign-off instead.
  const requiredHard = anglesForEdit(e).filter(a => hard.includes(a))
  const upheld = a => verdicts.some(v => v.angle === a && (v.verdict === 'upheld' || v.verdict === 'upheld-with-revision'))
  const unresolved = requiredHard.filter(a => !upheld(a))
  // record-touching edits always wait for the human, even when clean
  const mustSignoff = e.author_signoff_required || ['numeric', 'result-suppressing', 'claim-altering'].includes(e.edit_class)
  if (e.lane === 'C-new-analysis' || e.lane === 'D-author-decision') return { ...wrap(e, run, scribe, verdicts), status: 'proposal' }
  if (unresolved.length) return { ...wrap(e, run, scribe, verdicts), status: 'queued-for-signoff', reason: 'unverified hard-gate angle(s), not auto-applied: ' + unresolved.join(', ') }
  return { ...wrap(e, run, scribe, verdicts), status: mustSignoff ? 'queued-for-signoff' : 'applied' }
}
function wrap(e, run, scribe, verdicts) { return { edit: e, run, scribe, verdicts } }

// 1) Runners, in parallel: lane B re-runs and lane C drafted analyses write only into
// per-edit run dirs, never the manuscript. Lane D never runs code or edits.
const runById = {}
const runLaneEdits = edits.filter(e => e.lane === 'B-recompute' || e.lane === 'C-new-analysis')
const runResults = (await parallel(runLaneEdits.map(e => () =>
  cast('runner', promptRef('phase2/13_runner_rerun', { FINDING_JSON: { finding_id: e.finding_id }, EDIT_JSON: e, CODE_DIR: INPUTS.code || '(none)', DATA_DIR: INPUTS.data || '(none)', RUN_DIR: (PATHS.session || '.') + '/phase2/runs/' + e.edit_id, SANDBOX_NOTES_PATH: PATHS.sandbox_notes || '', HELPERS_DIR }), { ...GP, label: ('run:' + e.edit_id).slice(0, 56), phase: 'Implement', schema: RUNREC })
    .then(r => ({ id: e.edit_id, run: r }))
))).filter(Boolean)
runResults.forEach(r => { runById[r.id] = r.run })

// 2) Scribes, SEQUENTIAL batches on the one working copy. Pass ALL of the Runner's tokens
// (a numeric edit often needs several values: coefficient + SE + N); the Scribe
// transcribes only token-bound values either way.
const editWithTok = e => {
  const toks = (runById[e.edit_id] && runById[e.edit_id].provenance_tokens) || []
  const tok = toks.length ? JSON.stringify(toks.length === 1 ? toks[0] : toks) : (e.provenance_token || '')
  return { ...e, provenance_token: tok || e.provenance_token }
}
const scribeEdits = edits.filter(e => e.lane !== 'D-author-decision').map(editWithTok)
const dEdits = edits.filter(e => e.lane === 'D-author-decision')
const scribeById = {}
for (let i = 0; i < scribeEdits.length; i += SCRIBE_BATCH) {
  const b = scribeEdits.slice(i, i + SCRIBE_BATCH)
  const sb = await cast('scribe',
    promptRef('phase2/12_scribe_implementer', { EDIT_JSON: '(BATCH MODE, see EDITS_BATCH_JSON appended below; apply the full prompt procedure to EACH edit, in order)', SOURCE_FILE_PATH: workDir + '  (each edit names its own file; resolve as <this work dir>/<edit.file>)', WORKING_BRANCH: WORK_BRANCH, RULES_PATH: PATHS.rules || '' }) +
    '\nBATCH MODE (orchestrator instruction): you are implementing ' + b.length + ' edits in ONE session, IN ORDER, on the SAME working copy. For EACH edit follow the prompt file\'s procedure completely (locate the exact span, apply, one git commit per edit, capture the per-edit unified diff). If one edit\'s old_text cannot be located, mark THAT edit blocked-span-not-found and continue with the rest.\nEDITS_BATCH_JSON:\n' + JSON.stringify(b, null, 2) +
    '\nReturn {results:[{edit_id, status, diff, commit, new_text}]} with one entry PER edit via StructuredOutput.',
    { ...GP, label: 'scribe:batch' + Math.floor(i / SCRIBE_BATCH), phase: 'Implement', schema: SCRIBE_BATCH_SCHEMA })
  ;((sb && sb.results) || []).forEach(r => { scribeById[r.edit_id] = r })
}
// A scribe row the batch agent dropped or mis-keyed fails CLOSED downstream (the verifiers
// see null text and the edit routes to sign-off, and a dirty tree is caught by the
// Reconcile terminal gate), but the gap must be visible, never silent:
if (Object.keys(scribeById).length < scribeEdits.length) log('WARNING: ' + (scribeEdits.length - Object.keys(scribeById).length) + ' scribe result row(s) missing or mis-keyed; the affected edits route to author sign-off (fail closed), check the working-copy git log against the change map')
log('Implement: ' + runResults.length + ' re-runs, ' + Object.keys(scribeById).length + '/' + scribeEdits.length + ' edits scribed (' + dEdits.length + ' author-decision proposals not scribed)')

// 3) Verify, batched by angle across edits. decideEdit() gating is unchanged: a missing or
// cant-tell hard-gate verdict still routes the edit to sign-off, never auto-apply.
phase('Verify')
const allEdits = edits.map(e => (e.lane === 'D-author-decision' ? e : (scribeEdits.find(t => t.edit_id === e.edit_id) || e)))
const tgtFor = e => ({ id: e.edit_id, edit: e, scribe_new_text: (scribeById[e.edit_id] && scribeById[e.edit_id].new_text) || null, run_summary: runById[e.edit_id] ? { status: runById[e.edit_id].status, tokens: runById[e.edit_id].provenance_tokens || [] } : null })
const angleTargets = {}
allEdits.forEach(e => anglesForEdit(e).forEach(a => { (angleTargets[a] = angleTargets[a] || []).push(tgtFor(e)) }))
const vTasks = []
Object.keys(angleTargets).forEach(ang => {
  const ts = angleTargets[ang]
  for (let i = 0; i < ts.length; i += VBATCH) {
    const b = ts.slice(i, i + VBATCH)
    vTasks.push(() => cast('verify', promptRef('05_verification_panel', { ANGLE: ang, ANGLE_QUESTION: ANGLE_Q[ang] || ('Judge from the ' + ang + ' angle.'), TARGETS_JSON: b, PAPER_TXT_PATH: workDir + '  (the working copy; each target\'s edit.file names the file to read)', STAGED_SOURCES_DIR: PATHS.staged_sources || '(none)', QUOTE_GATE_PATH: PATHS.quote_gate || '', STYLE_GATE_PATH: PATHS.style_gate || (HELPERS_DIR ? HELPERS_DIR + '/style_gate.py' : ''), RULES_PATH: PATHS.rules || '', RUBRIC_PATH: PATHS.rubric || '' }), { ...GP, label: ('vfy:' + ang + ':b' + Math.floor(i / VBATCH)).slice(0, 56), phase: 'Verify', schema: VERIF_BATCH }))
  }
})
const vRes = (await parallel(vTasks)).filter(Boolean)
const vById = {}
vRes.forEach(r => (r.verdicts || []).forEach(v => { (vById[v.target_id] = vById[v.target_id] || []).push(v) }))
const results = allEdits.map(e => decideEdit(e, runById[e.edit_id] || null, scribeById[e.edit_id] || null, vById[e.edit_id] || []))

const applied = results.filter(r => r.status === 'applied')
const queued = results.filter(r => r.status === 'queued-for-signoff')
const proposals = results.filter(r => r.status === 'proposal')
const blocked = results.filter(r => r.status === 'blocked')
log('Verify: ' + vTasks.length + ' batched verifier agents; ' + applied.length + ' auto-applied, ' + queued.length + ' queued for sign-off, ' + proposals.length + ' proposals, ' + blocked.length + ' blocked')

// ---------- Reconcile ----------
phase('Reconcile')
const runArtifacts = results.map(r => r.run).filter(Boolean).flatMap(r => r.provenance_tokens || [])
// Consumed-token split (field-grounded): the deterministic run-match must run over the
// tokens a scribed edit actually transcribed; tokens a run produced but no edit consumed
// (raw IRF points, unrounded intermediates) are documented byproducts, never failures, // without this split, every descriptive run that computes more than it inserts dirties
// the reconcile. Orphan detection is unaffected: it works off the manuscript-vs-baseline
// diff, so a number that changed without a consumed token behind it still blocks.
const consumedTokens = results.filter(r => r.scribe && !/blocked/.test(r.scribe.status || '')).map(r => r.run).filter(Boolean).flatMap(r => r.provenance_tokens || [])
const unconsumedTokens = runArtifacts.filter(t => consumedTokens.indexOf(t) === -1)
const reconcile = await cast('reconcile', promptRef('phase2/14_consistency_reconciler', { REVISED_SOURCE_PATH: workDir, BASELINE_SOURCE_PATH: INPUTS.source || INPUTS.manuscript_text || '(none)', RUN_ARTIFACTS_JSON: consumedTokens, UNCONSUMED_TOKENS_JSON: unconsumedTokens, BASELINE_NUMBERS_JSON: baseline.provenance_tokens || [], RUN_DIR: (PATHS.session || '.') + '/phase2/runs/reconcile', HELPERS_DIR }), { ...GP, label: 'reconcile', phase: 'Reconcile', schema: RECON })
const reconcileClean = !reconcile.orphans.length && !reconcile.mismatches.length && !reconcile.run_mismatches.length && !(reconcile.integrity_flags || []).length
log('Reconcile: ' + (reconcileClean ? 'clean' : (reconcile.orphans.length + ' orphans, ' + reconcile.mismatches.length + ' mismatches, ' + reconcile.run_mismatches.length + ' run-mismatches, ' + (reconcile.integrity_flags || []).length + ' integrity-flags')))
// The reconciler is a TERMINAL GATE (prompts/phase2/14): a dirty reconcile blocks "final".
// Halt before packaging - the underlying edits route back; never assemble a "final"
// package on top of orphans, mismatches, or integrity flags. This also deterministically
// backstops a triage misclassification: an edit that changed a number without a token
// surfaces here as an orphan regardless of its edit_class.
if (!reconcileClean) {
  return {
    halted: 'reconcile-failed', scope, baseline_status: baseline.status, baseline_ran: baselineRan,
    casting: CASTING(),
    work_dir: workDir, branch: WORK_BRANCH,
    counts: { edits: edits.length, applied: applied.length, queued_for_signoff: queued.length, proposals: proposals.length, blocked: blocked.length },
    applied, queued_for_signoff: queued, proposals, blocked,
    reconcile, reconcile_clean: false,
    signoff_queue: queued.concat(proposals).map(r => ({ edit_id: r.edit.edit_id, finding_id: r.edit.finding_id, lane: r.edit.lane, edit_class: r.edit.edit_class, status: r.status })),
  }
}

// ---------- Package ----------
phase('Package')
const pkg = await cast('package', promptRef('phase2/15_repro_package', { SESSION_PATH: PATHS.session || '.', INPUT_MANIFEST_JSON: INPUTS, RUN_RECORDS_JSON: results.map(r => r.run).filter(Boolean), REVISED_SOURCE_PATH: workDir, BASELINE_RAN: baselineRan, PACKAGE_DIR: (PATHS.session || '.') + '/phase2/replication_package', SANDBOX_NOTES_PATH: PATHS.sandbox_notes || '', HELPERS_DIR }), { ...GP, label: 'repro-package', phase: 'Package', schema: PACKAGE })

// ---------- Disclose ----------
phase('Disclose')
const auditTrail = { applied: applied.map(r => ({ edit_id: r.edit.edit_id, finding_id: r.edit.finding_id, lane: r.edit.lane, justification: r.edit.justification_type })), queued: queued.map(r => r.edit.edit_id), proposals: proposals.map(r => r.edit.edit_id), blocked: blocked.map(r => ({ edit_id: r.edit.edit_id, reason: r.reason })), signoff_status: 'pending-author-review', improvement_mode: IMPROVE, reruns: results.map(r => r.run).filter(Boolean).map(r => r.run_id), reconcile, package_reproduced: pkg.reproduced }
const disclosure = await cast('disclosure', promptRef('phase2/16_disclosure', { AUDIT_TRAIL_JSON: auditTrail, HELPERS_DIR, REVISED_SOURCE_PATH: workDir }), { ...GP, label: 'disclosure', phase: 'Disclose', schema: DISCLOSURE })

return {
  scope, baseline_status: baseline.status, baseline_ran: baselineRan, work_dir: workDir, branch: WORK_BRANCH,
  casting: CASTING(),
  counts: { edits: edits.length, applied: applied.length, queued_for_signoff: queued.length, proposals: proposals.length, blocked: blocked.length },
  applied, queued_for_signoff: queued, proposals, blocked,
  reconcile, reconcile_clean: reconcileClean,
  package: pkg, package_reproduced: pkg.reproduced,
  deliverables: { redline: pkg.redline_path || null, clean_manuscript: pkg.clean_manuscript_path || null, clean_pdf: pkg.clean_pdf_path || null, tracked_docx: pkg.tracked_docx_path || null, changes_map: pkg.changes_map_path || null, map: pkg.map_path || null, package_dir: pkg.package_dir || null },
  disclosure,
  signoff_queue: queued.concat(proposals).map(r => ({ edit_id: r.edit.edit_id, finding_id: r.edit.finding_id, lane: r.edit.lane, edit_class: r.edit.edit_class, status: r.status })),
}
