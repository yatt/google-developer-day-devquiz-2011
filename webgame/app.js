// jsのソースはスコープが全て閉じられてる
// デッキは全てjsで処理される
// 
// カードにはcardNというhtmlタグidが付いている。背景色で
// #solveがhttp post formになっていて、おそらく全て表にしたらこいつをonにする
// 
// 2重ループで、jqueryの.clickで一枚裏返してもう1枚ひっくり返したのとbackground-colorが同じなら正解ってことで。
// おお、なんか知らんけど枚数が8枚から16枚に増えた。こりゃ手じゃ無理だわ。
// 
// なんかchrome extensionとか言ってるけどfirebugでやった。chromeのコンソールからでもよかっただろうけど。
// 

// 1
function bg(btn)
{
  return btn.css("background-color")
}
var deck = $("#deck > tbody > tr > td > div").map(function(i,n){ return $(n) })
var nmax = deck.length
var unrevealed = "rgb(221, 221, 221)"
for (var i = 0; i < nmax; i++)
{
  if (bg(deck[i]) != unrevealed )
      continue
  for (var j = 0; j < nmax; j++)
  {
      if (bg(deck[j]) != unrevealed )
          continue
      deck[i].click()
      deck[j].click()
      if (bg(deck[i]) == bg($(deck[j])))
          break
  }
}


// 2 正解したものは走査から除去; 54問目あたりから1024枚とかでてきたので前のソースでは時間がかかりすぎる
function bg(btn){return btn.css("background-color")}
var deck = $("#deck > tbody > tr > td > div").map(function(i,n){ return $(n) })
var cnt  =0
while(deck.length > 0)
{
  for (var j = 1; j < deck.length; j++)
  {
      deck[0].click()
      deck[j].click()
      if (bg(deck[0]) == bg($(deck[j])))
      {
          deck = $.grep(deck, function(n,idx){return idx != 0 && idx != j})
if(cnt < 100){
console.log(cnt + " " + deck.length)
cnt++
}
          break
      }
  }
}

// 3 いちいち全てをめくる必要無いよね. 色で一旦分類すればすぐじゃん。
function bg(btn){return btn.css("background-color")}
var deck = $("#deck > tbody > tr > td > div").map(function(i,n){ return $(n) })
var colors = {}
for (var i = 0; i < deck.length; i++)
{
  deck[i].click()
  var c = bg(deck[i])
  if (colors[c] == undefined)
      colors[c] = [i]
  else
      colors[c].push(i)
}
for (var rgb in colors)
{
  var cl = colors[rgb]
  for (var i = 0; i < cl.length; i+=2)
      deck[cl[i]].click(), deck[cl[i+1]].click()
}
