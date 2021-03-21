# hotel_system_management
init readme.md

# 系统环境
python 3.6.8
django 2.2.0
nginx

# 项目部署
    
        location / {
            root   html;
        }

        location /static/ {
            root   static;
        }

        location /admin/ {
            proxy_pass   http://127.0.0.1:8001;
        }

        location /api/ {
            proxy_pass   http://127.0.0.1:8001;
        }
    
## 后端使用
    端口： 8001
    admin 后台
    api   接口
    static 调用的静态文件
    
## 前端
    端口： 80
    由nginx处理
    



