
# 阶段1：构建环境
FROM node:20-alpine AS build-stage

# 设置工作目录
WORKDIR /app

# 复制依赖定义文件
# 优化构建缓存：仅当 package.json 变更时才重新 npm install
COPY package.json ./

# 安装依赖
# 使用 npm ci (clean install) 以确保确定的构建结果
RUN npm install

# 复制源代码
COPY . .

# 构建 Vue 应用
RUN npm run build

# 阶段2：生产环境
FROM nginx:stable-alpine AS production-stage

# 复制构建产物到 Nginx 目录
COPY --from=build-stage /app/dist /usr/share/nginx/html

# 复制自定义 Nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口 (容器内部)
EXPOSE 80

# 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]
