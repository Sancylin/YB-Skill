#!/usr/bin/env python3
"""Offline intake/coverage/identity gates. Screenshots and reviews judge visual quality; this script does not."""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from runlib.checks import content_diff, finite, fill_errors
from runlib.images import verify_image

REVISIONS = ('requirements', 'plan', 'design', 'library')
ARRAYS = ('evidence', 'sources', 'requirements', 'units', 'assumptions', 'reviews',
          'issues', 'slots', 'capabilities', 'implementations', 'localComponents', 'checks', 'captures')
PROTECTED = {'font','textStyle','variables','fills','effects','internalLayout'}
SNAPSHOT = {'ancestorIds','targetId','type','nodeId','sourceAssetKey','mainComponentKey','mainComponentId','properties','content','layout','name','parentId','overrides','protected'}
KINDS = {'source','authorization','plan','task','constraint','screenshot','baseline','reference','tool','review','verification','packet'}
OVERRIDE_KINDS = {'public-property','allowed-text','outer-layout','description-fill'}
HINT_FILL_ACTION = 'hide-fill'
RESOLUTION_STEPS = ('formal-instance','compose','gap')
SEARCH_SOURCES = ('semantic','page-routed','inventory','published-name')
INTAKE_MODES = ('text','prd-file')
DELIVERABLE_CHOICES = ('figma','web-demo','both')
DELIVERABLE_SOURCES = ('user-specified','asked','fallback')
INTERACTION_LEVELS = ('design','executed','not-applicable')
PROFILE_LEVELS = ('fast','standard','full')
PROFILE_SOURCES = ('auto','user')
COMPONENT_COVERAGE = ('known-existing','likely-existing','unknown')
AMBIGUITY_LEVELS = ('low','medium','high')
REQUIRED_TASK_SIMULATIONS = {'happy-path','first-use','error','interrupt','post-success'}
LAYOUT_MEASUREMENT_KINDS = {'edge-alignment','spacing-consistency','padding-pair','baseline-alignment','custom'}
PLAN_REVIEW_FLAGS = ('requiresPlanReview','structureChange','businessResultChanged')
CHANGE_IMPACTS = ('information-architecture-change','main-action-change','business-result-change')
REFERENCE_ORIGINS = ('built-in','target-file','user')
REFERENCE_SOURCE_KINDS = ('component-library-template','target-existing-page','user-reference')
REFERENCE_DECISIONS = ('matched','no-match','not-applicable')
REFERENCE_REUSE_ACTIONS = ('direct-reuse','adapt-reuse','reference-only')
REFERENCE_CHANGE_SCOPES = ('flow-order','content','states','outer-layout','navigation','responsive')
EXISTING_PAGE_SCAN_STATUSES = ('scanned','not-applicable')
BUILTIN_REFERENCE_ID = 'yuanbao-component-template'
BUILTIN_REFERENCE_FILE_KEY = 'iUyH8VSdURxlGrhp646zYJ'
BUILTIN_REFERENCE_SOURCE_KIND = 'component-library-template'
BUILTIN_REFERENCE_PAGE_NAME = '【AI参考案例】Template'
NEXT_ACTIONS = ('resume-plan','resume-resolve','resume-build','resume-review','resume-verify','deliver','report','wait-user')
STAGES = ('intake','experience-plan','experience-review','plan','plan-review','resolve','capability','build','blind-review',
          'system-audit','fix','verify','deliver','report')
PACKET_REQUIRED = {'schemaVersion','stage','reviewerId','revision','unitIds','evidenceRefs'}
PACKET_LEAK = {'previousVerdict','verdict','issueIds','findings','issues'}
VISUAL_OK_ROOTS = ('/name','/parentId','/layout','/properties','/content','/overrides','/ancestorIds','/mainComponentKey')
WHITELIST_ROOTS = VISUAL_OK_ROOTS + ('/protected',)


def skeleton():
    return dict(schemaVersion=3, runId='', mode='generate', deliverable='web-demo',
                environment='live', status='running', stage='intake', designerId='',
                revision={k:'pending' for k in REVISIONS},
                authorization={'write':False,'fix':False,'requirePlanConfirmation':False,'scope':[],'evidenceRefs':[]},
                intake={'inputMode':'','deliverableDecision':{'source':'','userChoice':None,'fallbackReason':None,'evidenceRefs':[]},'prdArtifact':None,'sourceDocs':[],'rewritePolicy':'','rewriteAuthorization':None,'clarifications':[]},
                referenceReview={'status':'pending','sources':[]},
                executionProfile={'level':'','source':'auto','assessment':{},'requiredSimulations':[],'reasons':[],'escalationHistory':[]},
                experienceDecision={'status':'pending','taskIds':[],'chosenModels':[],'confidence':'','evidenceRefs':[]},
                planEvidenceRefs=[], taskEvidenceRefs=[], nextAction='', blockers=[],
                **{k:[] for k in ARRAYS})


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def changes(before, after, prefix=''):
    if isinstance(before, dict) and isinstance(after, dict):
        result=[]
        for key in before.keys() | after.keys():
            path=f'{prefix}/{key}'
            if key not in before or key not in after: result.append(path)
            else: result.extend(changes(before[key], after[key], path))
        return result
    return [] if before == after else [prefix or '/']


class Gate:
    def __init__(self, run, root, gate, allow_fixture=False):
        self.r=run; self.root=root.resolve(); self.gate=gate
        self.allow_fixture=allow_fixture; self.errors=[]; self.ev={}; self.units={}; self.req={}

    def need(self, condition, message):
        if not condition: self.errors.append(message)
        return bool(condition)

    def text(self, value):
        return isinstance(value,str) and bool(value.strip()) and value not in {'pending','unresolved'}

    def valid_description_fill_adjustments(self, key, impl, baseline, after):
        adjustments=impl.get('descriptionFillAdjustments')
        ok=True
        if not (isinstance(adjustments,list) and adjustments):
            self.need(False,f'{key}: descriptionFillAdjustments must be a non-empty list');return False
        desc=baseline.get('description')
        if not self.text(desc):
            self.need(False,f'{key}: description fill adjustment needs canonical description');ok=False
        for i,item in enumerate(adjustments):
            if not isinstance(item,dict):
                self.need(False,f'{key}: descriptionFillAdjustments[{i}] must be object');ok=False;continue
            if not self.text(item.get('layerName')):
                self.need(False,f'{key}: descriptionFillAdjustments[{i}] missing layerName');ok=False
            if item.get('action')!=HINT_FILL_ACTION:
                self.need(False,f'{key}: descriptionFillAdjustments[{i}] invalid action');ok=False
            quote=item.get('descriptionQuote')
            if not (self.text(quote) and isinstance(desc,str) and quote in desc):
                self.need(False,f'{key}: descriptionFillAdjustments[{i}] quote not in canonical description');ok=False
        base_fills=(baseline.get('protected') or {}).get('fills')
        after_fills=(after.get('protected') or {}).get('fills')
        if base_fills==after_fills:
            self.need(False,f'{key}: description fill adjustment did not change fills');ok=False
        for error in fill_errors(base_fills,after_fills,adjustments):
            self.need(False,f'{key}: {error}');ok=False
        return ok

    def items(self, field):
        value=self.r.get(field)
        if not self.need(isinstance(value,list), f'{field}: expected array'): return []
        if not self.need(all(isinstance(x,dict) for x in value), f'{field}: expected objects'): return []
        return value

    def ids(self, records, field):
        out={}
        for row in records:
            key=row.get('id')
            if not self.need(self.text(key),f'{field}: missing id'): continue
            self.need(key not in out,f'{field}: duplicate id {key}')
            out[key]=row
        return out

    def path(self, record):
        path=record.get('path')
        if not self.text(path): return None
        p=(self.root/path).resolve()
        if not p.is_relative_to(self.root) or not p.is_file(): return None
        return p

    def refs(self, ids, label, kinds=None, required=True):
        if not self.need(isinstance(ids,list) and (bool(ids) or not required),f'{label}: missing evidenceRefs'): return False
        ok=True
        for eid in ids:
            if not isinstance(eid,str) or eid not in self.ev:
                self.need(False,f'{label}: unknown evidence {eid}'); ok=False; continue
            if kinds and self.ev[eid].get('kind') not in kinds:
                self.need(False,f'{label}: wrong evidence kind {eid}'); ok=False
        return ok

    def data(self, eid):
        if not isinstance(eid,str) or eid not in self.ev: return None
        p=self.path(self.ev[eid])
        if p:
            try: return load_json(p)
            except (ValueError, OSError): pass
        return None

    def current(self, value, stage='final'):
        keys=('requirements','plan') if stage=='plan' else REVISIONS
        return isinstance(value,dict) and all(self.text(value.get(k)) and value.get(k)==self.r.get('revision',{}).get(k) for k in keys)
    def interaction_level(self, unit, medium=None):
        levels=unit.get('interactionLevels')
        if isinstance(levels,dict): return levels.get(medium) if medium is not None else levels
        return unit.get('interactionLevel')
    def structured(self, label, refs, kinds=('tool','verification')):
        if not self.need(isinstance(refs,list) and bool(refs),f'{label}: evidenceRefs required'): return None
        for eid in refs:
            if not isinstance(eid,str) or eid not in self.ev: continue
            if kinds and self.ev[eid].get('kind') not in kinds: continue
            data=self.data(eid)
            if isinstance(data,dict): return data
        self.need(False,f'{label}: structured JSON evidence required')
        return None

    def findings(self, label, value, report=None):
        if not self.need(isinstance(value,list),f'{label}: structured findings required'): return
        if not value:
            self.need(isinstance(report,dict) and report.get('verdict')=='pass' and isinstance(report.get('checksPerformed'),list) and bool(report.get('checksPerformed')),f'{label}: structured findings required for issues; clean review needs checksPerformed')
            for check in (report or {}).get('checksPerformed',[]):
                self.need(isinstance(check,dict) and check.get('unitId') in self.units and self.text(check.get('summary')),f'{label}: invalid performed check')
                if isinstance(check,dict): self.refs(check.get('evidenceRefs'),label)
            return
        for i,item in enumerate(value):
            if not isinstance(item,dict):
                self.need(False,f'{label}: finding {i} must be object');continue
            self.need(item.get('unitId') in self.units,f'{label}: finding {i} unitId invalid')
            self.need(self.text(item.get('position')),f'{label}: finding {i} position required')
            self.need(self.text(item.get('summary')),f'{label}: finding {i} summary required')
            self.refs(item.get('evidenceRefs'),f'{label} finding {i}')
            severity=item.get('severity')
            if severity in ('P0','P1','P2'):
                issue_id=item.get('issueId')
                if self.need(issue_id in self.issue_map,f'{label}: finding {i} {severity} needs a ledger issueId'):
                    self.need(self.issue_map[issue_id].get('severity')==severity,f'{label}: finding {i} severity differs from issue {issue_id}')
            elif severity is not None:
                self.need(severity=='suggestion',f'{label}: finding {i} severity must be P0/P1/P2/suggestion')

    def reuse_ladder(self, key, slot):
        resolution=slot.get('resolution')
        ladder=slot.get('reuseLadder')
        if not self.need(isinstance(ladder,list) and bool(ladder),
                         f'{key}: reuseLadder required (formal-instance -> compose -> gap)'): return
        steps=[]; matched=0
        for i,item in enumerate(ladder):
            if not self.need(isinstance(item,dict),f'{key}: reuseLadder[{i}] must be object'): continue
            step=item.get('step')
            if not self.need(step in RESOLUTION_STEPS,f'{key}: reuseLadder[{i}] invalid step'): continue
            steps.append(step)
            self.need(self.text(item.get('reason')),f'{key}: reuseLadder {step} reason required')
            self.refs(item.get('evidenceRefs'),f'{key} reuseLadder {step}',{'tool','verification'})
            outcome=item.get('outcome')
            self.need(outcome in ('matched','exhausted'),f'{key}: reuseLadder {step} outcome invalid')
            if outcome=='matched':
                matched+=1
                self.need(i==len(ladder)-1,f'{key}: matched reuseLadder step must be last')
                self.need(step==resolution,f'{key}: matched reuseLadder step must equal resolution')
            elif i==len(ladder)-1:
                self.need(False,f'{key}: reuseLadder has no matched step')
        self.need(matched==1,f'{key}: reuseLadder needs exactly one matched step')
        self.need(steps==[x for x in RESOLUTION_STEPS if x in steps] and len(steps)==len(set(steps)),
                  f'{key}: reuseLadder must follow formal-instance -> compose -> gap order')
        if resolution in RESOLUTION_STEPS:
            expected=list(RESOLUTION_STEPS[:RESOLUTION_STEPS.index(resolution)+1])
            self.need(steps==expected,f'{key}: reuseLadder must record {expected} before {resolution}')

    def profile_level(self):
        if self.r.get('mode') not in ('generate','iterate'):
            return 'full'
        p=self.r.get('executionProfile')
        return p.get('level') if isinstance(p,dict) and p.get('level') in PROFILE_LEVELS else 'full'

    def profile_review_dimensions(self, stage):
        if self.r.get('mode') not in ('generate','iterate') or self.gate=='report':
            return ('requirements','experience','ux','ui') if stage=='plan' else ('ux','ui','system')
        level=self.profile_level()
        if stage=='plan':
            return {'fast':('requirements','experience'),'standard':('requirements','experience','ux'),'full':('requirements','experience','ux','ui')}[level]
        return {'fast':('ui',),'standard':('ux','ui'),'full':('ux','ui','system')}[level]

    def required_simulations(self, stage, dimension):
        if not ((stage=='plan' and dimension=='experience') or (stage=='final' and dimension=='ux')):
            return set()
        if self.r.get('mode') not in ('generate','iterate'):
            return REQUIRED_TASK_SIMULATIONS
        p=self.r.get('executionProfile') if isinstance(self.r.get('executionProfile'),dict) else {}
        configured=p.get('requiredSimulations',[])
        required={x for x in configured if isinstance(x,str) and x}
        if self.profile_level()=='full':
            required |= REQUIRED_TASK_SIMULATIONS
        elif stage=='final':
            required = {'happy-path'} if self.profile_level()=='standard' else set()
        return required

    def validate_execution_profile(self):
        if self.r.get('mode') not in ('generate','iterate'):
            return 'full'
        p=self.r.get('executionProfile')
        if not self.need(isinstance(p,dict),'executionProfile: object required'):
            return 'full'
        level=p.get('level')
        self.need(level in PROFILE_LEVELS,'executionProfile.level must be fast/standard/full')
        self.need(p.get('source') in PROFILE_SOURCES,'executionProfile.source must be auto/user')
        a=p.get('assessment')
        if not self.need(isinstance(a,dict),'executionProfile.assessment required'):
            return level if level in PROFILE_LEVELS else 'full'
        bools=('taskModelChanged','navigationChanged','informationArchitectureChanged','permissionChanged','highRiskDestructive','longAsync','partialSuccess','crossContextMultiStep','newExperiencePattern')
        for key in bools:
            self.need(isinstance(a.get(key),bool),f'executionProfile.assessment.{key} must be boolean')
        count=a.get('visibleUnitCount')
        self.need(isinstance(count,int) and not isinstance(count,bool) and count>=0,'executionProfile.assessment.visibleUnitCount must be a non-negative integer')
        self.need(a.get('componentCoverageExpectation') in COMPONENT_COVERAGE,'executionProfile.assessment.componentCoverageExpectation invalid')
        self.need(a.get('ambiguity') in AMBIGUITY_LEVELS,'executionProfile.assessment.ambiguity invalid')
        sims=p.get('requiredSimulations')
        self.need(isinstance(sims,list) and bool(sims) and all(self.text(x) for x in sims),'executionProfile.requiredSimulations must be a non-empty string array')
        if isinstance(sims,list): self.need('happy-path' in sims,'executionProfile.requiredSimulations must include happy-path')
        reasons=p.get('reasons')
        self.need(isinstance(reasons,list) and bool(reasons) and all(self.text(x) for x in reasons),'executionProfile.reasons required')
        history=p.get('escalationHistory')
        self.need(isinstance(history,list),'executionProfile.escalationHistory must be an array')
        if isinstance(history,list):
            for i,item in enumerate(history):
                if not self.need(isinstance(item,dict),f'executionProfile.escalationHistory[{i}] must be object'): continue
                self.need(item.get('from') in PROFILE_LEVELS and item.get('to') in PROFILE_LEVELS,f'executionProfile.escalationHistory[{i}] invalid levels')
                if item.get('from') in PROFILE_LEVELS and item.get('to') in PROFILE_LEVELS:
                    self.need(PROFILE_LEVELS.index(item.get('to'))>PROFILE_LEVELS.index(item.get('from')),f'executionProfile.escalationHistory[{i}] must escalate upward')
                self.need(self.text(item.get('reason')),f'executionProfile.escalationHistory[{i}] reason required')
                self.refs(item.get('evidenceRefs',[]),f'executionProfile.escalationHistory[{i}]',required=False)
        full=any(a.get(k) is True for k in ('navigationChanged','informationArchitectureChanged','permissionChanged','highRiskDestructive','longAsync','partialSuccess','crossContextMultiStep')) or a.get('ambiguity')=='high'
        standard=full or a.get('taskModelChanged') is True or a.get('newExperiencePattern') is True or (isinstance(count,int) and count>2) or a.get('componentCoverageExpectation')=='unknown' or a.get('ambiguity')=='medium'
        minimum='full' if full else 'standard' if standard else 'fast'
        if level in PROFILE_LEVELS:
            self.need(PROFILE_LEVELS.index(level)>=PROFILE_LEVELS.index(minimum),f'executionProfile.level too low; minimum is {minimum}')
            if level=='fast':
                self.need(isinstance(count,int) and 1<=count<=2,'executionProfile.fast requires 1-2 visible units')
        return level if level in PROFILE_LEVELS else minimum

    def layout_artifact(self, uid, medium, refs):
        art=self.structured(f'{uid}/{medium}/layout-geometry',refs,('tool','verification'))
        if not isinstance(art,dict): return
        self.need(art.get('unitId')==uid,f'{uid}/layout-geometry: unit mismatch')
        self.need(art.get('deliverable')==medium,f'{uid}/layout-geometry: deliverable mismatch')
        self.need(art.get('verdict')=='pass',f'{uid}/layout-geometry: not passed')
        self.need(isinstance(art.get('checked'),list) and bool(art.get('checked')),f'{uid}/layout-geometry: checked nodes required')
        self.need(art.get('violations')==[],f'{uid}/layout-geometry: unresolved violations')
        measurements=art.get('measurements')
        if self.need(isinstance(measurements,list) and bool(measurements),f'{uid}/layout-geometry: measurements required'):
            for i,m in enumerate(measurements):
                if not self.need(isinstance(m,dict),f'{uid}/layout-geometry: measurement {i} must be object'): continue
                kind=m.get('kind')
                self.need(kind in LAYOUT_MEASUREMENT_KINDS,f'{uid}/layout-geometry: measurement {i} kind invalid')
                values=m.get('values')
                if self.need(isinstance(values,list) and len(values)>=2 and all(finite(v) for v in values),f'{uid}/layout-geometry: measurement {i} needs >=2 finite values'):
                    tolerance=m.get('tolerance')
                    if self.need(finite(tolerance) and tolerance>=0,f'{uid}/layout-geometry: measurement {i} tolerance invalid'):
                        status=m.get('status')
                        self.need(status in ('within','authorized'),f'{uid}/layout-geometry: measurement {i} status invalid')
                        if status=='within': self.need(max(values)-min(values)<=tolerance,f'{uid}/layout-geometry: measurement {i} exceeds tolerance')
                        if status=='authorized': self.need(self.text(m.get('reason')),f'{uid}/layout-geometry: measurement {i} authorized needs reason')
                if kind=='custom': self.need(self.text(m.get('reason')),f'{uid}/layout-geometry: custom measurement {i} needs reason')

    def baseline_artifact(self, uid, medium, refs):
        art=self.structured(f'{uid}/{medium}/baseline',refs,('baseline','verification','tool'))
        if not isinstance(art,dict): return None
        self.need(art.get('unitId')==uid,f'{uid}/baseline: unit mismatch')
        self.need(art.get('deliverable')==medium,f'{uid}/baseline: deliverable mismatch')
        self.need(art.get('verdict')=='pass',f'{uid}/baseline: not passed')
        elements=art.get('elements')
        self.need(isinstance(elements,list) and bool(elements),f'{uid}/baseline: elements required')
        if isinstance(elements,list):
            for e in elements:
                if not isinstance(e,dict):
                    self.need(False,f'{uid}/baseline: element must be object');continue
                self.need(self.text(e.get('id')),f'{uid}/baseline: element id required')
                self.need(isinstance(e.get('live'),dict) and isinstance(e.get('ours'),dict),f'{uid}/baseline: live/ours geometry required')
                deltas=e.get('deltas',[])
                self.need(bool(deltas),f'{uid}/baseline: measured deltas required')
                if not self.need(isinstance(deltas,list),f'{uid}/baseline: deltas must be array'): continue
                for d in deltas:
                    if not isinstance(d,dict):
                        self.need(False,f'{uid}/baseline: delta must be object');continue
                    status=d.get('status')
                    self.need(status in ('within','authorized'),f'{uid}/baseline: delta {d.get("field")} unresolved')
                    if status=='within':
                        values=[d.get(k) for k in ('live','ours','delta','tolerance')]
                        if self.need(all(finite(v) for v in values),f'{uid}/baseline: finite numeric geometry required'):
                            live,ours,delta,tolerance=values
                            self.need(tolerance>=0 and abs(ours-live)<=tolerance,f'{uid}/baseline: delta exceeds tolerance')
                            self.need(abs(delta-(ours-live))<1e-9,f'{uid}/baseline: incorrect delta arithmetic')
                            field=d.get('field')
                            self.need(e.get('live',{}).get(field)==live and e.get('ours',{}).get(field)==ours,f'{uid}/baseline: delta differs from measured element')
                    if status=='authorized': self.need(self.text(d.get('reason')),f'{uid}/baseline: authorized delta {d.get("field")} needs reason')
        return art

    def overflow_artifact(self, uid, medium, refs):
        art=self.structured(f'{uid}/{medium}/overflow',refs,('tool','verification'))
        if not isinstance(art,dict): return
        self.need(art.get('unitId')==uid,f'{uid}/overflow: unit mismatch')
        self.need(art.get('deliverable')==medium,f'{uid}/overflow: deliverable mismatch')
        self.need(art.get('verdict')=='pass',f'{uid}/overflow: not passed')
        self.need(isinstance(art.get('checked'),list) and bool(art.get('checked')),f'{uid}/overflow: checked surfaces required')
        self.need(art.get('escapes')==[],f'{uid}/overflow: unresolved clipping/overflow')

    def audit_artifact(self, uid, medium, refs):
        art=self.structured(f'{uid}/{medium}/node-audit',refs,('verification','tool'))
        if not isinstance(art,dict): return
        self.need(art.get('unitId')==uid,f'{uid}/node-audit: unit mismatch')
        self.need(art.get('deliverable')==medium,f'{uid}/node-audit: deliverable mismatch')
        self.need(art.get('verdict')=='pass',f'{uid}/node-audit: not passed')
        self.need(isinstance(art.get('scanned'),list) and bool(art.get('scanned')),f'{uid}/node-audit: scanned nodes required')
        self.need(art.get('unregistered')==[],f'{uid}/node-audit: unregistered self-built components')
        self.need(art.get('misclassified')==[],f'{uid}/node-audit: misclassified self-built content')

    def content_artifact(self, uid, medium, refs):
        art=self.structured(f'{uid}/{medium}/content',refs,('verification','tool'))
        if not isinstance(art,dict): return
        self.need(art.get('unitId')==uid,f'{uid}/content: unit mismatch')
        self.need(art.get('verdict')=='pass',f'{uid}/content: not passed')
        self.need(art.get('mismatches')==[],f'{uid}/content: unresolved copy mismatch')
        if self.r.get('deliverable')=='both':
            fields=('source','figma','demo')
        else:
            fields=('source','figma') if medium=='figma' else ('source','demo')
        for field in fields: self.need(isinstance(art.get(field),dict) and bool(art.get(field)),f'{uid}/{medium}/content: missing {field} alignment')
        for field in fields[1:]:
            self.need(not content_diff(art.get('source'),art.get(field)),f'{uid}/{field}/content: computed content mismatch')

    def parity_artifact(self, uid, refs):
        art=self.structured(f'{uid}/parity',refs,('verification','tool'))
        if not isinstance(art,dict): return
        self.need(art.get('unitId')==uid,f'{uid}/parity: unit mismatch')
        self.need(art.get('verdict')=='pass',f'{uid}/parity: not passed')
        self.need(art.get('mismatches')==[],f'{uid}/parity: unresolved Figma/Demo mismatch')
        self.need(isinstance(art.get('figma'),dict) and bool(art.get('figma')),f'{uid}/parity: figma comparison required')
        self.need(isinstance(art.get('demo'),dict) and bool(art.get('demo')),f'{uid}/parity: demo comparison required')


    def validate_packet(self, review):
        ref=review.get('packetRef')
        if not self.need(isinstance(ref,str) and ref in self.ev and self.ev[ref].get('kind')=='packet',f"review {review.get('id')}: packetRef must reference kind=packet evidence"): return
        packet=self.data(ref)
        if not self.need(isinstance(packet,dict),f"review {review.get('id')}: missing packet"): return
        self.need(PACKET_REQUIRED<=set(packet), 'packet missing fields')
        self.need(not (set(packet)&PACKET_LEAK), 'packet: unexpected/missing fields (possible conclusion leak)')
        self.need(packet.get('schemaVersion')==3,'packet: schemaVersion')
        self.need(packet.get('reviewerId')==review.get('reviewerId'),'packet: reviewer mismatch')
        self.need(packet.get('stage')==review.get('stage'),'packet: stage mismatch')
        self.need(self.current(packet.get('revision'),review.get('stage')),'packet: stale revision')
        self.need(set(packet.get('unitIds',[]))==set(self.units),'packet: incomplete unit scope')
        kinds={'source','authorization','task','constraint','plan','reference'} if review.get('stage')=='plan' else {'source','authorization','task','constraint','screenshot'}
        self.refs(packet.get('evidenceRefs'), 'packet', kinds)
        material=set(packet.get('evidenceRefs',[]))
        required={eid for x in self.items('sources') if x.get('required') for eid in x.get('evidenceRefs',[])}
        required.update(e for change in self.r.get('changeSet',[]) for e in change.get('evidenceRefs',[]))
        self.need(required <= material,'packet: missing required source/attachment')
        if review.get('stage')=='plan':
            self.need(set(self.r.get('planEvidenceRefs',[]))<=material,'packet: missing plan')
        else:
            for capture in self.items('captures'):
                if self.current(capture.get('revision')):
                    self.need(capture.get('evidenceRef') in material,'packet: missing current capture')

    def reviews(self, stage):
        reviewmap=self.ids(self.items('reviews'),'reviews')
        superseded=set()
        for review in reviewmap.values():
            self.need(set(review.get('issueIds',[]))<=set(self.issue_map),f"{review.get('id')}: historical findings absent from ledger")
            self.refs(review.get('evidenceRefs'),str(review.get('id')),{'review'})
            for eid in review.get('evidenceRefs',[]):
                report=self.data(eid)
                self.need(isinstance(report,dict),f"{review.get('id')}: historical report missing")
                if isinstance(report,dict):
                    self.need(set(report.get('issueIds',[]))<=set(self.issue_map),f"{review.get('id')}: historical report findings absent from ledger")
                    for field in ('reviewerId','stage','dimension','revision','coverage','issueIds','verdict'):
                        self.need(report.get(field)==review.get(field),f"{review.get('id')}: historical report differs: {field}")
                    self.findings(f"{review.get('id')} report",report.get('findings'),report)
            supersedes=review.get('supersedes',[])
            self.need(isinstance(supersedes,list) and all(isinstance(o,str) for o in supersedes),f"{review.get('id')}: supersedes must be a string array")
            for oldid in supersedes if isinstance(supersedes,list) else []:
                old=reviewmap.get(oldid,{})
                self.need(bool(old) and oldid!=review.get('id') and old.get('stage')==review.get('stage') and old.get('dimension')==review.get('dimension'), 'invalid review supersession')
                self.need(set(old.get('coverage',[]))<=set(review.get('coverage',[])), 'supersession loses review coverage')
                self.need(set(old.get('issueIds',[]))<=set(self.issue_map),'superseded findings absent from ledger')
                if self.current(review.get('revision'),stage): superseded.add(oldid)
        def chain(rid, path):
            if rid in path: self.need(False,'review supersession cycle'); return
            for old in reviewmap.get(rid,{}).get('supersedes',[]):
                if old in reviewmap: chain(old,path|{rid})
        for rid in reviewmap: chain(rid,set())
        dimensions=self.profile_review_dimensions(stage)
        for dimension in dimensions:
            selected=[x for x in self.items('reviews') if x.get('stage')==stage and x.get('dimension')==dimension and self.current(x.get('revision'),stage) and x.get('id') not in superseded]
            self.need(bool(selected),f'{stage}/{dimension}: missing current review')
            covered=set()
            for review in selected:
                name=review.get('id'); reviewer=review.get('reviewerId')
                allowed=('pass','issues') if self.gate=='report' else ('pass',)
                self.need(review.get('verdict') in allowed,f'{name}: review verdict must be '+('/'.join(allowed)))
                self.need(self.text(reviewer),f'{name}: reviewer missing')
                self.refs(review.get('evidenceRefs'),name,{'review'})
                for eid in review.get('evidenceRefs',[]):
                    report=self.data(eid)
                    self.need(isinstance(report,dict),f'{name}: structured report missing')
                    if isinstance(report,dict):
                        for field in ('reviewerId','stage','dimension','revision','coverage','issueIds','verdict'):
                            self.need(report.get(field)==review.get(field),f'{name}: report differs from record: {field}')
                        self.findings(name,report.get('findings'),report)
                        required_sims=self.required_simulations(stage,dimension)
                        if required_sims:
                            sims=report.get('simulationScenarios')
                            if self.need(isinstance(sims,list),f'{name}: task simulation scenarios required'):
                                categories=set()
                                for j,sim in enumerate(sims):
                                    if not self.need(isinstance(sim,dict),f'{name}: simulationScenarios[{j}] must be object'):
                                        continue
                                    category=sim.get('category'); categories.add(category)
                                    self.need(self.text(category),f'{name}: simulationScenarios[{j}] category required')
                                    self.need(sim.get('verdict') in ('pass','issue'),f'{name}: simulationScenarios[{j}] verdict required')
                                    self.need(self.text(sim.get('summary')),f'{name}: simulationScenarios[{j}] summary required')
                                missing=required_sims-categories
                                self.need(not missing,f'{name}: missing task simulations '+','.join(sorted(missing)))
                        if stage=='plan' and dimension=='experience' and self.r.get('mode') in ('generate','iterate'):
                            self.need(report.get('profileVerdict')=='keep',f'{name}: profileVerdict must be keep after any required escalation')
                self.need(set(review.get('coverage',[]))<=set(self.units),f'{name}: unknown coverage')
                covered.update(review.get('coverage',[]))
                self.need(set(review.get('issueIds',[]))<=set(self.issue_map),f'{name}: issueIds absent from ledger')
                self.need(review.get('independent') is True and reviewer!=self.r.get('designerId'),f'{name}: independent reviewer required')
                self.validate_packet(review)
            self.need(set(self.units)<=covered,f'{stage}/{dimension}: incomplete coverage')
        ux={x.get('reviewerId') for x in self.items('reviews') if x.get('stage')==stage and x.get('dimension')=='ux' and self.current(x.get('revision'),stage) and x.get('id') not in superseded}
        ui={x.get('reviewerId') for x in self.items('reviews') if x.get('stage')==stage and x.get('dimension')=='ui' and self.current(x.get('revision'),stage) and x.get('id') not in superseded}
        self.need(not ux.intersection(ui),f'{stage}: UX and UI must use separate isolated reviewers')

    def issues(self):
        self.issue_map=self.ids(self.items('issues'),'issues')
        order={'P0':0,'P1':1,'P2':2,'suggestion':3}
        for key,x in self.issue_map.items():
            severity=x.get('severity'); original=x.get('originalSeverity')
            self.need(severity in order and original in order,f'{key}: unknown severity')
            if severity in order and original in order:
                self.need(order[severity]<=order[original],f'{key}: severity downgrade forbidden')
            self.need(x.get('stage') in ('plan','final'),f'{key}: invalid issue stage')
            self.refs(x.get('evidenceRefs'),key)
            self.need(bool(x.get('unitIds')) and set(x.get('unitIds',[]))<=set(self.units),f'{key}: issue scope')
            if self.gate!='deliver' and x.get('stage')=='final': continue
            if severity=='suggestion':
                self.need(self.text(x.get('reason')),f'{key}: suggestion needs rationale'); continue
            state=x.get('state')
            self.need(state in ('verified-closed','not-a-bug','duplicate'),f'{key}: unresolved {severity} ({state})')
            if state in ('verified-closed','not-a-bug','duplicate'):
                resolution=x.get('resolution',{})
                self.need(isinstance(resolution,dict),f'{key}: resolution object')
                if not isinstance(resolution,dict): continue
                self.need(self.current(resolution.get('revision'),'plan' if self.gate!='deliver' else 'final'),f'{key}: stale verification')
                self.refs(resolution.get('evidenceRefs'),key,{'verification'})
                verifier=resolution.get('reviewerId')
                self.need(self.text(verifier) and verifier != x.get('fixAuthor',self.r.get('designerId')),f'{key}: independent verification required')
                self.need(self.text(resolution.get('reason')),f'{key}: closure rationale')
                if state=='verified-closed': self.need(self.text(x.get('fixAuthor')),f'{key}: fix author required')
                if state=='duplicate':
                    target=self.issue_map.get(x.get('duplicateOf'),{})
                    self.need(target.get('state') in ('verified-closed','not-a-bug') and target.get('id')!=key,f'{key}: duplicate target not resolved')

    def intake(self, sources):
        if self.r.get('mode') != 'generate':
            return
        self.deliverable_decision()
        x = self.r.get('intake')
        if not self.need(isinstance(x, dict), 'intake record required for generate'):
            return
        clarifications=x.get('clarifications',[])
        if self.need(isinstance(clarifications,list) and all(isinstance(i,dict) for i in clarifications),'intake.clarifications must be an array of objects'):
            for i,item in enumerate(clarifications):
                self.need(self.text(item.get('question')),f'intake.clarifications[{i}] needs a question')
                self.need(item.get('answer') is None or isinstance(item.get('answer'),str),f'intake.clarifications[{i}].answer must be a string or null')
        input_mode = x.get('inputMode')
        self.need(input_mode in INTAKE_MODES, 'intake.inputMode must be text or prd-file')
        if input_mode == 'text':
            self.need(x.get('rewritePolicy') == 'authored', 'text intake must record rewritePolicy=authored')
            art = x.get('prdArtifact')
            if self.need(isinstance(art, dict), 'text intake requires an authored prdArtifact'):
                eid = art.get('evidenceRef')
                e = self.ev.get(eid) if eid else None
                if self.need(e is not None, 'prdArtifact.evidenceRef must reference recorded evidence'):
                    self.need(e.get('kind') == 'source', 'prdArtifact evidence must have kind=source')
                    self.need(e.get('provenance') == 'authored', 'prdArtifact evidence must be authored')
                    path = self.path(e)
                    text = ''
                    if path:
                        try: text = path.read_text(encoding='utf-8')
                        except (UnicodeDecodeError, OSError): text = ''
                    self.need(bool(text.strip()), 'text intake PRD document is empty')
                    original=x.get('originalSourceIds',[])
                    self.need(isinstance(original,list) and bool(original) and set(original)<=set(sources), 'text intake needs originalSourceIds')
                    for sid in original:
                        source=sources.get(sid,{})
                        self.need(source.get('required') is True, 'original user source must be required')
                        self.need(any(self.ev.get(ref,{}).get('provenance') in ('captured','fixture') for ref in source.get('evidenceRefs',[])), 'original user source must be captured')
        elif input_mode == 'prd-file':
            policy = x.get('rewritePolicy')
            self.need(policy in ('verbatim','rewrite-authorized'),
                      'uploaded PRD intake must record rewritePolicy=verbatim or rewrite-authorized')
            docs = x.get('sourceDocs')
            if self.need(isinstance(docs, list) and bool(docs), 'prd-file intake requires sourceDocs'):
                self.need(set(docs) <= set(sources), 'intake.sourceDocs must reference recorded sources')
                for sid in docs:
                    self.need(sources.get(sid, {}).get('readStatus') == 'read', f'intake source {sid}: uploaded PRD unread')
            if policy == 'verbatim':
                self.need(x.get('prdArtifact') is None, 'verbatim intake must not author a rewritten PRD artifact')
                self.need(x.get('rewriteAuthorization') is None, 'verbatim intake must not record rewriteAuthorization')
                self.need(not any(e.get('kind') == 'source' and e.get('provenance') == 'authored' for e in self.ev.values()),
                          'verbatim intake must not rewrite the uploaded PRD into an authored source')
            elif policy == 'rewrite-authorized':
                auth = x.get('rewriteAuthorization')
                if self.need(isinstance(auth, dict), 'rewrite-authorized intake requires rewriteAuthorization from the user request'):
                    self.refs(auth.get('evidenceRefs'), 'rewrite authorization', {'authorization'})
                art = x.get('prdArtifact')
                if art is not None and self.need(isinstance(art, dict), 'prdArtifact must be an object or null'):
                    e = self.ev.get(art.get('evidenceRef'))
                    if self.need(e is not None, 'prdArtifact.evidenceRef must reference recorded evidence'):
                        self.need(e.get('kind') == 'source', 'prdArtifact evidence must have kind=source')

    def deliverable_decision(self):
        x = self.r.get('intake')
        if not isinstance(x, dict):
            return
        d = x.get('deliverableDecision')
        if not self.need(isinstance(d, dict), 'intake.deliverableDecision required: ask Figma vs web-demo; default web-demo'):
            return
        source = d.get('source'); choice = d.get('userChoice'); reason = d.get('fallbackReason')
        deliverable = self.r.get('deliverable')
        self.need(source in DELIVERABLE_SOURCES, 'deliverableDecision.source must be user-specified/asked/fallback')
        self.need(deliverable in DELIVERABLE_CHOICES, 'invalid deliverable')
        if source == 'user-specified':
            self.need(choice in DELIVERABLE_CHOICES, 'user-specified deliverable needs figma/web-demo/both')
            if choice in DELIVERABLE_CHOICES:
                self.need(choice == deliverable, 'deliverableDecision.userChoice must equal deliverable')
            self.need(reason in (None, ''), 'deliverableDecision.fallbackReason must be empty when the user specified the deliverable')
            self.refs(d.get('evidenceRefs'), 'deliverable decision', {'source','authorization'})
        elif source == 'asked':
            if choice in DELIVERABLE_CHOICES:
                self.need(choice == deliverable, 'deliverableDecision.userChoice must equal deliverable')
                self.need(reason in (None, ''), 'deliverableDecision.fallbackReason must be empty when the user replied')
                self.refs(d.get('evidenceRefs'), 'deliverable decision', {'source','authorization'})
            else:
                self.need(choice is None, 'deliverableDecision.userChoice invalid')
                self.need(reason == 'no-reply', 'asked without a reply requires fallbackReason=no-reply')
                self.need(deliverable == 'web-demo', 'no deliverable reply must default to web-demo')
        else:
            self.need(choice is None, 'fallback must not claim a user choice')
            self.need(reason == 'cannot-ask', 'fallback requires fallbackReason=cannot-ask')
            self.need(deliverable == 'web-demo', 'unable to ask must default to web-demo')

    def reference_review(self):
        if self.r.get('mode') != 'generate':
            return
        review=self.r.get('referenceReview')
        if not self.need(isinstance(review,dict),'referenceReview required: inspect component-library Template and user Figma references before component resolution'):
            return
        self.need(review.get('status')=='reviewed','referenceReview.status must be reviewed')
        scan=review.get('existingPageScan')
        if self.need(isinstance(scan,dict),'referenceReview.existingPageScan required'):
            scan_status=scan.get('status')
            self.need(scan_status in EXISTING_PAGE_SCAN_STATUSES,'referenceReview.existingPageScan.status must be scanned/not-applicable')
            if scan_status=='scanned':
                self.need(self.text(scan.get('fileKey')),'referenceReview.existingPageScan.fileKey required')
                page_ids=scan.get('pageIds')
                if self.need(isinstance(page_ids,list) and all(self.text(x) for x in page_ids),'referenceReview.existingPageScan.pageIds must be a string array'):
                    if not page_ids:
                        self.need(self.text(scan.get('reason')),'empty existing page scan needs reason')
                self.refs(scan.get('evidenceRefs'),'referenceReview.existingPageScan',{'reference'})
            else:
                self.need(self.text(scan.get('reason')),'not-applicable existing page scan needs reason')
        sources=review.get('sources')
        if not self.need(isinstance(sources,list) and bool(sources),'referenceReview.sources must be a non-empty array'):
            return
        seen=set()
        for i,item in enumerate(sources):
            label=f'referenceReview.sources[{i}]'
            if not self.need(isinstance(item,dict),f'{label} must be an object'):
                continue
            rid=item.get('id')
            self.need(self.text(rid),f'{label}.id required')
            if self.text(rid):
                self.need(rid not in seen,f'{label}.id duplicated')
                seen.add(rid)
            origin=item.get('origin')
            self.need(origin in REFERENCE_ORIGINS,f'{label}.origin must be built-in/target-file/user')
            source_kind=item.get('sourceKind')
            self.need(source_kind in REFERENCE_SOURCE_KINDS,f'{label}.sourceKind must be component-library-template/target-existing-page/user-reference')
            if origin=='built-in':
                self.need(source_kind==BUILTIN_REFERENCE_SOURCE_KIND,f'{label}.sourceKind must be component-library-template for built-in')
            elif origin=='target-file':
                self.need(source_kind=='target-existing-page',f'{label}.sourceKind must be target-existing-page for target-file')
            elif origin=='user':
                self.need(source_kind=='user-reference',f'{label}.sourceKind must be user-reference for user source')
            self.need(self.text(item.get('fileKey')),f'{label}.fileKey required')
            self.need(self.text(item.get('nodeId')),f'{label}.nodeId required')
            self.need(self.text(item.get('pageName')),f'{label}.pageName required')
            self.need(self.text(item.get('nodeName')),f'{label}.nodeName required')
            self.need(self.text(item.get('url')),f'{label}.url required')
            decision=item.get('decision')
            self.need(decision in REFERENCE_DECISIONS,f'{label}.decision must be matched/no-match/not-applicable')
            self.need(self.text(item.get('reason')),f'{label}.reason required')
            self.refs(item.get('evidenceRefs'),label,{'reference'})
            for eid in item.get('evidenceRefs',[]) if isinstance(item.get('evidenceRefs'),list) else []:
                record=self.ev.get(eid,{})
                self.need(record.get('provenance') in ('captured','fixture'),f'{label} evidence must be captured from the live tool, not authored')
            if decision=='matched':
                patterns=item.get('extractedPatterns')
                self.need(isinstance(patterns,list) and bool(patterns) and all(self.text(x) for x in patterns),f'{label}.extractedPatterns required for matched reference')
                action=item.get('reuseAction')
                self.need(action in REFERENCE_REUSE_ACTIONS,f'{label}.reuseAction must be direct-reuse/adapt-reuse/reference-only')
                unit_ids=item.get('unitIds')
                if self.need(isinstance(unit_ids,list) and bool(unit_ids) and all(self.text(x) for x in unit_ids),f'{label}.unitIds required for matched reference'):
                    self.need(set(unit_ids)<=set(self.units),f'{label}.unitIds must reference current units')
                changes=item.get('changeScope')
                if self.need(isinstance(changes,list) and all(self.text(x) for x in changes),f'{label}.changeScope must be a string array'):
                    self.need(set(changes)<=set(REFERENCE_CHANGE_SCOPES),f'{label}.changeScope contains unsupported value')
                    if action=='direct-reuse':
                        self.need(set(changes)<= {'flow-order'},f'{label}.direct-reuse may only change flow-order')
                    elif action=='adapt-reuse':
                        self.need(bool(changes),f'{label}.adapt-reuse requires changeScope')
                if source_kind=='target-existing-page' and action in ('direct-reuse','adapt-reuse'):
                    for uid in unit_ids if isinstance(unit_ids,list) else []:
                        lb=self.units.get(uid,{}).get('liveBaseline',{})
                        self.need(isinstance(lb,dict) and lb.get('applicability')=='replicated',f'{label} target page reuse requires replicated liveBaseline for {uid}')
                        self.need(lb.get('screenRef')==item.get('nodeId'),f'{label} liveBaseline screenRef must match reused page nodeId')
        built=next((x for x in sources if isinstance(x,dict) and x.get('id')==BUILTIN_REFERENCE_ID),None)
        if self.need(isinstance(built,dict),f'referenceReview must include component-library Template {BUILTIN_REFERENCE_ID}'):
            self.need(built.get('origin')=='built-in',f'{BUILTIN_REFERENCE_ID}.origin must be built-in')
            self.need(built.get('sourceKind')==BUILTIN_REFERENCE_SOURCE_KIND,f'{BUILTIN_REFERENCE_ID}.sourceKind mismatch')
            self.need(built.get('fileKey')==BUILTIN_REFERENCE_FILE_KEY,f'{BUILTIN_REFERENCE_ID}.fileKey mismatch')
            self.need(built.get('pageName')==BUILTIN_REFERENCE_PAGE_NAME,f'{BUILTIN_REFERENCE_ID}.pageName mismatch')

    def _root(self):
        self.need(self.text(self.r.get('runId')) and self.text(self.r.get('designerId')),'runId/designerId required')
        self.need(not self.r.get('migration') or self.r['migration'].get('status')=='revalidated','migration requires recapture and revalidation')
        self.need(self.r.get('schemaVersion')==3,'schemaVersion must be 3; convert schemaVersion=2 input and recapture missing evidence')
        self.need(self.r.get('mode') in ('generate','iterate','review-existing','independent-review'),'invalid mode')
        self.need(self.r.get('deliverable') in ('figma','web-demo','both'),'invalid deliverable')
        status=self.r.get('status')
        self.need(status in ('running','complete','paused-blocked'),'invalid status')
        if status=='paused-blocked': self.need(False,'run is paused-blocked; record blockers/nextAction and resume before completing')
        self.need(isinstance(self.r.get('nextAction'),str),'nextAction must be a string')
        self.need(self.r.get('stage') in STAGES,'invalid stage')
        self.need(self.r.get('environment')=='live' or (self.allow_fixture and self.r.get('environment')=='fixture'),'fixture requires --allow-fixture; real delivery requires live')
        self.need(self.current(self.r.get('revision'),'plan'),'requirements/plan revisions required')
        for field in ARRAYS: self.items(field)
        self.ev=self.ids(self.items('evidence'),'evidence')
        for key,e in self.ev.items():
            p=self.path(e)
            self.need(p is not None,f'evidence {key}: file missing or outside run directory')
            self.need(e.get('kind') in KINDS,f'evidence {key}: kind')
            self.need(e.get('provenance') in ('captured','authored','fixture'),f'evidence {key}: provenance')
            self.need(e.get('provenance')!='fixture' or self.allow_fixture,f'evidence {key}: simulated evidence')
            if p:
                self.need(digest(p)==e.get('sha256'),f'evidence {key}: hash mismatch')
                if e.get('kind') in ('tool','screenshot','reference') and e.get('provenance')!='fixture':
                    self.need(self.text(e.get('producer')) and self.text(e.get('capturedAt')) and self.text(e.get('target')),f'evidence {key}: producer/capturedAt/target required')
                if e.get('kind')=='screenshot' and e.get('provenance')!='fixture':
                    error=verify_image(p)
                    self.need(error is None,f'evidence {key}: screenshot is not an image: {error}')
        auth=self.r.get('authorization')
        if isinstance(auth,dict):
            for flag in ('write','fix','requirePlanConfirmation'):
                if flag in auth: self.need(isinstance(auth[flag],bool),f'authorization.{flag} must be boolean')
        self.units=self.ids(self.items('units'),'units'); self.req=self.ids(self.items('requirements'),'requirements')
        self.need(self.r.get('nextAction') in (None,)+NEXT_ACTIONS or self.r.get('nextAction')=='','nextAction must be a known resume/stop action')
        self.need(isinstance(self.r.get('blockers'),list),'blockers must be an array')
        self.refs(self.r.get('taskEvidenceRefs',[]),'taskEvidenceRefs',{'task'},required=False)

    def plan(self):
        self._root()
        sources=self.ids(self.items('sources'),'sources')
        self.need(bool(sources) and bool(self.units) and bool(self.req),'sources/requirements/units cannot be empty')
        if self.r.get('mode')=='iterate' and not self.text(self.r.get('intake',{}).get('inputMode')):
            self.need(self.r.get('authorization',{}).get('fix') is True,'iterate without PRD intake requires fix authorization')
            self.need(any(x.get('origin')=='derived' for x in self.req.values()),'iterate without PRD intake must derive requirements from authorization/observed draft')
        for key,x in sources.items():
            self.need(isinstance(x.get('required'),bool),f'{key}: required must be boolean')
            if x.get('required'): self.need(x.get('readStatus')=='read',f'{key}: required source unread')
            self.refs(x.get('evidenceRefs'),key,{'source'})
        self.need(any(x.get('required') for x in sources.values()),'at least one required primary source needed')
        self.intake(sources)
        self.reference_review()
        changeset=self.r.get('changeSet',[])
        self.need(isinstance(changeset,list),'changeSet must be an array')
        for change in changeset if isinstance(changeset,list) else []:
            if not self.need(isinstance(change,dict),'change must be an object'): continue
            self.need(change.get('operation') in ('add','replace','remove'),'invalid change operation')
            self.refs(change.get('evidenceRefs'),'explicit user change',{'source','authorization'})
            self.need(self.text(change.get('reason')),'change reason required')
            old=change.get('previousRequirement')
            if change.get('operation') in ('replace','remove'):
                self.need(isinstance(old,dict) and self.text(old.get('id')) and self.text(old.get('statement')),'previous requirement snapshot required')
                if isinstance(old,dict): self.need(old.get('id') not in self.req,'superseded requirement still active')
            if change.get('operation')!='remove': self.need(change.get('requirementId') in self.req,'change target requirement missing')
        for key,x in self.req.items():
            self.need(self.text(x.get('statement')) and self.text(x.get('acceptance')),f'{key}: statement/acceptance required')
            self.need(x.get('origin') in ('explicit','derived','team'),f'{key}: origin')
            self.need(bool(x.get('sourceIds')) and set(x.get('sourceIds',[]))<=set(sources),f'{key}: source reference')
            self.need(bool(x.get('targets')) and set(x.get('targets',[]))<=set(self.units),f'{key}: targets')
            self.need(self.text(x.get('sourceLocation')),f'{key}: sourceLocation required')
            for sourceid in x.get('sourceIds',[]): self.need(sources.get(sourceid,{}).get('readStatus')=='read',f'{key}: referenced source unread')
        media={'figma','demo'} if self.r.get('deliverable')=='both' else {'demo' if self.r.get('deliverable')=='web-demo' else 'figma'}
        for key,x in self.units.items():
            self.need(x.get('required') is True,f'{key}: active scope units must be required; scope removal needs new plan and source authorization')
            self.need(bool(x.get('requirementIds')) and set(x.get('requirementIds',[]))<=set(self.req),f'{key}: requirementIds')
            for rid in x.get('requirementIds',[]): self.need(key in self.req.get(rid,{}).get('targets',[]),f'{key}: reverse requirement mapping')
            self.need(x.get('kind') in ('screen','state','non-ui'),f'{key}: kind')
            if x.get('kind')!='non-ui': self.need(set(x.get('deliverables',[]))==media,f'{key}: missing deliverable branch')
            levels=x.get('interactionLevels')
            if x.get('kind')!='non-ui' and isinstance(levels,dict):
                self.need(set(levels)==media,f'{key}: interactionLevels must cover each deliverable')
                self.need(all(v in INTERACTION_LEVELS for v in levels.values()),f'{key}: interactionLevels values')
            else:
                self.need(x.get('interactionLevel') in INTERACTION_LEVELS,f'{key}: interactionLevel')
            if x.get('kind')!='non-ui':
                lb=x.get('liveBaseline')
                if self.need(isinstance(lb,dict),f'{key}: liveBaseline decision required'):
                    app=lb.get('applicability')
                    self.need(app in ('replicated','new'),f'{key}: liveBaseline applicability')
                    if app=='replicated':
                        self.need(self.text(lb.get('screenRef')),f'{key}: liveBaseline screenRef required')
                        self.refs(lb.get('evidenceRefs'),f'{key} liveBaseline',{'baseline'})
                    elif app=='new':
                        self.need(self.text(lb.get('reason')),f'{key}: new pattern needs reason')
        for rid,x in self.req.items():
            for uid in x.get('targets',[]): self.need(rid in self.units.get(uid,{}).get('requirementIds',[]),f'{rid}: reverse unit mapping')
        for x in self.items('assumptions'):
            self.need(x.get('impact') in ('business','design'), 'assumption impact')
            if x.get('impact')=='business':
                self.need(x.get('status')=='resolved','critical business assumption unresolved')
                self.refs(x.get('evidenceRefs'),'assumption')
        profile=self.validate_execution_profile()
        experience=self.r.get('experienceDecision')
        if self.r.get('mode') in ('generate','iterate'):
            if self.need(isinstance(experience,dict),'experienceDecision: object required'):
                self.need(experience.get('status')=='reviewed','experienceDecision: reviewed status required')
                task_ids=experience.get('taskIds')
                self.need(isinstance(task_ids,list) and bool(task_ids) and all(self.text(x) for x in task_ids),'experienceDecision: taskIds required')
                chosen=experience.get('chosenModels')
                self.need(isinstance(chosen,list) and bool(chosen),'experienceDecision: chosenModels required')
                for i,item in enumerate(chosen if isinstance(chosen,list) else []):
                    if not self.need(isinstance(item,dict),f'experienceDecision: chosenModels[{i}] must be object'): continue
                    self.need(item.get('taskId') in (task_ids if isinstance(task_ids,list) else []),f'experienceDecision: chosenModels[{i}] taskId invalid')
                    self.need(self.text(item.get('model')),f'experienceDecision: chosenModels[{i}] model required')
                    rationale=item.get('rationale')
                    self.need(isinstance(rationale,list) and bool(rationale) and all(self.text(x) for x in rationale),f'experienceDecision: chosenModels[{i}] rationale required')
                self.need(experience.get('confidence') in ('high','medium','low'),'experienceDecision: confidence invalid')
                if isinstance(task_ids,list) and isinstance(chosen,list):
                    chosen_ids=[x.get('taskId') for x in chosen if isinstance(x,dict)]
                    self.need(len(chosen_ids)==len(set(chosen_ids)) and set(chosen_ids)==set(task_ids),'experienceDecision: each taskId needs exactly one chosenModel')
                if profile=='fast': self.need(experience.get('confidence')=='high','experienceDecision: fast requires high confidence; escalate to standard')
                self.refs(experience.get('evidenceRefs'),'experienceDecision',{'plan'})
        self.refs(self.r.get('planEvidenceRefs'),'plan',{'plan'})
        auth=self.r.get('authorization',{})
        if isinstance(auth,dict) and (auth.get('requirePlanConfirmation') is True or any(x.get('requirementsBasis')=='user-confirmed' for x in self.items('slots'))):
            confirmation=self.r.get('planConfirmation',{})
            self.need(isinstance(confirmation,dict) and self.current(confirmation.get('revision'),'plan'),'required user plan confirmation missing/stale')
            if isinstance(confirmation,dict): self.refs(confirmation.get('evidenceRefs'),'plan confirmation',{'authorization'})
        self.check_isolation(self.ids(self.items('capabilities'),'capabilities'))
        self.issues(); self.reviews('plan')

    def build(self):
        level=self.profile_level()
        if level=='fast':
            for slot in self.items('slots'):
                if slot.get('resolution')=='gap': self.need(False,f"{slot.get('id')}: fast profile discovered gap; escalate to standard")
                if slot.get('resolution')=='compose' and slot.get('layoutOnly') is not True: self.need(False,f"{slot.get('id')}: fast profile discovered non-layout compose; escalate to standard")
        auth=self.r.get('authorization',{})
        self.need(isinstance(auth,dict),'authorization object required')
        if not isinstance(auth,dict): return
        scope=auth.get('scope')
        self.need(auth.get('write') is True and isinstance(scope,list) and bool(scope) and all(isinstance(x,str) and x for x in scope),'write authorization/scope required (scope must be a non-empty string array)')
        self.refs(auth.get('evidenceRefs'),'authorization',{'authorization'})
        if any(x.get('fixAuthor') for x in self.items('issues')): self.need(auth.get('fix') is True,'fix authorization required')
        self.need(self.text(self.r.get('revision',{}).get('library')),'library revision required')
        slotmap=self.ids(self.items('slots'),'slots'); self.slotmap=slotmap
        live=self.r.get('liveLibrary'); live_ids=set()
        if slotmap and self.need(isinstance(live,dict),'liveLibrary identity required'):
            self.need(self.text(live.get('libraryKey')),'liveLibrary: libraryKey required')
            self.need(self.text(live.get('observedAt')),'liveLibrary: observedAt required')
            self.need(self.text(live.get('version')) or self.text(live.get('fingerprint')),'liveLibrary: version or fingerprint required')
            self.need(live.get('version') is None or self.text(live.get('version')),'liveLibrary: version must be a non-empty string or null')
            self.need(live.get('fingerprint') is None or self.text(live.get('fingerprint')),'liveLibrary: fingerprint must be a non-empty string or null')
            ids=live.get('ids')
            if self.need(isinstance(ids,list) and all(isinstance(x,str) for x in ids),'liveLibrary: observed ids must be a string array'):
                live_ids=set(ids)
                if not live_ids: self.need(live.get('emptyProof') is True,'liveLibrary: empty ids require emptyProof=true with tool evidence')
            self.refs(live.get('evidenceRefs'),'liveLibrary',{'tool'})
        catalog=self.r.get('libraryCatalog')
        catalog_ids=set(catalog.get('ids',[])) if isinstance(catalog,dict) and isinstance(catalog.get('ids'),list) else set()
        if isinstance(live,dict) and isinstance(catalog,dict) and self.text(live.get('libraryKey')) and self.text(catalog.get('libraryKey')):
            self.need(live.get('libraryKey')==catalog.get('libraryKey'),'liveLibrary/libraryCatalog libraryKey mismatch')
        if isinstance(catalog,dict) and catalog.get('complete') is True and live_ids:
            self.need(live_ids<=catalog_ids,'liveLibrary ids must be a subset of the complete libraryCatalog ids')
        if any(s.get('resolution')=='gap' for s in slotmap.values()):
            self.need(isinstance(catalog,dict),'libraryCatalog required to prove a gap')
            if isinstance(catalog,dict):
                self.need(self.text(catalog.get('libraryKey')),'libraryCatalog: libraryKey required')
                self.need(catalog.get('complete') is True,'libraryCatalog: complete live catalog required')
                self.need(isinstance(catalog.get('ids'),list) and all(isinstance(x,str) for x in catalog.get('ids',[])),'libraryCatalog: ids array required')
                self.refs(catalog.get('evidenceRefs'),'libraryCatalog',{'tool'})
        covered=set()
        for key,s in slotmap.items():
            self.need(bool(s.get('unitIds')) and set(s.get('unitIds',[]))<=set(self.units),f'{key}: unitIds')
            covered.update(s.get('unitIds',[]))
            self.need(s.get('requirementsBasis') in ('reviewed-plan','user-confirmed'),f'{key}: writable requirementsBasis')
            self.need(self.current(s.get('revision')) or (isinstance(s.get('revision'),dict) and all(s['revision'].get(k)==self.r['revision'].get(k) for k in ('requirements','plan','library'))),f'{key}: stale selection')
            self.need(s.get('resolution') in RESOLUTION_STEPS,f'{key}: unresolved slot')
            self.reuse_ladder(key,s)
            self.refs(s.get('evidenceRefs'),key,{'tool'})
            attempts=s.get('searchAttempts',[])
            self.need(isinstance(attempts,list) and bool(attempts),f'{key}: searchAttempts required')
            for attempt in attempts:
                self.need(isinstance(attempt,dict),f'{key}: search attempt must be object')
                if not isinstance(attempt,dict): continue
                self.need(attempt.get('source') in SEARCH_SOURCES and (self.text(attempt.get('query')) or self.text(attempt.get('pageId'))),f'{key}: search query/scope missing')
                self.refs(attempt.get('evidenceRefs'),key,{'tool'})
            candidates=s.get('candidates',[])
            self.need(isinstance(candidates,list) and all(isinstance(c,dict) for c in candidates),f'{key}: candidates must be an array of objects')
            candidates=[c for c in candidates if isinstance(c,dict)] if isinstance(candidates,list) else []
            if not candidates: self.need((s.get('resolution')=='gap' and s.get('inventory',{}).get('complete') is True and s.get('inventory',{}).get('eligibleIds')==[]) or (s.get('resolution')=='compose' and bool(s.get('childSlotIds'))),f'{key}: no candidates without empty catalog proof or resolved composition')
            for c in candidates:
                self.need(c.get('gateDecision') in ('pass','reject-proven-mismatch','blocked-insufficient-evidence'),f'{key}: candidate decision')
                self.need(self.text(c.get('reason')),f'{key}: candidate reason')
                self.refs(c.get('evidenceRefs'),key,{'tool'})
            chosen=s.get('chosenAssets',[])
            self.need(isinstance(chosen,list) and all(isinstance(a,str) and a for a in chosen),f'{key}: chosenAssets must be a non-empty-string array')
            chosen=chosen if isinstance(chosen,list) else []
            if s.get('resolution')=='formal-instance': self.need(bool(chosen),f'{key}: chosenAssets missing')
            if s.get('resolution')=='compose':
                layout_only=s.get('layoutOnly')
                self.need(isinstance(layout_only,bool),f'{key}: compose layoutOnly boolean required')
                if layout_only is True:
                    self.need(self.text(s.get('layoutReason')),f'{key}: layout-only compose needs layoutReason')
                    self.need(bool(s.get('childSlotIds')),f'{key}: layout-only compose needs resolved children')
                elif layout_only is False:
                    self.need(bool(chosen),f'{key}: composed formal host needs chosenAssets')
            for asset in chosen:
                self.need(any(c.get('key')==asset and c.get('gateDecision')=='pass' for c in candidates),f'{key}: chosen asset has no pass evidence')
                self.need(asset in live_ids,f'{key}: chosen asset not observed in live library')
            children=s.get('childSlotIds',[])
            self.need(isinstance(children,list) and all(isinstance(c,str) and c for c in children),f'{key}: childSlotIds must be a non-empty-string array')
            for child in children if isinstance(children,list) else []: self.need(child in slotmap and child!=key,f'{key}: invalid child slot')
            bindings=s.get('slotBindings',[])
            self.need(isinstance(bindings,list) and all(isinstance(b,dict) for b in bindings),f'{key}: slotBindings must be an array of objects')
            bindings=[b for b in bindings if isinstance(b,dict)] if isinstance(bindings,list) else []
            self.need({b.get('childSlotId') for b in bindings}==set(s.get('childSlotIds',[])),f'{key}: incomplete bindings')
            for binding in bindings:
                self.refs(binding.get('evidenceRefs'),key,{'tool'})
                self.need(self.text(binding.get('host')),f'{key}: binding host missing')
                valid_parents=set(chosen)
                if s.get('resolution')=='gap': valid_parents.add('local:'+key)
                if s.get('resolution')=='compose': valid_parents.add('layout:'+key)
                self.need(binding.get('parentAssetKey') in valid_parents,f'{key}: binding parent not selected/planned')
                child=slotmap.get(binding.get('childSlotId'),{})
                self.need(set(s.get('unitIds',[]))<=set(child.get('unitIds',[])),f'{key}: binding child does not cover parent units')
            if s.get('resolution')=='gap':
                inventory=s.get('inventory',{})
                eligible=inventory.get('eligibleIds',[]); scanned=inventory.get('scannedIds',[]); excludes=inventory.get('exclusions',[])
                self.need(isinstance(eligible,list) and all(isinstance(x,str) for x in eligible),f'{key}: inventory.eligibleIds must be a string array')
                self.need(isinstance(scanned,list) and all(isinstance(x,str) for x in scanned),f'{key}: inventory.scannedIds must be a string array')
                self.need(isinstance(excludes,list) and all(isinstance(e,dict) and self.text(e.get('id')) for e in excludes),f'{key}: inventory.exclusions must be objects with id')
                eligible=eligible if isinstance(eligible,list) else []; scanned=scanned if isinstance(scanned,list) else []; excludes=[e for e in excludes if isinstance(e,dict)] if isinstance(excludes,list) else []
                self.need(inventory.get('complete') is True,f'{key}: incomplete inventory')
                self.refs(inventory.get('evidenceRefs'),key,{'tool'})
                self.need(set(eligible)==set(scanned)|{e.get('id') for e in excludes},f'{key}: inventory coverage mismatch')
                self.need(not(set(scanned)&{e.get('id') for e in excludes}),f'{key}: conflicting inventory coverage')
                self.need(set(eligible)<=catalog_ids,f'{key}: inventory ids absent from live catalog')
                self.need(set(scanned)|{e.get('id') for e in excludes}==catalog_ids,f'{key}: unclassified catalog assets')
                if catalog_ids and not eligible:
                    self.need(self.text(inventory.get('scopeReason')),f'{key}: empty eligible set needs scopeReason against non-empty catalog')
                self.need(set(scanned)<={c.get('key') for c in candidates},f'{key}: scanned assets need candidate decisions')
                for exclusion in excludes:
                    self.need(self.text(exclusion.get('reason')),f'{key}: exclusion reason')
                    self.refs(exclusion.get('evidenceRefs'),key,{'tool'})
                self.need(all(c.get('gateDecision')=='reject-proven-mismatch' for c in candidates),f'{key}: gap has unresolved or matching candidates')
                self.refs(s.get('compositionEvidenceRefs'),key,{'verification','tool'})
                sources=[a.get('source') for a in attempts if isinstance(a,dict)]
                self.need(any(x in ('published-name','page-routed','inventory') for x in sources),f'{key}: gap requires published-name/inventory fallback attempt')
                trials=s.get('composeTrials')
                if self.need(isinstance(trials,list) and bool(trials),f'{key}: gap requires composeTrials (composition attempt evidence)'):
                    for i,trial in enumerate(trials):
                        if not self.need(isinstance(trial,dict),f'{key}: composeTrials[{i}] must be object'): continue
                        self.need(trial.get('outcome')=='reject-proven-mismatch',f'{key}: composeTrials[{i}] unresolved')
                        self.need(self.text(trial.get('reason')),f'{key}: composeTrials[{i}] reason required')
                        self.refs(trial.get('evidenceRefs'),f'{key} composeTrials {i}',{'tool','verification'})
                        host=trial.get('host')
                        self.need(host=='layout' or host in catalog_ids,f'{key}: composeTrials[{i}] host not in live catalog')
                        parts=trial.get('parts')
                        if not self.need(isinstance(parts,list),f'{key}: composeTrials[{i}] parts array required'): continue
                        if catalog_ids: self.need(bool(parts),f'{key}: composeTrials[{i}] needs published parts')
                        for part in parts: self.need(part in catalog_ids,f'{key}: composeTrials[{i}] part not in live catalog')
        expected={k for k,u in self.units.items() if u.get('kind')!='non-ui'}
        self.need(expected<=covered,'required units missing component resolution')
        def walk(key, parents):
            if key in parents: self.need(False,'slot dependency cycle'); return
            for child in slotmap.get(key,{}).get('childSlotIds',[]):
                if child in slotmap: walk(child,parents|{key})
        for key in slotmap: walk(key,set())
        capabilities=self.ids(self.items('capabilities'),'capabilities')
        mandatory={'read-library','independent-review','screenshot'}
        if self.r.get('deliverable') in ('figma','both'): mandatory|={'import-instance'}
        if self.r.get('deliverable') in ('web-demo','both'): mandatory|={'demo-mapping','demo-render'}
        if any(s.get('resolution')=='gap' for s in slotmap.values()):
            mandatory.add('compose-check')
            if self.r.get('deliverable')!='web-demo': mandatory.add('create-component')
        self.need(mandatory<=set(capabilities),'mandatory capability probes missing')
        for key,c in capabilities.items():
            if key in mandatory:
                self.need(c.get('status')=='passed',f'{key}: blocked/degraded capability')
            else:
                self.need(c.get('status') in ('passed','degraded','blocked'),f'{key}: invalid capability status')
            self.need(isinstance(c.get('revision'),dict) and all(c['revision'].get(k)==self.r['revision'].get(k) for k in ('requirements','plan','library')),f'{key}: stale capability')
            self.refs(c.get('evidenceRefs'),key,{'tool','verification'})
        self.check_isolation(capabilities)

    def check_isolation(self, capabilities):
        isolation=capabilities.get('independent-review')
        if not isolation: return
        art=self.structured('independent-review',isolation.get('evidenceRefs'),('verification','tool'))
        if isinstance(art,dict):
            self.need(art.get('isolated') is True,'independent-review: isolated context required')
            self.need(self.text(art.get('mechanism')),'independent-review: isolation mechanism required')
            reviewers=art.get('reviewerIds')
            self.need(isinstance(reviewers,list) and bool(reviewers),'independent-review: reviewerIds required')
            if isinstance(reviewers,list): self.need(self.r.get('designerId') not in reviewers,'independent-review: reviewer must differ from designer')

    def deliver(self):
        self.need(self.current(self.r.get('revision')),'all delivery revisions required')
        self.need(not self.r.get('blockers'),'run has blockers')
        self.reviews('final')
        impls=self.ids(self.items('implementations'),'implementations')
        locals_=self.ids(self.items('localComponents'),'localComponents')
        triggers=[]
        for key,x in impls.items():
            for flag in PLAN_REVIEW_FLAGS:
                if flag in x: self.need(isinstance(x.get(flag),bool),f'{key}: {flag} must be boolean')
            triggers.extend(f'{key}.{flag}' for flag in PLAN_REVIEW_FLAGS if x.get(flag) is True)
            impact=x.get('changeImpact')
            values=[impact] if isinstance(impact,str) else impact if isinstance(impact,list) else []
            if impact is not None:
                self.need(isinstance(impact,str) or isinstance(impact,list),f'{key}: changeImpact must be a string or array')
                self.need(all(isinstance(v,str) and v in CHANGE_IMPACTS for v in values),f'{key}: changeImpact must use documented values')
            triggers.extend(f'{key}.changeImpact={v}' for v in values if v in CHANGE_IMPACTS)
        if triggers:
            self.need(False,'plan review required ('+', '.join(triggers)+'); nextAction=resume-plan')
            self.need(self.r.get('nextAction')=='resume-plan','nextAction must be resume-plan when plan review is required')
        nodes=set()
        for key,x in impls.items():
            slot=self.slotmap.get(x.get('slotId'),{})
            self.need(x.get('unitId') in slot.get('unitIds',[]),f'{key}: implementation outside slot units')
            self.need(x.get('targetId') in self.r.get('authorization',{}).get('scope',[]),f'{key}: write target outside authorization')
            self.need(x.get('deliverable') in self.units.get(x.get('unitId'),{}).get('deliverables',[]),f'{key}: implementation deliverable')
            self.need(x.get('outcome')=='ok',f'{key}: incomplete/degraded implementation')
            self.need(self.current(x.get('revision')),f'{key}: stale implementation verification')
            nid=x.get('nodeId'); self.need(self.text(nid),f'{key}: nodeId required')
            identity=(x.get('deliverable'),x.get('targetId'),nid)
            self.need(identity not in nodes,f'{key}: duplicate node registration'); nodes.add(identity)
            self.refs([x.get('preEvidenceRef'),x.get('postEvidenceRef')],key,{'tool'})
            before=self.data(x.get('preEvidenceRef')); after=self.data(x.get('postEvidenceRef'))
            self.need(isinstance(before,dict) and isinstance(after,dict),f'{key}: snapshots must be JSON objects')
            if not isinstance(before,dict) or not isinstance(after,dict): continue
            for label,snap in [('pre',before),('post',after)]:
                self.need(SNAPSHOT<=set(snap),f'{key}: {label} snapshot fields incomplete')
                self.need(isinstance(snap.get('protected'),dict) and set(snap.get('protected',{}))==PROTECTED,f'{key}: {label} protected fields incomplete')
                self.need(isinstance(snap.get('ancestorIds'),list) and all(isinstance(n,str) for n in snap.get('ancestorIds',[])),f'{key}: ancestorIds missing/invalid')
                if snap.get('parentId'):
                    self.need(snap.get('parentId') in snap.get('ancestorIds',[]),f'{key}: ancestor chain does not include direct parent')
                self.need(isinstance(snap.get('properties'),dict) and isinstance(snap.get('layout'),dict) and isinstance(snap.get('overrides'),list),f'{key}: snapshot types')
            self.need(before.get('nodeId')==nid and before.get('sourceAssetKey')==after.get('sourceAssetKey'),f'{key}: snapshot identity changed')
            self.need(after.get('nodeId')==nid,f'{key}: snapshot node mismatch')
            self.need(before.get('targetId')==x.get('targetId') and after.get('targetId')==x.get('targetId'),f'{key}: observed write scope mismatch')
            raw_whitelist=x.get('writeWhitelist')
            self.need(raw_whitelist is None or isinstance(raw_whitelist,list),f'{key}: writeWhitelist must be an array or null')
            whitelist=raw_whitelist if isinstance(raw_whitelist,list) else []
            self.need(isinstance(whitelist,list) and all(isinstance(p,str) and p.startswith('/') and p!='/' for p in whitelist),f'{key}: invalid/broad whitelist')
            origin=x.get('origin')
            self.need(origin in ('formal','local','layout','content'),f'{key}: unknown origin')
            fill_exempt=False
            baseline=None
            if origin=='formal':
                self.refs([x.get('assetBaselineEvidenceRef')],key,{'tool'})
                baseline=self.data(x.get('assetBaselineEvidenceRef'))
                if isinstance(baseline,dict) and x.get('descriptionFillAdjustments') not in (None,[]):
                    fill_exempt=self.valid_description_fill_adjustments(key,x,baseline,after)
            for path in changes(before,after):
                if any(path==root or path.startswith(root+'/') for root in VISUAL_OK_ROOTS):
                    continue
                if path=='/protected/fills' or path.startswith('/protected/fills/'):
                    if origin!='formal' or fill_exempt: continue
                elif origin!='formal' and (path=='/protected' or path.startswith('/protected/')):
                    continue
                root='/'+path.lstrip('/').split('/')[0]
                if root not in {'/sourceAssetKey','/type','/nodeId','/targetId','/protected'}:
                    continue
                self.need(False,f'{key}: illegal mutation {path}')
            if whitelist:
                self.need(all(any(p==root or p.startswith(root+'/') for root in WHITELIST_ROOTS) for p in whitelist),f'{key}: whitelist contains forbidden identity/field')
            if origin=='formal':
                self.need(after.get('type')==('INSTANCE' if x.get('deliverable')=='figma' else 'DOM'),f'{key}: formal instance type mismatch')
                self.need(x.get('assetKey') in slot.get('chosenAssets',[]),f'{key}: unselected formal asset')
                self.need(after.get('sourceAssetKey')==x.get('assetKey'),f'{key}: wrong source asset')
                self.need(isinstance(baseline,dict),f'{key}: canonical asset baseline required')
                if isinstance(baseline,dict):
                    self.need(baseline.get('sourceAssetKey')==x.get('assetKey') and baseline.get('mainComponentKey')==after.get('mainComponentKey'),f'{key}: canonical variant/source mismatch')
                    bp,ap=baseline.get('protected'),after.get('protected')
                    self.need(isinstance(bp,dict) and isinstance(ap,dict) and set(bp)==PROTECTED and set(ap)==PROTECTED,f'{key}: protected formal fields differ from canonical asset')
                    if isinstance(bp,dict) and isinstance(ap,dict) and set(bp)==PROTECTED and set(ap)==PROTECTED:
                        adjustments=x.get('descriptionFillAdjustments')
                        for field in PROTECTED:
                            if field=='fills' and fill_exempt:
                                continue
                            self.need(bp.get(field)==ap.get(field),f'{key}: protected formal fields differ from canonical asset')
                    legal=baseline.get('legalPropertyNames',[])
                    self.need(isinstance(legal,list) and set(after.get('properties',{}))<=set(legal),f'{key}: nonpublic property')
                    self.need(all(isinstance(o,dict) and o.get('kind') in OVERRIDE_KINDS for o in after.get('overrides',[])),f'{key}: illegal override kind')
                if x.get('deliverable')=='figma': self.need(self.text(after.get('mainComponentKey')),f'{key}: expected concrete variant key missing')
            if origin=='local':
                self.need(after.get('type')==('INSTANCE' if x.get('deliverable')=='figma' else 'DOM'),f'{key}: local instance type mismatch')
                local=locals_.get(x.get('localComponentId'),{})
                self.need(local.get('slotId')==x.get('slotId') and slot.get('resolution')=='gap',f'{key}: unregistered local gap')
                self.need(after.get('mainComponentId')==local.get('nodeId') and nid in local.get('instanceNodeIds',[]),f'{key}: local instance relationship')
            expected=x.get('expectedFacts')
            self.need(expected is None or isinstance(expected,dict),f'{key}: expectedFacts must be an object or null')
            if isinstance(expected,dict) and expected:
                for prop,value in expected.items(): self.need(after.get(prop)==value,f'{key}: actual fact mismatch {prop}')
            if x.get('deliverable')=='demo' and origin=='formal':
                mapping=x.get('mapping',{})
                self.need(self.text(mapping.get('chosenLiveKey')),f'{key}: Demo mapping chosenLiveKey required')
                self.need(mapping.get('manifestAssetKey')==x.get('assetKey'),f'{key}: Demo mapping manifestAssetKey must equal the local assetKey')
                self.need(self.text(mapping.get('generatedExport')),f'{key}: Demo mapping generatedExport required')
                self.need(mapping.get('propertySchemaMatch') is True,f'{key}: Demo mapping property schema not verified')
                if mapping.get('chosenLiveKey')!=x.get('assetKey'):
                    mismatch=mapping.get('syncMismatch')
                    if self.need(isinstance(mismatch,dict),f'{key}: differing live key needs syncMismatch record'):
                        self.need(self.text(mismatch.get('reason')),f'{key}: syncMismatch reason required')
                        self.refs(mismatch.get('evidenceRefs'),key,{'tool','verification'})
                        self.need(mismatch.get('type')=='identity-migration',f'{key}: syncMismatch must be verified identity-migration')
                        eq=self.structured(f'{key} compatibility',mismatch.get('evidenceRefs'))
                        if isinstance(eq,dict):
                            self.need(eq.get('fromKey')==x.get('assetKey') and eq.get('toKey')==mapping.get('chosenLiveKey'),f'{key}: compatibility identity mismatch')
                            for field in ('schema','dependencies','visual'):
                                pair=eq.get(field,{})
                                self.need(isinstance(pair,dict) and self.text(pair.get('before')) and pair.get('before')==pair.get('after'),f'{key}: compatibility {field} differs or unknown')
                self.refs(mapping.get('evidenceRefs'),key,{'tool'})
        for key,c in locals_.items():
            self.need(self.slotmap.get(c.get('slotId'),{}).get('resolution')=='gap',f'{key}: local component without gap')
            self.refs(c.get('evidenceRefs'),key,{'tool'})
            self.refs([c.get('mainEvidenceRef')],key,{'tool'})
            main=self.data(c.get('mainEvidenceRef'))
            self.need(isinstance(main,dict),f'{key}: local main evidence missing')
            if isinstance(main,dict):
                self.need(main.get('nodeId')==c.get('nodeId') and main.get('type') in ({'COMPONENT','COMPONENT_SET'} if any(x.get('deliverable')=='figma' and x.get('localComponentId')==key for x in impls.values()) else {'CODE_COMPONENT'}),f'{key}: local main is not a reusable component')
                self.need(main.get('dependencyKeys')==c.get('dependencyKeys') and isinstance(c.get('dependencyKeys'),list),f'{key}: formal dependencies mismatch')
                self.need(bool(main.get('boundFoundations')) and self.text(main.get('description')),f'{key}: missing foundations/description')
            local_uses=[x for x in impls.values() if x.get('localComponentId')==key]
            self.need(len({x.get('deliverable') for x in local_uses})==1,f'{key}: register local main separately for each deliverable')
            reachable=set(); pending=list(self.slotmap.get(c.get('slotId'),{}).get('childSlotIds',[]))
            while pending:
                childid=pending.pop()
                if childid in reachable: continue
                reachable.add(childid);pending.extend(self.slotmap.get(childid,{}).get('childSlotIds',[]))
            reachable_assets={asset for sid in reachable for asset in self.slotmap.get(sid,{}).get('chosenAssets',[])}
            self.need(set(c.get('dependencyKeys',[]))<=reachable_assets,f'{key}: formal dependency has no recursive slot resolution')
            for use in local_uses:
                for dep in c.get('dependencyKeys',[]):
                    matches=[x for x in impls.values() if x.get('slotId') in reachable and x.get('assetKey')==dep and x.get('origin')=='formal' and x.get('unitId')==use.get('unitId') and x.get('deliverable')==use.get('deliverable') and x.get('targetId')==use.get('targetId')]
                    self.need(any(isinstance(self.data(x.get('postEvidenceRef')),dict) and use.get('nodeId') in self.data(x.get('postEvidenceRef')).get('ancestorIds',[]) for x in matches),f'{key}: formal dependency not instantiated inside local component')
            actual={x.get('nodeId') for x in local_uses}
            self.need(bool(actual) and actual==set(c.get('instanceNodeIds',[])),f'{key}: local instance registry mismatch')
            self.need(self.text(c.get('nodeId')),f'{key}: main component node missing')
        for sid,s in self.slotmap.items():
            for uid in s.get('unitIds',[]):
                for medium in self.units.get(uid,{}).get('deliverables',[]):
                    matched=[x for x in impls.values() if x.get('slotId')==sid and x.get('unitId')==uid and x.get('deliverable')==medium]
                    self.need(bool(matched),f'{sid}/{uid}/{medium}: missing implementation')
                    self.need(set(s.get('chosenAssets',[]))<={x.get('assetKey') for x in matched if x.get('origin')=='formal'},f'{sid}/{uid}/{medium}: selected asset not instantiated')
                    if s.get('resolution')=='gap': self.need(any(x.get('origin')=='local' for x in matched),f'{sid}: gap not built as reusable component')
        checks=self.items('checks'); self.ids(checks,'checks')
        for c in checks:
            self.need(self.text(c.get('unitId')),'checks: unitId must be a non-empty string')
            self.need(isinstance(c.get('deliverable'),str) and bool(c.get('deliverable')),'checks: deliverable must be a non-empty string')
        baselines={}
        for uid,u in self.units.items():
            media=u.get('deliverables',[]) if u.get('kind')!='non-ui' else ['non-ui']
            for medium in media:
                kinds=['visual','content','node-audit','layout-geometry'] if medium!='non-ui' else ['requirement']
                expected_level=u.get('interactionLevel') if u.get('kind')=='non-ui' else self.interaction_level(u,medium)
                if expected_level!='not-applicable': kinds+=['interaction']
                if medium!='non-ui':
                    kinds+=['overflow']
                    if (u.get('liveBaseline') or {}).get('applicability')=='replicated': kinds+=['baseline']
                    if self.r.get('deliverable')=='both' and medium=='figma': kinds+=['parity']
                for kind in kinds:
                    matches=[c for c in checks if c.get('unitId')==uid and (kind=='parity' or c.get('deliverable')==medium) and c.get('kind')==kind and self.current(c.get('revision'))]
                    self.need(bool(matches),f'{uid}/{medium}/{kind}: missing current check')
                    for c in matches:
                        self.need(c.get('result')=='pass',f'{uid}/{kind}: failed or unverified')
                        self.refs(c.get('evidenceRefs'),f'{uid}/{kind}')
                        if kind=='interaction': self.need(c.get('level')==expected_level,f'{uid}/{medium}: interaction evidence level mismatch')
                        if kind=='visual':
                            caps={cap.get('evidenceRef') for cap in self.items('captures') if cap.get('unitId')==uid and cap.get('deliverable')==medium and self.current(cap.get('revision'))}
                            shots={eid for eid in c.get('evidenceRefs',[]) if eid in self.ev and self.ev[eid].get('kind')=='screenshot'}
                            self.need(bool(caps) and caps<=shots,f'{uid}/{medium}/visual: must cite current screenshot')
                        if kind=='content': self.content_artifact(uid,medium,c.get('evidenceRefs'))
                        if kind=='node-audit': self.audit_artifact(uid,medium,c.get('evidenceRefs'))
                        if kind=='layout-geometry': self.layout_artifact(uid,medium,c.get('evidenceRefs'))
                        if kind=='overflow': self.overflow_artifact(uid,medium,c.get('evidenceRefs'))
                        if kind=='baseline':
                            art=self.baseline_artifact(uid,medium,c.get('evidenceRefs'))
                            if art: baselines[(uid,medium)]=art
                        if kind=='parity':
                            caps={cap.get('evidenceRef') for cap in self.items('captures') if cap.get('unitId')==uid and self.current(cap.get('revision'))}
                            self.need(len(caps)>=2 and caps<={eid for eid in c.get('evidenceRefs',[]) if eid in self.ev},f'{uid}/parity: must cite current Figma and Demo screenshots')
                            self.parity_artifact(uid,c.get('evidenceRefs'))
                if medium!='non-ui':
                    captures=[c for c in self.items('captures') if c.get('unitId')==uid and c.get('deliverable')==medium and self.current(c.get('revision'))]
                    self.need(bool(captures),f'{uid}/{medium}: missing current screenshot')
                    for c in captures: self.refs([c.get('evidenceRef')],uid,{'screenshot'})
        for key,x in impls.items():
            unit=self.units.get(x.get('unitId'),{})
            if (unit.get('liveBaseline') or {}).get('applicability')=='replicated' and x.get('origin') in ('formal','local','layout'):
                art=baselines.get((x.get('unitId'),x.get('deliverable')))
                self.need(isinstance(art,dict),f'{key}: replicated unit needs current baseline check')
                if isinstance(art,dict):
                    element_ids={e.get('id') for e in art.get('elements',[]) if isinstance(e,dict)}
                    self.need(self.text(x.get('baselineElementId')) and x.get('baselineElementId') in element_ids,f'{key}: implementation not covered by live baseline')
        refresh=[c for c in checks if c.get('kind')=='library-refresh' and self.current(c.get('revision'))]
        self.need(bool(refresh),'current library refresh missing')
        for c in refresh:
            self.need(c.get('result')=='pass','library drift unresolved')
            self.refs(c.get('evidenceRefs'),'library-refresh',{'tool'})

    def report(self):
        self._root()
        self.need(self.r.get('mode') in ('review-existing','independent-review'),'report gate requires a read-only mode')
        self.need(self.r.get('stage')=='report','read-only report requires stage=report')
        self.need(self.r.get('status')=='complete','read-only report requires status=complete')
        self.need(bool(self.units),'report requires observed units')
        for uid,u in self.units.items():
            if u.get('kind')=='non-ui': continue
            caps=[c for c in self.items('captures') if c.get('unitId')==uid and self.current(c.get('revision'))]
            self.need(bool(caps),f'{uid}: report needs a current screenshot')
            for c in caps: self.refs([c.get('evidenceRef')],uid,{'screenshot'})
        self.issues()
        self.reviews('final')

    def run(self):
        if not isinstance(self.r,dict): return ['run must be an object']
        try:
            readonly=self.r.get('mode') in ('review-existing','independent-review')
            if self.gate=='report':
                self.report()
            elif readonly:
                self.need(False,'read-only modes require --gate report')
            else:
                self.plan()
                if self.gate in ('build','deliver'): self.build()
                if self.gate=='deliver': self.deliver()
        except (TypeError, KeyError, AttributeError, ValueError, RecursionError) as error:
            self.errors.append(f'malformed contract: {type(error).__name__}: {error}')
        return self.errors


def packet(run, stage, reviewer):
    refs={e for s in run['sources'] for e in s['evidenceRefs']}
    refs.update(run.get('taskEvidenceRefs',[]))
    refs.update(e for change in run.get('changeSet',[]) for e in change.get('evidenceRefs',[]))
    if stage=='plan':
        refs.update(run['planEvidenceRefs'])
        refs.update(e for item in run.get('referenceReview',{}).get('sources',[]) for e in item.get('evidenceRefs',[]))
        refs.update(run.get('referenceReview',{}).get('existingPageScan',{}).get('evidenceRefs',[]))
    else: refs.update(c['evidenceRef'] for c in run['captures'] if c['revision']==run['revision'])
    return dict(schemaVersion=3,stage=stage,reviewerId=reviewer,revision=run['revision'],
                unitIds=[x['id'] for x in run['units']],evidenceRefs=sorted(refs))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run',nargs='?'); parser.add_argument('--init',type=Path)
    parser.add_argument('--gate',choices=('plan','build','deliver','report'),default='deliver')
    parser.add_argument('--allow-fixture',action='store_true')
    parser.add_argument('--packet',choices=('plan','final')); parser.add_argument('--reviewer')
    parser.add_argument('--producer'); parser.add_argument('--captured-at'); parser.add_argument('--target');
    parser.add_argument('--add-evidence'); parser.add_argument('--id'); parser.add_argument('--kind',choices=sorted(KINDS))
    parser.add_argument('--provenance',choices=('captured','authored','fixture'),default='captured')
    args=parser.parse_args()
    try:
        if args.init:
            args.init.mkdir(parents=True,exist_ok=True)
            target=args.init/'run.json'
            with target.open('x',encoding='utf-8') as f: json.dump(skeleton(),f,ensure_ascii=False,indent=2)
            print(target); return 0
        if not args.run: parser.error('run.json required')
        path=Path(args.run).resolve(); run=load_json(path)
        if args.add_evidence:
            if not args.id or not args.kind: parser.error('--id and --kind required')
            artifact=(path.parent/args.add_evidence).resolve()
            if not artifact.is_relative_to(path.parent) or not artifact.is_file(): parser.error('evidence must be a file inside run directory')
            if any(e['id']==args.id for e in run['evidence']): parser.error('evidence id already exists; preserve history')
            if args.kind in ('tool','screenshot') and args.provenance!='fixture' and not all((args.producer,args.captured_at,args.target)):
                parser.error('tool/screenshot evidence needs --producer --captured-at --target from actual capture')
            run['evidence'].append(dict(producer=args.producer,capturedAt=args.captured_at,target=args.target,id=args.id,path=str(artifact.relative_to(path.parent)),sha256=digest(artifact),kind=args.kind,provenance=args.provenance))
            tmp=path.with_suffix('.tmp'); tmp.write_text(json.dumps(run,ensure_ascii=False,indent=2)); tmp.replace(path)
            print(args.id); return 0
        if args.packet:
            if not args.reviewer: parser.error('--reviewer required')
            result=packet(run,args.packet,args.reviewer)
            allowed={'source','authorization','task','constraint','plan'} if args.packet=='plan' else {'source','authorization','task','constraint','screenshot'}
            ev={e['id']:e for e in run['evidence']}
            if not result['evidenceRefs'] or any(e not in ev or ev[e]['kind'] not in allowed for e in result['evidenceRefs']): parser.error('packet has missing or forbidden materials')
            print(json.dumps(result,ensure_ascii=False,indent=2)); return 0
        errors=Gate(run,path.parent,args.gate,args.allow_fixture).run()
        print(json.dumps({'gate':args.gate,'passed':not errors,'environment':run.get('environment') if isinstance(run,dict) else None,'errors':errors,'limits':'Checks intake input-mode/PRD provenance, target-page/component-library Template/user reference review evidence and page-level reuse decisions, adaptive execution-profile minimums/review dimensions, the deliverable decision (Figma vs web-demo, default web-demo), authorization scope/boolean flags, live library identity and observed asset membership (including subset of the complete catalog), the formal-instance/compose/gap reuse ladder, composition-attempt proof, live catalog coverage, component identity, current screenshots, layout geometry consistency, live baseline diffs, overflow escapes, content three-way alignment, Figma/Demo parity, finding-to-issue linkage, review packet linkage, and isolated review evidence. The report gate validates read-only review runs without build/deliver. Does not score visual quality or verify live Figma truth.'},ensure_ascii=False,indent=2))
        return 1 if errors else 0
    except (OSError,ValueError,TypeError,KeyError) as error:
        print(json.dumps({'passed':False,'errors':[str(error)]},ensure_ascii=False)); return 1

if __name__=='__main__': sys.exit(main())
