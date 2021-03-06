__copyright__ = "Copyright 2016, Netflix, Inc."
__license__ = "Apache, Version 2.0"

import os
import unittest

from core.asset import Asset
from core.quality_runner import VmafLegacyQualityRunner, VmafQualityRunner, \
    PsnrQualityRunner
from core.executor import run_executors_in_parallel
import config
from core.result_store import FileSystemResultStore


class QualityRunnerTest(unittest.TestCase):

    def tearDown(self):
        if hasattr(self, 'runner'):
            self.runner.remove_results()
            pass

    def setUp(self):
        self.result_store = FileSystemResultStore()

    def test_executor_id(self):
        asset = Asset(dataset="test", content_id=0, asset_id=1,
                      ref_path="dir/refvideo.yuv", dis_path="dir/disvideo.yuv",
                      asset_dict={})
        runner = VmafLegacyQualityRunner([asset], None)
        self.assertEquals(runner.executor_id, 'VMAF_legacy_V1.0')

    def test_run_vamf_legacy_runner(self):
        print 'test on running VMAF (legacy) runner...'
        ref_path = config.ROOT + "/resource/yuv/src01_hrc00_576x324.yuv"
        dis_path = config.ROOT + "/resource/yuv/src01_hrc01_576x324.yuv"
        asset = Asset(dataset="test", content_id=0, asset_id=0,
                      workdir_root=config.ROOT + "/workspace/workdir",
                      ref_path=ref_path,
                      dis_path=dis_path,
                      asset_dict={'width':576, 'height':324})

        asset_original = Asset(dataset="test", content_id=0, asset_id=1,
                      workdir_root=config.ROOT + "/workspace/workdir",
                      ref_path=ref_path,
                      dis_path=ref_path,
                      asset_dict={'width':576, 'height':324})

        self.runner = VmafLegacyQualityRunner(
            [asset, asset_original],
            None, fifo_mode=True,
            delete_workdir=True,
            result_store=None
        )
        self.runner.run()

        results = self.runner.results

        self.assertAlmostEqual(results[0]['VMAF_feature_vif_score'], 0.44455808333333313, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_motion_score'], 3.5916076041666667, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_adm_score'], 0.9155242291666666, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_ansnr_score'], 22.533456770833329, places=4)
        self.assertAlmostEqual(results[0]['VMAF_legacy_score'], 60.27316952679754, places=4)

        self.assertAlmostEqual(results[1]['VMAF_feature_vif_score'], 1.0, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_motion_score'], 3.5916076041666667, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_adm_score'], 1.0, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_ansnr_score'], 30.030914145833322, places=4)
        self.assertAlmostEqual(results[1]['VMAF_legacy_score'], 95.65756240092573, places=4)

    def test_run_vamf_legacy_runner_10le(self):
        print 'test on running VMAF (legacy) runner on 10 bit le...'
        ref_path = config.ROOT + "/resource/yuv/src01_hrc00_576x324.yuv422p10le.yuv"
        dis_path = config.ROOT + "/resource/yuv/src01_hrc01_576x324.yuv422p10le.yuv"
        asset = Asset(dataset="test", content_id=0, asset_id=0,
                      workdir_root=config.ROOT + "/workspace/workdir",
                      ref_path=ref_path,
                      dis_path=dis_path,
                      asset_dict={'width':576, 'height':324,
                                  'yuv_type':'yuv422p10le'})

        asset_original = Asset(dataset="test", content_id=0, asset_id=1,
                      workdir_root=config.ROOT + "/workspace/workdir",
                      ref_path=ref_path,
                      dis_path=ref_path,
                      asset_dict={'width':576, 'height':324,
                                  'yuv_type':'yuv422p10le'})

        self.runner = VmafLegacyQualityRunner(
            [asset, asset_original],
            None, fifo_mode=False,
            delete_workdir=True,
            result_store=None
        )
        self.runner.run()

        results = self.runner.results

        self.assertAlmostEqual(results[0]['VMAF_legacy_score'], 60.27316952679754, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_vif_score'], 0.44455808333333313, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_motion_score'], 3.5916076041666667, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_adm_score'], 0.9155242291666666, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_ansnr_score'], 22.533456770833329, places=4)

        self.assertAlmostEqual(results[1]['VMAF_legacy_score'], 95.65756240092573, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_vif_score'], 1.0, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_motion_score'], 3.5916076041666667, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_adm_score'], 1.0, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_ansnr_score'], 30.030914145833322, places=4)

    def test_run_vamf_legacy_runner_with_result_store(self):
        print 'test on running VMAF (legacy) runner with result store...'
        ref_path = config.ROOT + "/resource/yuv/src01_hrc00_576x324.yuv"
        dis_path = config.ROOT + "/resource/yuv/src01_hrc01_576x324.yuv"
        asset = Asset(dataset="test", content_id=0, asset_id=0,
                      workdir_root=config.ROOT + "/workspace/workdir",
                      ref_path=ref_path,
                      dis_path=dis_path,
                      asset_dict={'width':576, 'height':324})

        asset_original = Asset(dataset="test", content_id=0, asset_id=1,
                      workdir_root=config.ROOT + "/workspace/workdir",
                      ref_path=ref_path,
                      dis_path=ref_path,
                      asset_dict={'width':576, 'height':324})

        result_store = FileSystemResultStore(logger=None)

        self.runner = VmafLegacyQualityRunner(
            [asset, asset_original],
            None, fifo_mode=True,
            delete_workdir=True,
            result_store=result_store
        )

        print '    running for the first time with fresh calculation...'
        self.runner.run()
        result0, result1 = self.runner.results

        # NOTE: since stored results are actually VMAF_feature's not VMAF's,
        # the two paths below shouldn't exist
        self.assertFalse(os.path.exists(result_store._get_result_file_path(result0)))
        self.assertFalse(os.path.exists(result_store._get_result_file_path(result1)))

        print '    running for the second time with stored results...'
        self.runner.run()
        results = self.runner.results

        self.assertAlmostEqual(results[0]['VMAF_legacy_score'], 60.27316952679754, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_vif_score'], 0.44455808333333313, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_motion_score'], 3.5916076041666667, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_adm_score'], 0.9155242291666666, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_ansnr_score'], 22.533456770833329, places=4)

        self.assertAlmostEqual(results[1]['VMAF_legacy_score'], 95.65756240092573, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_vif_score'], 1.0, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_motion_score'], 3.5916076041666667, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_adm_score'], 1.0, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_ansnr_score'], 30.030914145833322, places=4)

    def test_run_vmaf_legacy_runner_not_unique(self):
        ref_path = config.ROOT + "/resource/yuv/src01_hrc00_576x324.yuv"
        dis_path = config.ROOT + "/resource/yuv/src01_hrc01_576x324.yuv"
        asset = Asset(dataset="test", content_id=0, asset_id=0,
                      workdir_root=config.ROOT + "/workspace/workdir",
                      ref_path=ref_path,
                      dis_path=dis_path,
                      asset_dict={'width':576, 'height':324})

        asset_original = Asset(dataset="test", content_id=0, asset_id=0,
                      workdir_root=config.ROOT + "/workspace/workdir",
                      ref_path=ref_path,
                      dis_path=ref_path,
                      asset_dict={'width':576, 'height':324})

        with self.assertRaises(AssertionError):
            self.runner = VmafLegacyQualityRunner(
                [asset, asset_original],
                None, fifo_mode=True)

    def test_run_vmaf_runner_v1_model(self):
        print 'test on running VMAF runner...'
        ref_path = config.ROOT + "/resource/yuv/src01_hrc00_576x324.yuv"
        dis_path = config.ROOT + "/resource/yuv/src01_hrc01_576x324.yuv"
        asset = Asset(dataset="test", content_id=0, asset_id=0,
                      workdir_root=config.ROOT + "/workspace/workdir",
                      ref_path=ref_path,
                      dis_path=dis_path,
                      asset_dict={'width':576, 'height':324})

        asset_original = Asset(dataset="test", content_id=0, asset_id=1,
                      workdir_root=config.ROOT + "/workspace/workdir",
                      ref_path=ref_path,
                      dis_path=ref_path,
                      asset_dict={'width':576, 'height':324})

        self.runner = VmafQualityRunner(
            [asset, asset_original],
            None, fifo_mode=True,
            delete_workdir=True,
            result_store=None,
            optional_dict={
                'model_filepath':config.ROOT + "/resource/model/nflx_v1.pkl",
            }
        )
        self.runner.run()

        results = self.runner.results

        self.assertAlmostEqual(results[0]['VMAF_feature_vif_score'], 0.44455808333333313, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_motion_score'], 3.5916076041666667, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_adm_score'], 0.9155242291666666, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_ansnr_score'], 22.533456770833329, places=4)
        self.assertAlmostEqual(results[0]['VMAF_score'], 70.2953285604173, places=4)

        self.assertAlmostEqual(results[1]['VMAF_feature_vif_score'], 1.0, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_motion_score'], 3.5916076041666667, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_adm_score'], 1.0, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_ansnr_score'], 30.030914145833322, places=4)
        self.assertAlmostEqual(results[1]['VMAF_score'], 100.0, places=4)

    def test_run_vmaf_runner(self):
        print 'test on running VMAF runner...'
        ref_path = config.ROOT + "/resource/yuv/src01_hrc00_576x324.yuv"
        dis_path = config.ROOT + "/resource/yuv/src01_hrc01_576x324.yuv"
        asset = Asset(dataset="test", content_id=0, asset_id=0,
                      workdir_root=config.ROOT + "/workspace/workdir",
                      ref_path=ref_path,
                      dis_path=dis_path,
                      asset_dict={'width':576, 'height':324})

        asset_original = Asset(dataset="test", content_id=0, asset_id=1,
                      workdir_root=config.ROOT + "/workspace/workdir",
                      ref_path=ref_path,
                      dis_path=ref_path,
                      asset_dict={'width':576, 'height':324})

        self.runner = VmafQualityRunner(
            [asset, asset_original],
            None, fifo_mode=True,
            delete_workdir=True,
            result_store=None,
        )
        self.runner.run()

        results = self.runner.results

        self.assertAlmostEqual(results[0]['VMAF_feature_vif_scale0_score'], 0.3655846219305399, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_vif_scale1_score'], 0.7722301581694561, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_vif_scale2_score'], 0.8681486658208089, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_vif_scale3_score'], 0.9207121810522212, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_motion_score'], 3.5916076041666667, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_adm2_score'], 0.92543343980061415, places=4)
        self.assertAlmostEqual(results[0]['VMAF_score'], 66.628190500372327, places=4)

        self.assertAlmostEqual(results[1]['VMAF_feature_vif_scale0_score'], 1.0000000132944864, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_vif_scale1_score'], 0.9999998271651448, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_vif_scale2_score'], 0.9999998649680067, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_vif_scale3_score'], 0.9999998102499, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_motion_score'], 3.5916076041666667, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_adm2_score'], 1.0, places=4)
        self.assertAlmostEqual(results[1]['VMAF_score'], 99.799881593902896, places=4)

        with self.assertRaises(KeyError):
            self.assertAlmostEqual(results[1]['VMAF_feature_vif_score'], 1.0, places=4)

        with self.assertRaises(KeyError):
            self.assertAlmostEqual(results[1]['VMAF_feature_ansnr_score'], 1.0, places=4)

    def test_run_vmaf_runner_checkerboard(self):
        print 'test on running VMAF runner on checkerboard pattern...'
        ref_path = config.ROOT + "/resource/yuv/checkerboard_1920_1080_10_3_0_0.yuv"
        dis_path = config.ROOT + "/resource/yuv/checkerboard_1920_1080_10_3_10_0.yuv"
        dis_path2 = config.ROOT + "/resource/yuv/checkerboard_1920_1080_10_3_1_0.yuv"
        asset = Asset(dataset="test", content_id=0, asset_id=0,
                      workdir_root=config.ROOT + "/workspace/workdir",
                      ref_path=ref_path,
                      dis_path=dis_path,
                      asset_dict={'width':1920, 'height':1080})

        asset_original = Asset(dataset="test", content_id=0, asset_id=1,
                      workdir_root=config.ROOT + "/workspace/workdir",
                      ref_path=ref_path,
                      dis_path=ref_path,
                      asset_dict={'width':1920, 'height':1080})

        asset2 = Asset(dataset="test", content_id=0, asset_id=2,
                      workdir_root=config.ROOT + "/workspace/workdir",
                      ref_path=ref_path,
                      dis_path=dis_path2,
                      asset_dict={'width':1920, 'height':1080})

        self.runner = VmafQualityRunner(
            [asset, asset_original, asset2],
            None, fifo_mode=True,
            delete_workdir=True,
            result_store=self.result_store,
        )
        self.runner.run()

        results = self.runner.results

        self.assertAlmostEqual(results[0]['VMAF_score'], 9.1131612984940862, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_vif_scale0_score'], 0.0, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_vif_scale1_score'], 0.0, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_vif_scale2_score'], 0.0, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_vif_scale3_score'], 0.0, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_motion_score'], 12.343795333333333, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_adm2_score'], 0.03143185071034834, places=4)

        self.assertAlmostEqual(results[1]['VMAF_score'], 99.806602803333135, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_vif_scale0_score'], 1.0000003177689212, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_vif_scale1_score'], 0.9999998487787267, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_vif_scale2_score'], 0.9999981097738688, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_vif_scale3_score'], 0.9999997220260903, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_motion_score'], 12.343795333333333, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_adm2_score'], 1.0, places=4)

        self.assertAlmostEqual(results[2]['VMAF_score'], 28.05946153566796, places=4)
        self.assertAlmostEqual(results[2]['VMAF_feature_vif_scale0_score'], 0.11275263500539146, places=4)
        self.assertAlmostEqual(results[2]['VMAF_feature_vif_scale1_score'], 0.29840546576776056, places=4)
        self.assertAlmostEqual(results[2]['VMAF_feature_vif_scale2_score'], 0.33792477828702316, places=4)
        self.assertAlmostEqual(results[2]['VMAF_feature_vif_scale3_score'], 0.49935011838091997, places=4)
        self.assertAlmostEqual(results[2]['VMAF_feature_motion_score'], 12.343795333333333, places=4)
        self.assertAlmostEqual(results[2]['VMAF_feature_adm2_score'], 0.8197112538432134, places=4)

    def test_run_vmaf_runner_flat(self):
        print 'test on running VMAF runner on flat pattern...'
        ref_path = config.ROOT + "/resource/yuv/flat_1920_1080_0.yuv"
        dis_path = config.ROOT + "/resource/yuv/flat_1920_1080_10.yuv"
        asset = Asset(dataset="test", content_id=0, asset_id=0,
                      workdir_root=config.ROOT + "/workspace/workdir",
                      ref_path=ref_path,
                      dis_path=dis_path,
                      asset_dict={'width':1920, 'height':1080})

        asset_original = Asset(dataset="test", content_id=0, asset_id=1,
                      workdir_root=config.ROOT + "/workspace/workdir",
                      ref_path=ref_path,
                      dis_path=ref_path,
                      asset_dict={'width':1920, 'height':1080})

        self.runner = VmafQualityRunner(
            [asset, asset_original],
            None, fifo_mode=True,
            delete_workdir=True,
            result_store=self.result_store,
        )
        self.runner.run()

        results = self.runner.results

        self.assertAlmostEqual(results[0]['VMAF_score'], 99.419836087060176, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_vif_scale0_score'], 1.0, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_vif_scale1_score'], 1.0, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_vif_scale2_score'], 1.0, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_vif_scale3_score'], 1.0, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_motion_score'], 0.0, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_adm2_score'], 1.0, places=4)

        self.assertAlmostEqual(results[1]['VMAF_score'], 99.419836087060176, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_vif_scale0_score'], 1.0, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_vif_scale1_score'], 1.0, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_vif_scale2_score'], 1.0, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_vif_scale3_score'], 1.0, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_motion_score'], 0.0, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_adm2_score'], 1.0, places=4)

    def test_run_vmaf_runner_with_rf_model(self):
        print 'test on running VMAF runner with custom input model...'
        ref_path = config.ROOT + "/resource/yuv/src01_hrc00_576x324.yuv"
        dis_path = config.ROOT + "/resource/yuv/src01_hrc01_576x324.yuv"
        asset = Asset(dataset="test", content_id=0, asset_id=0,
                      workdir_root=config.ROOT + "/workspace/workdir",
                      ref_path=ref_path,
                      dis_path=dis_path,
                      asset_dict={'width':576, 'height':324})

        asset_original = Asset(dataset="test", content_id=0, asset_id=1,
                      workdir_root=config.ROOT + "/workspace/workdir",
                      ref_path=ref_path,
                      dis_path=ref_path,
                      asset_dict={'width':576, 'height':324})

        self.runner = VmafQualityRunner(
            [asset, asset_original],
            None, fifo_mode=True,
            delete_workdir=True,
            result_store=self.result_store,
            optional_dict={
                'model_filepath':config.ROOT + "/resource/model/nflx_vmaff_rf_v1.pkl",
            }
        )
        self.runner.run()

        results = self.runner.results

        self.assertAlmostEqual(results[0]['VMAF_score'], 73.79861111111113, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_vif_score'], 0.44455808333333313, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_motion_score'], 3.5916076041666667, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_adm_score'], 0.9155242291666666, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_ansnr_score'], 22.533456770833329, places=4)

        self.assertAlmostEqual(results[1]['VMAF_score'], 98.22048611111109, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_vif_score'], 1.0, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_motion_score'], 3.5916076041666667, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_adm_score'], 1.0, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_ansnr_score'], 30.030914145833322, places=4)

    def test_run_psnr_runner(self):
        print 'test on running PSNR runner...'
        ref_path = config.ROOT + "/resource/yuv/src01_hrc00_576x324.yuv"
        dis_path = config.ROOT + "/resource/yuv/src01_hrc01_576x324.yuv"
        asset = Asset(dataset="test", content_id=0, asset_id=0,
                      workdir_root=config.ROOT + "/workspace/workdir",
                      ref_path=ref_path,
                      dis_path=dis_path,
                      asset_dict={'width':576, 'height':324})

        asset_original = Asset(dataset="test", content_id=0, asset_id=1,
                      workdir_root=config.ROOT + "/workspace/workdir",
                      ref_path=ref_path,
                      dis_path=ref_path,
                      asset_dict={'width':576, 'height':324})

        self.runner = PsnrQualityRunner(
            [asset, asset_original],
            None, fifo_mode=True,
            delete_workdir=True,
            result_store=None
        )
        self.runner.run()

        results = self.runner.results
        self.assertAlmostEqual(results[0]['PSNR_score'], 30.755063979166664, places=4)
        self.assertAlmostEqual(results[1]['PSNR_score'], 60.0, places=4)

class ParallelQualityRunnerTest(unittest.TestCase):

    def tearDown(self):
        if hasattr(self, 'runners'):
            for runner in self.runners:
                runner.remove_results()
            pass

    def test_run_parallel_vmaf_legacy_runner(self):
        print 'test on running VMAF (legacy) quality runner in parallel...'
        ref_path = config.ROOT + "/resource/yuv/src01_hrc00_576x324.yuv"
        dis_path = config.ROOT + "/resource/yuv/src01_hrc01_576x324.yuv"
        asset = Asset(dataset="test", content_id=0, asset_id=0,
                      workdir_root=config.ROOT + "/workspace/workdir",
                      ref_path=ref_path,
                      dis_path=dis_path,
                      asset_dict={'width':576, 'height':324})

        asset_original = Asset(dataset="test", content_id=0, asset_id=1,
                      workdir_root=config.ROOT + "/workspace/workdir",
                      ref_path=ref_path,
                      dis_path=ref_path,
                      asset_dict={'width':576, 'height':324})

        self.runners, results = run_executors_in_parallel(
            VmafLegacyQualityRunner,
            [asset, asset_original],
            fifo_mode=True,
            delete_workdir=True,
            parallelize=True,
            result_store=None
        )

        self.assertAlmostEqual(results[0]['VMAF_legacy_score'], 60.27316952679754, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_vif_score'], 0.44455808333333313, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_motion_score'], 3.5916076041666667, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_adm_score'], 0.9155242291666666, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_ansnr_score'], 22.533456770833329, places=4)

        self.assertAlmostEqual(results[1]['VMAF_legacy_score'], 95.65756240092573, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_vif_score'], 1.0, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_motion_score'], 3.5916076041666667, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_adm_score'], 1.0, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_ansnr_score'], 30.030914145833322, places=4)

    def test_run_parallel_psnr_runner(self):
        print 'test on running PSNR quality runner in parallel...'
        ref_path = config.ROOT + "/resource/yuv/src01_hrc00_576x324.yuv"
        dis_path = config.ROOT + "/resource/yuv/src01_hrc01_576x324.yuv"
        asset = Asset(dataset="test", content_id=0, asset_id=0,
                      workdir_root=config.ROOT + "/workspace/workdir",
                      ref_path=ref_path,
                      dis_path=dis_path,
                      asset_dict={'width':576, 'height':324})

        asset_original = Asset(dataset="test", content_id=0, asset_id=1,
                      workdir_root=config.ROOT + "/workspace/workdir",
                      ref_path=ref_path,
                      dis_path=ref_path,
                      asset_dict={'width':576, 'height':324})

        self.runners, results = run_executors_in_parallel(
            PsnrQualityRunner,
            [asset, asset_original],
            fifo_mode=True,
            delete_workdir=True,
            parallelize=True,
            result_store=None
        )

        self.assertAlmostEqual(results[0]['PSNR_score'], 30.755063979166664, places=4)
        self.assertAlmostEqual(results[1]['PSNR_score'], 60.0, places=4)

    def test_run_parallel_vamf_runner_with_model(self):
        print 'test on running VMAF quality runner in parallel with custom model...'
        ref_path = config.ROOT + "/resource/yuv/src01_hrc00_576x324.yuv"
        dis_path = config.ROOT + "/resource/yuv/src01_hrc01_576x324.yuv"
        asset = Asset(dataset="test", content_id=0, asset_id=0,
                      workdir_root=config.ROOT + "/workspace/workdir",
                      ref_path=ref_path,
                      dis_path=dis_path,
                      asset_dict={'width':576, 'height':324})

        asset_original = Asset(dataset="test", content_id=0, asset_id=1,
                      workdir_root=config.ROOT + "/workspace/workdir",
                      ref_path=ref_path,
                      dis_path=ref_path,
                      asset_dict={'width':576, 'height':324})

        self.runners, results = run_executors_in_parallel(
            VmafQualityRunner,
            [asset, asset_original],
            fifo_mode=True,
            delete_workdir=True,
            parallelize=True,
            result_store=None,
            optional_dict={
                'model_filepath':config.ROOT + "/resource/model/nflx_vmaff_rf_v1.pkl",
            }
        )

        self.assertAlmostEqual(results[0]['VMAF_score'], 73.79861111111113, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_vif_score'], 0.44455808333333313, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_motion_score'], 3.5916076041666667, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_adm_score'], 0.9155242291666666, places=4)
        self.assertAlmostEqual(results[0]['VMAF_feature_ansnr_score'], 22.533456770833329, places=4)

        self.assertAlmostEqual(results[1]['VMAF_score'], 98.22048611111109, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_vif_score'], 1.0, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_motion_score'], 3.5916076041666667, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_adm_score'], 1.0, places=4)
        self.assertAlmostEqual(results[1]['VMAF_feature_ansnr_score'], 30.030914145833322, places=4)


if __name__ == '__main__':
    unittest.main()
