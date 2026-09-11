"""Synthetic evidence tests, never live Figma verification."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('run_gate',ROOT/'scripts/validate-run.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)


class RunGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='yb-gate-test-'); self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name); self.r=m.skeleton()
        self.r.update(runId='test-run',designerId='designer',environment='fixture',deliverable='figma',revision={k:'v1' for k in m.REVISIONS})
        self.rev=self.r['revision']
        for eid,kind in [('source','source'),('plan','plan'),('task','task'),('auth','authorization'),('tool','tool'),('capture','screenshot'),('verify','verification'),('reference','reference')]:
            self.evidence(eid,kind,{'fixture':True,'purpose':'synthetic test'})
        self.r['authorization']=dict(write=True,fix=True,scope=['target'],evidenceRefs=['auth'])
        self.r['sources']=[dict(id='s1',required=True,readStatus='read',evidenceRefs=['source'])]
        self.r['intake']=dict(inputMode='prd-file',deliverableDecision=self.decision(),prdArtifact=None,sourceDocs=['s1'],rewritePolicy='verbatim',rewriteAuthorization=None,clarifications=[])
        self.r['referenceReview']=dict(
            status='reviewed',
            existingPageScan=dict(status='scanned',fileKey='target-file',pageIds=['existing-page'],evidenceRefs=['reference']),
            sources=[dict(id=m.BUILTIN_REFERENCE_ID,origin='built-in',sourceKind=m.BUILTIN_REFERENCE_SOURCE_KIND,fileKey=m.BUILTIN_REFERENCE_FILE_KEY,nodeId='page-template',pageName=m.BUILTIN_REFERENCE_PAGE_NAME,nodeName=m.BUILTIN_REFERENCE_PAGE_NAME,url='https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/example?node-id=page-template',decision='no-match',reason='No same-category Template pattern applies to the synthetic fixture.',evidenceRefs=['reference'])],
        )
        self.r['requirements']=[dict(id='r1',statement='Show content',acceptance='Actual business content visible',origin='explicit',sourceIds=['s1'],targets=['u1'],sourceLocation='section 1')]
        self.r['units']=[dict(id='u1',required=True,requirementIds=['r1'],kind='screen',deliverables=['figma'],interactionLevel='not-applicable',liveBaseline=dict(applicability='new',reason='No live counterpart; new surface.'))]
        self.r['executionProfile']=dict(level='full',source='auto',assessment=dict(taskModelChanged=True,navigationChanged=False,informationArchitectureChanged=False,permissionChanged=False,highRiskDestructive=False,longAsync=False,partialSuccess=False,crossContextMultiStep=False,newExperiencePattern=True,visibleUnitCount=1,componentCoverageExpectation='known-existing',ambiguity='low'),requiredSimulations=['happy-path','first-use','error','interrupt','post-success'],reasons=['Synthetic full-profile fixture.'],escalationHistory=[])
        self.r['experienceDecision']=dict(status='reviewed',taskIds=['task-main'],chosenModels=[dict(taskId='task-main',model='focused-task',rationale=['Best balances task completion and context retention.'])],confidence='high',evidenceRefs=['plan'])
        self.r['planEvidenceRefs']=['plan'];self.r['taskEvidenceRefs']=['task']
        self.r['captures']=[dict(unitId='u1',deliverable='figma',revision=self.rev,evidenceRef='capture')]
        for stage,dims in [('plan',['requirements','experience','ux','ui']),('final',['ux','ui','system'])]:
            for dim in dims: self.review(stage,dim)
        self.r['liveLibrary']=dict(libraryKey='lib-key',version='v1',fingerprint=None,observedAt='2026-09-09T00:00:00Z',ids=['component'],evidenceRefs=['tool'])
        self.r['slots']=[dict(id='slot',unitIds=['u1'],requirementsBasis='reviewed-plan',revision=self.rev,resolution='formal-instance',evidenceRefs=['tool'],reuseLadder=[dict(step='formal-instance',outcome='matched',reason='One published component covers the full responsibility.',evidenceRefs=['tool'])],searchAttempts=[dict(source='semantic',query='task content',evidenceRefs=['tool'])],candidates=[dict(key='component',gateDecision='pass',reason='Complete responsibility and state coverage',evidenceRefs=['tool'])],chosenAssets=['component'],childSlotIds=[],slotBindings=[])]
        self.evidence('independence','verification',dict(isolated=True,mechanism='isolated-subagent',reviewerIds=['plan-experience','plan-ux','final-ux']))
        for cid in ['read-library','independent-review','read-target','import-instance','write-text','layout','screenshot']: self.capability(cid,['independence'] if cid=='independent-review' else ['tool'])
        protected={key:[] for key in m.PROTECTED}; protected['font']=['Official Font']; protected['fills']={'padding':[{'visible':True,'color':'official'}]}
        snapshot=dict(ancestorIds=['target'],targetId='target',type='INSTANCE',nodeId='node',sourceAssetKey='component',mainComponentKey='variant-1',mainComponentId=None,properties={},content={'headline':'Business content'},layout={'width':100},name='Task content',parentId='target',overrides=[],protected=protected)
        self.evidence('pre','tool',snapshot);self.evidence('post','tool',snapshot)
        self.evidence('canonical','tool',dict(sourceAssetKey='component',mainComponentKey='variant-1',protected=protected,legalPropertyNames=[]))
        self.evidence('content','verification',dict(unitId='u1',source={'headline':'Business content'},figma={'headline':'Business content'},mismatches=[],verdict='pass'))
        self.evidence('overflow','tool',dict(unitId='u1',deliverable='figma',checked=[{'nodeId':'node','role':'screen-root'}],escapes=[],verdict='pass'))
        self.evidence('audit','tool',dict(unitId='u1',deliverable='figma',verdict='pass',scanned=[{'nodeId':'node','role':'screen-root'}],unregistered=[],misclassified=[]))
        self.evidence('layout','tool',dict(unitId='u1',deliverable='figma',verdict='pass',checked=[{'nodeId':'node','role':'screen-root','layoutMode':'VERTICAL'}],measurements=[{'kind':'edge-alignment','values':[16,16,16],'tolerance':1,'status':'within'}],violations=[]))
        self.r['implementations']=[dict(id='impl',slotId='slot',unitId='u1',targetId='target',deliverable='figma',outcome='ok',revision=self.rev,nodeId='node',preEvidenceRef='pre',postEvidenceRef='post',assetBaselineEvidenceRef='canonical',writeWhitelist=[],origin='formal',assetKey='component',expectedFacts={'content':snapshot['content'],'mainComponentKey':'variant-1'})]
        self.r['checks']=[
            dict(id='visual',unitId='u1',deliverable='figma',kind='visual',revision=self.rev,result='pass',evidenceRefs=['capture']),
            dict(id='content',unitId='u1',deliverable='figma',kind='content',revision=self.rev,result='pass',evidenceRefs=['content']),
            dict(id='overflow',unitId='u1',deliverable='figma',kind='overflow',revision=self.rev,result='pass',evidenceRefs=['overflow']),
            dict(id='node-audit',unitId='u1',deliverable='figma',kind='node-audit',revision=self.rev,result='pass',evidenceRefs=['audit']),
            dict(id='layout-geometry',unitId='u1',deliverable='figma',kind='layout-geometry',revision=self.rev,result='pass',evidenceRefs=['layout']),
            dict(id='library-refresh',unitId='u1',deliverable='figma',kind='library-refresh',revision=self.rev,result='pass',evidenceRefs=['tool']),
        ]

    def evidence(self,eid,kind,data):
        path=self.root/(eid+'.json');path.write_text(json.dumps(data))
        self.r['evidence']=[e for e in self.r['evidence'] if e['id']!=eid]
        self.r['evidence'].append(dict(id=eid,kind=kind,path=path.name,sha256=m.digest(path),provenance='fixture'))
        return eid

    def decision(self,source='user-specified',choice='figma',reason=None,refs=('source',)):
        return dict(source=source,userChoice=choice,fallbackReason=reason,evidenceRefs=list(refs))

    def text_evidence(self,eid,kind,text,provenance='authored'):
        path=self.root/(eid+'.md');path.write_text(text,encoding='utf-8')
        self.r['evidence']=[e for e in self.r['evidence'] if e['id']!=eid]
        self.r['evidence'].append(dict(id=eid,kind=kind,path=path.name,sha256=m.digest(path),provenance=provenance))
        return eid

    def edit_evidence(self,eid,change):
        record=next(e for e in self.r['evidence'] if e['id']==eid)
        data=m.load_json(self.root/record['path']);change(data);self.evidence(eid,record['kind'],data)

    def review(self,stage,dim,rid=None,verdict='pass',supersedes=None,issue_ids=None):
        rid=rid or stage+'-'+dim; reviewer=stage+'-'+dim
        packet_id=self.evidence('packet-'+rid,'packet',m.packet(self.r,stage,reviewer))
        record=dict(id=rid,stage=stage,dimension=dim,revision=self.rev,verdict=verdict,reviewerId=reviewer,evidenceRefs=['report-'+rid],coverage=['u1'],issueIds=issue_ids or [],independent=True,packetRef=packet_id,supersedes=supersedes or [])
        report=dict(record,findings=[dict(unitId='u1',position='screen root',summary='Checked the full task and content against the source.',evidenceRefs=['tool'])])
        if stage=='plan' and dim=='experience':
            report['profileVerdict']='keep'
        if (stage=='plan' and dim=='experience') or (stage=='final' and dim=='ux'):
            report['simulationScenarios']=[
                dict(category=category,verdict='pass',summary='Simulated the user task and found no blocking ambiguity.')
                for category in ('happy-path','first-use','error','interrupt','post-success')
            ]
        self.evidence('report-'+rid,'review',report)
        self.r['reviews'].append(record)
        return record

    def refresh_final_reviews(self):
        self.r['reviews']=[x for x in self.r['reviews'] if x.get('stage')!='final']
        for dim in ('ux','ui','system'): self.review('final',dim)

    def capability(self,cid,refs=None):
        self.r['capabilities'].append(dict(id=cid,status='passed',revision=self.rev,evidenceRefs=refs or ['tool']))

    def issue(self,state='open',severity='P2'):
        x=dict(id='i1',severity=severity,originalSeverity=severity,stage='final',evidenceRefs=['tool'],unitIds=['u1'],state=state,fixAuthor='designer',resolution=dict(revision=self.rev,evidenceRefs=['verify'],reviewerId='verifier',reason='Rechecked the corrected content.'))
        self.r['issues'].append(x);return x

    def errors(self,gate='deliver',allow_fixture=True):
        return m.Gate(self.r,self.root,gate,allow_fixture).run()

    def fails(self,text,gate='deliver'):
        errors=self.errors(gate);self.assertTrue(errors);self.assertTrue(any(text in e for e in errors),errors)

    def test_complete_fixture_passes_all_gates(self):
        for gate in ['plan','build','deliver']: self.assertEqual([],self.errors(gate))

    def set_fast_profile(self):
        self.r['executionProfile']=dict(level='fast',source='auto',assessment=dict(taskModelChanged=False,navigationChanged=False,informationArchitectureChanged=False,permissionChanged=False,highRiskDestructive=False,longAsync=False,partialSuccess=False,crossContextMultiStep=False,newExperiencePattern=False,visibleUnitCount=1,componentCoverageExpectation='known-existing',ambiguity='low'),requiredSimulations=['happy-path'],reasons=['Existing task model with one local unit.'],escalationHistory=[])
        self.r['reviews']=[x for x in self.r['reviews'] if (x.get('stage')=='plan' and x.get('dimension') in ('requirements','experience')) or (x.get('stage')=='final' and x.get('dimension')=='ui')]
        self.edit_evidence('report-plan-experience',lambda x:x.update(simulationScenarios=[dict(category='happy-path',verdict='pass',summary='Happy path remains unchanged.')],profileVerdict='keep'))

    def test_fast_profile_passes_with_reduced_review_dimensions(self):
        self.set_fast_profile()
        for gate in ['plan','build','deliver']: self.assertEqual([],self.errors(gate))

    def test_fast_profile_rejects_structural_risk(self):
        self.set_fast_profile(); self.r['executionProfile']['assessment']['navigationChanged']=True
        self.fails('minimum is full','plan')

    def test_fast_profile_escalates_on_gap(self):
        self.set_fast_profile(); self.r['slots'][0]['resolution']='gap'
        self.r['slots'][0]['reuseLadder']=[dict(step='formal-instance',outcome='exhausted',reason='No match',evidenceRefs=['tool']),dict(step='compose',outcome='exhausted',reason='No composition',evidenceRefs=['tool']),dict(step='gap',outcome='matched',reason='Gap',evidenceRefs=['tool'])]
        self.fails('fast profile discovered gap','build')

    def test_layout_geometry_is_mandatory(self):
        self.r['checks']=[x for x in self.r['checks'] if x.get('kind')!='layout-geometry']
        self.fails('layout-geometry: missing current check','deliver')

    def test_layout_geometry_rejects_inconsistent_spacing(self):
        self.edit_evidence('layout',lambda x:x.update(measurements=[{'kind':'spacing-consistency','values':[12,16,12],'tolerance':1,'status':'within'}]))
        self.fails('exceeds tolerance','deliver')

    def test_plan_experience_review_requires_task_simulation(self):
        self.edit_evidence('report-plan-experience',lambda x:x.pop('simulationScenarios',None))
        self.fails('task simulation scenarios required','plan')

    def test_final_ux_review_requires_all_task_simulation_categories(self):
        self.edit_evidence('report-final-ux',lambda x:x.update(simulationScenarios=[dict(category='happy-path',verdict='pass',summary='Happy path checked.')]))
        self.fails('missing task simulations')

    def test_fixture_never_passes_production_gate(self): self.assertTrue(self.errors(allow_fixture=False))
    def test_empty_skeleton_fails(self): self.assertTrue(m.Gate(m.skeleton(),self.root,'plan').run())
    def test_missing_attachment_fails(self):
        self.r['sources'].append(dict(id='attachment',required=True,readStatus='unread',evidenceRefs=['source']));self.fails('required source unread','plan')
    def test_optional_unread_referenced_source_fails(self):
        self.r['sources'][0].update(required=False,readStatus='unread');self.fails('referenced source unread','plan')
    def test_unresolved_business_assumption(self):
        self.r['assumptions']=[dict(id='a',impact='business',status='open',evidenceRefs=['source'])];self.fails('assumption unresolved','plan')
    def test_requirements_need_reverse_mapping(self):
        self.r['units'][0]['requirementIds']=[];self.fails('reverse unit mapping','plan')
    def test_scope_cannot_be_disabled(self):
        self.r['units'][0]['required']=False;self.fails('active scope','plan')
    def test_open_p2_blocks_delivery(self): self.issue();self.fails('unresolved P2')
    def test_fix_applied_is_not_verified(self): self.issue('fix-applied');self.fails('unresolved P2')
    def test_independent_closed_issue_passes(self): self.issue('verified-closed');self.assertEqual([],self.errors())
    def test_self_verification_fails(self): self.issue('verified-closed')['resolution']['reviewerId']='designer';self.fails('independent verification')
    def test_downgrade_fails(self): self.issue(severity='P2').update(severity='suggestion',reason='Just preference');self.fails('downgrade')
    def test_duplicate_cycle_fails(self): self.issue('duplicate')['duplicateOf']='i1';self.fails('duplicate target')
    def test_stale_final_review_fails(self):
        self.r['revision']=dict(self.rev,design='v2');self.fails('final/ux: missing current review')
    def test_missing_visual_check_fails(self):
        self.r['checks']=[x for x in self.r['checks'] if x['kind']!='visual'];self.fails('visual: missing')
    def test_missing_capture_fails(self): self.r['captures']=[];self.fails('missing current screenshot')
    def test_required_degraded_fails(self): self.r['capabilities'][0]['status']='degraded';self.fails('degraded capability')
    def test_wrong_asset_identity_fails(self):
        self.edit_evidence('post',lambda x:x.update(sourceAssetKey='other'));self.fails('wrong source asset')
    def test_unauthorized_target_fails(self): self.r['implementations'][0]['targetId']='foreign';self.fails('outside authorization')
    def test_missing_protected_snapshot_fields_fails(self):
        self.edit_evidence('post',lambda x:x.pop('protected'));self.fails('snapshot fields incomplete')
    def test_protected_font_override_cannot_be_whitelisted(self):
        self.edit_evidence('post',lambda x:x['protected'].update(font=['Replacement']))
        self.r['implementations'][0]['writeWhitelist']=['/protected/font'];self.fails('protected formal fields differ')
    def test_variable_unbinding_fails_even_in_whitelist(self):
        self.edit_evidence('canonical',lambda x:x['protected'].update(variables=['official-variable']))
        self.r['implementations'][0]['writeWhitelist']=['/protected/variables'];self.fails('protected formal fields differ')
    def test_unexplained_fill_change_fails(self):
        self.edit_evidence('post',lambda x:x['protected'].update(fills=['recolor']))
        self.r['implementations'][0]['writeWhitelist']=['/protected/fills']
        self.fails('protected formal fields differ')
    def test_description_hint_fill_hide_passes(self):
        self.edit_evidence('canonical',lambda x:x.update(description='实例化后把间距示意层填充透明度改为 0，保留几何。'))
        self.edit_evidence('post',lambda x:x['protected'].update(fills={'padding':[{'visible':False,'color':'official'}]}))
        self.r['implementations'][0].update(writeWhitelist=['/protected/fills'],descriptionFillAdjustments=[dict(layerName='padding',nodeId='padding',paintIndex=0,property='visible',before=True,after=False,action='hide-fill',descriptionQuote='把间距示意层填充透明度改为 0')])
        self.assertEqual([],self.errors())
    def test_description_fill_quote_must_be_in_canonical_description(self):
        self.edit_evidence('canonical',lambda x:x.update(description='只用公开属性'))
        self.edit_evidence('post',lambda x:x['protected'].update(fills={'padding':[{'visible':False,'color':'official'}]}))
        self.r['implementations'][0].update(writeWhitelist=['/protected/fills'],descriptionFillAdjustments=[dict(layerName='padding',nodeId='padding',paintIndex=0,property='visible',before=True,after=False,action='hide-fill',descriptionQuote='把间距示意层填充透明度改为 0')])
        self.fails('quote not in canonical description')
    def test_description_fill_cannot_cover_font_change(self):
        self.edit_evidence('canonical',lambda x:x.update(description='实例化后把间距示意层填充透明度改为 0'))
        self.edit_evidence('post',lambda x:x['protected'].update(fills={'padding':[{'visible':False,'color':'official'}]},font=['Replacement']))
        self.r['implementations'][0].update(writeWhitelist=['/protected/fills','/protected/font'],descriptionFillAdjustments=[dict(layerName='padding',nodeId='padding',paintIndex=0,property='visible',before=True,after=False,action='hide-fill',descriptionQuote='把间距示意层填充透明度改为 0')])
        self.fails('protected formal fields differ')
    def test_claimed_fill_adjustment_without_fill_change_fails(self):
        self.edit_evidence('canonical',lambda x:x.update(description='实例化后把间距示意层填充透明度改为 0'))
        self.r['implementations'][0].update(writeWhitelist=['/protected/fills'],descriptionFillAdjustments=[dict(layerName='padding',nodeId='padding',paintIndex=0,property='visible',before=True,after=False,action='hide-fill',descriptionQuote='把间距示意层填充透明度改为 0')])
        self.fails('did not change fills')
    def test_description_fill_override_kind_allowed(self):
        self.edit_evidence('canonical',lambda x:x.update(description='实例化后把间距示意层填充透明度改为 0，保留几何。'))
        self.edit_evidence('post',lambda x:x.update(overrides=[dict(kind='description-fill',path='/protected/fills')]) or x['protected'].update(fills={'padding':[{'visible':False,'color':'official'}]}))
        self.r['implementations'][0].update(writeWhitelist=['/protected/fills','/overrides'],descriptionFillAdjustments=[dict(layerName='padding',nodeId='padding',paintIndex=0,property='visible',before=True,after=False,action='hide-fill',descriptionQuote='把间距示意层填充透明度改为 0')])
        self.assertEqual([],self.errors())
    def test_broad_root_whitelist_fails(self): self.r['implementations'][0]['writeWhitelist']=['/'];self.fails('invalid/broad whitelist')
    def test_missing_property_fact_fails(self):
        self.r['implementations'][0]['expectedFacts']={'content':{'headline':'Wrong'}}
        self.fails('actual fact mismatch')
    def test_empty_expected_facts_passes(self):
        self.r['implementations'][0]['expectedFacts']={}
        self.assertEqual([],self.errors())
    def test_name_and_layout_change_without_whitelist_passes(self):
        self.edit_evidence('post',lambda x:x.update(name='Answer column',layout={'width':120}))
        self.r['implementations'][0]['writeWhitelist']=[]
        self.assertEqual([],self.errors())
    def test_snapshot_may_include_extra_tool_fields(self):
        self.edit_evidence('post',lambda x:x.update(rawToolDump={'ok':True}))
        self.assertEqual([],self.errors())
    def test_packet_may_include_extra_notes(self):
        self.edit_evidence('packet-final-ux',lambda x:x.update(notes='Reviewed screenshots first.'))
        self.assertEqual([],self.errors())
    def test_description_hint_fill_hide_without_whitelist_passes(self):
        self.edit_evidence('canonical',lambda x:x.update(description='实例化后把间距示意层填充透明度改为 0，保留几何。'))
        self.edit_evidence('post',lambda x:x['protected'].update(fills={'padding':[{'visible':False,'color':'official'}]}))
        self.r['implementations'][0].update(writeWhitelist=[],descriptionFillAdjustments=[dict(layerName='padding',nodeId='padding',paintIndex=0,property='visible',before=True,after=False,action='hide-fill',descriptionQuote='把间距示意层填充透明度改为 0')])
        self.assertEqual([],self.errors())
    def test_packet_cannot_include_conclusions(self):
        self.edit_evidence('packet-final-ux',lambda x:x.update(previousVerdict='passed'));self.fails('possible conclusion leak')
    def test_packet_cannot_include_system_evidence(self):
        self.edit_evidence('packet-final-ux',lambda x:x['evidenceRefs'].append('tool'));self.fails('wrong evidence kind')
    def test_review_packet_ref_must_be_packet_kind(self):
        self.r['reviews'][0]['packetRef']='tool';self.fails('packetRef must reference kind=packet')
    def test_review_packet_ref_must_exist(self):
        self.r['reviews'][0]['packetRef']='missing-packet';self.fails('packetRef must reference kind=packet')
    def test_report_cannot_omit_recorded_findings(self):
        self.edit_evidence('report-final-ux',lambda x:x.update(issueIds=['undisclosed']));self.fails('report differs from record')
    def test_hash_tampering_fails(self):
        (self.root/'source.json').write_text('tampered');self.fails('hash mismatch')
    def test_path_escape_fails(self): self.r['evidence'][0]['path']='../outside.json';self.fails('outside run directory')
    def test_history_supersession_allows_corrected_false_positive(self):
        self.issue('not-a-bug')
        old=next(x for x in self.r['reviews'] if x['id']=='final-ux');old.update(verdict='issues',issueIds=['i1'])
        self.evidence('report-final-ux','review',dict(old,findings=[dict(unitId='u1',position='screen root',summary='Original disputed finding.',evidenceRefs=['tool'])]))
        self.review('final','ux',rid='final-ux-recheck',supersedes=['final-ux'])
        self.assertEqual([],self.errors())
    def good_prd(self):
        body='# 任务管理 Requirement Spec\n\n## 业务目标 / 目标用户 / 用户任务 / 成功标准\n'+'目标用户需要查看和管理自己的任务，并能明确判断任务是否已完成。'*12
        body+='\n\n## 范围与约束\n范围内：任务查看、状态更新和必要业务规则。范围外：搜索与日历。'*6
        body+='\n\n## 业务规则 / 数据 / 权限 / 依赖\n任务有标题、状态与更新时间；用户只能修改自己有权限的任务。'*6
        body+='\n\n## 用户上下文与预期结果\n用户进入前已有任务数据；完成后应明确知道当前任务状态。'*6
        body+='\n\n## 异常事实与验收标准\n无数据、权限不足和网络失败属于需要覆盖的业务事实；逐条对照验收。'*6
        body+='\n\n## 假设与未决问题\n批量能力不在本次范围；未知项不得被提前写成页面方案。'*6
        return body

    def test_text_intake_requires_authored_prd(self):
        self.r['intake']=dict(inputMode='text',deliverableDecision=self.decision(),prdArtifact=None,sourceDocs=[],originalSourceIds=['s1'],rewritePolicy='authored')
        self.fails('prdArtifact','plan')

    def test_text_intake_complete_prd_passes(self):
        self.text_evidence('prd-doc','source',self.good_prd())
        self.r['intake']=dict(inputMode='text',deliverableDecision=self.decision(),prdArtifact={'path':'prd-doc.md','evidenceRef':'prd-doc'},sourceDocs=[],originalSourceIds=['s1'],rewritePolicy='authored',clarifications=[])
        self.assertEqual([],self.errors('plan'))

    def test_text_intake_empty_prd_fails(self):
        self.text_evidence('prd-doc','source','')
        self.r['intake']=dict(inputMode='text',deliverableDecision=self.decision(),prdArtifact={'path':'prd-doc.md','evidenceRef':'prd-doc'},sourceDocs=[],originalSourceIds=['s1'],rewritePolicy='authored')
        self.fails('PRD','plan')

    def test_text_intake_prd_must_be_authored_source(self):
        self.text_evidence('prd-doc','source',self.good_prd(),provenance='captured')
        self.r['intake']=dict(inputMode='text',deliverableDecision=self.decision(),prdArtifact={'path':'prd-doc.md','evidenceRef':'prd-doc'},sourceDocs=[],originalSourceIds=['s1'],rewritePolicy='authored')
        self.fails('authored','plan')

    def test_uploaded_prd_must_be_verbatim(self):
        self.r['intake']=dict(inputMode='prd-file',deliverableDecision=self.decision(),prdArtifact=None,sourceDocs=['s1'],rewritePolicy='authored')
        self.fails('verbatim','plan')

    def test_uploaded_prd_cannot_be_rewritten(self):
        self.text_evidence('rewrite','source','# 需求摘要\n精简后的内容。',provenance='authored')
        self.r['intake']=dict(inputMode='prd-file',deliverableDecision=self.decision(),prdArtifact=None,sourceDocs=['s1'],rewritePolicy='verbatim')
        self.fails('rewrite','plan')

    def test_uploaded_prd_must_be_read(self):
        self.r['sources'].append(dict(id='upload',required=True,readStatus='unread',evidenceRefs=['source']))
        self.r['intake']=dict(inputMode='prd-file',deliverableDecision=self.decision(),prdArtifact=None,sourceDocs=['upload'],rewritePolicy='verbatim')
        self.fails('uploaded PRD unread','plan')

    def test_generate_requires_intake_record(self):
        self.r.pop('intake')
        self.fails('intake record required','plan')

    def test_generate_requires_reference_review(self):
        self.r.pop('referenceReview')
        self.fails('referenceReview required','plan')

    def test_builtin_reference_must_be_inspected(self):
        self.r['referenceReview']['sources'][0]['evidenceRefs']=[]
        self.fails('referenceReview.sources[0]: missing evidenceRefs','plan')

    def test_generate_requires_existing_page_scan(self):
        self.r['referenceReview'].pop('existingPageScan')
        self.fails('existingPageScan required','plan')

    def test_existing_page_scan_needs_evidence(self):
        self.r['referenceReview']['existingPageScan']['evidenceRefs']=[]
        self.fails('existingPageScan: missing evidenceRefs','plan')

    def test_reference_evidence_cannot_be_authored(self):
        self.text_evidence('reference-authored','reference','# Fabricated reference note')
        self.r['referenceReview']['sources'][0]['evidenceRefs']=['reference-authored']
        self.fails('must be captured from the live tool','plan')

    def test_builtin_template_file_identity_is_fixed(self):
        self.r['referenceReview']['sources'][0]['fileKey']='wrong-file'
        self.fails('fileKey mismatch','plan')

    def test_builtin_template_node_is_resolved_live(self):
        self.r['referenceReview']['sources'][0]['nodeId']='runtime-page-id'
        self.r['referenceReview']['sources'][0]['url']='https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/example?node-id=runtime-page-id'
        for gate in ['plan','build','deliver']:
            self.assertEqual([],self.errors(gate))

    def test_builtin_template_source_kind_is_required(self):
        self.r['referenceReview']['sources'][0]['sourceKind']='user-reference'
        self.fails('sourceKind must be component-library-template for built-in','plan')

    def test_builtin_template_page_name_is_required(self):
        self.r['referenceReview']['sources'][0].pop('pageName')
        self.fails('pageName required','plan')

    def test_builtin_template_page_name_is_exact(self):
        self.r['referenceReview']['sources'][0]['pageName']='AI参考案例 Template'
        self.fails('pageName mismatch','plan')

    def test_matched_target_page_requires_reuse_action(self):
        self.r['referenceReview']['sources'].append(dict(
            id='existing-flow',origin='target-file',sourceKind='target-existing-page',
            fileKey='target-file',nodeId='existing-flow',pageName='现有流程',nodeName='任务页',
            url='https://www.figma.com/design/target-file/example?node-id=existing-flow',
            decision='matched',reason='Existing task page covers the frozen flow.',evidenceRefs=['reference'],
            extractedPatterns=['Existing shell and task sequence'],unitIds=['u1'],changeScope=[],
        ))
        self.fails('reuseAction must be','plan')

    def test_direct_reuse_only_allows_flow_order_change(self):
        self.r['referenceReview']['sources'].append(dict(
            id='existing-flow',origin='target-file',sourceKind='target-existing-page',
            fileKey='target-file',nodeId='existing-flow',pageName='现有流程',nodeName='任务页',
            url='https://www.figma.com/design/target-file/example?node-id=existing-flow',
            decision='matched',reason='Existing task page covers the frozen flow.',evidenceRefs=['reference'],
            extractedPatterns=['Existing shell and task sequence'],unitIds=['u1'],reuseAction='direct-reuse',changeScope=['content'],
        ))
        self.fails('direct-reuse may only change flow-order','plan')

    def test_adapt_reuse_requires_change_scope(self):
        self.r['referenceReview']['sources'].append(dict(
            id='existing-flow',origin='target-file',sourceKind='target-existing-page',
            fileKey='target-file',nodeId='existing-flow',pageName='现有流程',nodeName='任务页',
            url='https://www.figma.com/design/target-file/example?node-id=existing-flow',
            decision='matched',reason='Existing task page can be adapted.',evidenceRefs=['reference'],
            extractedPatterns=['Existing shell and task sequence'],unitIds=['u1'],reuseAction='adapt-reuse',changeScope=[],
        ))
        self.fails('adapt-reuse requires changeScope','plan')

    def test_target_page_direct_reuse_requires_matching_baseline(self):
        self.replicated()
        self.r['referenceReview']['sources'].append(dict(
            id='existing-flow',origin='target-file',sourceKind='target-existing-page',
            fileKey='target-file',nodeId='live:561:23392',pageName='现有流程',nodeName='任务页',
            url='https://www.figma.com/design/target-file/example?node-id=live-561-23392',
            decision='matched',reason='Existing task page directly covers the frozen flow.',evidenceRefs=['reference'],
            extractedPatterns=['Existing shell and task sequence'],unitIds=['u1'],reuseAction='direct-reuse',changeScope=['flow-order'],
        ))
        self.assertEqual([],self.errors('plan'))
        self.r['units'][0]['liveBaseline']['screenRef']='different-node'
        self.fails('screenRef must match reused page nodeId','plan')

    def test_matched_template_child_flow_can_be_adapted_without_live_baseline(self):
        self.r['referenceReview']['sources'].append(dict(
            id='template-minor-flow',origin='built-in',sourceKind='component-library-template',
            fileKey=m.BUILTIN_REFERENCE_FILE_KEY,nodeId='minor-flow',pageName=m.BUILTIN_REFERENCE_PAGE_NAME,
            nodeName='未成年模式任务流程',url='https://www.figma.com/design/iUyH8VSdURxlGrhp646zYJ/example?node-id=minor-flow',
            decision='matched',reason='The template contains the same two-step task flow.',evidenceRefs=['reference'],
            extractedPatterns=['Two-step task sequence','Shared completion state'],unitIds=['u1'],
            reuseAction='adapt-reuse',changeScope=['content','states'],
        ))
        for gate in ['plan','build','deliver']:
            self.assertEqual([],self.errors(gate))

    def test_matched_reference_requires_extracted_patterns(self):
        self.r['referenceReview']['sources'][0]['decision']='matched'
        self.fails('extractedPatterns required','plan')

    def test_reference_evidence_reaches_plan_packet(self):
        packet=m.packet(self.r,'plan','plan-experience')
        self.assertIn('reference',packet['evidenceRefs'])

    def test_uploaded_prd_rewrite_requires_user_authorization(self):
        self.r['intake']=dict(inputMode='prd-file',deliverableDecision=self.decision(),prdArtifact=None,sourceDocs=['s1'],rewritePolicy='rewrite-authorized')
        self.fails('rewriteAuthorization','plan')

    def test_uploaded_prd_rewrite_with_user_authorization_passes(self):
        self.evidence('rewrite-auth','authorization',{'request':'把这份 PRD 精简成摘要'})
        self.text_evidence('rewrite','source','# 需求摘要\n用户要求精简后的内容。',provenance='authored')
        self.r['intake']=dict(inputMode='prd-file',deliverableDecision=self.decision(),prdArtifact={'evidenceRef':'rewrite'},sourceDocs=['s1'],
                              rewritePolicy='rewrite-authorized',rewriteAuthorization={'evidenceRefs':['rewrite-auth']})
        self.assertEqual([],self.errors('plan'))

    def test_uploaded_prd_rewrite_authorization_must_be_user_evidence(self):
        self.r['intake']=dict(inputMode='prd-file',deliverableDecision=self.decision(),prdArtifact=None,sourceDocs=['s1'],
                              rewritePolicy='rewrite-authorized',rewriteAuthorization={'evidenceRefs':['tool']})
        self.fails('wrong evidence kind','plan')

    def test_deliverable_decision_required(self):
        self.r['intake'].pop('deliverableDecision')
        self.fails('deliverableDecision required','plan')

    def test_deliverable_user_choice_must_match_root(self):
        self.r['intake']['deliverableDecision']=self.decision(choice='web-demo')
        self.fails('must equal deliverable','plan')

    def test_deliverable_user_choice_needs_evidence(self):
        self.r['intake']['deliverableDecision']=self.decision(refs=[])
        self.fails('deliverable decision: missing evidenceRefs','plan')

    def test_deliverable_no_reply_defaults_to_web_demo(self):
        self.r['deliverable']='web-demo';self.r['units'][0]['deliverables']=['demo']
        self.r['intake']['deliverableDecision']=self.decision(source='asked',choice=None,reason='no-reply',refs=[])
        self.assertEqual([],self.errors('plan'))

    def test_deliverable_no_reply_cannot_stay_figma(self):
        self.r['intake']['deliverableDecision']=self.decision(source='asked',choice=None,reason='no-reply',refs=[])
        self.fails('must default to web-demo','plan')

    def test_deliverable_cannot_ask_defaults_to_web_demo(self):
        self.r['deliverable']='web-demo';self.r['units'][0]['deliverables']=['demo']
        self.r['intake']['deliverableDecision']=self.decision(source='fallback',choice=None,reason='cannot-ask',refs=[])
        self.assertEqual([],self.errors('plan'))

    def test_deliverable_asked_without_reply_needs_reason(self):
        self.r['intake']['deliverableDecision']=self.decision(source='asked',choice=None,reason=None,refs=[])
        self.fails('fallbackReason=no-reply','plan')

    def gap(self):
        self.r['libraryCatalog']=dict(libraryKey=self.r['liveLibrary']['libraryKey'],complete=True,ids=['component'],evidenceRefs=['tool'])
        self.r['slots'][0].update(
            resolution='gap',chosenAssets=[],
            candidates=[dict(key='component',gateDecision='reject-proven-mismatch',reason='The published part cannot carry the unique responsibility.',evidenceRefs=['tool'])],
            searchAttempts=[dict(source='semantic',query='task content',evidenceRefs=['tool']),dict(source='semantic',query='unique business content',evidenceRefs=['tool']),dict(source='published-name',query='Component',evidenceRefs=['tool'])],
            reuseLadder=[
                dict(step='formal-instance',outcome='exhausted',reason='No single published component covers the full responsibility.',evidenceRefs=['tool']),
                dict(step='compose',outcome='exhausted',reason='Every published composition still lacks a required capability.',evidenceRefs=['tool']),
                dict(step='gap',outcome='matched',reason='Only a new reusable component can carry the unique business content.',evidenceRefs=['tool']),
            ],
            composeTrials=[dict(host='layout',parts=['component'],outcome='reject-proven-mismatch',reason='The published part cannot carry the unique responsibility.',evidenceRefs=['tool'])],
            inventory=dict(complete=True,eligibleIds=['component'],scannedIds=['component'],exclusions=[],evidenceRefs=['tool']),
            compositionEvidenceRefs=['tool'])
        for cid in ['create-component','bind-foundations','compose-check']:self.capability(cid)
    def layout_compose(self,slot,children):
        slot.update(resolution='compose',chosenAssets=[],candidates=[],layoutOnly=True,
                    layoutReason='Pure layout host; it only arranges published children.',
                    childSlotIds=children,
                    slotBindings=[dict(childSlotId=c,parentAssetKey='layout:'+slot['id'],host='content',evidenceRefs=['tool']) for c in children],
                    reuseLadder=[dict(step='formal-instance',outcome='exhausted',reason='No single published component covers the host responsibility.',evidenceRefs=['tool']),
                                 dict(step='compose',outcome='matched',reason='Published children compose under a pure layout host.',evidenceRefs=['tool'])])
    def test_empty_catalog_can_prove_gap(self):
        self.gap();slot=self.r['slots'][0]
        self.r['libraryCatalog']['ids']=[]
        self.r['liveLibrary']['ids']=[];self.r['liveLibrary']['emptyProof']=True
        slot['composeTrials'][0]['parts']=[];slot['candidates']=[]
        slot['inventory'].update(eligibleIds=[],scannedIds=[],exclusions=[])
        self.assertEqual([],self.errors('build'))
    def test_complete_empty_catalog_rejects_nonempty_live_library(self):
        self.gap();self.r['libraryCatalog']['ids']=[]
        self.fails('liveLibrary ids must be a subset','build')
    def test_complete_catalog_rejects_unlisted_live_id(self):
        self.gap();self.r['liveLibrary']['ids']=['component','stale']
        self.fails('liveLibrary ids must be a subset','build')
    def test_partial_inventory_cannot_prove_gap(self): self.gap();self.r['slots'][0]['inventory']['eligibleIds']=['unread'];self.fails('coverage mismatch','build')
    def test_gap_unknown_candidate_blocks(self):
        self.gap();self.r['slots'][0]['candidates']=[dict(key='unknown',gateDecision='blocked-insufficient-evidence',reason='Unclear',evidenceRefs=['tool'])];self.fails('gap has unresolved','build')
    def test_gap_requires_real_component(self): self.gap();self.fails('gap not built as reusable component')
    def test_gap_requires_reuse_ladder(self):
        self.gap();self.r['slots'][0].pop('reuseLadder');self.fails('reuseLadder required','build')
    def test_gap_requires_compose_exhausted_before_gap(self):
        self.gap();self.r['slots'][0]['reuseLadder']=[x for x in self.r['slots'][0]['reuseLadder'] if x['step']!='compose']
        self.fails('reuseLadder must record','build')
    def test_gap_requires_compose_trials(self):
        self.gap();self.r['slots'][0].pop('composeTrials');self.fails('composeTrials','build')
    def test_gap_compose_trial_parts_must_be_in_live_catalog(self):
        self.gap();self.r['slots'][0]['composeTrials'][0]['parts']=['not-published'];self.fails('part not in live catalog','build')
    def test_gap_requires_live_catalog(self):
        self.gap();self.r['libraryCatalog']['complete']=False;self.fails('complete live catalog','build')
    def test_gap_inventory_ids_must_come_from_catalog(self):
        self.gap();slot=self.r['slots'][0];slot['candidates']=[dict(key='other',gateDecision='reject-proven-mismatch',reason='Not a fit.',evidenceRefs=['tool'])];
        slot['inventory'].update(eligibleIds=['other'],scannedIds=['other'],exclusions=[]);self.fails('absent from live catalog','build')
    def test_gap_does_not_require_repeated_semantic_searches(self):
        self.gap();self.r['slots'][0]['searchAttempts']=[dict(source='semantic',query='task content',evidenceRefs=['tool']),dict(source='published-name',query='Component',evidenceRefs=['tool'])]
        self.assertEqual([],self.errors('build'))
    def test_gap_requires_name_or_inventory_fallback(self):
        self.gap();self.r['slots'][0]['searchAttempts']=[dict(source='semantic',query='task content',evidenceRefs=['tool']),dict(source='semantic',query='unique content',evidenceRefs=['tool'])]
        self.fails('fallback attempt','build')
    def test_gap_requires_compose_check_capability(self):
        self.gap();self.r['capabilities']=[c for c in self.r['capabilities'] if c['id']!='compose-check'];self.fails('mandatory capability probes missing','build')
    def test_nonempty_catalog_needs_scoped_eligible_ids(self):
        self.gap();slot=self.r['slots'][0];slot['candidates']=[];slot['inventory'].update(eligibleIds=[],scannedIds=[],exclusions=[])
        self.fails('scopeReason','build')
        slot['inventory']['scopeReason']='No published asset is possibly relevant to this domain.'
        self.fails('unclassified catalog assets','build')
    def test_compose_requires_layout_only_or_formal_host(self):
        child=copy.deepcopy(self.r['slots'][0]);child['id']='child';self.layout_compose(self.r['slots'][0],['child']);self.r['slots'].append(child)
        self.r['slots'][0].pop('layoutOnly');self.fails('compose layoutOnly boolean required','build')
    def test_compose_layout_host_needs_reason(self):
        child=copy.deepcopy(self.r['slots'][0]);child['id']='child';self.layout_compose(self.r['slots'][0],['child']);self.r['slots'].append(child)
        self.r['slots'][0].pop('layoutReason');self.fails('layoutReason','build')
    def test_compose_requires_formal_instance_exhausted(self):
        child=copy.deepcopy(self.r['slots'][0]);child['id']='child';self.layout_compose(self.r['slots'][0],['child']);self.r['slots'].append(child)
        self.r['slots'][0]['reuseLadder']=[dict(step='compose',outcome='matched',reason='Layout host with published children.',evidenceRefs=['tool'])]
        self.fails('reuseLadder must record','build')
    def test_formal_slot_ladder_must_match_resolution(self):
        self.r['slots'][0]['reuseLadder']=[dict(step='compose',outcome='matched',reason='Wrong step.',evidenceRefs=['tool'])]
        self.fails('matched reuseLadder step must equal resolution','build')
    def test_subslot_cycle_blocks(self):
        self.r['slots'][0].update(childSlotIds=['slot'],slotBindings=[dict(childSlotId='slot',host='self',evidenceRefs=['tool'])]);self.capability('slot-write');self.fails('dependency cycle','build')
    def test_interaction_executed_cannot_use_design_only(self):
        self.r['units'][0]['interactionLevel']='executed'
        self.r['checks'].append(dict(id='interaction',unitId='u1',deliverable='figma',kind='interaction',revision=self.rev,result='pass',level='design',evidenceRefs=['verify']))
        self.fails('interaction evidence level mismatch')
    def test_both_requires_demo_branch(self):
        self.r['deliverable']='both';self.r['intake']['deliverableDecision']=self.decision(choice='both')
        self.fails('missing deliverable branch')
    def test_local_gap_component_and_instance_pass(self):
        self.gap()
        self.evidence('local-main','tool',dict(nodeId='main',type='COMPONENT',dependencyKeys=[],boundFoundations=['official-foundation'],description='Required unique business content.'))
        self.r['localComponents']=[dict(id='local',slotId='slot',nodeId='main',dependencyKeys=[],instanceNodeIds=['node'],evidenceRefs=['local-main'],mainEvidenceRef='local-main')]
        self.r['implementations'][0].update(origin='local',localComponentId='local',expectedFacts={'mainComponentId':'main'})
        for eid in ['pre','post']:
            self.edit_evidence(eid,lambda x:x.update(sourceAssetKey=None,mainComponentKey=None,mainComponentId='main'))
        self.assertEqual([],self.errors())

    def test_demo_delivery_passes_with_manifest_evidence(self):
        self.r['deliverable']='web-demo'; self.r['intake']['deliverableDecision']=self.decision(choice='web-demo'); self.r['units'][0]['deliverables']=['demo']
        for item in self.r['captures']+self.r['checks']+self.r['implementations']:item['deliverable']='demo'
        self.edit_evidence('content',lambda x:x.update(demo={'headline':'Business content'}))
        self.edit_evidence('overflow',lambda x:x.update(deliverable='demo'))
        self.edit_evidence('audit',lambda x:x.update(deliverable='demo'))
        self.edit_evidence('layout',lambda x:x.update(deliverable='demo'))
        for eid in ['pre','post']:self.edit_evidence(eid,lambda x:x.update(type='DOM'))
        for cid in ['demo-mapping','demo-render','demo-interaction']:self.capability(cid)
        self.r['implementations'][0]['mapping']=dict(chosenLiveKey='component',manifestAssetKey='component',generatedExport='Component',propertySchemaMatch=True,evidenceRefs=['tool'])
        self.assertEqual([],self.errors())

    def test_observed_scope_cannot_be_faked_by_record(self):
        self.edit_evidence('post',lambda x:x.update(targetId='foreign'))
        self.fails('observed write scope mismatch')

    def test_explicit_checkpoint_requires_actual_confirmation(self):
        self.r['authorization']['requirePlanConfirmation']=True
        self.fails('required user plan confirmation missing','plan')
        self.r['planConfirmation']=dict(revision=self.rev,evidenceRefs=['auth'])
        self.assertEqual([],self.errors('plan'))

    def test_user_confirmed_basis_needs_confirmation(self):
        self.r['slots'][0]['requirementsBasis']='user-confirmed'
        self.fails('required user plan confirmation missing','build')

    def test_historical_findings_cannot_disappear_from_ledger(self):
        old=self.review('final','ux',rid='old-ux',verdict='issues',issue_ids=['lost-p1'])
        old['revision']=dict(self.rev,design='old')
        self.evidence('report-old-ux','review',dict(old,findings=[dict(unitId='u1',position='screen root',summary='An unresolved historical issue.',evidenceRefs=['tool'])]))
        self.fails('historical findings absent from ledger')

    def test_binding_requires_host_and_parent(self):
        parent=copy.deepcopy(self.r['slots'][0]);parent['id']='parent';self.layout_compose(parent,['slot'])
        parent['slotBindings'][0].pop('host');parent['slotBindings'][0].pop('parentAssetKey')
        self.r['slots'].append(parent);self.capability('slot-write')
        self.fails('binding host missing','build')
        parent['slotBindings'][0]['host']='body'
        self.fails('binding parent not selected','build')
        parent['slotBindings'][0]['parentAssetKey']='layout:parent'
        self.assertEqual([],self.errors('build'))

    def local_fixture(self):
        self.gap()
        self.evidence('local-main','tool',dict(nodeId='main',type='COMPONENT',dependencyKeys=[],boundFoundations=['official-foundation'],description='Unique content.'))
        self.r['localComponents']=[dict(id='local',slotId='slot',nodeId='main',dependencyKeys=[],instanceNodeIds=['node'],evidenceRefs=['local-main'],mainEvidenceRef='local-main')]
        self.r['implementations'][0].update(origin='local',localComponentId='local',expectedFacts={'mainComponentId':'main'})
        for eid in ['pre','post']:self.edit_evidence(eid,lambda x:x.update(sourceAssetKey=None,mainComponentKey=None,mainComponentId='main'))

    def test_figma_local_cannot_use_code_component(self):
        self.local_fixture();self.edit_evidence('local-main',lambda x:x.update(type='CODE_COMPONENT'))
        self.fails('local main is not a reusable component')

    def test_local_formal_dependency_needs_recursive_resolution(self):
        self.local_fixture();self.r['localComponents'][0]['dependencyKeys']=['unselected']
        self.edit_evidence('local-main',lambda x:x.update(dependencyKeys=['unselected']))
        self.fails('formal dependency has no recursive slot resolution')

    def test_layout_composition_needs_no_nonexistent_parent_component(self):
        child=copy.deepcopy(self.r['slots'][0]);child['id']='child'
        self.layout_compose(self.r['slots'][0],['child'])
        self.r['slots'].append(child);self.capability('slot-write')
        self.assertEqual([],self.errors('build'))

    def test_local_formal_dependency_is_verified_in_actual_ancestry(self):
        child=copy.deepcopy(self.r['slots'][0]);child['id']='child'
        child_impl=copy.deepcopy(self.r['implementations'][0]);child_impl.update(id='child-impl',slotId='child',nodeId='child-node',preEvidenceRef='child-pre',postEvidenceRef='child-post')
        for eid in ['pre','post']:
            value=m.load_json(self.root/(eid+'.json'));value.update(nodeId='child-node',ancestorIds=['node','target'],parentId='node')
            self.evidence('child-'+eid,'tool',value)
        self.local_fixture()
        self.r['slots'][0].update(childSlotIds=['child'],slotBindings=[dict(childSlotId='child',parentAssetKey='local:slot',host='actions',evidenceRefs=['tool'])],candidates=[dict(key='component',gateDecision='reject-proven-mismatch',reason='Only handles the child responsibility',evidenceRefs=['tool'])],inventory=dict(complete=True,eligibleIds=['component'],scannedIds=['component'],exclusions=[],evidenceRefs=['tool']))
        self.r['slots'].append(child);self.r['implementations'].append(child_impl)
        self.r['localComponents'][0]['dependencyKeys']=['component']
        self.edit_evidence('local-main',lambda x:x.update(dependencyKeys=['component']))
        self.assertEqual([],self.errors())
        self.edit_evidence('child-post',lambda x:x.update(ancestorIds=['target']))
        self.fails('formal dependency not instantiated inside local component')

    def test_composition_build_does_not_require_formal_slot_api(self):
        child=copy.deepcopy(self.r['slots'][0]);child['id']='child'
        self.layout_compose(self.r['slots'][0],['child'])
        self.r['slots'].append(child)
        self.assertEqual([],self.errors('build'))

    def test_authorized_reparent_updates_derived_ancestry(self):
        self.edit_evidence('post',lambda x:x.update(parentId='layout-host',ancestorIds=['layout-host','target']))
        self.r['implementations'][0]['writeWhitelist']=['/parentId']
        self.assertEqual([],self.errors())
        self.r['implementations'][0]['writeWhitelist'].append('/ancestorIds')
        self.assertEqual([],self.errors())

    def test_visual_layout_change_does_not_need_whitelist(self):
        self.edit_evidence('post',lambda x:x.update(ancestorIds=['target','page']))
        self.assertEqual([],self.errors())

    def test_cli_init_does_not_overwrite(self):
        target=self.root/'new';cmd=[sys.executable,str(ROOT/'scripts/validate-run.py'),'--init',str(target)]
        self.assertEqual(0,subprocess.run(cmd,capture_output=True).returncode)
        self.assertNotEqual(0,subprocess.run(cmd,capture_output=True).returncode)

    def replicated(self):
        self.evidence('live','baseline',{'fixture':True,'purpose':'live reference'})
        self.r['units'][0]['liveBaseline']=dict(applicability='replicated',screenRef='live:561:23392',evidenceRefs=['live'])
        self.evidence('baseline','baseline',dict(unitId='u1',deliverable='figma',verdict='pass',elements=[dict(id='chip',live={'w':63},ours={'w':65},deltas=[dict(field='w',live=63,ours=65,delta=2,tolerance=2,status='within')])]))
        self.r['implementations'][0]['baselineElementId']='chip'
        self.r['checks'].append(dict(id='baseline',unitId='u1',deliverable='figma',kind='baseline',revision=self.rev,result='pass',evidenceRefs=['baseline']))

    def both(self):
        self.r['deliverable']='both'; self.r['intake']['deliverableDecision']=self.decision(choice='both'); self.r['units'][0]['deliverables']=['figma','demo']
        for cid in ['demo-mapping','demo-render','demo-interaction']: self.capability(cid)
        demo=copy.deepcopy(self.r['implementations'][0]); demo['id']='impl-demo'; demo['deliverable']='demo'
        base=m.load_json(self.root/next(e['path'] for e in self.r['evidence'] if e['id']=='pre'))
        for eid in ['pre-demo','post-demo']: self.evidence(eid,'tool',dict(base,type='DOM'))
        demo.update(preEvidenceRef='pre-demo',postEvidenceRef='post-demo',mapping=dict(chosenLiveKey='component',manifestAssetKey='component',generatedExport='Component',propertySchemaMatch=True,evidenceRefs=['tool']))
        self.r['implementations'].append(demo)
        self.evidence('capture-demo','screenshot',{'fixture':True})
        self.r['captures'].append(dict(unitId='u1',deliverable='demo',revision=self.rev,evidenceRef='capture-demo'))
        self.evidence('overflow-demo','tool',dict(unitId='u1',deliverable='demo',checked=[{'nodeId':'node'}],escapes=[],verdict='pass'))
        self.evidence('audit-demo','tool',dict(unitId='u1',deliverable='demo',verdict='pass',scanned=[{'nodeId':'node'}],unregistered=[],misclassified=[]))
        self.evidence('layout-demo','tool',dict(unitId='u1',deliverable='demo',verdict='pass',checked=[{'nodeId':'node','role':'screen-root','layoutMode':'VERTICAL'}],measurements=[{'kind':'edge-alignment','values':[16,16,16],'tolerance':1,'status':'within'}],violations=[]))
        self.edit_evidence('content',lambda x:x.update(demo={'headline':'Business content'}))
        self.r['checks'].append(dict(id='demo-visual',unitId='u1',deliverable='demo',kind='visual',revision=self.rev,result='pass',evidenceRefs=['capture-demo']))
        self.r['checks'].append(dict(id='demo-content',unitId='u1',deliverable='demo',kind='content',revision=self.rev,result='pass',evidenceRefs=['content']))
        self.r['checks'].append(dict(id='demo-overflow',unitId='u1',deliverable='demo',kind='overflow',revision=self.rev,result='pass',evidenceRefs=['overflow-demo']))
        self.r['checks'].append(dict(id='demo-node-audit',unitId='u1',deliverable='demo',kind='node-audit',revision=self.rev,result='pass',evidenceRefs=['audit-demo']))
        self.r['checks'].append(dict(id='demo-layout-geometry',unitId='u1',deliverable='demo',kind='layout-geometry',revision=self.rev,result='pass',evidenceRefs=['layout-demo']))
        self.evidence('parity','verification',dict(unitId='u1',verdict='pass',mismatches=[],figma={'elements':['chip']},demo={'elements':['chip']}))
        self.r['checks'].append(dict(id='parity',unitId='u1',deliverable='figma',kind='parity',revision=self.rev,result='pass',evidenceRefs=['capture','capture-demo','parity']))

    def demo_run(self):
        self.r['deliverable']='web-demo'; self.r['intake']['deliverableDecision']=self.decision(choice='web-demo'); self.r['units'][0]['deliverables']=['demo']
        for item in self.r['captures']+self.r['checks']+self.r['implementations']:item['deliverable']='demo'
        self.edit_evidence('content',lambda x:x.update(demo={'headline':'Business content'}))
        self.edit_evidence('overflow',lambda x:x.update(deliverable='demo'))
        self.edit_evidence('audit',lambda x:x.update(deliverable='demo'))
        self.edit_evidence('layout',lambda x:x.update(deliverable='demo'))
        for eid in ['pre','post']:self.edit_evidence(eid,lambda x:x.update(type='DOM'))
        for cid in ['demo-mapping','demo-render','demo-interaction']:self.capability(cid)
        self.r['implementations'][0]['mapping']=dict(chosenLiveKey='component',manifestAssetKey='component',generatedExport='Component',propertySchemaMatch=True,evidenceRefs=['tool'])

    def readonly_run(self):
        self.r.update(mode='review-existing',stage='report',status='complete')
        self.r['sources']=[]; self.r['requirements']=[]; self.r['slots']=[]; self.r['implementations']=[]
        self.r['localComponents']=[]; self.r['capabilities']=[]; self.r['assumptions']=[]
        self.r['authorization']=dict(write=False,fix=False,requirePlanConfirmation=False,scope=[],evidenceRefs=[])
        self.r['intake']=dict(inputMode='',deliverableDecision=dict(source='',userChoice=None,fallbackReason=None,evidenceRefs=[]),prdArtifact=None,sourceDocs=[],rewritePolicy='',rewriteAuthorization=None,clarifications=[])
        self.r['units'][0]['requirementIds']=[]

    def test_visual_check_must_cite_current_screenshot(self):
        next(c for c in self.r['checks'] if c['kind']=='visual')['evidenceRefs']=['tool']
        self.fails('must cite current screenshot')

    def test_content_check_needs_three_way_alignment(self):
        self.r['deliverable']='both';self.r['intake']['deliverableDecision']=self.decision(choice='both');self.r['units'][0]['deliverables']=['figma','demo']
        self.fails('missing demo alignment')

    def test_content_mismatch_blocks(self):
        self.edit_evidence('content',lambda x:x.update(mismatches=['placeholder copy']))
        self.fails('unresolved copy mismatch')

    def test_overflow_escape_blocks(self):
        self.edit_evidence('overflow',lambda x:x.update(escapes=[{'node':'avatar'}]))
        self.fails('unresolved clipping/overflow')

    def test_node_audit_requires_structured_artifact(self):
        next(c for c in self.r['checks'] if c['kind']=='node-audit')['evidenceRefs']=['tool']
        self.fails('node-audit: not passed')

    def test_unregistered_self_built_component_blocks(self):
        self.edit_evidence('audit',lambda x:x.update(unregistered=[{'nodeId':'raw-button','reason':'Hand-drawn button'}]))
        self.fails('unregistered self-built components')

    def test_misclassified_self_built_content_blocks(self):
        self.edit_evidence('audit',lambda x:x.update(misclassified=[{'nodeId':'raw-card','claimed':'layout'}]))
        self.fails('misclassified self-built content')

    def test_node_audit_needs_scanned_nodes(self):
        self.edit_evidence('audit',lambda x:x.update(scanned=[]))
        self.fails('scanned nodes required')

    def test_replicated_unit_requires_live_baseline_evidence(self):
        self.r['units'][0]['liveBaseline']=dict(applicability='replicated',screenRef='live:1',evidenceRefs=[])
        self.fails('liveBaseline: missing evidenceRefs','plan')

    def test_new_pattern_requires_reason(self):
        self.r['units'][0]['liveBaseline']=dict(applicability='new',reason='')
        self.fails('new pattern needs reason','plan')

    def test_replicated_unit_requires_baseline_check(self):
        self.replicated();self.r['checks']=[c for c in self.r['checks'] if c['kind']!='baseline']
        self.fails('baseline: missing current check')

    def test_baseline_open_delta_blocks(self):
        self.replicated();self.edit_evidence('baseline',lambda x:x['elements'][0]['deltas'][0].update(status='open'))
        self.fails('unresolved')

    def test_baseline_tolerance_breach_blocks(self):
        self.replicated();self.edit_evidence('baseline',lambda x:(x['elements'][0]['ours'].update(w=72),x['elements'][0]['deltas'][0].update(ours=72,delta=9)))
        self.fails('exceeds tolerance')

    def test_authorized_deviation_needs_reason(self):
        self.replicated();self.edit_evidence('baseline',lambda x:x['elements'][0]['deltas'][0].update(status='authorized',reason=''))
        self.fails('needs reason')

    def test_self_built_layout_needs_baseline_coverage(self):
        self.replicated()
        snap=dict(ancestorIds=['target'],targetId='target',type='FRAME',nodeId='node2',sourceAssetKey=None,mainComponentKey=None,mainComponentId=None,properties={},content={},layout={},name='layout',parentId='target',overrides=[],protected={k:[] for k in m.PROTECTED})
        self.evidence('pre2','tool',snap);self.evidence('post2','tool',dict(snap))
        self.r['implementations'].append(dict(id='layout',slotId='slot',unitId='u1',targetId='target',deliverable='figma',outcome='ok',revision=self.rev,nodeId='node2',preEvidenceRef='pre2',postEvidenceRef='post2',writeWhitelist=[],origin='layout',expectedFacts={}))
        self.fails('implementation not covered by live baseline')
        self.r['implementations'][-1]['baselineElementId']='chip'
        self.assertEqual([],self.errors())

    def test_independent_review_needs_isolation_evidence(self):
        self.edit_evidence('independence',lambda x:x.update(isolated=False))
        self.fails('isolated context required','build')

    def test_independent_review_capability_is_mandatory(self):
        self.r['capabilities']=[c for c in self.r['capabilities'] if c['id']!='independent-review']
        self.fails('mandatory capability probes missing','build')

    def test_review_findings_must_be_structured(self):
        self.edit_evidence('report-final-ux',lambda x:x.update(findings='looks fine'))
        self.fails('structured findings required')

    def test_both_requires_parity_check(self):
        self.both();self.r['checks']=[c for c in self.r['checks'] if c['kind']!='parity']
        self.fails('parity: missing current check')

    def test_both_parity_mismatch_blocks(self):
        self.both();self.edit_evidence('parity',lambda x:x.update(mismatches=['right actions differ']))
        self.fails('unresolved Figma/Demo mismatch')

    def test_live_library_identity_required(self):
        self.r.pop('liveLibrary')
        self.fails('liveLibrary identity required','build')

    def test_chosen_asset_must_be_observed_in_live_library(self):
        self.r['liveLibrary']['ids']=['other']
        self.fails('chosen asset not observed in live library','build')

    def test_live_library_and_catalog_keys_must_match(self):
        self.gap();self.r['libraryCatalog']['libraryKey']='other-lib'
        self.fails('libraryKey mismatch','build')

    def test_finding_severity_needs_ledger_issue(self):
        self.edit_evidence('report-final-ux',lambda x:x['findings'][0].update(severity='P2'))
        self.fails('needs a ledger issueId')

    def test_finding_severity_must_match_issue(self):
        self.issue(severity='P2');self.edit_evidence('report-final-ux',lambda x:x['findings'][0].update(severity='P1',issueId='i1'))
        self.fails('severity differs from issue')

    def test_finding_with_linked_issue_passes(self):
        self.issue('verified-closed',severity='P2')
        self.edit_evidence('report-final-ux',lambda x:x['findings'][0].update(severity='P2',issueId='i1'))
        self.assertEqual([],self.errors())

    def test_demo_mapping_allows_differing_live_key_with_sync_record(self):
        self.demo_run()
        self.r['implementations'][0]['mapping'].update(chosenLiveKey='live-component',syncMismatch=dict(type='identity-migration',reason='Live key drifted from the local manifest; the published wrapper still carries the schema.',evidenceRefs=['tool']))
        self.evidence('compat','verification',dict(fromKey=self.r['implementations'][0]['assetKey'],toKey='live-component',**{k:dict(before='hash',after='hash') for k in ('schema','dependencies','visual')}))
        self.r['implementations'][0]['mapping']['syncMismatch']['evidenceRefs']=['compat']
        self.assertEqual([],self.errors())

    def test_demo_mapping_differing_live_key_needs_sync_record(self):
        self.demo_run()
        self.r['implementations'][0]['mapping'].update(chosenLiveKey='live-component')
        self.fails('needs syncMismatch record')

    def test_demo_mapping_manifest_key_must_match_local_asset(self):
        self.demo_run()
        self.r['implementations'][0]['mapping'].update(manifestAssetKey='other')
        self.fails('manifestAssetKey must equal the local assetKey')

    def test_optional_capability_may_be_degraded(self):
        self.r['capabilities'].append(dict(id='demo-interaction',status='degraded',revision=self.rev,evidenceRefs=['tool']))
        self.assertEqual([],self.errors())

    def test_web_demo_requires_screenshot_capability(self):
        self.demo_run()
        self.r['capabilities']=[c for c in self.r['capabilities'] if c['id']!='screenshot']
        self.fails('mandatory capability probes missing')

    def test_gap_scanned_assets_need_candidate_decisions(self):
        self.gap()
        self.r['libraryCatalog']['ids']=['component','other']
        self.r['slots'][0]['inventory'].update(scannedIds=['component','other'],eligibleIds=['component','other'])
        self.fails('scanned assets need candidate decisions','build')

    def test_read_only_report_passes(self):
        self.readonly_run()
        self.assertEqual([],self.errors('report'))

    def test_read_only_mode_rejects_design_gates(self):
        self.readonly_run()
        self.fails('read-only modes require --gate report','plan')
        self.fails('read-only modes require --gate report','build')

    def test_read_only_report_requires_report_stage(self):
        self.readonly_run();self.r['stage']='intake'
        self.fails('read-only report requires stage=report','report')

    def test_invalid_stage_fails(self):
        self.r['stage']='nonsense'
        self.fails('invalid stage','plan')

    def test_read_only_report_accepts_issues_verdict(self):
        self.readonly_run(); self.issue(severity='P1')
        for dim in ('ux','ui','system'):
            review=next(x for x in self.r['reviews'] if x['stage']=='final' and x['dimension']==dim)
            review['verdict']='issues'; review['issueIds']=['i1']
            report=m.load_json(self.root/next(e['path'] for e in self.r['evidence'] if e['id']=='report-'+review['id']))
            report.update(verdict='issues',issueIds=['i1'],findings=[dict(unitId='u1',position='screen root',summary='P1 visual mismatch against the source.',evidenceRefs=['tool'],severity='P1',issueId='i1')])
            self.evidence('report-'+review['id'],'review',report)
        self.assertEqual([],self.errors('report'))

    def test_read_only_issues_verdict_requires_findings(self):
        self.readonly_run()
        review=next(x for x in self.r['reviews'] if x['stage']=='final' and x['dimension']=='ux')
        review['verdict']='issues'
        report=m.load_json(self.root/next(e['path'] for e in self.r['evidence'] if e['id']=='report-'+review['id']))
        report.update(verdict='issues',findings=[])
        self.evidence('report-'+review['id'],'review',report)
        self.fails('structured findings required','report')

    def test_read_only_report_requires_current_screenshot(self):
        self.readonly_run(); self.r['captures']=[]
        self.fails('report needs a current screenshot','report')

    def test_chosen_asset_must_come_from_live_library_not_catalog(self):
        self.r['libraryCatalog']=dict(libraryKey='lib-key',complete=True,ids=['component','extra'],evidenceRefs=['tool'])
        self.r['slots'][0]['candidates'].append(dict(key='extra',gateDecision='pass',reason='Catalog-only candidate.',evidenceRefs=['tool']))
        self.r['slots'][0]['chosenAssets']=['extra']
        self.fails('chosen asset not observed in live library','build')

    def test_both_uses_per_deliverable_interaction_levels(self):
        self.both(); self.r['units'][0].pop('interactionLevel',None)
        self.r['units'][0]['interactionLevels']={'figma':'design','demo':'executed'}
        self.r['checks'].append(dict(id='figma-interaction',unitId='u1',deliverable='figma',kind='interaction',revision=self.rev,result='pass',level='design',evidenceRefs=['verify']))
        self.r['checks'].append(dict(id='demo-interaction',unitId='u1',deliverable='demo',kind='interaction',revision=self.rev,result='pass',level='executed',evidenceRefs=['verify']))
        self.refresh_final_reviews()
        self.assertEqual([],self.errors())

    def test_both_interaction_level_mismatch_blocks(self):
        self.both(); self.r['units'][0].pop('interactionLevel',None)
        self.r['units'][0]['interactionLevels']={'figma':'design','demo':'executed'}
        self.r['checks'].append(dict(id='figma-interaction',unitId='u1',deliverable='figma',kind='interaction',revision=self.rev,result='pass',level='executed',evidenceRefs=['verify']))
        self.r['checks'].append(dict(id='demo-interaction',unitId='u1',deliverable='demo',kind='interaction',revision=self.rev,result='pass',level='executed',evidenceRefs=['verify']))
        self.fails('interaction evidence level mismatch')

    def test_interaction_levels_must_cover_each_deliverable(self):
        self.both(); self.r['units'][0].pop('interactionLevel',None)
        self.r['units'][0]['interactionLevels']={'figma':'design'}
        self.fails('interactionLevels must cover each deliverable','plan')

    def test_plan_review_trigger_blocks_delivery(self):
        self.r['implementations'][0]['requiresPlanReview']=True
        self.fails('plan review required')
        self.r['implementations'][0].update(requiresPlanReview=False,changeImpact=['main-action-change'])
        self.fails('plan review required')

    def test_plan_review_trigger_requires_resume_plan(self):
        self.r['implementations'][0]['structureChange']=True
        self.r['nextAction']='deliver'
        self.fails('nextAction must be resume-plan')
    def test_plan_review_rejects_unknown_change_impact(self):
        self.r['implementations'][0]['changeImpact']=['ia-change']
        self.fails('changeImpact must use documented values')
    def test_plan_review_rejects_nonstring_change_impact(self):
        self.r['implementations'][0]['changeImpact']=[True]
        self.fails('changeImpact must use documented values')
    def test_plan_review_rejects_nonboolean_flag(self):
        self.r['implementations'][0]['requiresPlanReview']='true'
        self.fails('requiresPlanReview must be boolean')

    def test_paused_blocked_status_blocks_gates(self):
        self.r['status']='paused-blocked'
        self.fails('paused-blocked','plan')

    def test_unknown_next_action_fails(self):
        self.r['nextAction']='do-something-else'
        self.fails('nextAction must be a known','plan')

    def test_task_evidence_refs_must_be_task_kind(self):
        self.r['taskEvidenceRefs']=['tool']
        self.fails('wrong evidence kind','plan')
    def test_missing_task_evidence_refs_is_tolerated(self):
        self.r.pop('taskEvidenceRefs')
        self.assertEqual([],self.errors('plan'))

    def test_plan_gate_checks_review_isolation(self):
        self.edit_evidence('independence',lambda x:x.update(isolated=False))
        self.fails('isolated context required','plan')

    def test_empty_live_library_requires_proof(self):
        self.r['liveLibrary']['ids']=[]
        self.fails('empty ids require emptyProof','build')

    def test_empty_live_library_with_proof_passes(self):
        self.gap(); self.r['liveLibrary']['ids']=[]; self.r['liveLibrary']['emptyProof']=True
        slot=self.r['slots'][0]; self.r['libraryCatalog']['ids']=[]
        slot['composeTrials'][0]['parts']=[]; slot['candidates']=[]
        slot['inventory'].update(eligibleIds=[],scannedIds=[],exclusions=[])
        self.assertEqual([],self.errors('build'))
    def test_authorization_scope_must_be_string_array(self):
        self.r['authorization']['scope']='target'
        self.fails('scope must be a non-empty string array','build')
    def test_authorization_scope_rejects_empty_list(self):
        self.r['authorization']['scope']=[]
        self.fails('scope must be a non-empty string array','build')
    def test_blockers_must_be_array(self):
        self.r['blockers']={}
        self.fails('blockers must be an array','build')
    def test_slot_bindings_must_be_array(self):
        self.r['slots'][0]['slotBindings']={}
        self.fails('slotBindings must be an array of objects','build')
    def test_child_slot_ids_must_be_array(self):
        self.r['slots'][0]['childSlotIds']={}
        self.fails('childSlotIds must be a non-empty-string array','build')
    def test_candidates_must_be_objects(self):
        self.gap();self.r['slots'][0]['candidates']=['component']
        self.fails('candidates must be an array of objects','build')
    def test_chosen_assets_must_be_strings(self):
        self.r['slots'][0]['chosenAssets']=[{}]
        self.fails('chosenAssets must be a non-empty-string array','build')
    def test_inventory_ids_must_be_string_arrays(self):
        self.gap();self.r['slots'][0]['inventory']['eligibleIds']=[1]
        self.fails('inventory.eligibleIds must be a string array','build')
    def test_inventory_exclusions_need_ids(self):
        self.gap();self.r['slots'][0]['inventory']['exclusions']=[{}]
        self.fails('inventory.exclusions must be objects with id','build')
    def test_live_library_fingerprint_must_be_string_or_null(self):
        self.r['liveLibrary']['fingerprint']={}
        self.fails('fingerprint must be a non-empty string or null','build')
    def test_checks_need_unit_and_deliverable(self):
        self.r['checks'][0]['unitId']={}
        self.fails('checks: unitId must be a non-empty string')
    def test_checks_deliverable_must_be_string(self):
        self.r['checks'][0]['deliverable']={}
        self.fails('checks: deliverable must be a non-empty string')
    def test_write_whitelist_must_be_array_or_null(self):
        self.r['implementations'][0]['writeWhitelist']={}
        self.fails('writeWhitelist must be an array or null')
    def test_expected_facts_must_be_object_or_null(self):
        self.r['implementations'][0]['expectedFacts']=[]
        self.fails('expectedFacts must be an object or null')
    def test_clarifications_must_be_array(self):
        self.r['intake']['clarifications']={}
        self.fails('clarifications must be an array of objects','plan')
    def test_clarification_needs_question(self):
        self.r['intake']['clarifications']=[{'answer':'later'}]
        self.fails('clarifications[0] needs a question','plan')
    def test_clarification_answer_must_be_string_or_null(self):
        self.r['intake']['clarifications']=[{'question':'Which deliverable?','answer':{}}]
        self.fails('clarifications[0].answer must be a string or null','plan')
    def test_checks_need_unique_ids(self):
        self.r['checks'][0]['id']=self.r['checks'][1]['id']
        self.fails('duplicate id')
    def test_review_supersedes_must_be_array(self):
        self.r['reviews'][0]['supersedes']={}
        self.fails('supersedes must be a string array')
    def test_authorization_flags_must_be_boolean(self):
        self.r['authorization']['fix']={}
        self.fails('authorization.fix must be boolean')
    def test_verbatim_intake_rejects_empty_artifact_object(self):
        self.r['intake']['prdArtifact']={}
        self.fails('verbatim intake must not author a rewritten PRD artifact','plan')
    def test_verbatim_intake_rejects_rewrite_authorization(self):
        self.r['intake']['rewriteAuthorization']={}
        self.fails('verbatim intake must not record rewriteAuthorization','plan')

    def test_baseline_artifact_requires_deliverable(self):
        self.replicated(); self.edit_evidence('baseline',lambda x:x.pop('deliverable'))
        self.fails('baseline: deliverable mismatch')

    def test_both_replicated_needs_per_deliverable_baseline(self):
        self.replicated(); self.both()
        self.fails('replicated unit needs current baseline check')

    def test_both_replicated_passes_with_per_deliverable_baseline(self):
        self.replicated(); self.both()
        self.evidence('baseline-demo','baseline',dict(unitId='u1',deliverable='demo',verdict='pass',elements=[dict(id='chip',live={'w':63},ours={'w':65},deltas=[dict(field='w',live=63,ours=65,delta=2,tolerance=2,status='within')])]))
        self.r['checks'].append(dict(id='baseline-demo',unitId='u1',deliverable='demo',kind='baseline',revision=self.rev,result='pass',evidenceRefs=['baseline-demo']))
        self.refresh_final_reviews()
        self.assertEqual([],self.errors())

    def test_iterate_without_prd_requires_fix_authorization_and_derived_requirements(self):
        self.r['mode']='iterate'; self.r['intake']['inputMode']=''; self.r['authorization']['fix']=False
        self.fails('iterate without PRD intake requires fix authorization','plan')
        self.r['authorization']['fix']=True
        self.fails('iterate without PRD intake must derive requirements','plan')
        self.r['requirements'][0]['origin']='derived'
        self.assertEqual([],self.errors('plan'))

if __name__=='__main__':unittest.main()
