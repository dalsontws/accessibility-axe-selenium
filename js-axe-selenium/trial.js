
var AxeReports = require('axe-reports')
var AxeBuilder = require("axe-webdriverjs");
var WebDriver = require("selenium-webdriver");

var driver = new WebDriver.Builder().forBrowser("chrome").build();
const fs = require("fs");
var By = WebDriver.By

var dict = []
var array = []
var urls = []


  // let screenshotNumber = 0;
  
  // const browser = await puppeteer.launch({headless:false, defaultViewport:null})
  
  // const page = await browser.newPage()
  // //await page.setBypassCSP(true)
  
  // await page.goto('https://www.mycareersfuture.sg/', {waitUntil:'networkidle2'})//get the main links
  
  // const stories = await page.evaluate(() => {
  // const links = Array.from(document.querySelectorAll('a'))
  // return links.map(link => link.href)
  // })
  driver.get("https://www.cpf.gov.sg/Members")
  // var urls = driver.findElements(By.tagName("a")).then(function(){
  //   var links = urls.getAttribute("href")
  // console.log(links)
  // })
  var promise = require('selenium-webdriver').promise;
  var links = driver.findElements(By.tagName('a'))
  links.then(function (elements) {
    var pendingHref = elements.map(function (elem) {
        return elem.getAttribute('href');
    });

    promise.all(pendingHref).then(function (allHref) {
        // `allHtml` will be an `Array` of strings
//        console.log(allHref)
        var urls = allHref.filter(function (el){
          return el != null;
        })
        var url = urls.filter(function (ele){
          return ele != 'javascript:;';
        })

        var url1 = url.filter(function (elem){
          return elem != '';
        })

        let unique = [...new Set(url1)];
//        console.log(unique);
        
        
for (var i=0; i<5;i++){
    
    driver.get(unique[i]).then(function(){
 
    const results = new AxeBuilder(driver)
    .configure(config)
    .analyze().then(function(results){
    // console.log(results)
    // Report(results);
    dict.push(results);
    JSONReport(dict);
    AxeReports.createCsvReport(results)})
    })
  }

  driver.close()
  })
        
    });





    
  

    
    

  //var links = await driver.findElements(By.css("a"))
  //var links = ["https://www.cpf.gov.sg/Members"]
  

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
        var href = node.getAttribute("href");

        if (href === null || href === "" || href === "#") {
          return false;
        } else {
          return true;
        }
      }
    }
  ]
};

  
  

Report = function(results) {
  var violations = results.violations;
  var passes = results.passes;
  var manual = results.incomplete;
  var violation,
    violationCount,
    nodes,
    node,
    nodeCount,
    element,
    any,
    anys

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


