<<<<<<< HEAD
<<<<<<< HEAD

var AxeReports = require('axe-reports')
var AxeBuilder = require("axe-webdriverjs");
var WebDriver = require("selenium-webdriver");

var driver = new WebDriver.Builder().forBrowser("chrome").build();
const fs = require("fs");
var By = WebDriver.By

var dict = []
var array = []
var urls = []

  driver.get(process.env.WEBSITE)

  var promise = require('selenium-webdriver').promise;
  var links = driver.findElements(By.tagName('a'))
  links.then(function (elements) {
    var pendingHref = elements.map(function (elem) {
        return elem.getAttribute('href');
    });

    promise.all(pendingHref).then(function (allHref) {
        var urls = allHref.filter(function (el){
          return el != null;
        })
        var url = urls.filter(function (ele){
          return ele != 'javascript:;';
        })

        var url1 = url.filter(function (elem){
          return elem != '';
        })
        var url2 = url1.filter(function (elem){
              return elem.includes(process.env.WEBSITE);})

        let unique = [...new Set(url2)];


//         console.log(unique);
        
        
for (var i=0; i<unique.length;i++){
    
    driver.get(unique[i]).then(function(){

    const results = new AxeBuilder(driver)
//    .configure(config)
    .analyze().then(function(results){
    dict.push(results);
    JSONReport(dict);
    AxeReports.createCsvReport(results)
    })
    })

  }

  driver.close()
  })

    });



  const config = {
  rules: [
    {
      id: "fake-rule",
      selector: "a",
      enabled: true,
      tags: ["custom"],
      all: [],
      any: ["fake-rule"],
      none: [],
      metadata: {
        description:
          "This is a rule used for testing the bok choy integration.",
        help: "I can't help",
        helpUrl: "There isn't a help url for this!"
      }
    }
  ],
  checks: [
    {
      id: "fake-rule",
      metadata: {
        impact: "serious",
        messages: {
          pass: "Element has Bok Choy",
          fail: "Element has no Bok Choy",
          incomplete: {
            BokChoy: "Bok Choy could not be seen"
          }
        }
      },

      evaluate: function(node, options) {
        var href = node.findElements("href");

        if (href === null || href === "" || href === "#") {
          return false;
        } else {
          return true;
        }
      }
    }
  ]
};


JSONReport = function(dict) {
  fs.writeFile("./Report.json", JSON.stringify(dict, null, 4), err => {
    if (err) {
      console.error(err);
      return;
    }

=======
=======
>>>>>>> master
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
<<<<<<< HEAD
>>>>>>> master
=======
>>>>>>> master
  });
}

getAllUrls(domain, domain);

driver.close();
