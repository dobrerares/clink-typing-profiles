import json
from pathlib import Path
import unittest

PROFILE = Path(__file__).resolve().parents[1] / 'Profiles/rares-glass.clinkprofile'

class QuietProfileTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads(PROFILE.read_text())['config']
    def test_sound_explicitly_off(self):
        self.assertIs(self.config['soundEnabled'], False)
    def test_normal_default_geometry(self):
        for key in ['keyHeight','keySpacing','rowSpacing','keyWidthFraction','adaptiveShrink','adaptiveGrow','adaptiveSpace']:
            self.assertNotIn(key, self.config)
    def test_number_row_haptics_popups_cursor(self):
        for key in ['showNumberRow','hapticsEnabled','cursorActivationHaptic','keyPopupEnabled']:
            self.assertIs(self.config[key], True)
        self.assertEqual(self.config['keyPopupStyle'], 'floating')
        self.assertEqual(self.config['cursorMovementType'], 'spacebar')
    def test_stable_minimal_motion(self):
        for key in ['keyBloomScale','spaceBloomScale','spaceCursorDragScale']:
            self.assertEqual(self.config[key], 1)
        self.assertFalse(self.config['swipeKeyMorph'])
        self.assertFalse(self.config['swipeShowTrail'])
        self.assertEqual(self.config['glassReleaseResponse'], 0.12)
        self.assertEqual(self.config['popupSpringResponse'], 0.22)
        self.assertEqual(len(list(PROFILE.parent.glob('*.clinkprofile'))), 1)
    def test_no_automatic_punctuation_repair(self):
        self.assertFalse(self.config['autoPunctuationEnabled'])
        self.assertTrue(self.config['punctuationSpacingEnabled'])
    def test_no_invented_plugins_theme_or_language_ids(self):
        self.assertFalse(set(self.config) & {'plugins','languages','theme','keyStyle','languageMode'})

if __name__ == '__main__':
    unittest.main()
