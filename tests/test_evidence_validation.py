"""Evidence validation negative cases and legitimate controls; synthetic, not live validation."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import test_run_gate as fixtures
from runlib.checks import content_diff,fill_errors
from runlib.images import verify_image
from runlib.tools import catalog_contract


def module(name):
    p=Path(__file__).resolve().parents[1]/'scripts'/name
    spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


class EvidenceValidationTests(unittest.TestCase):
    def setUp(self):
        self.f=fixtures.RunGateTests();self.f.setUp();self.addCleanup(self.f.doCleanups)

    def test_audit_reports_identity_migration_not_removal(self):
        audit=module('audit-library.py').audit
        local=[dict(nodeId='1:1',assetKey='old',name='X',properties=[],dependencies=[],childInstanceTags=[])]
        live=[dict(nodeId='1:1',assetKey='new',name='X',properties=[],dependencies=[dict(name='Y')],childInstanceTags=[])]
        result=audit(local,live)
        self.assertEqual([],result['added']);self.assertEqual([],result['removed'])
        self.assertEqual(1,len(result['rekeyed']))
        self.assertEqual(('old','new'),(result['rekeyed'][0]['fromKey'],result['rekeyed'][0]['toKey']))
        self.assertEqual(['dependencies'],result['rekeyed'][0]['fields'])
        self.assertEqual([],result['changed'])

    def test_audit_detects_true_addition_and_removal(self):
        audit=module('audit-library.py').audit
        result=audit([dict(nodeId='1:1',assetKey='a',name='A')],[dict(nodeId='2:2',assetKey='b',name='B')])
        self.assertEqual(['2:2'],result['added']);self.assertEqual(['1:1'],result['removed'])
        self.assertEqual([],result['rekeyed']);self.assertEqual([],result['changed'])

    def test_changed_text_cannot_claim_empty_mismatches(self):
        self.f.edit_evidence('content',lambda a:a.update(figma={'headline':'WRONG'}))
        self.f.fails('computed content mismatch')

    def test_fabricated_delta_cannot_pass(self):
        self.f.replicated();self.f.edit_evidence('baseline',lambda a:a['elements'][0]['deltas'][0].update(delta=0))
        self.f.fails('incorrect delta arithmetic')

    def test_nonfinite_geometry_rejected(self):
        for value in (float('nan'),float('inf'),True):
            with self.subTest(value=value):
                self.f.replicated();self.f.edit_evidence('baseline',lambda a:a['elements'][0]['deltas'][0].update(delta=value))
                self.f.fails('finite numeric geometry')

    def test_unexamined_added_asset_invalidates_gap(self):
        self.f.gap();self.f.r['libraryCatalog']['ids'].append('unexamined')
        self.f.fails('unclassified catalog assets','build')

    def test_proven_exclusion_restores_full_coverage(self):
        self.f.gap();self.f.r['libraryCatalog']['ids'].append('unrelated')
        inventory=self.f.r['slots'][0]['inventory'];inventory['eligibleIds'].append('unrelated')
        inventory['exclusions'].append(dict(id='unrelated',reason='Published type does not provide this capability',evidenceRefs=['tool']))
        self.assertEqual([],self.f.errors('build'))

    def test_exact_fill_visibility_change_passes(self):
        a={'n':[dict(visible=True,color='brand')]};b={'n':[dict(visible=False,color='brand')]}
        adjustments=[dict(nodeId='n',paintIndex=0,property='visible',before=True,after=False)]
        self.assertEqual([],fill_errors(a,b,adjustments))
        b['n'][0]['color']='other'
        self.assertTrue(fill_errors(a,b,adjustments))

    def test_wrong_node_and_duplicate_adjustment_rejected(self):
        a={'n':[dict(opacity=1)]};b={'n':[dict(opacity=0)]}
        item=dict(nodeId='n',paintIndex=0,property='opacity',before=1,after=0)
        self.assertEqual([],fill_errors(a,b,[item]))
        self.assertTrue(fill_errors(a,b,[item,item]))
        self.assertTrue(fill_errors(a,b,[dict(item,nodeId='wrong')]))

    def test_unrelated_fill_recolor_fails_full_gate(self):
        self.f.edit_evidence('canonical',lambda a:a.update(description='隐藏示意填充'))
        self.f.edit_evidence('post',lambda a:a['protected'].update(fills={'padding':[dict(visible=False,color='WRONG')]}))
        self.f.r['implementations'][0]['descriptionFillAdjustments']=[dict(layerName='padding',nodeId='padding',paintIndex=0,property='visible',before=True,after=False,action='hide-fill',descriptionQuote='隐藏示意填充')]
        self.f.fails('unauthorized fill difference')

    def test_changes_reach_blind_packet(self):
        import test_run_gate
        self.f.evidence('cancel-login','authorization',{'request':'取消登录'})
        self.f.r['changeSet']=[dict(operation='remove',reason='User cancelled login',previousRequirement=dict(id='old-login',statement='Login'),evidenceRefs=['cancel-login'])]
        for review in self.f.r['reviews']:
            packet=test_run_gate.m.packet(self.f.r,review['stage'],review['reviewerId'])
            self.assertIn('cancel-login',packet['evidenceRefs'])
            self.f.evidence(review['packetRef'],'packet',packet)
        self.assertEqual([],self.f.errors())

    def test_clean_review_can_have_no_findings(self):
        self.f.edit_evidence('report-final-ux',lambda a:a.update(findings=[],checksPerformed=[dict(unitId='u1',summary='Checked main task',evidenceRefs=['capture'])]))
        self.assertEqual([],self.f.errors())

    def test_short_prd_with_original_source_not_blocked_by_length(self):
        self.f.text_evidence('prd','source','目标：查看三条任务。范围：列表。任务流：进入、加载、显示，失败可重试。内容：原需求。验收：三条可见。')
        self.f.r['intake'].update(inputMode='text',rewritePolicy='authored',prdArtifact={'evidenceRef':'prd'},originalSourceIds=['s1'])
        self.assertEqual([],self.f.errors('plan'))

    def test_v2_requires_migration(self):
        self.f.r['schemaVersion']=2;self.f.fails('schemaVersion must be 3','plan')

    def test_migration_preserves_original_and_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);old=root/'old';old.mkdir();source=old/'run.json'
            source.write_text(json.dumps(dict(self.f.r,schemaVersion=2)))
            before=source.read_bytes();dest=module('migrate-run.py').migrate(source,root/'new')
            migrated=json.loads(dest.read_text())
            self.assertEqual(before,source.read_bytes());self.assertEqual(before,(dest.parent/'run.v2.json').read_bytes())
            self.assertEqual('needs-recapture',migrated['migration']['status'])
            self.assertEqual('paused-blocked',migrated['status'])
            with self.assertRaises(ValueError):module('migrate-run.py').migrate(source,root/'new')

    def test_content_comparator_preserves_semantic_differences(self):
        self.assertEqual([],content_diff({'x':'é\r\n'}, {'x':'e\u0301\n'}))
        for value in ('不允许','允许 ','允许。'):
            self.assertTrue(content_diff({'x':'允许'},{'x':value}))
        self.assertTrue(content_diff({'x':'1'},{'x':'2'}))

    def test_comparator_rejects_empty_source(self):
        with self.assertRaises(ValueError):module('compare-evidence.py').compare({'source':{},'figma':{},'media':['figma']},'content')

    def test_catalog_contract_respects_actual_interface(self):
        self.assertTrue(catalog_contract(only_published=True,truncated=False)['complete'])
        self.assertFalse(catalog_contract(only_published=True,truncated=True)['complete'])
        self.assertFalse(catalog_contract(only_published=True,truncated=False,has_more=True)['complete'])
        self.assertEqual('next-page',catalog_contract(only_published=True,truncated=False,has_more=True,supports_cursor=True,cursor='next')['nextAction'])

    def test_image_must_decode(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'image.png';p.write_bytes(b'\x89PNG\r\n\x1a\n'+b'fake'*10)
            self.assertIsNotNone(verify_image(p))
            Image.new('RGB',(2,2)).save(p);self.assertIsNone(verify_image(p))

if __name__=='__main__':unittest.main()
