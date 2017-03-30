左上角的菜单配置文件放在以下目录：
```
/usr/share/applications
```
命名方案以xxx.desktop,在这我以Gitkraken为列，创建一个Gitkraken图标.
```
[Desktop Entry]
Name=Gitkraken
Comment=A git UI client.
GenericName=Gitkraken
# 应用程序启动shell路径
Exec=/opt/Gitkraken/gitkraken %F
＃ 图标路径
Icon=/opt/Gitkraken/logo.png
Type=Application
StartupNotify=true
＃所属分类
Categories=GNOME;Development;
MimeType=text/plain;
```
保存命名为gitkraken.desktop,重启后生效.
