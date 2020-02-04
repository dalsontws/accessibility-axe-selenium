const AxeReports = require('axe-reports');
const AxeBuilder = require('axe-webdriverjs');
const WebDriver = require('selenium-webdriver');

const { By } = WebDriver;

const driver = new WebDriver.Builder().forBrowser('chrome').build();

const allUrls = new Set();

const domain = process.env.WEBSITE;

allUrls.add(domain);

function getAllUrls(mainDomain, link) {
  const currentUrlSet = new Set();

  driver.get(link).then(() => {
    AxeBuilder(driver)
      .analyze()
      .then(results => {
        AxeReports.createCsvReport(results);
      });

    const elements = driver.findElements(By.tagName('a'));
    elements
      .then(elementsResult => {
        elementsResult.forEach(element => {
          element.getAttribute('href').then(url => {
            if (url !== null && url.startsWith(mainDomain)) {
              currentUrlSet.add(url);
            }
          });
        });
      })
      .then(() => {
        const newUrlsSet = new Set([...currentUrlSet].filter(x => !allUrls.has(x)));
        const newUrlsArray = [...newUrlsSet];
        newUrlsSet.forEach(allUrls.add, allUrls);
        newUrlsArray.forEach(newLink => {
          getAllUrls(mainDomain, newLink);
        });
      });
  });
}

getAllUrls(domain, domain);

driver.close();
