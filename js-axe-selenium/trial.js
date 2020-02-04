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

var AxeReports = require("axe-reports");
var AxeBuilder = require("axe-webdriverjs");
var WebDriver = require("selenium-webdriver");

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

<<<<<<< HEAD
  if (typeof violations !== "undefined") {
    violationCount = violations.length;
  }
  console.log("\nKinds of violations:" + violationCount);
  for (i = 0; i < violationCount; i += 1) {
    violation = violations[i];
    nodes = violation.nodes;

    if (typeof nodes !== "undefined") {
      nodeCount = nodes.length;
    }

    console.log("\nThere are " + nodeCount + " times of " + violation.id);

    for (j = 0; j < nodeCount; j += 1) {
      node = nodes[j];
      if (typeof node !== "undefined") {
        element = node.target;
        anys = node.any;
      }

      if (typeof anys !== "undefined") {
        anyCount = anys.length;
      }

      //trial for outputting DOM element & error message
      for (k = 0; k < anyCount; k += 1) {
        any = anys[k];

        violationImpact = any.impact;
        // if(any.message && any.impact !== 'undefined'){
        // console.log('\nDOM element: ' + element[k] + ' has error ' + any.message + '\n' + any.impact);
      }
    }
  }
};

//return report results to Crawl.py file for processing
JSONReport = function(dict) {
  fs.writeFile("./object3.json", JSON.stringify(dict, null, 4), err => {
    if (err) {
      console.error(err);
      return;
    }
//    console.log("File has been created");
  });
};
=======
driver.close();
>>>>>>> e11be0808c1ae682ce9fde22d3e38c81725bb6a1
