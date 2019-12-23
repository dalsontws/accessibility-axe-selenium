var AxeBuilder = require("axe-webdriverjs");
var WebDriver = require("selenium-webdriver");

var driver = new WebDriver.Builder().forBrowser("chrome").build();

var arr = [];
var dict = [];

const fs = require("fs");
fs.readFile("./data.json", "utf8", (err, jsonString) => {
  if (err) {
    console.log("Error reading file from disk:", err);
    return;
  }
  try {
    const link = JSON.parse(jsonString);
    for (var key in link) {
      if (link.hasOwnProperty(key)) {
        arr.push(key);
      }
    }
  } catch (err) {
    console.log("Error parsing JSON string:", err);
  }

  console.log(arr);
  console.log(arr.length);

  for (var i = 0; i < arr.length; i++) {
    driver.get(arr[i]).then(function() {
      AxeBuilder(driver)
        .configure(config)
        .analyze(function(results) {
          // console.log(results);

          dict.push(results);
          var addReport = Report(results);
          dict.push(addReport);

          JSONReport(dict);
        });
    });
  }

  //driver.close();
});

//trial configuration of rules and checks
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

//Repeated processing functionality implemented in Crawl.py
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
    anys,
    anyCount,
    passesCount,
    avgScore;
  var score = 0;
  var vScore = 0;

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

      //primitive scoring system for trial
      //Refer to Google Lighthouse Accessibility Scoring System for criteria scoring
      //Scoring is not part of configuration of original axe-core rules

      // switch(violationImpact){
      //   case "moderate":
      //     vScore += 5;
      //     break;
      //   case "serious":
      //     vScore += 7.5;
      //     break;
      //   case "critical":
      //     vScore += 10;
      //     break;
      //   case null:
      //     vScore += 2;
      //     break;
      //   default:
      //     break;
      // }
    }
  }

  // if(typeof passes !== 'undefined'){
  //  passesCount = passes.length;
  // }
  // console.log('\nNumber of passes: ' + passesCount);

  // for(l=0;l<passesCount;l+=1){
  //  passesImpact = passes[l].impact;

  //  switch(passesImpact){
  //    case "moderate":
  //      score += 5;
  //      break;
  //    case "serious":
  //      score += 7.5;
  //      break;
  //    case "critical":
  //      score += 10;
  //      break;
  //    case null:
  //      score += 2;
  //      break;
  //    default:
  //      break;
  // }
};
// console.log('\nvScore: ' + vScore + '\nScore: ' + score);
// avgScore = score + vScore;
// console.log('\nAccessibility Score: ' + (score/avgScore)*100);

//Incomplete tests to be marked as Manual checking?
//Add impact:Manual as a configuration?
//      if(typeof manual !== 'undefined'){
//       manualCount = manual.length;
//      }
//      console.log('\nNumber of manual checks to be conducted: ' + manualCount);

//      for(m=0;m<manualCount;m+=1){
//       manualCheck = manual[m];
//                 mNodes = manualCheck.nodes;

//     if(typeof mNodes !== 'undefined'){
//       mNodeCount = mNodes.length;}

//       console.log('\nThere are ' + mNodeCount + ' times of ' + manualCheck.id);

//      for (n=0; n< mNodeCount; n+=1){
//         mNode = mNodes[n];
//         if(typeof mNode !== 'undefined'){
//         mElement = mNode.target;
//         mAnys = mNode.any;}

//       for (o=0; o<anyCount;o+=1){
//       mAny = mAnys[o];
//       console.log('\nDOM element: ' + mElement[o] + ' has to be checked for error ' + mAny.message + '\n' + mAny.impact);
// }}
// }

//return report results to Crawl.py file for processing
JSONReport = function(dict) {
  fs.writeFile("./object.json", JSON.stringify(dict, null, 4), err => {
    if (err) {
      console.error(err);
      return;
    }
    console.log("File has been created");
  });
};

// }
