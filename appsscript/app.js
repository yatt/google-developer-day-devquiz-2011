function main()
{
   var lst = getDataFromWeb();

 for (var i = 0; i < lst.length; i++){
   var cityname = lst[i]["city_name"];
   var data = lst[i]["data"];
   var ss = createSheet(cityname);


   for (var j = 0; j < data.length; j++)
   {
     var datum = data[j];
     var j1 = j + 1;

     ss.getRange("A" + j1).setValue(datum["capacity"]);
     ss.getRange("B" + j1).setValue(datum["usage"]);
     ss.getRange("C" + j1).setValue(datum["usage"] / datum["capacity"]);

     ss.getRange("C" + j1).setNumberFormat("0.00%");
   }
 }
}

function getDataFromWeb()
{
 var source = "http://gdd-2011-quiz-japan.appspot.com/apps_script/data?param=-466816610380598921";
 var response = UrlFetchApp.fetch(source);
 var data = eval(response.getContentText());
 return data;
}

function createSheet(name)
{
 return SpreadsheetApp.getActiveSpreadsheet().insertSheet(name);
}

// ---------------------------------------

function testSheetData0()
{
 var rng = SpreadsheetApp.getActiveSpreadsheet().getRange("A1");
 rng.setValue("hoge");
}
function testSheetData1()
{
 var ss = SpreadsheetApp.getActiveSpreadsheet();
 for (var i = 0; i < 9; i++)
   for (var j = 0; j < 9; j++)
   {
     var name = "ABCDEFGHI"
     ss.getRange(name[i]+ (j+1)).setValue(i * j);
   }
}


// 解くのに必要な部分がドキュメント化されてないとかクール（）だ
function setFormat()
{
 var ss = SpreadsheetApp.getActiveSpreadsheet();
 ss.getRange("C1").setNumberFormat("0.00%");
}
function getFormat()
{
 var ss = SpreadsheetApp.getActiveSpreadsheet();
 ss.getRange("D2").setValue(ss.getRange("C2").getNumberFormat());
}
