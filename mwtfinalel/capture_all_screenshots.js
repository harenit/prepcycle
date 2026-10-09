import puppeteer from 'puppeteer-core';
import fs from 'fs';
import path from 'path';

const CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const OUT_DIR = path.resolve("./screenshots");

if (!fs.existsSync(OUT_DIR)) {
  fs.mkdirSync(OUT_DIR, { recursive: true });
}

async function run() {
  const browser = await puppeteer.launch({
    executablePath: CHROME_PATH,
    headless: "new",
    defaultViewport: { width: 1280, height: 800 },
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();

  console.log("1. Capturing Login Page...");
  await page.goto("http://localhost:5173/login", { waitUntil: "networkidle2" });
  await new Promise(r => setTimeout(r, 1500));
  await page.screenshot({ path: path.join(OUT_DIR, "8_1_login.png") });

  console.log("2. Logging in as Student...");
  await page.type('input[type="email"]', 'student1@prepcycle.test');
  await page.type('input[type="password"]', 'Student@12345');
  await page.click('button[type="submit"]');
  await page.waitForNavigation({ waitUntil: "networkidle2" }).catch(() => {});
  await new Promise(r => setTimeout(r, 2000));

  console.log("3. Capturing Exam Explorer...");
  await page.goto("http://localhost:5173/exam-explorer", { waitUntil: "networkidle2" });
  await new Promise(r => setTimeout(r, 1500));
  await page.screenshot({ path: path.join(OUT_DIR, "8_2_exam_explorer.png") });

  console.log("4. Capturing Progress Tracking...");
  await page.goto("http://localhost:5173/progress", { waitUntil: "networkidle2" });
  await new Promise(r => setTimeout(r, 1500));
  await page.screenshot({ path: path.join(OUT_DIR, "8_3_progress_roadmap.png") });

  console.log("5. Capturing Marketplace...");
  await page.goto("http://localhost:5173/marketplace", { waitUntil: "networkidle2" });
  await new Promise(r => setTimeout(r, 1500));
  await page.screenshot({ path: path.join(OUT_DIR, "8_5_marketplace.png") });

  console.log("6. Capturing Community...");
  await page.goto("http://localhost:5173/community", { waitUntil: "networkidle2" });
  await new Promise(r => setTimeout(r, 1500));
  await page.screenshot({ path: path.join(OUT_DIR, "8_7_community.png") });

  console.log("7. Capturing Settings...");
  await page.goto("http://localhost:5173/settings", { waitUntil: "networkidle2" });
  await new Promise(r => setTimeout(r, 1500));
  await page.screenshot({ path: path.join(OUT_DIR, "8_8_settings.png") });

  console.log("8. Logging in as Mentor...");
  await page.goto("http://localhost:5173/login", { waitUntil: "networkidle2" });
  await page.evaluate(() => localStorage.clear());
  await page.reload({ waitUntil: "networkidle2" });
  await page.type('input[type="email"]', 'mentor@prepcycle.com');
  await page.type('input[type="password"]', 'Mentor@12345');
  await page.click('button[type="submit"]');
  await page.waitForNavigation({ waitUntil: "networkidle2" }).catch(() => {});
  await new Promise(r => setTimeout(r, 2000));
  await page.goto("http://localhost:5173/mentor", { waitUntil: "networkidle2" });
  await new Promise(r => setTimeout(r, 1500));
  await page.screenshot({ path: path.join(OUT_DIR, "8_4_mentor_dashboard.png") });

  console.log("9. Logging in as Delivery Partner...");
  await page.goto("http://localhost:5173/login", { waitUntil: "networkidle2" });
  await page.evaluate(() => localStorage.clear());
  await page.reload({ waitUntil: "networkidle2" });
  await page.type('input[type="email"]', 'delivery@prepcycle.com');
  await page.type('input[type="password"]', 'Delivery@12345');
  await page.click('button[type="submit"]');
  await page.waitForNavigation({ waitUntil: "networkidle2" }).catch(() => {});
  await new Promise(r => setTimeout(r, 2000));
  await page.goto("http://localhost:5173/delivery", { waitUntil: "networkidle2" });
  await new Promise(r => setTimeout(r, 1500));
  await page.screenshot({ path: path.join(OUT_DIR, "8_6_delivery_fulfillment.png") });

  console.log("10. Logging in as Admin...");
  await page.goto("http://localhost:5173/login", { waitUntil: "networkidle2" });
  await page.evaluate(() => localStorage.clear());
  await page.reload({ waitUntil: "networkidle2" });
  await page.type('input[type="email"]', 'admin@prepcycle.com');
  await page.type('input[type="password"]', 'Admin@12345');
  await page.click('button[type="submit"]');
  await page.waitForNavigation({ waitUntil: "networkidle2" }).catch(() => {});
  await new Promise(r => setTimeout(r, 2000));
  await page.goto("http://localhost:5173/admin", { waitUntil: "networkidle2" });
  await new Promise(r => setTimeout(r, 1500));
  await page.screenshot({ path: path.join(OUT_DIR, "8_9_admin_dashboard.png") });

  await browser.close();
  console.log("ALL SCREENSHOTS CAPTURED SUCCESSFULLY!");
}

run().catch(console.error);
