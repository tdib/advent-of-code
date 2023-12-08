val lines = java.io.File("input.txt").readLines()
fun c(h:String,p:Int):Int{
val c=h.groupBy{it}.mapValues{(_,values)->values.size}.toMutableMap()
var j=c.getOrDefault('J',0)
if(p>1){c.remove('J')}else{j=0}
return if(c.containsValue(5-j)||j>3){7}else if(c.containsValue(4-j)){6}else if((c.filter{it.value==2}.size==2&&j==1)||(c.containsValue(3)&&c.containsValue(2))){5}else if(c.containsValue(3-j)){4}else if(c.filter{it.value==2}.size==2){3}else if(c.containsValue(2-j)){2}else{1}}
fun s(w:List<Triple<Int,String,Int>>,l:List<Char>)=w.sortedWith(compareBy{ a:Triple<Int,String,Int>->a.first}.thenComparing{a,b->Comparator{ m:String, n:String->m.zip(n).map{(x,b)->l.indexOf(b)-l.indexOf(x)}.find{it!=0}?:0}.compare(a.second,b.second)})
fun p(p:Int)=s(lines.map{val(a,b)=it.split(" ");Triple(c(a,p),a,b.toInt())},x).mapIndexed{i,t->t.third*(i+1)}.sum()
var x="A K Q J T 9 8 7 6 5 4 3 2".split(" ").map{it[0]}.toMutableList()
println("Part 1 answer: ${p(1)}")
x.add(x.removeAt(3))
println("Part 2 answer: ${p(2)}")