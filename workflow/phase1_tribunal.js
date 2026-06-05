export const meta = {
  name: 'paper-workshop-act1-tribunal',
  description: 'Act I (TRIBUNAL): a topic-adapted referee fleet + competing traditions + generalists, every comment cleared by a multi-angle verification panel, synthesized by a fresh chair.',
  phases: [
    { title: 'Cartography', detail: 'ingest the paper into an addressable substrate' },
    { title: 'Roster', detail: 'scout classifies the paper and casts the seats' },
    { title: 'Specialists', detail: 'blind, independent seats + generalists + pre-mortem' },
    { title: 'Quote-gate', detail: 'deterministic grounding of every quote' },
    { title: 'Cross-critique', detail: 'integrators consolidate under rival lenses' },
    { title: 'Verification', detail: 'multi-angle blind verifiers clear every finding' },
    { title: 'Completeness', detail: 'audit coverage of every claim and section' },
    { title: 'Synthesis', detail: 'fresh chair composes the report from verified findings' },
  ],
}

// ---------- args & helpers ----------
const A = args || {}
const PATHS = A.paths || {}
const TIER = A.tier || 'thorough'
const REGISTER = A.register || 'supportive'
const PROMPTS_DIR = PATHS.prompts_dir || ''

// Each seat/verifier reads its OWN prompt template from the installed skill and applies
// the given substitutions to that file's {{TOKEN}} placeholders. Keeps args tiny and makes
// the skill self-contained (it loads its own prompts from disk; nothing is inlined).
const promptRef = (name, vars) =>
  'Your task instructions are in the file: ' + PROMPTS_DIR + '/' + name + '.md\n' +
  'READ that file with your tools and follow it EXACTLY as your role. It contains {{TOKEN}} ' +
  'placeholders — substitute these values (and read any path given as a file):\n' +
  JSON.stringify(vars || {}, null, 2) +
  '\nProduce output strictly matching the required schema.'
const GP = { agentType: 'general-purpose' } // full tool access (Read/Write/Bash)

// ---------- compact inline schemas (mirror schemas/*.json) ----------
const LOC = { type: 'object', additionalProperties: false, properties: { page: { type: ['integer', 'null'] }, section: { type: 'string' }, paragraph: { type: ['integer', 'null'] }, sentence_range: { type: ['string', 'null'] } }, required: ['section'] }
const FINDING = {
  type: 'object', additionalProperties: false,
  properties: {
    id: { type: 'string' }, seat_id: { type: 'string' }, tradition: { type: 'string' },
    finding_type: { type: 'string', enum: ['claim-support', 'identification', 'statistical', 'robustness', 'framing-overclaim', 'related-work', 'citation-accuracy', 'reproducibility', 'ethics-integrity', 'presentation', 'clarity', 'relevance', 'understandability', 'absence-silence'] },
    location: LOC, quote: { type: 'string' }, issue: { type: 'string' }, why_it_matters: { type: 'string' },
    severity: { type: 'string', enum: ['High', 'Medium', 'Low'] },
    magnitude: { type: 'string', enum: ['moves-a-number', 'moves-a-conclusion', 'presentation-only'] },
    proposed_fix: { type: 'string' }, risk_of_fix: { type: 'string' },
    verification_status: { type: 'string', enum: ['quote-verified', 'logic-checked', 'citation-grounded', 'needs-author-confirmation', 'cant-tell'] },
  },
  required: ['id', 'seat_id', 'tradition', 'finding_type', 'location', 'quote', 'issue', 'why_it_matters', 'severity', 'magnitude', 'proposed_fix', 'risk_of_fix', 'verification_status'],
}
const FINDINGS = { type: 'object', additionalProperties: false, properties: { findings: { type: 'array', items: FINDING }, covered_ranges: { type: 'array', items: { type: 'string' } } }, required: ['findings'] }
const SEAT = { type: 'object', additionalProperties: false, properties: { seat_id: { type: 'string' }, role_title: { type: 'string' }, tradition: { type: 'string' }, objective_function: { type: 'string', enum: ['find-the-fatal-flaw', 'find-the-strongest-defensible-version', 'find-what-no-seat-staffed', 'neutral-audit'] }, jurisdiction: { type: 'string' }, justifying_quote: { type: 'string' }, rival_of: { type: ['string', 'null'] }, out_of_scope: { type: 'string' }, owned_claim_ids: { type: 'array', items: { type: 'string' } } }, required: ['seat_id', 'role_title', 'tradition', 'objective_function', 'jurisdiction', 'justifying_quote', 'rival_of', 'out_of_scope', 'owned_claim_ids'] }
const GEN = { type: 'object', additionalProperties: false, properties: { seat_id: { type: 'string' }, function: { type: 'string', enum: ['relevance', 'understandability', 'cross-field-significance'] }, rationale: { type: 'string' } }, required: ['seat_id', 'function', 'rationale'] }
const ROSTER = { type: 'object', additionalProperties: false, properties: { paper_type: { type: 'array', items: { type: 'string' } }, precis: { type: 'string' }, central_tensions: { type: 'array', items: { type: 'string' } }, mandatory_floor: { type: 'array', items: { type: 'string' } }, seats: { type: 'array', items: SEAT }, generalist_seats: { type: 'array', items: GEN }, not_staffed: { type: 'array', items: { type: 'object', additionalProperties: false, properties: { dimension: { type: 'string' }, why: { type: 'string' } }, required: ['dimension', 'why'] } } }, required: ['paper_type', 'precis', 'central_tensions', 'mandatory_floor', 'seats', 'generalist_seats', 'not_staffed'] }
const CARTO = { type: 'object', additionalProperties: false, properties: { paper_txt_path: { type: 'string' }, inventory_path: { type: 'string' }, sentence_map_path: { type: 'string' }, precis_path: { type: 'string' }, source_manifest_path: { type: 'string' }, n_claims: { type: 'integer' }, n_sentences: { type: 'integer' } }, required: ['paper_txt_path', 'inventory_path', 'sentence_map_path', 'precis_path', 'n_claims', 'n_sentences'] }
const VERIF = { type: 'object', additionalProperties: false, properties: { target_id: { type: 'string' }, angle: { type: 'string' }, verdict: { type: 'string', enum: ['upheld', 'upheld-with-revision', 'rejected', 'cant-tell'] }, reason: { type: 'string' }, suggested_revision: { type: ['string', 'null'] } }, required: ['target_id', 'angle', 'verdict', 'reason', 'suggested_revision'] }
const VERIF_BATCH = { type: 'object', additionalProperties: false, properties: { verdicts: { type: 'array', items: VERIF } }, required: ['verdicts'] }
const INTEGRATION = { type: 'object', additionalProperties: false, properties: { lens: { type: 'string' }, clusters: { type: 'array', items: { type: 'object', additionalProperties: false, properties: { theme: { type: 'string' }, finding_ids: { type: 'array', items: { type: 'string' } }, merged_issue: { type: 'string' }, recommended_severity: { type: 'string', enum: ['High', 'Medium', 'Low'] }, priority: { type: 'string', enum: ['must', 'should', 'nice'] } }, required: ['theme', 'finding_ids', 'merged_issue', 'recommended_severity', 'priority'] } }, crux_notes: { type: 'array', items: { type: 'string' } }, missing_issue: { type: 'string' } }, required: ['lens', 'clusters', 'crux_notes', 'missing_issue'] }
const COVERAGE = { type: 'object', additionalProperties: false, properties: { claims_total: { type: 'integer' }, claims_covered: { type: 'integer' }, sentences_total: { type: 'integer' }, sentences_covered: { type: 'integer' }, dimension_coverage: { type: 'array', items: { type: 'object', additionalProperties: false, properties: { dimension: { type: 'string' }, status: { type: 'string' } }, required: ['dimension', 'status'] } }, reopen: { type: 'array', items: { type: 'string' } }, not_covered: { type: 'array', items: { type: 'string' } } }, required: ['claims_total', 'claims_covered', 'sentences_total', 'sentences_covered', 'dimension_coverage', 'reopen', 'not_covered'] }
const SYNTHESIS = { type: 'object', additionalProperties: false, properties: { verdict: { type: 'string' }, top_strengths: { type: 'array', items: { type: 'string' } }, prioritized_findings: { type: 'array', items: { type: 'object', additionalProperties: false, properties: { finding_id: { type: 'string' }, priority: { type: 'string', enum: ['must', 'should', 'nice'] }, one_line: { type: 'string' }, panel_summary: { type: 'string' } }, required: ['finding_id', 'priority', 'one_line', 'panel_summary'] } }, kill_shots: { type: 'array', items: { type: 'string' } }, referee_verdicts: { type: 'array', items: { type: 'object', additionalProperties: false, properties: { seat_id: { type: 'string' }, verdict: { type: 'string' } }, required: ['seat_id', 'verdict'] } }, venue_verdict: { type: 'object', additionalProperties: false, properties: { bucket: { type: 'string', enum: ['desk-reject-risk', 'major-revision', 'competitive'] }, objections: { type: 'array', items: { type: 'object', additionalProperties: false, properties: { objection: { type: 'string' }, quote: { type: 'string' } }, required: ['objection', 'quote'] } }, swing_factor: { type: 'string' } }, required: ['bucket', 'objections', 'swing_factor'] }, validity_verdict: { type: 'string' }, minority_report: { type: 'string' }, rejected_suggestions: { type: 'array', items: { type: 'object', additionalProperties: false, properties: { suggestion: { type: 'string' }, why_rejected: { type: 'string' } }, required: ['suggestion', 'why_rejected'] } }, coverage_certificate: COVERAGE }, required: ['verdict', 'top_strengths', 'prioritized_findings', 'kill_shots', 'referee_verdicts', 'venue_verdict', 'validity_verdict', 'minority_report', 'rejected_suggestions', 'coverage_certificate'] }

// ---------- verification angles ----------
const ANGLE_Q = {
  'quote-locator': 'Does the quote exist verbatim at the stated location? Run the deterministic quote gate via Bash and report its result.',
  'logical-validity': 'Does the criticism actually FOLLOW from the quoted text? A real quote with an invalid inference must be rejected.',
  'factual-literature': 'Is the norm/method/citation the finding appeals to actually correct, checked against staged sources (never memory)?',
  'severity-calibration': 'Is the severity honest under the locked rubric — neither inflated nor deflated?',
  'decision-relevance': 'Would fixing this change a number or a conclusion, or only presentation? Is it non-trivial?',
  'fix-safety': 'Would the proposed fix introduce a NEW error or break a correct passage?',
  'steelman-charity': 'Try hard to DEFEND the paper. Does it already address this elsewhere, or is the criticism mistaken?',
}
function anglesFor(tier) {
  if (tier === 'quick') return ['logical-validity', 'fix-safety', 'steelman-charity']
  if (tier === 'thorough') return ['quote-locator', 'logical-validity', 'severity-calibration', 'decision-relevance', 'fix-safety', 'steelman-charity']
  return ['quote-locator', 'logical-validity', 'factual-literature', 'severity-calibration', 'decision-relevance', 'fix-safety', 'steelman-charity']
}
const REDUNDANCY = (TIER === 'exhaustive' || TIER === 'monumental') ? 2 : 1

// ---------- PHASE A: Cartography ----------
phase('Cartography')
let carto
if (PATHS.paper_txt_path) {
  carto = { paper_txt_path: PATHS.paper_txt_path, inventory_path: PATHS.inventory_path, sentence_map_path: PATHS.sentence_map_path, precis_path: PATHS.precis_path, source_manifest_path: PATHS.source_manifest_path || '', n_claims: A.n_claims || 0, n_sentences: A.n_sentences || 0 }
  log('Cartography: using pre-staged substrate at ' + carto.paper_txt_path)
} else {
  carto = await agent('Read the paper at ' + A.pdf_path + ' (PDF or text). Following the method in ' + PATHS.helpers_dir + '/pdf_extraction.md, write into ' + PATHS.session + '/cartography: paper.txt (verbatim full text — do NOT paraphrase; the quote-gate matches against it), claim_inventory.json, sentence_map.json (disjoint, gapless sentence ranges with ids), precis.md (neutral, no praise/critique), source_manifest.json. Return the paths and counts.', { ...GP, label: 'cartography', phase: 'Cartography', schema: CARTO })
  log('Cartography: ' + carto.n_claims + ' claims, ' + carto.n_sentences + ' sentences')
}
const seatPaths = { PAPER_TXT_PATH: carto.paper_txt_path, INVENTORY_PATH: carto.inventory_path, PRECIS_PATH: carto.precis_path, RULES_PATH: PATHS.rules || '', RUBRIC_PATH: PATHS.rubric || '', STAGED_SOURCES_DIR: PATHS.staged_sources || '(none)', QUOTE_GATE_PATH: PATHS.quote_gate || '', REGISTER }

// ---------- PHASE B: Roster ----------
phase('Roster')
let roster
if (A.roster) {
  roster = A.roster
  log('Roster: using author-approved roster (' + roster.seats.length + ' seats + ' + roster.generalist_seats.length + ' generalists)')
} else {
  roster = await agent(promptRef('00_scout_roster', { BRIEF_PATH: PATHS.brief || '', PAPER_TXT_PATH: carto.paper_txt_path, INVENTORY_PATH: carto.inventory_path, PRECIS_PATH: carto.precis_path, TIER }), { ...GP, label: 'scout:roster', phase: 'Roster', schema: ROSTER })
  log('Roster: ' + roster.paper_type.join('+') + ' — ' + roster.seats.length + ' seats + ' + roster.generalist_seats.length + ' generalists')
}

// ---------- PHASE D: Specialists (blind, independent) ----------
phase('Specialists')
const seatTasks = []
roster.seats.forEach(s => seatTasks.push(() => agent(promptRef('01_specialist_seat', { ...seatPaths, SEAT_JSON: s }), { ...GP, label: ('seat:' + s.seat_id).slice(0, 56), phase: 'Specialists', schema: FINDINGS }).then(r => tag(r, s.seat_id, s.tradition))))
roster.generalist_seats.forEach(g => seatTasks.push(() => agent(promptRef('02_generalist_seat', { ...seatPaths, FUNCTION: g.function }), { ...GP, label: ('gen:' + g.function).slice(0, 56), phase: 'Specialists', schema: FINDINGS }).then(r => tag(r, g.seat_id, g.function + '-generalist'))))
// desk-reject pre-mortem (verbatim, exempt from chair)
seatTasks.push(() => agent(promptRef('03_premortem', { PAPER_TXT_PATH: carto.paper_txt_path, PRECIS_PATH: carto.precis_path, RULES_PATH: PATHS.rules || '' }), { ...GP, label: 'premortem', phase: 'Specialists', schema: FINDINGS }).then(r => tag(r, 'S-premortem', 'desk-reject-premortem')))
// close-reader sweeps at the heavy tiers (sentence-coverage invariant)
const sweeps = (TIER === 'exhaustive' || TIER === 'monumental') ? Math.max(1, Math.ceil((carto.n_sentences || 0) / 40)) : 0
for (let i = 0; i < sweeps; i++) {
  const seat = { seat_id: 'S-closeread-' + i, role_title: 'Close reader', tradition: 'line-by-line close reading', objective_function: 'neutral-audit', jurisdiction: 'sentence ranges block ' + i + ' (read sentence_map.json, review ranges [' + (i * 40) + ',' + ((i + 1) * 40) + ') and return covered_ranges)', justifying_quote: '(coverage sweep)', rival_of: null, out_of_scope: 'other blocks', owned_claim_ids: [] }
  seatTasks.push(() => agent(promptRef('01_specialist_seat', { ...seatPaths, SEAT_JSON: { ...seat, sentence_map_path: carto.sentence_map_path } }) + '\nALSO: read the sentence map at ' + carto.sentence_map_path + ' and return covered_ranges = the list of sentence-range ids you reviewed.', { ...GP, label: 'closeread:' + i, phase: 'Specialists', schema: FINDINGS }).then(r => tag(r, seat.seat_id, seat.tradition)))
}
function tag(r, seatId, tradition) {
  const fs = (r && r.findings) || []
  fs.forEach((f, i) => { f.seat_id = f.seat_id || seatId; f.tradition = f.tradition || tradition; if (!f.id) f.id = seatId + '-F' + (i + 1) })
  return { findings: fs, covered_ranges: (r && r.covered_ranges) || [] }
}
const seatResults = (await parallel(seatTasks)).filter(Boolean)
let findings = []
let coveredRanges = []
seatResults.forEach(r => { findings.push(...r.findings); coveredRanges.push(...(r.covered_ranges || [])) })
// stable global ids
findings.forEach((f, i) => { f.id = 'F-' + String(i + 1).padStart(3, '0') })
const premortemFindings = findings.filter(f => f.tradition === 'desk-reject-premortem')
log('Specialists: ' + findings.length + ' raw findings from ' + seatResults.length + ' seats')

// ---------- Quote-gate ----------
phase('Quote-gate')
if (findings.length) {
  const gate = await agent('Write this findings JSON to a temp file and run the deterministic quote gate against the manuscript text, then return its JSON result array verbatim.\nFINDINGS: ' + JSON.stringify({ findings }) + '\nRun: python "' + (PATHS.quote_gate || '') + '" batch --source-file "' + carto.paper_txt_path + '" --findings <tempfile>\nReturn exactly the script\'s JSON output (array of {id, matched, match_level, severity_hint}).', { ...GP, label: 'quote-gate', phase: 'Quote-gate', schema: { type: 'object', additionalProperties: false, properties: { results: { type: 'array', items: { type: 'object', additionalProperties: false, properties: { id: { type: 'string' }, matched: { type: 'boolean' }, match_level: { type: 'string' } }, required: ['id', 'matched', 'match_level'] } } }, required: ['results'] } })
  const byId = {}
  ;(gate.results || []).forEach(r => { byId[r.id] = r })
  findings.forEach(f => { const r = byId[f.id]; if (r && !r.matched && f.finding_type !== 'absence-silence') { f.verification_status = 'needs-author-confirmation' } })
  log('Quote-gate: ' + (gate.results || []).filter(r => r.matched).length + '/' + (gate.results || []).length + ' quotes verified')
}

// ---------- PHASE E: Cross-critique ----------
phase('Cross-critique')
const LENSES = ['value-maximizer', 'risk-minimizer', 'coherence']
const integration = (await parallel(LENSES.map(L => () => agent(promptRef('04_cross_critique', { ALL_FINDINGS_JSON: findings, LENS: L, RULES_PATH: PATHS.rules || '' }), { ...GP, label: 'integrate:' + L, phase: 'Cross-critique', schema: INTEGRATION })))).filter(Boolean)
// corroboration diagnostic
const locKey = f => (f.location.section || '') + '|' + f.finding_type
const counts = {}
findings.forEach(f => { counts[locKey(f)] = (counts[locKey(f)] || 0) + 1 })

// ---------- PHASE F: Verification panel (BATCHED by angle: cost is ~constant in #findings) ----------
// Each angle reviews findings in batches, so the panel costs angles x ceil(#findings/BATCH) x
// REDUNDANCY agents — NOT findings x angles. Independence is preserved (one blind agent per
// angle/batch, never per-finding-per-angle), but agent count stays feasible.
phase('Verification')
const angles = anglesFor(TIER)
const BATCH = (TIER === 'monumental' ? 25 : TIER === 'exhaustive' ? 20 : 15)
const batches = []
for (let i = 0; i < findings.length; i += BATCH) batches.push(findings.slice(i, i + BATCH))
const panelTasks = []
angles.forEach(ang => batches.forEach((b, bi) => {
  for (let k = 0; k < REDUNDANCY; k++) panelTasks.push(() =>
    agent(promptRef('05_verification_panel', { ANGLE: ang, ANGLE_QUESTION: ANGLE_Q[ang], TARGETS_JSON: b, PAPER_TXT_PATH: carto.paper_txt_path, STAGED_SOURCES_DIR: seatPaths.STAGED_SOURCES_DIR, QUOTE_GATE_PATH: PATHS.quote_gate || '', RULES_PATH: PATHS.rules || '', RUBRIC_PATH: PATHS.rubric || '' }),
      { ...GP, label: ('vfy:' + ang + ':b' + bi + (REDUNDANCY > 1 ? ':r' + k : '')).slice(0, 56), phase: 'Verification', schema: VERIF_BATCH }))
}))
const panelResults = (await parallel(panelTasks)).filter(Boolean)
const verdictsById = {}
panelResults.forEach(r => (r.verdicts || []).forEach(v => { (verdictsById[v.target_id] = verdictsById[v.target_id] || []).push(v) }))
const verified = findings.map(f => decide(f, verdictsById[f.id] || []))
log('Verification: ' + panelTasks.length + ' batched verifier agents over ' + angles.length + ' angles x ' + batches.length + ' batches' + (REDUNDANCY > 1 ? ' x' + REDUNDANCY : ''))

function majority(verdicts, angle) {
  const v = verdicts.filter(x => x.angle === angle)
  if (!v.length) return null
  const rej = v.filter(x => x.verdict === 'rejected').length
  const rev = v.filter(x => x.verdict === 'upheld-with-revision')
  if (rej > v.length / 2) return { verdict: 'rejected', rev }
  return { verdict: rev.length > v.length / 2 ? 'upheld-with-revision' : 'upheld', rev }
}
function decide(f, verdicts) {
  const out = { ...f }
  let delivered = true
  let reject_reason = ''
  // hard gate: logical-validity
  const lv = majority(verdicts, 'logical-validity')
  if (lv && lv.verdict === 'rejected') { delivered = false; reject_reason = 'logical-validity: criticism does not follow from the quote' }
  // steelman defense
  const sm = majority(verdicts, 'steelman-charity')
  if (delivered && sm && sm.verdict === 'rejected') { delivered = false; reject_reason = 'steelman: the paper already addresses this / the criticism is mistaken' }
  // decision-relevance triviality
  const dr = majority(verdicts, 'decision-relevance')
  if (delivered && dr && dr.verdict === 'rejected') { delivered = false; reject_reason = 'decision-relevance: trivial / not decision-relevant' }
  // severity calibration (most conservative downward revision wins)
  const sc = majority(verdicts, 'severity-calibration')
  if (sc && sc.rev && sc.rev.length) {
    const order = { High: 3, Medium: 2, Low: 1 }
    let target = out.severity
    sc.rev.forEach(r => { const m = (r.suggested_revision || '').match(/High|Medium|Low/g); if (m) { const last = m[m.length - 1]; if (order[last] < order[target]) target = last } })
    out.severity = target
  }
  // fix-safety: withhold an unsafe fix but keep the finding
  const fx = majority(verdicts, 'fix-safety')
  if (fx && fx.verdict === 'rejected') { out.risk_of_fix = 'WITHHELD by fix-safety verifier: ' + (out.risk_of_fix || 'proposed fix may introduce a new error'); out.proposed_fix = '' }
  // quote-locator handled in quote-gate; ensure status reflects logic-check pass
  if (delivered && out.verification_status === 'quote-verified' && lv && lv.verdict !== 'rejected') out.verification_status = 'logic-checked'
  return { finding: out, verdicts, delivered, reject_reason }
}
const deliveredFindings = verified.filter(v => v.delivered).map(v => v.finding)
const rejected = verified.filter(v => !v.delivered).map(v => ({ suggestion: v.finding.issue, why_rejected: v.reject_reason }))
deliveredFindings.forEach(f => { f.raised_by_n_blind_seats = counts[locKey(f)] || 1 })
log('Verification: ' + deliveredFindings.length + ' findings cleared the panel; ' + rejected.length + ' rejected')

// ---------- PHASE H: Completeness ----------
phase('Completeness')
const coverage = await agent(promptRef('07_completeness_audit', { CLAIM_INVENTORY_PATH: carto.inventory_path, SENTENCE_MAP_PATH: carto.sentence_map_path, COVERED_LOCATIONS_JSON: { covered_ranges: coveredRanges, finding_locations: deliveredFindings.map(f => f.location) }, COVERAGE_RUBRIC_PATH: PATHS.coverage_rubric || '' }), { ...GP, label: 'completeness', phase: 'Completeness', schema: COVERAGE })
log('Completeness: claims ' + coverage.claims_covered + '/' + coverage.claims_total + ', sentences ' + coverage.sentences_covered + '/' + coverage.sentences_total + ', reopen=' + coverage.reopen.length)

// ---------- PHASE G: Synthesis ----------
phase('Synthesis')
const synthesis = await agent(promptRef('06_chair_synthesis', { VERIFIED_FINDINGS_JSON: deliveredFindings, INTEGRATION_JSON: integration, PREMORTEM_JSON: premortemFindings, COVERAGE_JSON: coverage, REGISTER, RULES_PATH: PATHS.rules || '', RUBRIC_PATH: PATHS.rubric || '' }), { ...GP, label: 'chair:synthesis', phase: 'Synthesis', schema: SYNTHESIS })

return {
  tier: TIER, register: REGISTER,
  roster: { paper_type: roster.paper_type, seats: roster.seats.length, generalists: roster.generalist_seats.length, central_tensions: roster.central_tensions, not_staffed: roster.not_staffed },
  counts: { raw_findings: findings.length, delivered: deliveredFindings.length, rejected: rejected.length },
  findings: deliveredFindings,
  rejected_in_panel: rejected,
  integration,
  coverage,
  synthesis,
}
