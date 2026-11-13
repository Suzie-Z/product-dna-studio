"""Real browser + HTTP + document parsers; ONLY provider transport is deterministic."""

import os, shutil, threading, time, unittest
from pathlib import Path
from unittest.mock import patch
from playwright.sync_api import sync_playwright
import ai_server, request_state, ephemeral_sessions
from tests.v2_fixtures import *

ART = Path(
    os.environ.get(
        "V2_ARTIFACT_DIR", str(Path(__file__).resolve().parents[1] / "work/v2-qa")
    )
)


class Browser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ART.mkdir(parents=True, exist_ok=True)
        cls.env = patch.dict(
            os.environ,
            {
                "PM_INTERNAL_TEST_TOKEN": "synthetic-only",
                "DAILY_GENERATION_LIMIT": "1000",
                "INTERNAL_TEST_DAILY_LIMIT": "1000",
                "TRIAL_START_DATE": "",
                "PUBLIC_COUNTER_ENV": "",
            },
        )
        cls.env.start()
        cls.provider = patch("ai_transport.provider", side_effect=model_transport)
        cls.provider_mock = cls.provider.start()
        cls.server = ai_server.ThreadingHTTPServer(("127.0.0.1", 0), ai_server.Handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.url = "http://127.0.0.1:" + str(cls.server.server_port)
        cls.p = sync_playwright().start()
        cls.browser = cls.p.chromium.launch(
            executable_path=shutil.which("chromium"),
            headless=True,
            args=["--no-sandbox"],
        )

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.p.stop()
        cls.server.shutdown()
        cls.server.server_close()
        cls.provider.stop()
        cls.env.stop()

    def setUp(self):
        ai_server.RECENT.clear()
        request_state.CACHE.clear()
        ephemeral_sessions.SESSIONS.clear()
        self.context = self.browser.new_context(
            viewport={"width": 1440, "height": 1000},
            extra_http_headers={"X-PM-Internal-Test": "synthetic-only"},
        )
        self.page = self.context.new_page()
        self.page.emulate_media(reduced_motion="reduce")
        self.errors = []
        self.page.on("pageerror", lambda e: self.errors.append(str(e)))
        self.page.goto(self.url)
        self.page.evaluate("document.fonts.ready")

    def tearDown(self):
        self.assertEqual(self.errors, [])
        self.context.close()

    def upload(self, profile="technology", kind="pdf"):
        self.page.locator("#cv-file").set_input_files(
            {
                "name": "synthetic-career." + kind,
                "mimeType": "application/pdf"
                if kind == "pdf"
                else "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "buffer": pdf_bytes(profile) if kind == "pdf" else docx_bytes(profile),
            }
        )
        self.page.locator("#review-panel").wait_for(state="visible")

    def generate(self):
        self.page.locator("#analyse").click()
        self.page.locator("#journey").wait_for(state="visible")
        self.page.evaluate("document.fonts.ready")

    def test_three_screen_complete_flow_screenshots(self):
        p = self.page
        p.screenshot(path=str(ART / "01-discover-desktop.png"), full_page=True)
        self.assertEqual(p.locator("textarea").count(), 0)
        self.upload()
        p.screenshot(path=str(ART / "01b-review-desktop.png"), full_page=True)
        self.generate()
        self.assertEqual(p.locator(".island-card").count(), 3)
        families = p.locator(".island-card").evaluate_all(
            "(els)=>els.map(x=>x.dataset.family)"
        )
        self.assertEqual(len(set(families)), 3)
        p.screenshot(path=str(ART / "02-journey-desktop.png"), full_page=True)
        p.locator("#island-world").screenshot(path=str(ART / "distinct-islands.png"))
        p.locator("#island-world details").first.locator("summary").click()
        p.locator("#island-world .evidence-button").first.click()
        self.assertTrue(p.locator("#evidence-dialog").is_visible())
        self.assertIn("Designed service", p.locator("#evidence-content").inner_text())
        p.keyboard.press("Escape")
        p.locator("#reveal").click()
        self.assertEqual(p.locator(".strength-card").count(), 3)
        p.screenshot(path=str(ART / "03-dna-desktop.png"), full_page=True)
        p.locator("#recognition-evidence").click()
        self.assertEqual(p.locator(".evidence-item").count(), 3)
        p.keyboard.press("Escape")
        p.locator("#back-journey").click()
        p.locator("#back-review").click()
        before = self.provider_mock.call_count
        p.locator("#analyse").click()
        p.locator("#journey").wait_for(state="visible")
        self.assertEqual(before, self.provider_mock.call_count)

    def test_docx_multiple_jobs_overlap_missing_dates(self):
        self.upload("education", "docx")
        self.assertEqual(self.page.locator(".review-row").count(), 3)
        self.assertIn("overlap", self.page.locator("#review-note").inner_text())
        self.assertEqual(
            self.page.get_by_label("Period, chapter 3", exact=True).input_value(), ""
        )
        self.generate()
        self.assertIn(
            "Period not provided", self.page.locator("#island-world").inner_text()
        )
        self.page.locator("#reveal").click()
        self.assertIn("Classroom", self.page.locator("#evolution").inner_text())

    def test_cross_profession_break_and_transition(self):
        self.upload("healthcare", "docx")
        self.generate()
        self.assertIn("A pause", self.page.locator("#island-world").inner_text())
        self.page.locator("#reveal").click()
        self.assertIn("care", self.page.locator("#identity").inner_text())

    def test_mobile_three_screens_and_no_overflow(self):
        p = self.page
        p.set_viewport_size({"width": 390, "height": 844})
        p.screenshot(path=str(ART / "01-discover-mobile.png"), full_page=True)
        self.upload("creative", "docx")
        self.generate()
        p.screenshot(path=str(ART / "02-journey-mobile.png"), full_page=True)
        self.assertLessEqual(p.evaluate("document.documentElement.scrollWidth"), 390)
        p.locator("#reveal").click()
        p.screenshot(path=str(ART / "03-dna-mobile.png"), full_page=True)
        self.assertLessEqual(p.evaluate("document.documentElement.scrollWidth"), 390)

    def test_review_correction_and_reorder(self):
        self.upload()
        p = self.page
        p.get_by_label("Role, chapter 2", exact=True).fill("Technical Product Manager")
        p.get_by_role("button", name="Move up, chapter 3", exact=True).click()
        self.generate()
        self.assertIn("Applied AI", p.locator(".stage-role").nth(1).inner_text())
        self.assertEqual(
            p.locator(".stage-role").nth(2).inner_text(), "Technical Product Manager"
        )

    def test_loading_cancel_and_retry(self):
        p = self.page
        original = model_transport

        def slow(*a, **k):
            if a[0] == "responses":
                time.sleep(0.4)
            return original(*a, **k)

        with patch("ai_transport.provider", side_effect=slow):
            p.locator("#cv-file").set_input_files(
                {
                    "name": "sample.pdf",
                    "mimeType": "application/pdf",
                    "buffer": pdf_bytes(),
                }
            )
            p.locator("#loading").wait_for(state="visible")
            p.locator("#cancel").click()
            self.assertIn("Paused", p.locator("#error-panel").inner_text())
            p.wait_for_timeout(900)
            self.assertFalse(p.locator("#review-panel").is_visible())
            p.locator("#retry").click()
            p.locator("#review-panel").wait_for(state="visible")

    def test_invalid_file_and_failed_provider_retry_preserves_review(self):
        p = self.page
        p.locator("#cv-file").set_input_files(
            {"name": "file.txt", "mimeType": "text/plain", "buffer": b"unsupported"}
        )
        self.assertIn("PDF or DOCX", p.locator("#error-panel").inner_text())
        self.upload()
        with patch("career_intelligence.structured", return_value={"invalid": True}):
            p.locator("#analyse").click()
            p.locator("#error-panel").wait_for(state="visible")
            self.assertTrue(p.locator("#review-panel").is_visible())
            self.assertEqual(p.locator(".review-row").count(), 3)
        p.locator("#retry").click()
        p.locator("#journey").wait_for(state="visible")

    def test_visual_family_fallback_and_consistent_camera(self):
        plans = self.page.evaluate(
            'CareerDesign.plan([{id:"s1",role:"Unknown",domain:"unlisted"},{id:"s2",role:"Another",domain:"unlisted"}],[])'
        )
        self.assertNotEqual(plans[0]["family"], plans[1]["family"])
        self.assertEqual({x["camera"] for x in plans}, {"isometric"})
        self.assertEqual({x["light"] for x in plans}, {"upper-left"})

    def test_artwork_bounds_at_all_sizes(self):
        self.upload()
        self.generate()
        p = self.page
        for width, height in [
            (1440, 900),
            (1366, 768),
            (1092, 614),
            (768, 1024),
            (390, 844),
            (320, 700),
        ]:
            p.set_viewport_size({"width": width, "height": height})
            self.assertLessEqual(
                p.evaluate("document.documentElement.scrollWidth"), width
            )
            bad = p.locator(".island-art svg").evaluate_all(
                "els=>els.filter(e=>{const b=e.getBBox();return b.x<0||b.y<0||b.x+b.width>361||b.y+b.height>241}).map(e=>e.getBBox().toJSON())"
            )
            self.assertEqual(bad, [], (width, bad))

    def test_twelve_chapters_and_long_labels_keep_distinct_silhouettes(self):
        p = self.page
        signatures = p.evaluate(
            """()=>{const stages=Array.from({length:12},(_,i)=>({id:'s'+(i+1),role:'Engineer',domain:'engineering'}));return CareerDesign.plan(stages,[]).map(p=>p.family+':'+p.variant)}"""
        )
        self.assertEqual(len(set(signatures)), 12)
        data = complete()
        data["stages"][0]["role"] = (
            "A long but valid multidisciplinary engineering and operational leadership role"
        )
        data["stage_insights"][0]["capabilities"] = [
            {"label": "Cross-functional systems interpretation", "fact_ids": ["f1"]}
            for _ in range(4)
        ]
        p.evaluate(
            '(data)=>CareerJourney.render(document.getElementById("island-world"),data,()=>{})',
            data,
        )
        p.locator('[data-screen="journey"]').evaluate(
            "(b)=>{b.disabled=false;b.click()}"
        )
        # Navigation is protected without a result; render into the visible entry screen for the isolated stress check.
        p.evaluate(
            'document.getElementById("discover").hidden=true;document.getElementById("journey").hidden=false'
        )
        for width in [1440, 768, 390, 320]:
            p.set_viewport_size({"width": width, "height": 844})
            self.assertLessEqual(
                p.evaluate("document.documentElement.scrollWidth"), width
            )

    def test_six_worlds_same_palette_contact_sheet(self):
        p = self.page
        p.evaluate(
            """()=>{document.body.replaceChildren();const root=document.createElement('main');root.innerHTML='<div class="section-intro centered"><p class="eyebrow">One world. Distinct places.</p><h1>Six miniature worlds</h1><p>Same palette, camera and lighting. Different geography and architecture.</p></div>';const grid=document.createElement('div');grid.className='island-world';['workshop','laboratory','bridges','garden','observatory','community'].forEach((family,i)=>{const card=document.createElement('article');card.className='island-card';const art=document.createElement('div');art.className='island-art';art.innerHTML=CareerIslands.render({stageId:'s'+i,family,palette:CareerDesign.palette[0],variant:0});const h=document.createElement('h2');h.textContent=family[0].toUpperCase()+family.slice(1);card.append(art,h);grid.append(card)});root.append(grid);document.body.append(root)}"""
        )
        p.screenshot(
            path=str(ART / "six-island-worlds-same-palette.png"), full_page=True
        )

    def test_keyboard_and_privacy(self):
        p = self.page
        p.locator("#privacy-open").click()
        self.assertIn("ten minutes", p.locator("#privacy-dialog").inner_text())
        p.keyboard.press("Escape")
        self.assertFalse(p.locator("#privacy-dialog").is_visible())
        self.assertEqual(
            p.locator("#cv-file").get_attribute("accept"),
            ".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
        self.assertEqual(p.locator("audio, canvas, textarea").count(), 0)


if __name__ == "__main__":
    unittest.main()
