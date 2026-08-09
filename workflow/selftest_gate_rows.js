// Selftest for the deterministic quote-locator audit row.
//
// Act I removed the LLM `quote-locator` panel angle: the deterministic quote/absence gates
// already run at the Phase-D barrier and their result is already enforced there, so a panel
// agent re-running the same script added no judgment (decide() never reads that angle). The row
// is now transcribed in code, and this test is what keeps that transcription honest.
//
// It extracts the REAL gateRow() out of workflow/phase1_tribunal.js between its sentinels and
// runs it, so the test cannot drift away from the shipped logic. Run: node workflow/selftest_gate_rows.js
'use strict'
const fs = require('fs')
const path = require('path')

const root = path.join(__dirname, '..')
const src = fs.readFileSync(path.join(root, 'workflow', 'phase1_tribunal.js'), 'utf8')
const m = src.match(/\/\/ <gate-row-fn>\r?\n([\s\S]*?)\/\/ <\/gate-row-fn>/)
if (!m) {
  console.error('FAIL: could not find the <gate-row-fn> sentinels in workflow/phase1_tribunal.js')
  process.exit(1)
}
// eslint-disable-next-line no-new-func
const gateRow = new Function(m[1] + '\nreturn gateRow')()

let ok = true
function expect(name, cond) {
  console.log((cond ? '  PASS ' : '  FAIL ') + name)
  ok = ok && cond
}
const F = (type, extra) => Object.assign({ id: 'F-001', finding_type: type }, extra || {})
const matched = { id: 'F-001', matched: true, match_level: 'normalized' }
const unmatched = { id: 'F-001', matched: false, match_level: 'none' }
const certAbsent = { absence_gate: { certified: 'absent' } }
const certPresent = { absence_gate: { certified: 'present' } }
const certNoResult = { absence_gate: { certified: 'no-result' } }

console.log('== ordinary (quote-gated) finding ==')
expect('matched quote -> upheld', gateRow(F('statistical'), matched).verdict === 'upheld')
expect('matched quote -> no revision asked', gateRow(F('statistical'), matched).suggested_revision === null)
expect('unmatched quote -> upheld-with-revision', gateRow(F('statistical'), unmatched).verdict === 'upheld-with-revision')
expect('unmatched quote -> revision names needs-author-confirmation',
  /needs-author-confirmation/.test(gateRow(F('statistical'), unmatched).suggested_revision))
expect('MISSING gate row -> cant-tell (not a verdict we did not obtain)',
  gateRow(F('statistical'), undefined).verdict === 'cant-tell')
expect('missing gate row still asks for needs-author-confirmation',
  /needs-author-confirmation/.test(gateRow(F('statistical'), undefined).suggested_revision))

console.log('== absence-silence: quote-EXEMPT, absence-gated ==')
expect('exempt quote + absent certificate -> upheld',
  gateRow(F('absence-silence', certAbsent), undefined).verdict === 'upheld')
expect('exempt quote + PRESENT certificate -> upheld-with-revision',
  gateRow(F('absence-silence', certPresent), undefined).verdict === 'upheld-with-revision')
expect('exempt quote + no certificate -> cant-tell',
  gateRow(F('absence-silence'), undefined).verdict === 'cant-tell')
expect('exempt quote reported as exempt-absence in the reason',
  /quote_gate=exempt-absence/.test(gateRow(F('absence-silence', certAbsent), undefined).reason))

console.log('== contribution-undersell / improvement-proposal: BOTH gates ==')
for (const t of ['contribution-undersell', 'improvement-proposal']) {
  expect(t + ': matched quote + absent certificate -> upheld',
    gateRow(F(t, certAbsent), matched).verdict === 'upheld')
  // the regression this test exists for: a clean absence certificate must NOT rescue a
  // foothold quote that the quote gate rejected
  expect(t + ': UNMATCHED quote + absent certificate -> NOT upheld',
    gateRow(F(t, certAbsent), unmatched).verdict !== 'upheld')
  expect(t + ': matched quote + present certificate -> NOT upheld',
    gateRow(F(t, certPresent), matched).verdict !== 'upheld')
  expect(t + ': matched quote + no-result certificate -> cant-tell',
    gateRow(F(t, certNoResult), matched).verdict === 'cant-tell')
}

console.log('== shape + cross-file consistency ==')
const row = gateRow(F('statistical'), matched)
expect('angle is quote-locator', row.angle === 'quote-locator')
expect('target_id echoes the finding id', row.target_id === 'F-001')
const VERDICTS = ['upheld', 'upheld-with-revision', 'rejected', 'cant-tell']
expect('every verdict emitted is in the verification schema enum', [
  gateRow(F('statistical'), matched), gateRow(F('statistical'), unmatched), gateRow(F('statistical'), undefined),
  gateRow(F('absence-silence', certAbsent), undefined), gateRow(F('contribution-undersell', certPresent), matched),
].every(r => VERDICTS.indexOf(r.verdict) >= 0))
expect('reason states the row is not an LLM verdict', /not an LLM verdict/.test(row.reason))

// the row builder's absence-class list must agree with the Python gate's ABSENCE_CLASSES
const py = fs.readFileSync(path.join(root, 'helpers', 'absence_gate.py'), 'utf8')
const pyList = (py.match(/ABSENCE_CLASSES\s*=\s*[{(\[]([^})\]]*)[})\]]/) || [])[1] || ''
const pyTypes = (pyList.match(/"[^"]+"|'[^']+'/g) || []).map(s => s.slice(1, -1)).sort()
const jsTypes = (m[1].match(/const ABSENCE_TYPES = \[([^\]]*)\]/) || [, ''])[1]
  .split(',').map(s => s.trim().replace(/^'|'$/g, '')).filter(Boolean).sort()
expect('JS ABSENCE_TYPES matches absence_gate.py ABSENCE_CLASSES (' + jsTypes.join(',') + ')',
  pyTypes.length > 0 && JSON.stringify(pyTypes) === JSON.stringify(jsTypes))

console.log(ok ? 'selftest: OK' : 'selftest: FAILED')
process.exit(ok ? 0 : 1)
