## 实现webhook拉取代码
每次服务器需要进行代码更新的时候，需要登录服务器执行`git pull`命令。
当服务器多的时候，简单的工作也会变得管繁琐起来，如果能通过webhook的形式拉取代码可以提升效率。

### 以PHP实现webhook拉取代码
```php
<?php
exec("git pull >>git.log 2>&1", $out);
var_dump($out);
```
`2>&1` 中2表示stderr标准错误,1表示stdout标准输出，如果不加此项，错误信息将被丢失。
而前面标准输出已被重定向到git.log，因此任何信息都会写入git.log日志中。

以上的代码，在执行的过程，可能并不顺利，可能会得到以下错误信息:
```
Host key verification failed.
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```
产生错误的原因在于
* 登录服务执行`git pull`时，是基于当前登录用户如root或者Administrator，而对应账户家目录下存在.ssh证书文件。
* 通过web-php去请求时，执行该命令的账户可能不再是root或者Administrator，当账户目录下不存在.ssh证书文件时，则会报错。

如何查看脚本是从何处寻找登录公钥的呢？
```php
<?php
exec("ssh -v git@github.com 2>&1",$out);
var_dump($out);
```
通过以上脚本可以得到加载密钥的寻址过程：
```
array (size=39)
  0 => string 'OpenSSH_7.7p1, OpenSSL 1.0.2p  14 Aug 2018' (length=42)
  1 => string 'debug1: Reading configuration data /etc/ssh/ssh_config' (length=54)
  2 => string 'Pseudo-terminal will not be allocated because stdin is not a terminal.' (length=70)
  3 => string 'debug1: Connecting to github.com [52.74.223.119] port 22.' (length=57)
  4 => string 'debug1: Connection established.' (length=31)
  5 => string 'debug1: key_load_public: No such file or directory' (length=50)
  6 => string 'debug1: identity file /c/Windows/system32/config/systemprofile/.ssh/id_rsa type -1' (length=82)
  7 => string 'debug1: key_load_public: No such file or directory' (length=50)
  8 => string 'debug1: identity file /c/Windows/system32/config/systemprofile/.ssh/id_rsa-cert type -1' (length=87)
  9 => string 'debug1: key_load_public: No such file or directory' (length=50)
  10 => string 'debug1: identity file /c/Windows/system32/config/systemprofile/.ssh/id_dsa type -1' (length=82)
  11 => string 'debug1: key_load_public: No such file or directory' (length=50)
  12 => string 'debug1: identity file /c/Windows/system32/config/systemprofile/.ssh/id_dsa-cert type -1' (length=87)
  13 => string 'debug1: key_load_public: No such file or directory' (length=50)
  14 => string 'debug1: identity file /c/Windows/system32/config/systemprofile/.ssh/id_ecdsa type -1' (length=84)
  15 => string 'debug1: key_load_public: No such file or directory' (length=50)
  16 => string 'debug1: identity file /c/Windows/system32/config/systemprofile/.ssh/id_ecdsa-cert type -1' (length=89)
  17 => string 'debug1: key_load_public: No such file or directory' (length=50)
  18 => string 'debug1: identity file /c/Windows/system32/config/systemprofile/.ssh/id_ed25519 type -1' (length=86)
  19 => string 'debug1: key_load_public: No such file or directory' (length=50)
  20 => string 'debug1: identity file /c/Windows/system32/config/systemprofile/.ssh/id_ed25519-cert type -1' (length=91)
  21 => string 'debug1: key_load_public: No such file or directory' (length=50)
  22 => string 'debug1: identity file /c/Windows/system32/config/systemprofile/.ssh/id_xmss type -1' (length=83)
  23 => string 'debug1: key_load_public: No such file or directory' (length=50)
  24 => string 'debug1: identity file /c/Windows/system32/config/systemprofile/.ssh/id_xmss-cert type -1' (length=88)
  25 => string 'debug1: Local version string SSH-2.0-OpenSSH_7.7' (length=48)
  26 => string 'debug1: Remote protocol version 2.0, remote software version babeld-04534c95' (length=76)
  27 => string 'debug1: no match: babeld-04534c95' (length=33)
  28 => string 'debug1: Authenticating to github.com:22 as 'git'' (length=48)
  29 => string 'debug1: SSH2_MSG_KEXINIT sent' (length=29)
  30 => string 'debug1: SSH2_MSG_KEXINIT received' (length=33)
  31 => string 'debug1: kex: algorithm: curve25519-sha256' (length=41)
  32 => string 'debug1: kex: host key algorithm: rsa-sha2-512' (length=45)
  33 => string 'debug1: kex: server->client cipher: chacha20-poly1305@openssh.com MAC: <implicit> compression: none' (length=99)
  34 => string 'debug1: kex: client->server cipher: chacha20-poly1305@openssh.com MAC: <implicit> compression: none' (length=99)
  35 => string 'debug1: expecting SSH2_MSG_KEX_ECDH_REPLY' (length=41)
  36 => string 'debug1: Server host key: ssh-rsa SHA256:nThbg6kXUpJWGl7E1IGOCspRomTxdCARLviKw6E5SY8' (length=83)
  37 => string 'debug1: read_passphrase: can't open /dev/tty: No such device or address' (length=71)
  38 => string 'Host key verification failed.' (length=29)
```
可以看到,脚本试图从`/c/Windows/system32/config/systemprofile/.ssh/`目录中寻找密钥未找到。
那么，我们只需把root或者Administrator目录的.ssh复制过来则可.
